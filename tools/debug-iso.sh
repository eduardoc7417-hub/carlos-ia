#!/bin/sh
# Inicia a ISO, entra pelo console serial e roda comandos de diagnóstico.
# Uso: debug-iso.sh <iso> <arquivo-de-comandos>
set -u
ISO=$1
CMDS=$2
S=/tmp/qemu-serial
LOG=/tmp/debug-serial.log
rm -f "$S" "$LOG"
qemu-system-x86_64 -machine q35 -accel kvm -accel tcg -cpu max -smp 4 -m 4096 -vga virtio \
  -cdrom "$ISO" -boot d -display none -monitor none \
  -chardev "socket,id=s0,path=$S,server=on,wait=off,logfile=$LOG" -serial chardev:s0 -no-reboot &
PID=$!

send() { printf '%s\n' "$1" | socat - "UNIX-CONNECT:$S" >/dev/null 2>&1; }

sleep 3
LIMIT=$(( $(date +%s) + 300 ))
until grep -q 'login:' "$LOG" 2>/dev/null || [ "$(date +%s)" -ge "$LIMIT" ]; do send ""; sleep 5; done
sleep 25
send carlos; sleep 3; send live; sleep 5
send "sudo sh -c 'stty cols 180; echo INICIO-DIAG'"; sleep 2
while IFS= read -r line; do
  send "$line"; sleep 3
done < "$CMDS"
send "echo FIM-DIAG"; sleep 3
kill "$PID" 2>/dev/null
sed -n '/INICIO-DIAG/,$p' "$LOG" | tr -d '\r' | sed -e 's/\x1b\]3008;[^\x1b]*\x1b\\//g' -e 's/\x1b\[[0-9;?]*[a-zA-Z]//g' | cut -c1-200
