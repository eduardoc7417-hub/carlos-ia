#!/bin/sh
# Mostra o estado do ambiente de construção. Não altera nada.
head -3 /etc/os-release
echo "debian_version: $(cat /etc/debian_version)"
echo "kernel: $(uname -r)"
df -h / | tail -1
free -h | head -2
echo "cpus: $(nproc)"
ls -l /dev/kvm 2>&1
echo "avx2: $(grep -m1 -o avx2 /proc/cpuinfo)"
echo "vmx threads: $(grep -c vmx /proc/cpuinfo)"
echo "usuarios:"
awk -F: '$3>=1000 && $3<65000 {print "  " $1, $3}' /etc/passwd
echo "pid1: $(ps -p 1 -o comm=)"
echo "rede: $(timeout 8 getent hosts deb.debian.org | head -1)"
for t in lb qemu-system-x86_64 git xorriso mksquashfs; do
  echo "$t: $(command -v "$t" || echo ausente)"
done
