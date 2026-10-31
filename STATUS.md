# Status real

Atualizado em 2026-10-31. Estados: planejado, em desenvolvimento, implementado, testado, aprovado.

| Componente | Estado | Observação |
|---|---|---|
| ISO 0.3 (sid, GNOME 51, CarlosUI) | Testado em parte | Área de trabalho abre em BIOS e UEFI no QEMU (`TESTES.md`) |
| CarlosUI: dock, barra, vidro, botões à esquerda | Em desenvolvimento | Primeira versão; aplicativos e janelas não testados |
| Papéis de parede (8 Aurora e 6 Flor) | Implementado | Ajuste das flores feito no script; arte ainda não regenerada nem incluída em ISO |
| Instalador | Planejado | Não existe |
| Carlos AI Lite e Pro para Linux e Otimizador | Em desenvolvimento | Na outra conversa, em `carlos-ai/`; não integrados |
| Protótipo Carlos AI no Windows | Testado em parte | Só a Lite (`prototipos/carlos-ai/RESULTADOS.md`) |
| Apps Android, .exe e Pacote Cleo | Planejado | Não testados |
| Computador real | Planejado | Só QEMU até agora |

## Onde parei

1. Rodar `python3 -I tools/gen-art.py` no Debian para aplicar o ajuste das flores e conferir a prévia.
2. Investigar pelo console serial, com `tools/debug-iso.sh`: relógio em UTC e abertura na visão geral.
3. Colocar o menu Aurora na barra superior.
4. Integrar a Carlos AI e o Otimizador quando a outra conversa terminar.
5. Integrar o instalador e testar a instalação em disco virtual.
