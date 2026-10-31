#!/bin/sh
# Gera a ISO do Carlos OS Aurora. Rodar como root no Debian do WSL.
# A construção usa o disco do WSL; só a ISO e o hash voltam para out/.
set -eu
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
WORK=/opt/carlos-build
NAME=carlos-os-aurora-0.1.1-minimal-amd64

mkdir -p "$WORK" "$PROJECT/out"
cd "$WORK"
lb clean --purge >/dev/null 2>&1 || true
rm -rf config auto

lb config noauto \
  --mode debian \
  --distribution trixie \
  --architectures amd64 \
  --archive-areas "main non-free-firmware" \
  --security true \
  --updates true \
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
  --bootappend-live "boot=live components hostname=carlos-os username=carlos locales=pt_BR.UTF-8 keyboard-layouts=br console=tty0 console=ttyS0,115200n8"

rsync -a "$PROJECT/config/live/" config/

lb build

ISO=$(ls -1 ./*.iso | head -1)
cp "$ISO" "$PROJECT/out/$NAME.iso"
cd "$PROJECT/out"
sha256sum "$NAME.iso" | tee "$NAME.iso.sha256"
ls -l "$NAME.iso"
