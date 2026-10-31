#!/bin/sh
# Mostra o andamento da construção da ISO. Não altera nada.
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
echo "processos:"
ps -eo etimes,comm --sort=-etimes | grep -E ' (lb|debootstrap|apt-get|dpkg|mksquashfs|xorriso)$' | head -6
du -sh /opt/carlos-build 2>/dev/null
echo "log:"
tail -8 /opt/build.log | cut -c1-160
echo "erros:"
grep -nE '^E: |^P: .*error|Error' /opt/build.log | tail -5 | cut -c1-160
echo "saida:"
ls -la "$PROJECT/out"
