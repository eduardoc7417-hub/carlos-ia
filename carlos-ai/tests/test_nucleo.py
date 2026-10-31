"""Testa o núcleo: histórico, config, download com SHA-256 e, com GGUF_TESTE, o llama-server real."""
import hashlib
import http.server
import json
import os
import stat
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

APP = os.environ.get("CARLOS_APP", str(Path(__file__).parents[1] / "app"))
sys.path.insert(0, APP)
from carlos_ai import nucleo  # noqa: E402

GGUF = os.environ.get("GGUF_TESTE")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        for var, nome in (("XDG_CONFIG_HOME", "c"), ("XDG_DATA_HOME", "d"), ("XDG_CACHE_HOME", "k")):
            os.environ[var] = os.path.join(self.tmp.name, nome)

    def tearDown(self):
        self.tmp.cleanup()


class Dados(Base):
    def test_historico_desligado_por_padrao(self):
        self.assertFalse(nucleo.carregar_config()["historico"])

    def test_historico_privado_e_apagavel(self):
        nucleo.salvar_historico([{"role": "user", "content": "olá"}])
        caminho = nucleo.dir_dados() / "historico.json"
        self.assertEqual(stat.S_IMODE(caminho.stat().st_mode) & 0o077, 0)
        self.assertEqual(nucleo.carregar_historico()[0]["content"], "olá")
        nucleo.apagar_historico()
        self.assertFalse(caminho.exists())
        nucleo.apagar_historico()

    def test_config_corrompida_usa_padrao(self):
        nucleo.salvar_config({"versao": "pro", "desconhecida": 1})
        self.assertEqual(nucleo.carregar_config()["versao"], "pro")
        self.assertNotIn("desconhecida", nucleo.carregar_config())
        (nucleo.dir_config() / "config.json").write_text("{quebrado")
        self.assertEqual(nucleo.carregar_config()["versao"], "lite")

    def test_perfis_tem_modelo_no_catalogo(self):
        for perfil in nucleo.PERFIS.values():
            self.assertIn(perfil["modelo"], nucleo.CATALOGO)
        for modelo in nucleo.CATALOGO.values():
            for arquivo in modelo["arquivos"]:
                self.assertTrue(arquivo["url"].startswith("https://"))
                self.assertEqual(len(arquivo["sha256"]), 64)

    def test_explicacao_nao_afirma_acao(self):
        texto = nucleo.pergunta_sobre_otimizador({"ajustes": [{"titulo": "A", "situacao": "aplicado"}],
                                                  "sugestoes": [{"texto": "S"}]})
        self.assertIn("Não diga que fez", texto)


class Servidorzinho(http.server.BaseHTTPRequestHandler):
    conteudo = b"x" * 3000000
    def do_GET(self):
        inicio = 0
        if self.headers.get("Range"):
            inicio = int(self.headers["Range"].split("=")[1].split("-")[0])
            self.send_response(206)
        else:
            self.send_response(200)
        corpo = self.conteudo[inicio:]
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)
    def log_message(self, *a):
        pass


class Download(Base):
    def setUp(self):
        super().setUp()
        self.http = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Servidorzinho)
        threading.Thread(target=self.http.serve_forever, daemon=True).start()

    def tearDown(self):
        self.http.shutdown()
        super().tearDown()

    def catalogo(self, sha=None):
        c = Servidorzinho.conteudo
        return {"t": {"arquivos": [{"nome": "m.gguf", "url": f"http://127.0.0.1:{self.http.server_address[1]}/m",
                                    "tamanho": len(c), "sha256": sha or hashlib.sha256(c).hexdigest()}]}}

    def test_baixa_e_confere(self):
        progresso = []
        nucleo.baixar_modelo("t", progresso.append, catalogo=self.catalogo())
        self.assertEqual((nucleo.dir_modelos() / "m.gguf").stat().st_size, 3000000)
        self.assertEqual(progresso[-1], 1.0)

    def test_retoma(self):
        nucleo.dir_modelos().mkdir(parents=True)
        (nucleo.dir_modelos() / "m.gguf.part").write_bytes(Servidorzinho.conteudo[:1000000])
        nucleo.baixar_modelo("t", catalogo=self.catalogo())
        self.assertEqual((nucleo.dir_modelos() / "m.gguf").read_bytes(), Servidorzinho.conteudo)

    def test_hash_errado_apaga(self):
        with self.assertRaises(nucleo.ErroCarlos):
            nucleo.baixar_modelo("t", catalogo=self.catalogo("0" * 64))
        self.assertEqual(list(nucleo.dir_modelos().iterdir()), [])

    def test_cancelar(self):
        cancelar = threading.Event()
        cancelar.set()
        with self.assertRaises(nucleo.ErroCarlos):
            nucleo.baixar_modelo("t", cancelar=cancelar, catalogo=self.catalogo())
        self.assertFalse((nucleo.dir_modelos() / "m.gguf").exists())


@unittest.skipUnless(GGUF, "defina GGUF_TESTE com um modelo local")
class Real(Base):
    def test_ciclo(self):
        s = nucleo.Servidor()
        inicio = time.monotonic()
        s.garantir(GGUF, 2048, threads=2)
        print(f"\ncarregou em {time.monotonic() - inicio:.1f} s", flush=True)
        pid = s.processo.pid
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                linha = f.read().split(b"\0")
            self.assertIn(b"127.0.0.1", linha)
            self.assertNotIn(s.token.encode(), linha, "o token não pode aparecer na linha de comando")

            import urllib.error
            import urllib.request
            pedido = urllib.request.Request(f"http://127.0.0.1:{s.porta}/v1/chat/completions", data=b"{}",
                                            headers={"Content-Type": "application/json"})
            with self.assertRaises(urllib.error.HTTPError) as erro:
                urllib.request.urlopen(pedido, timeout=10)
            self.assertEqual(erro.exception.code, 401, "sem token não pode responder")

            texto = "".join(s.conversar([{"role": "user", "content": "Quem é você? Responda em uma frase."}]))
            print("resposta:", texto, flush=True)
            self.assertTrue(texto.strip())

            s.garantir(GGUF, 2048, threads=2)
            self.assertEqual(s.processo.pid, pid, "mesma configuração reaproveita o processo")

            cancelar = threading.Event()
            partes = 0
            for _ in s.conversar([{"role": "user", "content": "Conte até cem."}], cancelar):
                partes += 1
                cancelar.set()
            self.assertEqual(partes, 1)
        finally:
            s.parar()
        self.assertFalse(s.ativo)
        self.assertFalse(os.path.exists(f"/proc/{pid}"), "o processo precisa sair")

    def test_sobrevive_ao_fim_da_linha_que_o_iniciou(self):
        s = nucleo.Servidor()
        linha = threading.Thread(target=s.garantir, args=(GGUF, 2048), kwargs={"threads": 2})
        linha.start()
        linha.join()
        time.sleep(2)
        try:
            self.assertTrue(s.ativo, "o servidor não pode morrer junto com a linha de trabalho")
        finally:
            s.parar()

    def test_modelo_ausente(self):
        with self.assertRaises(nucleo.ErroCarlos):
            nucleo.Servidor().garantir("/nao/existe.gguf", 2048)


if __name__ == "__main__":
    unittest.main(verbosity=1)
