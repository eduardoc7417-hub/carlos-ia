"""Abre a janela instalada em Xvfb, faz uma pergunta real e tira capturas. Uso: ui_smoke.py <pasta de saída>"""
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, "/usr/lib/carlos-ai")
SAIDA = sys.argv[1]
GGUF = os.environ.get("GGUF_TESTE", "")
casa = tempfile.mkdtemp()
os.environ.update(HOME=casa, XDG_CONFIG_HOME=casa + "/c", XDG_DATA_HOME=casa + "/d", XDG_CACHE_HOME=casa + "/k",
                  GSK_RENDERER="cairo", GTK_A11Y="none", ADW_DISABLE_PORTAL="1", LC_ALL="C.UTF-8")
os.makedirs(casa + "/c/carlos-ai")
json.dump({"gguf_local": {"lite": GGUF}, "historico": True, "threads": 2, "inatividade_min": 5},
          open(casa + "/c/carlos-ai/config.json", "w"))

from gi.repository import GLib  # noqa: E402
from carlos_ai import interface, nucleo  # noqa: E402

app = interface.Aplicativo()
falhas = []
resultado = {}


def foto(nome):
    subprocess.run(["import", "-window", "root", os.path.join(SAIDA, nome)], check=False)


def passos():
    j = app.janela
    yield 1
    foto("ui-1-inicio.png")
    # Sem modelo e sem GGUF local, o download precisa pedir confirmação e não começar.
    j.config["gguf_local"]["lite"] = ""
    j.campo.get_buffer().set_text("Olá")
    j.enviar_ou_parar()
    yield 2
    foto("ui-2-consentimento.png")
    resultado["baixou_sem_pedir"] = nucleo.dir_modelos().exists() and any(nucleo.dir_modelos().iterdir())
    resultado["ocupado_sem_pedir"] = j.ocupado
    dialogo = j.get_visible_dialog()
    resultado["dialogo"] = dialogo.get_heading() if dialogo else None
    if dialogo:
        dialogo.force_close()
    j.campo.get_buffer().set_text("")
    j.abrir_configuracoes()
    yield 2
    foto("ui-3-configuracoes.png")
    j.get_visible_dialog().force_close()
    if GGUF:
        j.config["gguf_local"]["lite"] = GGUF
        j.campo.get_buffer().set_text("Qual é a capital de Minas Gerais?")
        j.enviar_ou_parar()
        fim = time.monotonic() + 240
        while j.ocupado and time.monotonic() < fim:
            yield 1
        foto("ui-4-resposta.png")
        resultado["mensagens"] = j.mensagens
        resultado["estado"] = j.rotulo_estado.get_label()
        resultado["historico_salvo"] = len(nucleo.carregar_historico())
        pid = j.servidor.processo.pid if j.servidor.ativo else None
        resultado["servidor_ativo"] = bool(pid)
        if not pid:
            falhas.append("servidor morreu depois da resposta")

        # Parar no meio da resposta.
        j.campo.get_buffer().set_text("Conte de um até duzentos, um número por linha.")
        j.enviar_ou_parar()
        while not j.rotulo_resposta and time.monotonic() < fim + 120:
            yield 1
        j.enviar_ou_parar()
        while j.ocupado and time.monotonic() < fim + 180:
            yield 1
        resultado["estado_parar"] = j.rotulo_estado.get_label()
        if resultado["estado_parar"] != "Resposta interrompida.":
            falhas.append("parar não interrompeu")

        # Otimizador: a IA explica o estado publicado, sem alterar nada.
        j.nova_conversa()
        resultado["mensagens_apos_nova"] = len(j.mensagens)
        resultado["historico_apos_nova"] = len(nucleo.carregar_historico())
        estado = {"ajustes": [{"id": "x", "titulo": "Proteger páginas em uso", "situacao": "aplicado"}],
                  "sugestoes": [{"id": "y", "texto": "Não há swap nem zram ativos."}]}
        os.makedirs("/run/carlos-otimizador", exist_ok=True)
        json.dump(estado, open("/run/carlos-otimizador/estado.json", "w"))
        j.abrir_configuracoes()
        j.get_visible_dialog().set_visible_page_name("otimizador")
        yield 2
        foto("ui-5-otimizador.png")
        j.get_visible_dialog().force_close()
        j.perguntar(nucleo.pergunta_sobre_otimizador(estado))
        fim2 = time.monotonic() + 240
        while j.ocupado and time.monotonic() < fim2:
            yield 1
        foto("ui-6-explicacao.png")
        resultado["explicacao"] = j.mensagens[-1]["content"][:400]

        # Inatividade: com o limite vencido, o servidor precisa sair.
        j.servidor.ultimo_uso -= 3600
        j._verificar_inatividade()
        resultado["servidor_apos_inatividade"] = j.servidor.ativo
        resultado["estado_inatividade"] = j.rotulo_estado.get_label()
        if j.servidor.ativo or os.path.exists(f"/proc/{pid}"):
            falhas.append("servidor não saiu por inatividade")
    app.quit()


gerador = None


def avancar():
    global gerador
    if app.janela is None:
        return True
    if gerador is None:
        gerador = passos()
    try:
        GLib.timeout_add_seconds(next(gerador), avancar)
    except StopIteration:
        pass
    except Exception as erro:  # noqa: BLE001
        falhas.append(repr(erro))
        app.quit()
    return False


GLib.timeout_add_seconds(2, avancar)
app.run(None)
print(json.dumps(resultado, ensure_ascii=False, indent=1))
print("falhas:", falhas)
sys.exit(1 if falhas else 0)
