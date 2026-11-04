#!/bin/bash
# Cria (uma vez) e monta o disco do LFS em /mnt/lfs. Rodar como root a cada vez que o WSL reiniciar.
# O usuário lfs e as pastas do capítulo 4 ficam com a jhalfs.
# shortcut: um arquivo de imagem ext4 dentro do WSL em vez de uma partição real; para instalar em hardware, use um disco de verdade.
set -euo pipefail
IMAGEM=/var/lib/carlos-lfs/lfs.img
if [ ! -f "$IMAGEM" ]; then
  mkdir -p "$(dirname "$IMAGEM")"
  truncate -s 60G "$IMAGEM"
  mkfs.ext4 -q -L carlos-lfs "$IMAGEM"
fi
mkdir -p /mnt/lfs
mountpoint -q /mnt/lfs || mount -o loop "$IMAGEM" /mnt/lfs
mkdir -p /mnt/lfs/sources
chmod a+wt /mnt/lfs/sources
df -h /mnt/lfs | tail -1
