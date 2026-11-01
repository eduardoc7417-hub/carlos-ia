#!/bin/sh
# Grava um vídeo real da VM: captura a tela em sequência enquanto percorre a interface.
# Uso: gravar-demo.sh <saida.mp4>. Precisa da VM ligada e da sessão aberta.
SAIDA=$1
V=$(dirname "$0")/vm.sh
R=/tmp/gravacao
MON=/opt/vm/mon.sock
rm -rf "$R"; mkdir -p "$R"

(
  n=0
  while [ ! -e "$R/parar" ]; do
    n=$((n+1))
    echo "screendump $R/$(printf %05d $n).png -f png" | socat - "UNIX-CONNECT:$MON" >/dev/null
    sleep 0.4
  done
) &

sleep 4
sh "$V" click 20 15; sleep 4
sh "$V" key esc; sleep 2
sh "$V" key meta_l; sleep 5
sh "$V" key meta_l; sleep 3
sh "$V" key meta_l; sleep 3
sh "$V" type "programas"; sleep 2; sh "$V" key ret; sleep 10
sh "$V" key alt-f4; sleep 3
sh "$V" key meta_l; sleep 3
sh "$V" type "carlos"; sleep 2; sh "$V" key ret; sleep 8
sh "$V" key alt-f4; sleep 3
sh "$V" key meta_l; sleep 3
sh "$V" type "android"; sleep 2; sh "$V" key ret; sleep 25
sh "$V" key alt-f4; sleep 3
sh "$V" key alt-f4; sleep 4

touch "$R/parar"
sleep 2
quadros=$(ls "$R"/*.png | wc -l)
echo "quadros: $quadros"
ffmpeg -y -loglevel error -framerate 2.5 -pattern_type glob -i "$R/*.png" \
  -vf "scale=1280:-2,format=yuv420p" -r 25 -c:v libx264 -crf 26 -movflags +faststart "$SAIDA"
ls -lh "$SAIDA" | cut -c25-
ffprobe -v error -show_entries format=duration -of csv=p=0 "$SAIDA"
cp "$R/$(printf %05d $((quadros/5))).png" /tmp/q1.png
cp "$R/$(printf %05d $((quadros/2))).png" /tmp/q2.png
cp "$R/$(printf %05d $((quadros*4/5))).png" /tmp/q3.png
