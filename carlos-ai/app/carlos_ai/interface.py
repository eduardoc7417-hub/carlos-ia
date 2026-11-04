"""Janela GTK4 + libadwaita da Carlos AI. A lógica fica em nucleo.py."""
import threading
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk  # noqa: E402

from . import VERSAO, nucleo  # noqa: E402

APP_ID = "org.carlosos.CarlosAI"


class Janela(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Carlos AI", default_width=760, default_height=640)
        self.config = nucleo.carregar_config()
        self.servidor = nucleo.Servidor()
        self.mensagens = []
        self.ocupado = False
        self.cancelar = None
        self.rotulo_resposta = None

        self.toasts = Adw.ToastOverlay()
        self.set_content(self.toasts)
        raiz = Adw.ToolbarView()
        self.toasts.set_child(raiz)

        topo = Adw.HeaderBar()
        raiz.add_top_bar(topo)
        self.seletor = Gtk.DropDown.new_from_strings([p["nome"] for p in nucleo.PERFIS.values()])
        self.seletor.set_selected(list(nucleo.PERFIS).index(self.config["versao"]))
        self.seletor.set_tooltip_text("Versão da Carlos AI")
        self.seletor.connect("notify::selected", self._versao_mudou)
        topo.pack_start(self.seletor)
        nova = Gtk.Button(icon_name="tab-new-symbolic", tooltip_text="Nova conversa")
        nova.connect("clicked", lambda *_: self.nova_conversa())
        topo.pack_start(nova)
        ajustes = Gtk.Button(icon_name="emblem-system-symbolic", tooltip_text="Configurações")
        ajustes.connect("clicked", lambda *_: self.abrir_configuracoes())
        topo.pack_end(ajustes)

        corpo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        raiz.set_content(corpo)

        self.vazio = Adw.StatusPage(
            icon_name="carlos-ai", title="Como posso ajudar?",
            description="Roda neste computador, sem internet. A Carlos AI só sugere: nada é executado por ela.",
            vexpand=True,
        )
        corpo.append(self.vazio)

        self.lista = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12,
                             margin_top=12, margin_bottom=12, margin_start=16, margin_end=16)
        self.rolagem = Gtk.ScrolledWindow(vexpand=True, visible=False,
                                          hscrollbar_policy=Gtk.PolicyType.NEVER)
        clamp = Adw.Clamp(maximum_size=720, child=self.lista)
        self.rolagem.set_child(clamp)
        corpo.append(self.rolagem)

        estado = Gtk.Box(spacing=8, margin_start=16, margin_end=16, margin_top=4)
        self.giro = Gtk.Spinner()
        self.rotulo_estado = Gtk.Label(label="", xalign=0, wrap=True, hexpand=True)
        self.rotulo_estado.add_css_class("dim-label")
        self.rotulo_estado.add_css_class("caption")
        estado.append(self.giro)
        estado.append(self.rotulo_estado)
        corpo.append(estado)

        entrada = Gtk.Box(spacing=8, margin_start=16, margin_end=16, margin_top=8, margin_bottom=16)
        moldura = Gtk.Frame(hexpand=True)
        rolagem_campo = Gtk.ScrolledWindow(max_content_height=120, propagate_natural_height=True,
                                           hscrollbar_policy=Gtk.PolicyType.NEVER)
        self.campo = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR, accepts_tab=False,
                                  top_margin=8, bottom_margin=8, left_margin=8, right_margin=8)
        self.campo.update_property([Gtk.AccessibleProperty.LABEL], ["Pergunta"])
        teclas = Gtk.EventControllerKey()
        teclas.connect("key-pressed", self._tecla)
        self.campo.add_controller(teclas)
        rolagem_campo.set_child(self.campo)
        moldura.set_child(rolagem_campo)
        entrada.append(moldura)
        self.enviar = Gtk.Button(icon_name="go-up-symbolic", tooltip_text="Enviar", valign=Gtk.Align.END)
        self.enviar.add_css_class("suggested-action")
        self.enviar.add_css_class("circular")
        self.enviar.connect("clicked", lambda *_: self.enviar_ou_parar())
        entrada.append(self.enviar)
        corpo.append(entrada)

        self.connect("close-request", self._fechando)
        GLib.timeout_add_seconds(20, self._verificar_inatividade)

        if self.config["historico"]:
            for mensagem in nucleo.carregar_historico():
                self.mensagens.append(mensagem)
                self._adicionar_balao(mensagem["role"], mensagem["content"])
        self.campo.grab_focus()

    # Estado
    @property
    def versao(self):
        return list(nucleo.PERFIS)[self.seletor.get_selected()]

    def _modelo_id(self):
        return self.config["modelos"][self.versao]

    def _indicar(self, texto, girando=False):
        self.rotulo_estado.set_label(texto)
        self.giro.set_spinning(girando)

    def _aviso(self, texto):
        self.toasts.add_toast(Adw.Toast(title=GLib.markup_escape_text(texto), timeout=6))

    def _definir_ocupado(self, ocupado):
        self.ocupado = ocupado
        self.enviar.set_icon_name("media-playback-stop-symbolic" if ocupado else "go-up-symbolic")
        self.enviar.set_tooltip_text("Parar" if ocupado else "Enviar")

    def _versao_mudou(self, *_):
        if self.ocupado and self.cancelar is not None:
            self.cancelar.set()
        self.config["versao"] = self.versao
        nucleo.salvar_config(self.config)
        self._indicar("")

    def _verificar_inatividade(self):
        limite = self.config["inatividade_min"] * 60
        if limite and not self.ocupado and self.servidor.ativo and self.servidor.ocioso_ha() >= limite:
            self.servidor.parar()
            self._indicar("Modelo descarregado por inatividade.")
        return GLib.SOURCE_CONTINUE

    def _fechando(self, *_):
        if self.cancelar is not None:
            self.cancelar.set()
        self.servidor.parar()
        return False

    def _tecla(self, _controle, tecla, _codigo, modificadores):
        if tecla in (0xff0d, 0xff8d) and not modificadores & 1:  # Enter sem Shift
            if not self.ocupado:
                self.enviar_ou_parar()
            return True
        return False

    # Conversa
    def _adicionar_balao(self, papel, texto):
        self.vazio.set_visible(False)
        self.rolagem.set_visible(True)
        rotulo = Gtk.Label(label=texto, wrap=True, selectable=True, xalign=0, use_markup=False,
                           wrap_mode=2)  # Pango.WrapMode.WORD_CHAR
        if papel == "user":
            cartao = Gtk.Box(halign=Gtk.Align.END)
            cartao.add_css_class("card")
            rotulo.set_margin_top(8)
            rotulo.set_margin_bottom(8)
            rotulo.set_margin_start(12)
            rotulo.set_margin_end(12)
            cartao.append(rotulo)
            self.lista.append(cartao)
        else:
            rotulo.set_halign(Gtk.Align.START)
            self.lista.append(rotulo)
        GLib.idle_add(self._rolar_fim)
        return rotulo

    def _rolar_fim(self):
        ajuste = self.rolagem.get_vadjustment()
        ajuste.set_value(ajuste.get_upper())
        return GLib.SOURCE_REMOVE

    def nova_conversa(self):
        if self.cancelar is not None:
            self.cancelar.set()
        self.mensagens = []
        while (filho := self.lista.get_first_child()) is not None:
            self.lista.remove(filho)
        self.rolagem.set_visible(False)
        self.vazio.set_visible(True)
        if self.config["historico"]:
            nucleo.apagar_historico()
        self.campo.grab_focus()

    def enviar_ou_parar(self):
        if self.ocupado:
            if self.cancelar is not None:
                self.cancelar.set()
            return
        buffer = self.campo.get_buffer()
        texto = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False).strip()
        if not texto:
            return
        buffer.set_text("")
        self.perguntar(texto)

    def perguntar(self, texto):
        """Envia a pergunta; se faltar o modelo, primeiro pede consentimento para baixar."""
        local = self.config["gguf_local"].get(self.versao)
        if not local and not nucleo.modelo_instalado(self._modelo_id()):
            self.campo.get_buffer().set_text(texto)
            self.pedir_download(self._modelo_id())
            return
        caminho = Path(local) if local else nucleo.caminho_modelo(self._modelo_id())
        tamanho = caminho.stat().st_size if caminho.is_file() else 0
        if not local:
            tamanho = nucleo.tamanho_total(self._modelo_id())
        livre = nucleo.memoria_disponivel()
        if not self.servidor.ativo and livre is not None and livre < tamanho * 1.15:
            self._aviso(f"Pouca memória livre ({nucleo.formatar_tamanho(livre)}): o modelo pode deixar o sistema lento.")

        self.mensagens.append({"role": "user", "content": texto})
        self._adicionar_balao("user", texto)
        self.rotulo_resposta = None
        self.cancelar = threading.Event()
        self._definir_ocupado(True)
        self._indicar("Carregando o modelo…" if not self.servidor.ativo else "Pensando…", True)
        threading.Thread(
            target=self._gerar,
            args=(caminho, nucleo.PERFIS[self.versao]["num_ctx"], list(self.mensagens), self.cancelar),
            daemon=True,
        ).start()

    def _gerar(self, caminho, num_ctx, mensagens, cancelar):
        resposta = []
        erro = None
        try:
            self.servidor.garantir(caminho, num_ctx, self.config["threads"], self.config["camadas_gpu"])
            GLib.idle_add(self._indicar, "Pensando…", True)
            for pedaco in self.servidor.conversar(mensagens, cancelar):
                resposta.append(pedaco)
                GLib.idle_add(self._mostrar_pedaco, "".join(resposta), cancelar)
        except nucleo.ErroCarlos as e:
            erro = str(e)
        GLib.idle_add(self._concluir, "".join(resposta), erro, cancelar)

    def _mostrar_pedaco(self, texto, cancelar):
        if cancelar is not self.cancelar or cancelar.is_set():
            return GLib.SOURCE_REMOVE
        if self.rotulo_resposta is None:
            self.rotulo_resposta = self._adicionar_balao("assistant", texto)
        else:
            self.rotulo_resposta.set_label(texto)
            GLib.idle_add(self._rolar_fim)
        return GLib.SOURCE_REMOVE

    def _concluir(self, resposta, erro, cancelar):
        if cancelar is not self.cancelar:
            return GLib.SOURCE_REMOVE  # conversa já foi trocada
        if resposta:
            if self.rotulo_resposta is None:
                self._adicionar_balao("assistant", resposta)
            if self.mensagens:
                self.mensagens.append({"role": "assistant", "content": resposta})
        elif self.mensagens and self.mensagens[-1]["role"] == "user":
            self.mensagens.pop()
        if self.config["historico"] and self.mensagens:
            nucleo.salvar_historico(self.mensagens)
        self._definir_ocupado(False)
        if erro:
            self._indicar(erro)
        elif cancelar.is_set():
            self._indicar("Resposta interrompida.")
        else:
            self._indicar("Pronto. Confira as respostas: a Carlos AI pode errar.")
        self.cancelar = None
        self.campo.grab_focus()
        return GLib.SOURCE_REMOVE

    # Download, sempre com consentimento
    def pedir_download(self, modelo_id):
        modelo = nucleo.CATALOGO[modelo_id]
        tamanho = nucleo.formatar_tamanho(nucleo.tamanho_total(modelo_id))
        dialogo = Adw.AlertDialog(
            heading=f"Baixar {modelo['nome']}?",
            body=f"Tamanho: {tamanho}\nLicença: {modelo['licenca']}\n{modelo['licenca_url']}\n\n"
                 "Ao baixar, você aceita essa licença. O arquivo vem do Hugging Face, é conferido por SHA-256 "
                 "e depois a Carlos AI funciona sem internet.",
        )
        dialogo.add_response("nao", "Agora não")
        dialogo.add_response("sim", "Baixar")
        dialogo.set_response_appearance("sim", Adw.ResponseAppearance.SUGGESTED)
        dialogo.set_close_response("nao")
        dialogo.connect("response", lambda _d, r: self._iniciar_download(modelo_id) if r == "sim" else None)
        dialogo.present(self)

    def _iniciar_download(self, modelo_id):
        self.cancelar = threading.Event()
        self._definir_ocupado(True)
        self._indicar("Baixando… 0%", True)
        threading.Thread(target=self._baixar, args=(modelo_id, self.cancelar), daemon=True).start()

    def _baixar(self, modelo_id, cancelar):
        erro = None
        def progresso(fracao):
            GLib.idle_add(self._indicar, f"Baixando… {fracao * 100:.0f}%", True)
        try:
            nucleo.baixar_modelo(modelo_id, progresso, cancelar)
        except nucleo.ErroCarlos as e:
            erro = str(e)
        GLib.idle_add(self._fim_download, erro)

    def _fim_download(self, erro):
        self._definir_ocupado(False)
        self.cancelar = None
        self._indicar(erro or "Modelo pronto. Envie a pergunta.")
        return GLib.SOURCE_REMOVE

    # Configurações
    def abrir_configuracoes(self):
        dialogo = Adw.PreferencesDialog(title="Configurações")
        dialogo.add(self._pagina_geral(dialogo))
        dialogo.add(self._pagina_otimizador(dialogo))
        dialogo.present(self)

    def _salvar(self, chave, valor):
        self.config[chave] = valor
        nucleo.salvar_config(self.config)

    def _pagina_geral(self, dialogo):
        pagina = Adw.PreferencesPage(title="Geral", icon_name="emblem-system-symbolic")

        privacidade = Adw.PreferencesGroup(title="Privacidade",
                                           description="Sem telemetria. O histórico fica só neste computador.")
        historico = Adw.SwitchRow(title="Guardar a última conversa", active=self.config["historico"])
        def mudar_historico(linha, _p):
            self._salvar("historico", linha.get_active())
            if not linha.get_active():
                nucleo.apagar_historico()
        historico.connect("notify::active", mudar_historico)
        privacidade.add(historico)
        apagar = Adw.ActionRow(title="Apagar conversas")
        botao = Gtk.Button(label="Apagar", valign=Gtk.Align.CENTER)
        botao.add_css_class("destructive-action")
        botao.connect("clicked", lambda *_: (nucleo.apagar_historico(), self.nova_conversa(),
                                             dialogo.add_toast(Adw.Toast(title="Conversas apagadas."))))
        apagar.add_suffix(botao)
        privacidade.add(apagar)
        pagina.add(privacidade)

        desempenho = Adw.PreferencesGroup(title="Desempenho")
        inatividade = Adw.SpinRow.new_with_range(0, 120, 1)
        inatividade.set_title("Descarregar o modelo após (minutos)")
        inatividade.set_subtitle("0 mantém carregado enquanto a janela estiver aberta")
        inatividade.set_value(self.config["inatividade_min"])
        inatividade.connect("notify::value", lambda r, _p: self._salvar("inatividade_min", int(r.get_value())))
        desempenho.add(inatividade)
        threads = Adw.SpinRow.new_with_range(0, 64, 1)
        threads.set_title("Threads")
        threads.set_subtitle(f"0 é automático ({nucleo.threads_padrao()} aqui). Vale ao recarregar o modelo.")
        threads.set_value(self.config["threads"])
        threads.connect("notify::value", lambda r, _p: self._salvar("threads", int(r.get_value())))
        desempenho.add(threads)
        pagina.add(desempenho)

        self._grupos_modelo = {}
        modelos = Adw.PreferencesGroup(title="Modelos", description="Nada é baixado sem a sua confirmação.")
        for modelo_id, modelo in nucleo.CATALOGO.items():
            modelos.add(self._linha_modelo(modelo_id, modelo, dialogo))
        pagina.add(modelos)

        sobre = Adw.PreferencesGroup()
        sobre.add(Adw.ActionRow(title="Carlos AI", subtitle=f"Versão {VERSAO}"))
        pagina.add(sobre)
        return pagina

    def _linha_modelo(self, modelo_id, modelo, dialogo):
        tamanho = nucleo.formatar_tamanho(nucleo.tamanho_total(modelo_id))
        versao = nucleo.PERFIS[modelo["versao"]]["nome"]
        linha = Adw.ActionRow(title=GLib.markup_escape_text(modelo["nome"]),
                              subtitle=GLib.markup_escape_text(f"{versao} · {tamanho} · {modelo['licenca']}"))
        usar = Gtk.CheckButton(active=self.config["modelos"][modelo["versao"]] == modelo_id,
                               valign=Gtk.Align.CENTER, tooltip_text="Usar este modelo")
        def escolher(botao):
            if botao.get_active():
                self.config["modelos"][modelo["versao"]] = modelo_id
                nucleo.salvar_config(self.config)
        usar.connect("toggled", escolher)
        grupo = self._grupos_modelo.setdefault(modelo["versao"], usar)
        if grupo is not usar:
            usar.set_group(grupo)
        linha.add_prefix(usar)
        if nucleo.modelo_instalado(modelo_id):
            remover = Gtk.Button(icon_name="user-trash-symbolic", tooltip_text="Apagar do disco",
                                 valign=Gtk.Align.CENTER)
            remover.add_css_class("flat")
            def apagar(*_):
                self.servidor.parar()
                nucleo.apagar_modelo(modelo_id)
                remover.set_sensitive(False)
            remover.connect("clicked", apagar)
            linha.add_suffix(remover)
        else:
            baixar = Gtk.Button(icon_name="folder-download-symbolic", tooltip_text="Baixar",
                                valign=Gtk.Align.CENTER)
            baixar.add_css_class("flat")
            def pedir(*_):
                dialogo.close()
                self.pedir_download(modelo_id)
            baixar.connect("clicked", pedir)
            linha.add_suffix(baixar)
        return linha

    def _pagina_otimizador(self, dialogo):
        pagina = Adw.PreferencesPage(title="Otimizador", name="otimizador", icon_name="power-profile-balanced-symbolic")
        estado = nucleo.estado_otimizador()
        if estado is None:
            grupo = Adw.PreferencesGroup(title="Otimizador Carlos",
                                         description="O serviço não está ativo neste computador.")
            pagina.add(grupo)
            return pagina

        ajustes = Adw.PreferencesGroup(title="Ajustes automáticos",
                                       description="Lista fixa, reversível. Nenhum usa modelo de IA.")
        for ajuste in estado.get("ajustes", []):
            ajustes.add(Adw.ActionRow(title=GLib.markup_escape_text(ajuste["titulo"]),
                                      subtitle=GLib.markup_escape_text(ajuste["situacao"])))
        pagina.add(ajustes)

        sugestoes = Adw.PreferencesGroup(title="Sugestões",
                                         description="Só você decide: nada aqui é aplicado automaticamente.")
        itens = estado.get("sugestoes", [])
        for sugestao in itens:
            sugestoes.add(Adw.ActionRow(title=GLib.markup_escape_text(sugestao["texto"])))
        if not itens:
            sugestoes.add(Adw.ActionRow(title="Nenhuma sugestão no momento."))
        explicar = Gtk.Button(label="Explicar com a IA", halign=Gtk.Align.START, margin_top=12)
        def pedir_explicacao(*_):
            dialogo.close()
            self.perguntar(nucleo.pergunta_sobre_otimizador(estado))
        explicar.connect("clicked", pedir_explicacao)
        sugestoes.add(explicar)
        pagina.add(sugestoes)
        return pagina


class Aplicativo(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.janela = None

    def do_activate(self):
        if self.janela is None:
            self.janela = Janela(self)
        self.janela.present()


def main():
    return Aplicativo().run(None)
