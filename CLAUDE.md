# Carlos OS Aurora

Distribuição Linux com interface própria (CarlosUI) inspirada no macOS, sem mostrar a base no uso normal.
Responder em português do Brasil, de forma curta. Não declarar nada como testado sem executar.

## Economia de créditos

- Ler só os arquivos necessários; não refazer pesquisas já salvas em `reports/` e `research_notes/`.
- Não usar subagentes nem pesquisa profunda, salvo pedido explícito.
- Para consultar a construção, rodar `tools/status.sh` em vez de exibir logs completos.

## Decisões

- Base: Debian sid com data fixa do repositório e live-build, por pedido do usuário de ter o GNOME mais recente. Substitui Debian 13 (`docs/decisao-base.md`), Ubuntu e Linux From Scratch.
- Interface: GNOME 51; a pesquisa foi feita para o GNOME 50, então conferir cada extensão no 51.
- Construção: WSL2 Debian; o QEMU usa KVM quando disponível, mas serve para boot e instalação, não para medir fluidez.
- Situação real em `STATUS.md`, testes em `TESTES.md`, fases em `ROADMAP.md`.
- Carlos AI: só depois da base funcional (`docs/carlos-ai.md`).

## Ambiente

Hardware de referência e de desenvolvimento: i5-4570, 16 GB, Intel HD 4600, Windows 11 Pro.
Rodar scripts como root, sem senha, e pelo arquivo (o PowerShell quebra `|` dentro de comandos entre aspas):

    wsl.exe -d Debian -u root -- sh /mnt/c/Users/carlos/Downloads/Carlos-OS-Aurora/tools/<script>.sh

- `tools/setup-host.sh`: instala as ferramentas.
- `tools/build-iso.sh`: gera a ISO em `out/`; o trabalho fica em `/opt/carlos-build`; log em `/opt/build.log`.
- `tools/test-iso.sh <iso> <bios|uefi>`: teste de boot.
- `tools/status.sh`: andamento da construção.

## Cuidados

- O pendrive `CARLOS_OS_A` (E:) é a única cópia do trabalho anterior: não formatar nem gravar.
- Não formatar o computador principal sem autorização.
- Não usar fontes SF, logo, ícones ou papéis de parede da Apple.

## Próximos marcos

Ver `ROADMAP.md`. A ISO mínima já inicia em BIOS e UEFI no QEMU; o próximo é o GNOME 51.
