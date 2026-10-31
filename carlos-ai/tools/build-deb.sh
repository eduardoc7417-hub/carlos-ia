#!/bin/sh
# Gera carlos-ai e carlos-otimizador em dist/. Rodar no Linux, como root.
# A árvore é montada fora de /mnt/c: o NTFS não guarda as permissões do pacote.
set -eu
B=$(cd "$(dirname "$0")/.." && pwd)
V=$(sed -n 's/^VERSAO = "\(.*\)"/\1/p' "$B/app/carlos_ai/__init__.py")
T=$(mktemp -d /tmp/carlos-deb.XXXXXX)
trap 'rm -rf "$T"' EXIT
mkdir -p "$B/dist"

# carlos-ai
P=$T/carlos-ai
install -d "$P/DEBIAN" "$P/usr/bin" "$P/usr/lib/carlos-ai/carlos_ai" "$P/usr/share/applications" \
  "$P/usr/share/icons/hicolor/scalable/apps" "$P/usr/share/doc/carlos-ai"
install -m 755 "$B/app/bin/carlos-ai" "$P/usr/bin/carlos-ai"
install -m 644 "$B"/app/carlos_ai/*.py "$P/usr/lib/carlos-ai/carlos_ai/"
install -m 644 "$B/app/org.carlosos.CarlosAI.desktop" "$P/usr/share/applications/"
install -m 644 "$B/app/carlos-ai.svg" "$P/usr/share/icons/hicolor/scalable/apps/"
install -m 644 "$B/README.md" "$P/usr/share/doc/carlos-ai/"
cat > "$P/DEBIAN/control" <<EOF
Package: carlos-ai
Version: $V
Section: utils
Priority: optional
Architecture: all
Maintainer: Carlos OS Aurora <carlos@localhost>
Depends: python3, python3-gi, gir1.2-gtk-4.0, gir1.2-adw-1 (>= 1.5), librsvg2-common, llama.cpp-tools
Recommends: carlos-otimizador
Description: Assistente local do Carlos OS Aurora (Lite e Pro)
 Janela de conversa com llama-server iniciado sob demanda. Sem telemetria.
 O modelo é um download opcional, feito só com o consentimento do usuário.
EOF
cat > "$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
[ "$1" = configure ] || exit 0
gtk-update-icon-cache -q -t /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database -q 2>/dev/null || true
EOF
chmod 755 "$P/DEBIAN/postinst"
dpkg-deb --root-owner-group -Zxz --build "$P" "$B/dist/carlos-ai_${V}_all.deb"

# carlos-otimizador
P=$T/carlos-otimizador
install -d "$P/DEBIAN" "$P/usr/bin" "$P/usr/lib/systemd/system" "$P/usr/share/doc/carlos-otimizador"
install -m 755 "$B/otimizador/carlos-otimizador" "$P/usr/bin/carlos-otimizador"
install -m 644 "$B/otimizador/carlos-otimizador.service" "$P/usr/lib/systemd/system/"
install -m 644 "$B/README.md" "$P/usr/share/doc/carlos-otimizador/"
cat > "$P/DEBIAN/control" <<EOF
Package: carlos-otimizador
Version: $V
Section: admin
Priority: optional
Architecture: all
Maintainer: Carlos OS Aurora <carlos@localhost>
Depends: python3, systemd
Description: Ajustes seguros e reversíveis de memória e energia
 Serviço leve, sem modelo de IA. Aplica só uma lista fixa, restaura os valores
 originais ao parar e transforma o resto em sugestões.
EOF
cat > "$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
[ "$1" = configure ] || exit 0
systemctl enable carlos-otimizador.service >/dev/null 2>&1 || true
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || true
  systemctl restart carlos-otimizador.service || true
fi
EOF
cat > "$P/DEBIAN/prerm" <<'EOF'
#!/bin/sh
set -e
if [ "$1" = remove ] && [ -d /run/systemd/system ]; then
  systemctl stop carlos-otimizador.service || true
fi
EOF
cat > "$P/DEBIAN/postrm" <<'EOF'
#!/bin/sh
set -e
if [ "$1" = remove ] || [ "$1" = purge ]; then
  systemctl disable carlos-otimizador.service >/dev/null 2>&1 || true
fi
[ "$1" = purge ] && rm -rf /var/lib/carlos-otimizador /etc/carlos-otimizador
[ -d /run/systemd/system ] && systemctl daemon-reload || true
EOF
chmod 755 "$P"/DEBIAN/postinst "$P"/DEBIAN/prerm "$P"/DEBIAN/postrm
dpkg-deb --root-owner-group -Zxz --build "$P" "$B/dist/carlos-otimizador_${V}_all.deb"
ls -l "$B/dist"
