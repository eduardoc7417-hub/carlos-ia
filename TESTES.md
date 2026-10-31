# Testes executados

Só entra aqui o que foi executado de verdade.

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
