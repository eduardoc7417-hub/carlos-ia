# Resultados dos testes

Executados em 2026-10-31 com `tools/testar.sh`, em um chroot Debian sid (`/opt/carlos-ai-teste`) dentro do WSL.
Versões: Python 3.14, GTK 4.24.1, libadwaita 1.10.0, llama.cpp 0.7.0. Modelo: Gemma 3 1B, cópia já existente no Ollama.

## Testado

| Item | Resultado |
|---|---|
| `.deb` gerados, instalados e reinstalados com `apt` | ok; dependências resolvidas no sid |
| Serviço fica habilitado (`systemctl is-enabled`) | ok, no chroot |
| `desktop-file-validate` e `systemd-analyze verify` | ok; só avisos de permissão do arquivo no NTFS, fora do pacote |
| `test_otimizador.py`: 11 testes em árvore falsa | ok |
| Aplicar, reverter, SIGTERM, volta depois de queda, bateria, zram, respeito à mudança do usuário | ok, em árvore falsa |
| Memória do Otimizador | 17,6 MB de RSS, em árvore falsa |
| `test_nucleo.py`: 12 testes | ok |
| Download com retomada, SHA-256 errado e cancelamento | ok, em servidor HTTP local |
| `llama-server` real: carga, resposta, recusa sem token (401), token fora da linha de comando, encerramento | ok |
| Janela em Xvfb (renderizador cairo), pelas funções internas da interface | ok; capturas em `tests/capturas/` |
| Consentimento: sem confirmação, nada é baixado | ok |
| Pergunta real, parar, nova conversa, histórico salvo e apagado | ok |
| Descarga por inatividade, com o relógio de inatividade adiantado | ok |
| "Explicar com a IA", com um estado de exemplo escrito pelo teste | ok |

Carga do modelo: 26 a 37 s no WSL, lendo do disco do Windows e com outros trabalhos na máquina. Não serve como
medida de desempenho.

## Bugs encontrados pelos testes e corrigidos

- O `llama-server` morria ao fim de cada resposta: `PR_SET_PDEATHSIG` segue a linha que criou o processo.
  Agora uma linha permanente faz o lançamento.
- A leitura de `/proc/pressure/memory` não encontrava o valor de `avg300`.

## Não testado

- **Otimizador em um sistema real:** ele nunca escreveu em `/proc/sys` ou `/sys` reais nem rodou sob systemd, pois o
  kernel do WSL é compartilhado com a construção da ISO. As restrições da unidade (`MemoryMax`, `ProtectSystem` e
  outras) também não foram exercitadas. Testar no QEMU, antes de confiar.
- **GNOME 51 em sessão real:** a janela só rodou em Xvfb, como root, sem Wayland nem GNOME Shell.
- **Modelos reais pelo aplicativo:** nenhum download real do Hugging Face. Os hashes vieram da API dele; o Gemma de
  teste é a cópia do Ollama, não o arquivo do catálogo.
- **Carlos AI Pro:** o Qwen2.5 7B, em duas partes, não foi baixado nem carregado. Só o Lite rodou com modelo real.
- **`qwen2.5-1.5b` no llama.cpp** e cliques reais de mouse e teclado na janela.
- **Hardware real:** i5-4570 fora do WSL, AVX2 pelo backend `haswell` e GPU (`camadas_gpu` fica em 0).

## Limites conhecidos

- O `llama-server` é processo filho do aplicativo, não serviço de usuário do systemd como propõe `docs/carlos-ai.md`.
- O histórico guarda só a última conversa.
- As qualidades de resposta medidas em `prototipos/carlos-ai/RESULTADOS.md` continuam valendo: o Lite erra bastante.
