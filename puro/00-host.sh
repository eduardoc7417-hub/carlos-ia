#!/bin/bash
# Prepara o Debian (host) para compilar o LFS 13.1 (systemd). Rodar como root, uma vez.
set -euo pipefail
apt-get update
apt-get install -y build-essential bison gawk m4 texinfo python3 patch xz-utils wget file e2fsprogs
# O LFS exige que /bin/sh seja o bash (no Debian é o dash).
ln -sf bash /usr/bin/sh
