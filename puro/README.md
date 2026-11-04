# Carlos OS Aurora: Linux From Scratch

Sistema compilado do zero, sem distribuição de base, seguindo o livro **LFS 13.1 (systemd)**, tag `r13.1`.
O Debian do WSL serve só para compilar (é o "host"); nada dele entra no sistema.

## Etapa 1: núcleo bootável

Rodar no WSL, na ordem. Os scripts que pedem root usam `-u root`, e o 06 usa o usuário `construtor`:

| Script | Usuário | O que faz |
|---|---|---|
| `00-host.sh` | root | Pacotes do host e `/bin/sh` → bash. Uma vez. |
| `01-disco.sh` | root | Cria e monta o disco de 60 GB em `/mnt/lfs`. Repita sempre que o WSL reiniciar (os outros scripts já chamam). |
| `02-fontes.sh` | root | Baixa os 94 pacotes e confere o MD5. Pode repetir. |
| `03-conferir-host.sh` | root | Roda a conferência oficial do livro. |
| `04-jhalfs.sh` | root | Instala a jhalfs (automação oficial do LFS) e o usuário `construtor`. Uma vez. |
| `06-compilar.sh gerar` | construtor | Gera os scripts dos capítulos 4 a 11 a partir do livro (`05-configurar-jhalfs.py` define as opções). |
| `06-compilar.sh compilar` | construtor | Compila. Se parar, rode de novo: continua de onde parou. |
| `07-kernel-imagem.sh` | root | Kernel 7.1.8 (`kernel-dentro.sh`), disco de 16 GB com GRUB. |
| `08-testar-qemu.sh` | root | Liga no QEMU e espera o `login:`. Com `--usar`, abre o console. |

Exemplo, no PowerShell:

    wsl --cd "<pasta>\lfs" -d Debian -u construtor -- bash 06-compilar.sh compilar

Os logs de cada pacote ficam em `/mnt/lfs/jhalfs/logs/` e os dos testes em `/mnt/lfs/jhalfs/test-logs/`.

## Atalhos que precisam mudar antes de distribuir

- O `root` fica **sem senha** para o primeiro teste (`kernel-dentro.sh`).
- O disco é uma imagem dentro do WSL, e o `fstab` aponta para `/dev/vda1` (o disco da máquina virtual).
- A rede é estática para o QEMU (`10.0.2.15`, placa `enp0s3`).
