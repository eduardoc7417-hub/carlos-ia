#!/bin/sh
# Inicializa a ISO no QEMU sem interface gráfica e procura o prompt de login no console serial.
# Uso: test-iso.sh <iso> <bios|uefi> [segundos]
set -u
ISO=$1
MODE=$2
LIMIT=${3:-1200}
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LOG="$PROJECT/out/boot-$MODE.log"
FW=""
if [ "$MODE" = uefi ]; then
  cp /usr/share/OVMF/OVMF_VARS_4M.fd /tmp/ovmf-vars.fd
  FW="-drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd -drive if=pflash,format=raw,file=/tmp/ovmf-vars.fd"
fi

: > "$LOG"
# shellcheck disable=SC2086
qemu-system-x86_64 -machine q35 -accel kvm -accel tcg -cpu max -smp 2 -m 2048 $FW \
  -cdrom "$ISO" -boot d -display none -monitor none -serial "file:$LOG" -no-reboot &
PID=$!

START=$(date +%s)
RESULT=TIMEOUT
while kill -0 "$PID" 2>/dev/null; do
  if grep -q 'login:' "$LOG"; then RESULT=OK; break; fi
  if grep -qE 'Kernel panic|Unable to find a medium' "$LOG"; then RESULT=FAIL; break; fi
  [ $(( $(date +%s) - START )) -ge "$LIMIT" ] && break
  sleep 5
done
ELAPSED=$(( $(date +%s) - START ))
kill "$PID" 2>/dev/null
echo "modo=$MODE resultado=$RESULT segundos=$ELAPSED log=$LOG"
tail -5 "$LOG"
[ "$RESULT" = OK ]
