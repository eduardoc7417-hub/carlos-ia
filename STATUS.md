# Status real

Atualizado em 2026-10-31. Estados: planejado, em desenvolvimento, implementado, testado, aprovado.

| Componente | Estado | Observação |
|---|---|---|
| ISO 0.7 (sid, GNOME 51, CarlosUI) | Testado em VM | Live e instalação em UEFI no QEMU (`TESTES.md`) |
| Instalador (Calamares) | Testado em VM | Instalação em UEFI; BIOS não testado. Precisa de internet para instalar o GRUB |
| CarlosUI: dock, barra, vidro, Menu Aurora | Em desenvolvimento | Sem ícones próprios, perfis de vidro nem ampliação do dock |
| Papéis de parede (8 Aurora e 6 Flor) | Implementado | Na ISO; seleção nas Configurações não testada |
| Carlos AI | Em desenvolvimento | Lite respondeu uma pergunta no sistema instalado; Pro não testada |
| Otimizador Carlos | Em desenvolvimento | Serviço ativo no sistema instalado; ajustes reais não avaliados |
| Programas .exe (Wine) | Em desenvolvimento | Bloco de Notas de 64 bits abriu na VM; integrado à ISO 0.8, não testada |
| Apps Android (Waydroid) | Em desenvolvimento | Android abriu na VM; integrado à ISO 0.8, não testada; imagem baixada com consentimento |
| Pacote Cleo, VS Code | Planejado | Não testados |
| Computador real | Planejado | Só QEMU até agora; rede, áudio e fluidez sem teste |

## Onde parei (2026-10-31, 21:40)

ISO 0.8 gerada em `out/` (SHA-256 `8f87caa1da8fd223271d5e17a277142e943311b3e23ff8aaed16961e8d4ca645`).
Instalou em disco virtual (`/opt/vm/disco.qcow2`) e reiniciou sem a ISO.

Falta, nesta ordem:

1. Abrir o ícone Android de novo no sistema instalado: o download foi interrompido e recomeça.
2. Testar um `.exe` de 64 bits.
3. Gravar o vídeo com a Flor Violeta (`ffmpeg` pode faltar no Debian do WSL) e publicar no GitHub.
4. Entregar o texto do lançamento 0.8, com o pacote de código-fonte exigido pela GPL.
5. Depois, a versão 0.9 em Debian. O Carlos OS Puro fica para mais tarde (`docs/carlos-os-puro.md`).

Para ligar a VM: `sh tools/vm.sh run nenhuma` como root no Debian do WSL. Com janela: `VM_TELA=gtk` antes do comando.

## Atualização (2026-11-01)

ISO 0.9 gerada (SHA-256 `dcfb6f10ad5efe5f2a45ec7eae1286dda96086e93a6273a4c1820eae625b72b7`), com Btrfs, restauração, zram, loja e Wine.
Resultados em `TESTES.md`. Faltam: instalar app pela loja, vídeo, dual boot em VM, logo na tela de boot e pacote de código-fonte.

## Defeitos conhecidos

- A imagem de apresentação do instalador aparece em branco durante a instalação.
- A base sid muda com frequência: a ISO final precisa fixar a data do repositório.
- A distribuição pública da ISO exige oferecer o código-fonte dos pacotes GPL; isso ainda não foi resolvido.
