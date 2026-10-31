#!/bin/sh
# Cria um chroot Debian sid só para testar os pacotes, fora de /opt/carlos-build.
# Pode ser repetido; não altera o sistema do WSL além de instalar o debootstrap, se faltar.
set -eu
R=/opt/carlos-ai-teste
PACOTES="python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 librsvg2-common llama.cpp-tools xvfb xauth imagemagick adwaita-icon-theme fonts-dejavu-core desktop-file-utils dbus dbus-x11 systemd curl ca-certificates"

command -v debootstrap >/dev/null || apt-get install -y --no-install-recommends debootstrap
if [ -e "$R" ] && [ ! -e "$R/.base-ok" ]; then
  grep -E 'dpkg: error|Errors were|exit status' "$R/debootstrap/debootstrap.log" 2>/dev/null | tail -5 || true
  if grep -q " $R" /proc/mounts; then echo "ha montagens em $R; abortado"; exit 1; fi
  rm -rf "$R"
fi
if [ ! -e "$R/.base-ok" ]; then
  nice -n 15 ionice -c 3 debootstrap --variant=minbase sid "$R" https://deb.debian.org/debian
  touch "$R/.base-ok"
fi
mount -t proc proc "$R/proc"
trap 'umount "$R/proc"' EXIT
printf '#!/bin/sh\nexit 101\n' > "$R/usr/sbin/policy-rc.d"; chmod 755 "$R/usr/sbin/policy-rc.d"
chroot "$R" sh -c "export DEBIAN_FRONTEND=noninteractive; nice -n 15 apt-get install -y -q --no-install-recommends $PACOTES >/var/log/preparo.log 2>&1 || { tail -25 /var/log/preparo.log; exit 1; }"
chroot "$R" sh -c 'dpkg-query -W -f "\${Package} \${Version}\n" python3 libgtk-4-1 libadwaita-1-0 llama.cpp-tools; command -v llama-server || dpkg -L llama.cpp-tools | grep bin/ | head -20'
du -sh --exclude=proc "$R"
echo preparado
