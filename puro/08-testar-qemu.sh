#!/bin/bash
# Liga a imagem no QEMU (no host, só para testar) e confere se o Carlos OS chega no login. Rodar como root.
#   bash 08-testar-qemu.sh          -> teste automático: espera o "login:" pela porta serial, até 10 minutos
#   bash 08-testar-qemu.sh --usar   -> abre o console para você usar (sair: Ctrl+A e depois X)
set -euo pipefail
IMAGEM=/var/lib/carlos-lfs/carlos-os.img
command -v qemu-system-x86_64 >/dev/null || apt-get install -y qemu-system-x86
ACEL=(-accel tcg)
[ -w /dev/kvm ] && ACEL=(-accel kvm -cpu host)
QEMU=(qemu-system-x86_64 "${ACEL[@]}" -m 2G -smp 2 -nographic
      -drive "file=$IMAGEM,format=raw,if=virtio" -nic user,model=virtio-net-pci)

if [ "${1:-}" = --usar ]; then
  exec "${QEMU[@]}"
fi
LOG=/var/lib/carlos-lfs/boot.log
timeout 600 "${QEMU[@]}" -serial "file:$LOG" -monitor none -display none &
for _ in $(seq 600); do
  grep -q 'login:' "$LOG" 2>/dev/null && break
  sleep 1
done
kill %1 2>/dev/null || true
if grep -q 'login:' "$LOG"; then
  grep -aE 'Linux version|Welcome|login:' "$LOG" | head -5
  echo "OK: o Carlos OS ligou e chegou no login."
else
  tail -30 "$LOG"
  echo "FALHOU: não chegou no login. Log completo em $LOG" >&2
  exit 1
fi
