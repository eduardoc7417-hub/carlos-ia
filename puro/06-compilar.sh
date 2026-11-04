#!/bin/bash
# Gera os scripts dos capítulos 4 a 9 a partir do livro e compila. Rodar como construtor.
#   bash 06-compilar.sh gerar     -> só gera os scripts em /mnt/lfs/jhalfs
#   bash 06-compilar.sh compilar  -> roda o make; pode ser repetido: continua de onde parou
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
sudo bash "$AQUI/01-disco.sh" >/dev/null
case "${1:-}" in
  gerar)
    python3 "$AQUI/05-configurar-jhalfs.py"
    cd ~/jhalfs
    # Respostas: "rodar a jhalfs?" e "está satisfeito com as opções?".
    printf 'yes\nyes\n' | ./jhalfs run
    ;;
  compilar)
    # A jhalfs exige um terminal de pelo menos 80x24; em segundo plano não há um, então o script cria um falso.
    script -qefc 'stty rows 40 cols 120; make -C /mnt/lfs/jhalfs' /dev/null
    ;;
  *) echo "uso: $0 gerar|compilar" >&2; exit 2 ;;
esac
