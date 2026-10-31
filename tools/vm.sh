#!/bin/sh
# Máquina virtual de teste, controlada por comandos, com disco virtual próprio. Nunca usa discos reais.
# Uso: vm.sh run <iso|nenhuma> | shot <nome> | click <x> <y> | key <tecla> | type <texto> | stop
# Coordenadas em pixels da tela de 1280x800.
PROJECT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIR=/opt/vm
DISK=$DIR/disco.qcow2
MON=$DIR/mon.sock
QMP=$DIR/qmp.sock

qmp() {
  { echo '{"execute":"qmp_capabilities"}'; sleep 0.2; echo "$1"; sleep 0.3; } | socat - "UNIX-CONNECT:$QMP" >/dev/null
}

mon() {
  echo "$1" | socat - "UNIX-CONNECT:$MON" >/dev/null
}

case "$1" in
  run)
    mkdir -p "$DIR"
    [ -f "$DISK" ] || qemu-img create -f qcow2 "$DISK" 40G >/dev/null
    [ -f "$DIR/vars.fd" ] || cp /usr/share/OVMF/OVMF_VARS_4M.fd "$DIR/vars.fd"
    CD=""
    [ "$2" != nenhuma ] && CD="-cdrom $2"
    # shellcheck disable=SC2086
    exec qemu-system-x86_64 -machine q35 -accel kvm -accel tcg -cpu max -smp 4 -m 4096 \
      -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
      -drive if=pflash,format=raw,file="$DIR/vars.fd" \
      -drive file="$DISK",if=virtio,format=qcow2 $CD \
      -vga virtio -device qemu-xhci -device usb-tablet -nic user,model=e1000 \
      -display none -serial "file:$DIR/serial.log" \
      -monitor "unix:$MON,server,nowait" -qmp "unix:$QMP,server,nowait"
    ;;
  shot)
    mon "screendump /tmp/vm-$2.png -f png"
    sleep 2
    cp "/tmp/vm-$2.png" "$PROJECT/out/vm-$2.png"
    ;;
  click)
    X=$(( $2 * 32767 / 1280 ))
    Y=$(( $3 * 32767 / 800 ))
    # Tudo numa conexão só: com conexões separadas, o clique demora e vira toque longo.
    {
      echo '{"execute":"qmp_capabilities"}'
      sleep 0.2
      echo '{"execute":"input-send-event","arguments":{"events":[{"type":"abs","data":{"axis":"x","value":'$X'}},{"type":"abs","data":{"axis":"y","value":'$Y'}}]}}'
      sleep 0.2
      echo '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":true,"button":"left"}}]}}'
      sleep 0.05
      echo '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":false,"button":"left"}}]}}'
      sleep 0.2
    } | socat - "UNIX-CONNECT:$QMP" >/dev/null
    ;;
  key)
    mon "sendkey $2"
    ;;
  type)
    printf '%s' "$2" | sed 's/./&\n/g' | while IFS= read -r c; do
      case "$c" in
        [a-z0-9]) k=$c ;;
        [A-Z]) k=shift-$(printf '%s' "$c" | tr A-Z a-z) ;;
        ' ') k=spc ;;
        -) k=minus ;;
        .) k=dot ;;
        *) continue ;;
      esac
      mon "sendkey $k"
      sleep 0.25
    done
    ;;
  stop)
    mon quit
    ;;
esac
