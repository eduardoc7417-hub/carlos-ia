#!/bin/bash
# Baixa o código-fonte de todos os pacotes do LFS 13.1 e confere o MD5 de cada um, como manda o livro.
# Pode ser repetido: só baixa o que falta.
set -euo pipefail
LIVRO=https://www.linuxfromscratch.org/lfs/view/13.1-systemd
bash "$(dirname "$0")/01-disco.sh" >/dev/null
cd /mnt/lfs/sources
wget -q -O wget-list "$LIVRO/wget-list-systemd"
wget -q -O md5sums "$LIVRO/md5sums"
# O wget sai com erro se um único servidor falhar; quem decide se está tudo certo é o MD5 logo abaixo.
wget --input-file=wget-list --continue --no-verbose --tries=3 --timeout=60 2>&1 | tee wget.log | grep -vE ' -> ' || true
if ! md5sum -c --quiet md5sums; then
  echo "Faltam ou estão corrompidos os arquivos acima. Rode de novo; veja os erros em /mnt/lfs/sources/wget.log." >&2
  exit 1
fi
chown root:root ./*
echo "Todos os $(wc -l < md5sums) arquivos conferem."
