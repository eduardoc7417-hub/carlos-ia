#!/bin/bash
# Instala a jhalfs (automação oficial do LFS) e o usuário que a roda. Rodar como root, uma vez.
# A jhalfs exige um usuário comum com sudo; o usuário "construtor" só existe dentro deste WSL de compilação.
set -euo pipefail
apt-get install -y git sudo libxml2-utils xsltproc docbook-xml docbook-xsl
if ! id construtor >/dev/null 2>&1; then
  useradd -m -s /bin/bash construtor
fi
echo 'construtor ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/construtor
chmod 440 /etc/sudoers.d/construtor
if [ ! -d ~construtor/jhalfs ]; then
  sudo -u construtor git clone -q https://github.com/lfs-book/jhalfs.git ~construtor/jhalfs
fi
sudo -u construtor git -C ~construtor/jhalfs log -1 --format='jhalfs %h %cs'
