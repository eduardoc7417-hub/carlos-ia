# Testes executados

Só entra aqui o que foi executado de verdade.

## 2026-10-31: Wine e Android no sistema instalado (VM, pacotes instalados à mão)

- Wine 10: o Bloco de Notas de 64 bits abriu. Falta testar um `.exe` baixado.
- Waydroid 1.6.3 com LineageOS 20: exigiu `binder_linux` com `devices=binder,hwbinder,vndbinder`. Com vídeo por
  software (`gralloc=default`, `egl=swiftshader`), abriu até a tela inicial. Com os valores padrão, a tela ficou preta na VM.
- Troca de papel de parede pelo usuário funcionou (Flor Esmeralda). A tela de bloqueio aparece certa.

Não coberto: instalar apps Android, apps só ARM, Play Store, Android com GPU real. A ISO 0.8 ainda não foi testada.

## 2026-10-31: ISO 0.7, instalação em disco virtual

- SHA-256: `bf425b7ec91f24eea30d8d01458f2c97cb15f4843c092176f3cb9d8e15a91c43`
- Ambiente: QEMU com KVM, UEFI, 4 vCPU, 4 GB, disco virtual de 40 GB, com internet. Ferramenta: `tools/vm.sh`.
- Calamares concluiu a instalação ("Tudo pronto") após corrigir a falta de `dosfstools` e `squashfs-tools`.
- Sem a ISO, o sistema iniciou no login Aurora, aceitou a senha da conta de teste e abriu a área de trabalho.
- `carlos-otimizador` ativo (27,6 MB). `live-boot` removido. A janela da Carlos AI abriu.

- Carlos AI Lite: pedido de consentimento exibido, Gemma 3 1B baixado e uma pergunta respondida em português, em até 50 s.

Não coberto: qualidade e velocidade da Carlos AI, Carlos AI Pro, ajustes do Otimizador, instalação em BIOS ou sem internet,
Firefox e demais aplicativos, troca de papel de parede, rede real, áudio e computador real.

Na mesma VM, com a ISO 0.5: o Menu Aurora abriu ao clicar. Com a 0.6: a sessão abriu direto na área de trabalho,
com horário de Brasília.

## 2026-10-31: ISO 0.3 com CarlosUI

- SHA-256: `275d8ca2d10e8d0d5bef5ca264746337033910f5cec19866c92a9e78f73e5f34`
- Ambiente: QEMU com KVM, 4 vCPU, 4 GB e vídeo virtio. Comando: `tools/test-gui.sh`.
- BIOS e UEFI: prompt `login:` no console serial (55 s e 75 s) e entrada automática.
  As capturas mostram GNOME, dock, barra translúcida e papel de parede próprios.
- Versões instaladas: `gnome-shell 51.0-3`, `gdm3 51.1-1+b1`, kernel 7.2.14.

Defeitos vistos: relógio em UTC e abertura na visão geral. Não coberto: aplicativos, janelas, rede, áudio,
instalação e computador real.

## 2026-10-31: boot da ISO 0.1.1

- SHA-256: `d065205c9b1e12799da2b115e462c8088d7c96b1550def3b8e732bc2364c51d7`
- Ambiente: QEMU 10.0.13 no Debian do WSL2, Windows 11 Pro, i5-4570; convidado com 2 vCPU e 2 GB.
- Comando: `tools/test-iso.sh <iso> <bios|uefi>`. O convidado registrou `Hypervisor detected: KVM`.

| Modo | Resultado | Tempo até `login:` | Log |
|---|---|---|---|
| BIOS | OK | 45 s | `out/boot-bios.log` |
| UEFI | OK | 50 s | `out/boot-uefi.log` |

Coberto: menu de boot sem tecla, kernel, sistema live e prompt no console serial, com o nome Carlos OS Aurora 0.1.
Não coberto: entrar no sistema, rede, áudio, vídeo, instalação e computador real.

## 2026-10-31: ISO 0.1 original

O hash confere com o `.sha256`. O teste em BIOS foi interrompido após cerca de 10 minutos, parado no menu
(`timeout 0`, log serial vazio). Não é prova de falha do sistema. O UEFI não foi executado nessa ISO.
