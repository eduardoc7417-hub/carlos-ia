#!/bin/sh
# Só consulta: tamanho instalado das dependências de IA no chroot e o que os pacotes puxam.
R=/opt/carlos-ai-teste
chroot "$R" dpkg-query -W -f '${Package} ${Installed-Size} KB\n' llama.cpp-tools libllama0 libggml0 carlos-ai carlos-otimizador
chroot "$R" dpkg-query -W -f '${Package}: ${Depends}\n' llama.cpp-tools
chroot "$R" sh -c 'dpkg -L libggml0 | grep -E "\.so" | head; dpkg -l | grep -E "libggml" | cut -c1-70'
grep -m1 -o avx2 /proc/cpuinfo
