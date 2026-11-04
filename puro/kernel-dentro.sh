#!/bin/bash
# Roda DENTRO do chroot do Carlos OS (chamado pelo 07-kernel-imagem.sh). Compila o kernel do capítulo 10.
set -euo pipefail
KVER=7.1.8
cd /sources
rm -rf "linux-$KVER"
tar -xf "linux-$KVER.tar.xz"
cd "linux-$KVER"
make mrproper
make defconfig
# Exigências do livro para o systemd (cap. 10.3) e o que a máquina virtual precisa (virtio), tudo embutido no kernel.
scripts/config \
  -e DEVTMPFS -e DEVTMPFS_MOUNT -e CGROUPS -e MEMCG -e PSI -e INOTIFY_USER -e TMPFS_POSIX_ACL -e TMPFS_XATTR \
  -e SECCOMP -e SECCOMP_FILTER -e AUTOFS_FS -e DMIID -e BPF_SYSCALL -e CGROUP_BPF -e IPV6 -d UEVENT_HELPER \
  -e EXT4_FS -e VIRTIO_PCI -e VIRTIO_BLK -e VIRTIO_NET -e VIRTIO_CONSOLE -e HW_RANDOM_VIRTIO -e SERIAL_8250_CONSOLE
make olddefconfig
make
make modules_install
cp -v arch/x86/boot/bzImage "/boot/vmlinuz-$KVER-carlos"
cp -v System.map "/boot/System.map-$KVER"
cp -v .config "/boot/config-$KVER"
cd /sources && rm -rf "linux-$KVER"
# shortcut: root sem senha para o primeiro teste no QEMU; antes de distribuir, defina uma senha (passwd root).
passwd -d root
