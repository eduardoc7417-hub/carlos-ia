#!/bin/sh
# Instala as ferramentas de construção e teste no Debian do WSL. Rodar como root.
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  live-build debootstrap squashfs-tools xorriso grub-pc-bin grub-efi-amd64-bin \
  mtools dosfstools syslinux syslinux-common isolinux \
  qemu-system-x86 qemu-utils ovmf git ca-certificates rsync socat \
  python3 python3-numpy python3-pil fonts-inter
lb --version
qemu-system-x86_64 --version | head -1
