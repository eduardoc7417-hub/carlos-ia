#!/bin/sh
# Gera os .deb e testa no chroot sid de preparar-teste.sh. Um processo pesado por vez.
# Passe o caminho de um GGUF (de preferência o blob do Ollama no Windows) para o teste real.
set -u
B=$(cd "$(dirname "$0")/.." && pwd)
R=/opt/carlos-ai-teste
GGUF=${1:-}

sh "$B/tools/build-deb.sh" || exit 1
mkdir -p "$R/opt/t" "$R/opt/saida" "$R/proc" "$R/dev"
cp "$B"/dist/*.deb "$B"/tests/*.py "$R/opt/t/"
mountpoint -q "$R/proc" || mount -t proc proc "$R/proc"
mountpoint -q "$R/dev" || mount --bind /dev "$R/dev"
trap 'umount "$R/dev" "$R/proc" "$R/opt/modelo.gguf" 2>/dev/null' EXIT

# Instalar sem iniciar serviços: o chroot não é um sistema em execução.
printf '#!/bin/sh\nexit 101\n' > "$R/usr/sbin/policy-rc.d"; chmod 755 "$R/usr/sbin/policy-rc.d"
echo "=== instalar"
chroot "$R" sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y -q --reinstall --no-install-recommends /opt/t/carlos-ai_*_all.deb /opt/t/carlos-otimizador_*_all.deb 2>&1 | tail -3'
echo "instalar exit $?"
chroot "$R" dpkg-query -W carlos-ai carlos-otimizador
chroot "$R" systemctl is-enabled carlos-otimizador.service
echo "=== validar"
chroot "$R" desktop-file-validate /usr/share/applications/org.carlosos.CarlosAI.desktop && echo desktop ok
systemd-analyze verify "$B/otimizador/carlos-otimizador.service" 2>&1 | grep -v 'carlos-otimizador is not executable\|Command /usr/bin' | head
chroot "$R" llama-server --version 2>&1 | head -3
chroot "$R" sh -c 'llama-server --help 2>&1 | grep -E -- "--no-webui|--api-key|LLAMA_API_KEY" | head'
echo "=== otimizador"
chroot "$R" python3 /opt/t/test_otimizador.py /usr/bin/carlos-otimizador 2>&1 | grep -v ResourceWarning | tail -15
echo "=== nucleo"
if [ -n "$GGUF" ]; then
  : > "$R/opt/modelo.gguf"
  mountpoint -q "$R/opt/modelo.gguf" || mount --bind -o ro "$GGUF" "$R/opt/modelo.gguf"
  G=/opt/modelo.gguf
else
  G=
fi
chroot "$R" env CARLOS_APP=/usr/lib/carlos-ai GGUF_TESTE="$G" nice -n 10 python3 /opt/t/test_nucleo.py 2>&1 | tail -20
echo "=== janela"
chroot "$R" env GGUF_TESTE="$G" nice -n 10 xvfb-run -a -s "-screen 0 900x720x24" dbus-run-session -- python3 /opt/t/ui_smoke.py /opt/saida 2>&1 | grep -v 'dconf\|Vulkan\|MESA\|libEGL' | tail -30
mkdir -p "$B/tests/capturas"
cp "$R"/opt/saida/*.png "$B/tests/capturas/" 2>/dev/null
ls "$B/tests/capturas"
echo fim
