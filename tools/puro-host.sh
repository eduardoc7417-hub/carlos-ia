#!/bin/sh
# Prepara o Debian do WSL para compilar o Carlos OS Puro. Não toca em discos reais.
# O disco é um arquivo em /opt/puro, usado por loop, e só cresce conforme o uso.
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get install -y --no-install-recommends \
  build-essential bison gawk m4 texinfo python3 xz-utils wget patch file bzip2 >/dev/null
mkdir -p /opt/puro
[ -f /opt/puro/disco.img ] || truncate -s 150G /opt/puro/disco.img
ls -lhs /opt/puro/disco.img
df -h /opt | tail -1
for t in bash gcc g++ ld bison gawk m4 make patch perl python3 sed tar makeinfo xz; do
  printf '%s: ' "$t"
  "$t" --version 2>/dev/null | head -1 | cut -c1-60
done
echo "sh -> $(readlink -f /bin/sh)"
echo "awk -> $(readlink -f /usr/bin/awk)"
echo "yacc -> $(readlink -f /usr/bin/yacc 2>/dev/null)"
echo "kernel: $(uname -r); cpus: $(nproc)"
