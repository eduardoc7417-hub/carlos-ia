#!/bin/bash
# Roda o version-check.sh do capítulo 2.2 do livro (o código do livro é MIT), tirado direto da página oficial.
set -euo pipefail
wget -q -O- https://www.linuxfromscratch.org/lfs/view/13.1-systemd/chapter02/hostreqs.html |
  python3 -c '
import html, re, sys
pagina = sys.stdin.read()
for bloco in re.findall(r"<pre class=\"userinput\"><kbd class=\s*\"command\">(.*?)</kbd></pre>", pagina, re.S):
    texto = html.unescape(re.sub(r"<[^>]+>", "", bloco))
    if "version-check.sh" in texto:
        print(texto.split("\n", 1)[1].rsplit("EOF", 1)[0])
        break
' > /tmp/version-check.sh
bash /tmp/version-check.sh
