#!/bin/bash
# Compila o kernel no chroot e monta um disco bootável (BIOS + GRUB) para testar no QEMU. Rodar como root depois do 06.
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
LFS=/mnt/lfs
KVER=7.1.8
IMAGEM=/var/lib/carlos-lfs/carlos-os.img
DESTINO=/mnt/carlos-img
bash "$AQUI/01-disco.sh" >/dev/null

montar_virtuais() {  # cap. 7.3: sistemas de arquivos virtuais do kernel dentro do chroot
  local raiz=$1
  for d in dev dev/pts proc sys run; do mkdir -p "$raiz/$d"; done
  mountpoint -q "$raiz/dev" || mount --bind /dev "$raiz/dev"
  mountpoint -q "$raiz/dev/pts" || mount -t devpts devpts -o gid=5,mode=0620 "$raiz/dev/pts"
  mountpoint -q "$raiz/proc" || mount -t proc proc "$raiz/proc"
  mountpoint -q "$raiz/sys" || mount -t sysfs sysfs "$raiz/sys"
  mountpoint -q "$raiz/run" || mount -t tmpfs tmpfs "$raiz/run"
}
desmontar_virtuais() {
  local raiz=$1
  for d in run sys proc dev/pts dev; do mountpoint -q "$raiz/$d" && umount "$raiz/$d"; done
  return 0
}
dentro() {  # roda um comando no chroot com o ambiente limpo do livro
  chroot "$1" /usr/bin/env -i HOME=/root TERM=xterm PATH=/usr/bin:/usr/sbin MAKEFLAGS="-j$(nproc)" "${@:2}"
}

# 1. Kernel
montar_virtuais "$LFS"
trap 'desmontar_virtuais "$LFS"' EXIT
cp "$AQUI/kernel-dentro.sh" "$LFS/tmp/kernel-dentro.sh"
dentro "$LFS" /bin/bash /tmp/kernel-dentro.sh
cp "$LFS/boot/config-$KVER" "$AQUI/config-$KVER"   # guarda a configuração do kernel no projeto
desmontar_virtuais "$LFS"
trap - EXIT

# 2. Disco com uma partição, copiado do /mnt/lfs sem as ferramentas de compilação
rm -f "$IMAGEM"
truncate -s 16G "$IMAGEM"
echo 'start=2048, type=83, bootable' | sfdisk -q "$IMAGEM"
LOOP=$(losetup -fP --show "$IMAGEM")
trap 'umount -R "$DESTINO" 2>/dev/null; losetup -d "$LOOP"' EXIT
mkfs.ext4 -q -L carlos-os "${LOOP}p1"
mkdir -p "$DESTINO"
mount "${LOOP}p1" "$DESTINO"
(cd "$LFS" && tar --exclude=./sources --exclude=./tools --exclude=./jhalfs --exclude=./lost+found -cf - .) | tar -C "$DESTINO" -xpf -

# 3. GRUB do próprio Carlos OS, instalado no começo do disco
montar_virtuais "$DESTINO"
dentro "$DESTINO" grub-install --target=i386-pc --boot-directory=/boot "$LOOP"
cat > "$DESTINO/boot/grub/grub.cfg" << EOF
set default=0
set timeout=3
insmod part_msdos
insmod ext2
set root=(hd0,msdos1)
menuentry "Carlos OS Aurora (LFS 13.1)" {
  linux /boot/vmlinuz-$KVER-carlos root=/dev/vda1 ro console=tty0 console=ttyS0,115200
}
EOF
desmontar_virtuais "$DESTINO"
echo "Imagem pronta: $IMAGEM"
