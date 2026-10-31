# Carlos AI e Otimizador Carlos

Dois pacotes para Debian sid, GNOME 51, x86-64:

- **carlos-ai:** aplicativo GTK4 + libadwaita, com Lite e Pro na mesma arquitetura.
- **carlos-otimizador:** serviço leve, sem modelo de IA, com ajustes reversíveis de memória e energia.

Os resultados dos testes estão em `tests/RESULTADOS.md`.

## Gerar e instalar

Como root, no Linux:

    sh tools/build-deb.sh
    apt install ./dist/carlos-ai_*_all.deb ./dist/carlos-otimizador_*_all.deb

O `carlos-ai` depende de `llama.cpp-tools`, disponível no Debian sid. O modelo não vem no pacote.

## Carlos AI

```
Janela GTK4 → API local em 127.0.0.1, com porta aleatória e token → llama-server → GGUF em ~/.local/share/carlos-ai/modelos
```

- O `llama-server` sobe na primeira pergunta, é filho do aplicativo e sai por inatividade (5 minutos por padrão) ou ao
  fechar a janela. Nada fica ativo no boot.
- **Modelos:** o download só começa depois de o usuário ver nome, tamanho e licença e confirmar. O SHA-256 é conferido.
  - Lite: Gemma 3 1B (806 MB, Gemma Terms of Use) ou Qwen2.5 1.5B (1,1 GB, Apache 2.0).
  - Pro: Qwen2.5 7B (4,7 GB, Apache 2.0).
- **Histórico:** desligado por padrão. Se ligado, guarda a última conversa só neste computador e pode ser apagado.
- **Limites:** sem telemetria. O aplicativo não executa comandos: o único processo que ele inicia é o `llama-server`.

## Otimizador Carlos

Acorda uma vez por minuto e aplica só a lista fixa do programa (`carlos-otimizador lista`):

| Identificador | Ajuste | Quando |
|---|---|---|
| `memoria-swappiness-zram` | `vm.swappiness=100` | há zram |
| `memoria-page-cluster-zram` | `vm.page-cluster=0` | há zram |
| `memoria-mglru-protecao` | `lru_gen/min_ttl_ms=1000` | sempre |
| `memoria-thp-madvise` | `transparent_hugepage=madvise` | sempre |
| `energia-escrita-bateria` | `vm.dirty_writeback_centisecs=1500` | na bateria |
| `energia-nmi-bateria` | `kernel.nmi_watchdog=0` | na bateria |
| `energia-epp-bateria` | EPP `balance_power` | na bateria, sem `power-profiles-daemon` ativo |

- **Reversível:** o valor original fica em `/var/lib/carlos-otimizador/originais.json` e volta quando o serviço para ou a
  condição deixa de valer. Um valor que outra pessoa ou programa mudou depois é respeitado.
- **Fora da lista:** só vira sugestão (pressão de memória, falta de swap, disco cheio, serviços lentos no boot), publicada
  em `/run/carlos-otimizador/estado.json`. O botão "Explicar com a IA" abre a Carlos AI sob demanda: ela explica e não altera nada.
- **Sem modelo:** o serviço não carrega modelo nem usa rede (`PrivateNetwork=yes`).

Controle:

    systemctl disable --now carlos-otimizador      # desliga e reverte
    carlos-otimizador estado                       # mostra ajustes e sugestões

Para desligar ajustes, crie `/etc/carlos-otimizador/config.json`. A configuração só desliga: não aceita caminhos nem valores.

    {"desligados": ["memoria-thp-madvise"]}

Com `{"ativo": false}`, todos ficam desligados.

## Testes

No Debian do WSL, como root:

    sh tools/preparar-teste.sh
    sh tools/testar.sh /caminho/para/modelo.gguf

Eles usam o chroot `/opt/carlos-ai-teste`, sem tocar em `/opt/carlos-build`.
