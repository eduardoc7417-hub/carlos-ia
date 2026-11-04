#!/bin/bash
# Roda a etapa 1 inteira, do disco vazio ao fim do capítulo 9. Rodar como root.
# Pode ser repetido: o download só baixa o que falta, e o make da jhalfs continua de onde parou.
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
bash "$AQUI/01-disco.sh"
bash "$AQUI/02-fontes.sh"
if [ ! -f /mnt/lfs/jhalfs/Makefile ]; then
  sudo -u construtor bash "$AQUI/06-compilar.sh" gerar
fi
sudo -u construtor bash "$AQUI/06-compilar.sh" compilar
