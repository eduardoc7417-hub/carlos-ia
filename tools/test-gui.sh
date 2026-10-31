#!/bin/sh
# Inicializa a ISO com vídeo virtual, espera o login no console serial e salva capturas da tela.
# Uso: test-gui.sh <iso> <bios|uefi> [segundos]
set -u
ISO=$1
MODE=$2
LIMIT=${3:-900}
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LOG="$PROJECT/out/gui-$MODE.log"
SOCK=/tmp/qemu-mon-$MODE
FW=""
if [ "$MODE" = uefi ]; then
  cp /usr/share/OVMF/OVMF_VARS_4M.fd /tmp/ovmf-vars.fd
  FW="-drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd -drive if=pflash,format=raw,file=/tmp/ovmf-vars.fd"
fi

: > "$LOG"
# shellcheck disable=SC2086
qemu-system-x86_64 -machine q35 -accel kvm -accel tcg -cpu max -smp 4 -m 4096 $FW \
  -vga virtio -cdrom "$ISO" -boot d -display none -serial "file:$LOG" \
  -monitor "unix:$SOCK,server,nowait" -no-reboot &
PID=$!

shot() {
  echo "screendump /tmp/gui-$MODE-$1.png -f png" | socat - "UNIX-CONNECT:$SOCK" >/dev/null
  sleep 2
  cp "/tmp/gui-$MODE-$1.png" "$PROJECT/out/gui-$MODE-$1.png"
}

START=$(date +%s)
RESULT=TIMEOUT
while kill -0 "$PID" 2>/dev/null; do
  if grep -q 'login:' "$LOG"; then RESULT=OK; break; fi
  if grep -qE 'Kernel panic|Unable to find a medium' "$LOG"; then RESULT=FAIL; break; fi
  [ $(( $(date +%s) - START )) -ge "$LIMIT" ] && break
  sleep 5
done
ELAPSED=$(( $(date +%s) - START ))
sleep 45
shot 1
sleep 30
# Abre a visão geral com a tecla Super para mostrar a interface em uso.
echo "sendkey meta_l" | socat - "UNIX-CONNECT:$SOCK" >/dev/null
sleep 8
shot 2
kill "$PID" 2>/dev/null
echo "modo=$MODE login=$RESULT segundos=$ELAPSED log=$LOG"
grep -nE 'Failed to start|gdm|GNOME Display' "$LOG" | tail -8 | cut -c1-140
[ "$RESULT" = OK ]
