"""Núcleo sem interface: perfis, modelos, histórico, llama-server e conversa.

Regras do projeto, que este módulo garante:
- nenhuma conexão de rede além do download que o usuário autorizar e do llama-server local;
- o único processo iniciado é o llama-server, sem privilégios e só em 127.0.0.1;
- nenhuma resposta do modelo é executada.
"""
import ctypes
import hashlib
import http.client
import json
import os
import queue
import secrets
import shutil
import signal
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

IDENTIDADE = (
    "Você é a Carlos AI, assistente local do Carlos OS Aurora. "
    "Responda sempre em português do Brasil, de forma clara e curta. "
    "Quando perguntarem quem você é, diga que é a Carlos AI. "
    "Você não executa comandos nem altera nada no computador: apresente qualquer "
    "comando apenas como sugestão, que o usuário decide se usa. "
    "Se não souber algo, diga que não sabe."
)

PERFIS = {
    "lite": {"nome": "Lite", "num_ctx": 2048, "modelo": "gemma3-1b"},
    "pro": {"nome": "Pro", "num_ctx": 4096, "modelo": "qwen2.5-7b"},
}

_HF = "https://huggingface.co/"
CATALOGO = {
    "gemma3-1b": {
        "nome": "Gemma 3 1B (Q4_K_M)",
        "versao": "lite",
        "licenca": "Gemma Terms of Use",
        "licenca_url": "https://ai.google.dev/gemma/terms",
        "arquivos": [
            {
                "nome": "gemma-3-1b-it-Q4_K_M.gguf",
                "url": _HF + "ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf",
                "tamanho": 806058240,
                "sha256": "8ccc5cd1f1b3602548715ae25a66ed73fd5dc68a210412eea643eb20eb75a135",
            }
        ],
    },
    "qwen2.5-1.5b": {
        "nome": "Qwen2.5 1.5B (Q4_K_M)",
        "versao": "lite",
        "licenca": "Apache 2.0",
        "licenca_url": "https://www.apache.org/licenses/LICENSE-2.0",
        "arquivos": [
            {
                "nome": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
                "url": _HF + "Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf",
                "tamanho": 1117320736,
                "sha256": "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e",
            }
        ],
    },
    "qwen2.5-7b": {
        "nome": "Qwen2.5 7B (Q4_K_M)",
        "versao": "pro",
        "licenca": "Apache 2.0",
        "licenca_url": "https://www.apache.org/licenses/LICENSE-2.0",
        "arquivos": [
            {
                "nome": "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
                "url": _HF + "Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
                "tamanho": 3993201344,
                "sha256": "dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db",
            },
            {
                "nome": "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf",
                "url": _HF + "Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf",
                "tamanho": 689872288,
                "sha256": "539cf93f78e887edea1c04e2d7d8cdaca9d01dae9c9025bcb8accbe29df3d72a",
            },
        ],
    },
}

CONFIG_PADRAO = {
    "versao": "lite",
    "modelos": {"lite": "gemma3-1b", "pro": "qwen2.5-7b"},
    "gguf_local": {"lite": "", "pro": ""},
    "threads": 0,
    "inatividade_min": 5,
    "camadas_gpu": 0,
    "historico": False,
}


class ErroCarlos(Exception):
    """Erro com mensagem pronta para mostrar ao usuário."""


def _xdg(variavel, padrao):
    return Path(os.environ.get(variavel) or Path.home() / padrao) / "carlos-ai"


def dir_config():
    return _xdg("XDG_CONFIG_HOME", ".config")


def dir_dados():
    return _xdg("XDG_DATA_HOME", ".local/share")


def dir_cache():
    return _xdg("XDG_CACHE_HOME", ".cache")


def dir_modelos():
    return dir_dados() / "modelos"


def gravar_privado(caminho, texto):
    """Grava de forma atômica, legível só pelo usuário."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporario = tempfile.mkstemp(dir=caminho.parent, prefix=".tmp-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as saida:
            saida.write(texto)
        os.replace(temporario, caminho)
    except BaseException:
        os.unlink(temporario)
        raise


def carregar_config():
    config = json.loads(json.dumps(CONFIG_PADRAO))
    try:
        salvo = json.loads((dir_config() / "config.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return config
    for chave, valor in salvo.items():
        if isinstance(config.get(chave), dict) and isinstance(valor, dict):
            config[chave].update(valor)
        elif chave in config:
            config[chave] = valor
    if config["versao"] not in PERFIS:
        config["versao"] = "lite"
    return config


def salvar_config(config):
    gravar_privado(dir_config() / "config.json", json.dumps(config, ensure_ascii=False, indent=2))


# Histórico: desligado por padrão; guarda só a última conversa, neste computador.
def carregar_historico():
    try:
        mensagens = json.loads((dir_dados() / "historico.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [m for m in mensagens if isinstance(m, dict) and m.get("role") in ("user", "assistant")]


def salvar_historico(mensagens):
    gravar_privado(dir_dados() / "historico.json", json.dumps(mensagens, ensure_ascii=False, indent=1))


def apagar_historico():
    try:
        (dir_dados() / "historico.json").unlink()
    except FileNotFoundError:
        pass


# Modelos
def tamanho_total(modelo_id):
    return sum(a["tamanho"] for a in CATALOGO[modelo_id]["arquivos"])


def formatar_tamanho(octetos):
    if octetos >= 1e9:
        return f"{octetos / 1e9:.1f} GB".replace(".", ",")
    return f"{octetos / 1e6:.0f} MB"


def modelo_instalado(modelo_id):
    return all(
        (dir_modelos() / a["nome"]).is_file()
        and (dir_modelos() / a["nome"]).stat().st_size == a["tamanho"]
        for a in CATALOGO[modelo_id]["arquivos"]
    )


def caminho_modelo(modelo_id):
    """Arquivo a passar ao llama-server: em modelos divididos, o primeiro."""
    return dir_modelos() / CATALOGO[modelo_id]["arquivos"][0]["nome"]


def apagar_modelo(modelo_id):
    for arquivo in CATALOGO[modelo_id]["arquivos"]:
        for caminho in (dir_modelos() / arquivo["nome"], dir_modelos() / (arquivo["nome"] + ".part")):
            try:
                caminho.unlink()
            except FileNotFoundError:
                pass


def sha256_arquivo(caminho, cancelar=None):
    resumo = hashlib.sha256()
    with open(caminho, "rb") as entrada:
        while bloco := entrada.read(1 << 20):
            if cancelar is not None and cancelar.is_set():
                raise ErroCarlos("Download cancelado.")
            resumo.update(bloco)
    return resumo.hexdigest()


def baixar_modelo(modelo_id, progresso=None, cancelar=None, catalogo=None):
    """Baixa e confere o SHA-256. Só deve ser chamado depois do consentimento do usuário."""
    arquivos = (catalogo or CATALOGO)[modelo_id]["arquivos"]
    destino = dir_modelos()
    destino.mkdir(parents=True, exist_ok=True, mode=0o700)
    total = sum(a["tamanho"] for a in arquivos)
    faltam = sum(a["tamanho"] for a in arquivos if not (destino / a["nome"]).is_file())
    if shutil.disk_usage(destino).free < faltam + 200_000_000:
        raise ErroCarlos(f"Espaço insuficiente: são necessários {formatar_tamanho(faltam)} livres.")

    concluido = 0
    for arquivo in arquivos:
        final = destino / arquivo["nome"]
        if final.is_file() and final.stat().st_size == arquivo["tamanho"]:
            concluido += arquivo["tamanho"]
            continue
        parcial = destino / (arquivo["nome"] + ".part")
        ja = parcial.stat().st_size if parcial.exists() else 0
        if ja > arquivo["tamanho"]:
            parcial.unlink()
            ja = 0
        if ja < arquivo["tamanho"]:
            pedido = urllib.request.Request(arquivo["url"], headers={"User-Agent": "carlos-ai"})
            if ja:
                pedido.add_header("Range", f"bytes={ja}-")
            try:
                resposta = urllib.request.urlopen(pedido, timeout=60)
            except OSError as erro:
                raise ErroCarlos(f"Falha no download: {erro}") from erro
            with resposta:
                # Um servidor sem suporte a Range reenvia o arquivo inteiro.
                modo = "ab" if ja and resposta.status == 206 else "wb"
                if modo == "wb":
                    ja = 0
                with open(parcial, modo) as saida:
                    while bloco := resposta.read(1 << 20):
                        if cancelar is not None and cancelar.is_set():
                            raise ErroCarlos("Download cancelado.")
                        saida.write(bloco)
                        ja += len(bloco)
                        if progresso:
                            progresso((concluido + ja) / total)
        if sha256_arquivo(parcial, cancelar) != arquivo["sha256"]:
            parcial.unlink()
            raise ErroCarlos(f"O arquivo {arquivo['nome']} falhou na verificação de SHA-256 e foi apagado.")
        os.replace(parcial, final)
        concluido += arquivo["tamanho"]
    if progresso:
        progresso(1.0)


def threads_padrao():
    """Núcleos físicos, se der para saber; senão, todos os lógicos."""
    try:
        pares = set()
        bloco = {}
        for linha in Path("/proc/cpuinfo").read_text().splitlines() + [""]:
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                bloco[chave.strip()] = valor.strip()
            elif bloco:
                if "core id" in bloco:
                    pares.add((bloco.get("physical id"), bloco["core id"]))
                bloco = {}
        if pares:
            return len(pares)
    except OSError:
        pass
    return os.cpu_count() or 2


def memoria_disponivel():
    try:
        for linha in Path("/proc/meminfo").read_text().splitlines():
            if linha.startswith("MemAvailable:"):
                return int(linha.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return None


def _morrer_com_o_pai():
    ctypes.CDLL("libc.so.6", use_errno=True).prctl(1, signal.SIGTERM)  # PR_SET_PDEATHSIG


def _lancador(pedidos):
    """Roda em uma linha permanente: PR_SET_PDEATHSIG dispara quando a *linha* que criou o filho termina."""
    while True:
        argumentos, resposta = pedidos.get()
        try:
            resposta.put(subprocess.Popen(preexec_fn=_morrer_com_o_pai, **argumentos))
        except OSError as erro:
            resposta.put(erro)


class Servidor:
    """llama-server filho do aplicativo: sobe sob demanda e sai por inatividade."""

    def __init__(self, executavel="llama-server"):
        self.executavel = executavel
        self._pedidos = queue.Queue()
        threading.Thread(target=_lancador, args=(self._pedidos,), daemon=True).start()
        self.processo = None
        self.porta = None
        self.token = None
        self.chave = None
        self.ultimo_uso = 0.0

    @property
    def ativo(self):
        return self.processo is not None and self.processo.poll() is None

    def garantir(self, caminho, num_ctx, threads=0, camadas_gpu=0, tempo_limite=300):
        chave = (str(caminho), num_ctx, threads, camadas_gpu)
        if self.ativo and self.chave == chave:
            self.ultimo_uso = time.monotonic()
            return
        self.parar()
        if shutil.which(self.executavel) is None:
            raise ErroCarlos("O programa llama-server não está instalado.")
        if not Path(caminho).is_file():
            raise ErroCarlos(f"Modelo não encontrado: {caminho}")

        with socket.socket() as livre:
            livre.bind(("127.0.0.1", 0))
            self.porta = livre.getsockname()[1]
        self.token = secrets.token_urlsafe(24)
        ambiente = dict(os.environ, LLAMA_API_KEY=self.token)
        comando = [
            self.executavel,
            "--model", str(caminho),
            "--host", "127.0.0.1",
            "--port", str(self.porta),
            "--ctx-size", str(num_ctx),
            "--threads", str(threads or threads_padrao()),
            "--n-gpu-layers", str(camadas_gpu),
            "--no-webui",
        ]
        registro = dir_cache() / "llama-server.log"
        registro.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with open(registro, "wb") as saida:
            resposta = queue.Queue()
            self._pedidos.put((dict(args=comando, stdin=subprocess.DEVNULL, stdout=saida,
                                    stderr=subprocess.STDOUT, env=ambiente), resposta))
            lancado = resposta.get()
        if isinstance(lancado, OSError):
            raise ErroCarlos(f"Não foi possível iniciar o llama-server: {lancado}")
        self.processo = lancado
        self.chave = chave
        limite = time.monotonic() + tempo_limite
        while time.monotonic() < limite:
            if self.processo.poll() is not None:
                codigo = self.processo.returncode
                self.processo = None
                raise ErroCarlos(f"O llama-server encerrou ao carregar o modelo (código {codigo}). Veja {registro}.")
            if self._saudavel():
                self.ultimo_uso = time.monotonic()
                return
            time.sleep(0.25)
        self.parar()
        raise ErroCarlos("O modelo demorou demais para carregar.")

    def _saudavel(self):
        try:
            conexao = http.client.HTTPConnection("127.0.0.1", self.porta, timeout=2)
            conexao.request("GET", "/health")
            situacao = conexao.getresponse().status
            conexao.close()
            return situacao == 200
        except OSError:
            return False

    def parar(self):
        if self.processo is None:
            return
        if self.processo.poll() is None:
            self.processo.terminate()
            try:
                self.processo.wait(10)
            except subprocess.TimeoutExpired:
                self.processo.kill()
                self.processo.wait()
        self.processo = None

    def ocioso_ha(self):
        return time.monotonic() - self.ultimo_uso

    def conversar(self, mensagens, cancelar=None, temperatura=0.3):
        """Gera pedaços de texto. O histórico enviado é o que recebe, com a identidade na frente."""
        if not self.ativo:
            raise ErroCarlos("O modelo não está carregado.")
        self.ultimo_uso = time.monotonic()
        corpo = json.dumps({
            "messages": [{"role": "system", "content": IDENTIDADE}] + mensagens,
            "stream": True,
            "temperature": temperatura,
        })
        conexao = http.client.HTTPConnection("127.0.0.1", self.porta, timeout=600)
        try:
            conexao.request("POST", "/v1/chat/completions", corpo.encode("utf-8"), {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.token,
            })
            resposta = conexao.getresponse()
            if resposta.status != 200:
                raise ErroCarlos(f"O llama-server recusou o pedido (HTTP {resposta.status}).")
            for linha in resposta:
                self.ultimo_uso = time.monotonic()
                if cancelar is not None and cancelar.is_set():
                    return
                linha = linha.strip()
                if not linha.startswith(b"data:"):
                    continue
                dados = linha[5:].strip()
                if dados == b"[DONE]":
                    return
                escolhas = json.loads(dados).get("choices") or []
                if escolhas:
                    pedaco = escolhas[0].get("delta", {}).get("content")
                    if pedaco:
                        yield pedaco
        except (OSError, http.client.HTTPException) as erro:
            if cancelar is None or not cancelar.is_set():
                raise ErroCarlos(f"A conexão com o llama-server caiu: {erro}") from erro
        finally:
            conexao.close()


def estado_otimizador(caminho="/run/carlos-otimizador/estado.json"):
    """O que o Otimizador publicou, ou None se ele não estiver ativo."""
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def pergunta_sobre_otimizador(estado):
    """Monta o pedido de explicação: a IA só explica; quem decide é o usuário."""
    linhas = ["O Otimizador Carlos publicou este estado do computador:"]
    for ajuste in estado.get("ajustes", []):
        linhas.append(f"- Ajuste {ajuste['titulo']}: {ajuste['situacao']}")
    for sugestao in estado.get("sugestoes", []):
        linhas.append(f"- Sugestão: {sugestao['texto']}")
    linhas.append("Explique em linguagem simples o que isso significa e o que eu poderia fazer. "
                  "Não diga que fez qualquer alteração.")
    return "\n".join(linhas)
