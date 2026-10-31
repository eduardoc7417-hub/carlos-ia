#!/bin/sh
# Só consulta: mostra o que o Debian do WSL tem para construir e testar o pacote.
. /etc/os-release; echo "sistema: $PRETTY_NAME"
uname -m
for c in dpkg-deb fakeroot python3 glib-compile-schemas xvfb-run llama-server systemd-analyze desktop-file-validate appstreamcli; do
  printf '%s: ' "$c"; command -v "$c" || echo nao
done
for m in gi; do python3 -c "import $m; print('python $m ok')" 2>/dev/null || echo "python $m nao"; done
python3 - <<'EOF' 2>/dev/null || echo "gtk4/adw nao"
import gi
gi.require_version('Gtk','4.0'); gi.require_version('Adw','1')
from gi.repository import Gtk, Adw
print('gtk', Gtk.get_major_version(), Gtk.get_minor_version(), 'adw', Adw.MAJOR_VERSION, Adw.MINOR_VERSION)
EOF
echo "--- apt"
apt-cache policy llama.cpp python3-gi gir1.2-adw-1 2>/dev/null | grep -E '^[a-z]|Candidate'
cat /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null | grep -vE '^\s*#' | head -8
echo "--- carga"
cat /proc/loadavg; free -m | sed -n 2p; df -m /opt | tail -1
pgrep -a 'lb|mksquashfs|xorriso|qemu' | cut -c1-90 | head
pidof systemd >/dev/null && echo systemd ativo || echo sem systemd
