#!/bin/sh
# Gera a ISO do Carlos OS Aurora. Rodar como root no Debian do WSL.
# A construção usa o disco do WSL; só a ISO e o hash voltam para out/.
set -eu
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
WORK=/opt/carlos-build
NAME=carlos-os-aurora-0.9-instalavel-amd64
# Espelho rápido no desenvolvimento; a lista exata de pacotes fica em out/. A ISO final fixa a data no snapshot.
MIRROR=https://deb.debian.org/debian/

mkdir -p "$WORK" "$PROJECT/out"
cd "$WORK"
# --all mantém o cache de pacotes, para não baixar tudo de novo.
lb clean --all >/dev/null 2>&1 || true
rm -rf config auto

lb config noauto \
  --mode debian \
  --distribution sid \
  --architectures amd64 \
  --archive-areas "main non-free-firmware" \
  --security false \
  --updates false \
  --mirror-bootstrap "$MIRROR" \
  --mirror-chroot "$MIRROR" \
  --mirror-binary "$MIRROR" \
  --parent-mirror-bootstrap "$MIRROR" \
  --parent-mirror-chroot "$MIRROR" \
  --parent-mirror-binary "$MIRROR" \
  --apt-options "--yes -o Acquire::ForceIPv4=true -o Acquire::Retries=5" \
  --binary-images iso-hybrid \
  --bootloaders "grub-efi,syslinux" \
  --debian-installer none \
  --memtest none \
  --apt-recommends false \
  --firmware-binary false \
  --firmware-chroot false \
  --iso-application "Carlos OS Aurora" \
  --iso-publisher "Carlos OS Aurora" \
  --iso-volume "CARLOS_OS_AURORA" \
  --bootappend-live "boot=live components hostname=carlos-os username=carlos locales=pt_BR.UTF-8 keyboard-layouts=br timezone=America/Sao_Paulo quiet splash console=ttyS0,115200n8 console=tty0"

# A pasta do Windows mostra tudo como 777: as permissões da imagem são definidas aqui.
rsync -a --chmod=D755,F644 "$PROJECT/config/live/" config/
find config/hooks -type f -exec chmod 755 {} +
chmod 755 config/includes.chroot/usr/lib/live/config/* config/includes.chroot/usr/share/calamares/helpers/* config/includes.chroot/usr/bin/*
mkdir -p config/packages.chroot
cp "$PROJECT"/carlos-ai/dist/*.deb config/packages.chroot/

lb build

ISO=$(ls -1 ./*.iso | head -1)
cp "$ISO" "$PROJECT/out/$NAME.iso"
cp ./*.packages "$PROJECT/out/$NAME.packages" 2>/dev/null || true
cd "$PROJECT/out"
sha256sum "$NAME.iso" | tee "$NAME.iso.sha256"
ls -l "$NAME.iso"
