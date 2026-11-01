# Carlos OS Puro: plano

Projeto à parte, em Linux From Scratch (LFS), sem Debian. Estado: **planejado, nada construído**.
Não substitui a linha em Debian, que continua sendo a versão para uso (`ROADMAP.md`).

## Regras

- Construir só em disco virtual, nunca em disco real.
- Rodar uma etapa pesada por vez e não usar `/opt/carlos-build` nem `/opt/vm`.
- Registrar em `TESTES.md` só o que foi executado. As estimativas de `reports/` não são medições.

## Preparação

Feito em 2026-10-31 com `tools/puro-host.sh`: ferramentas instaladas e disco esparso de 150 GB em `/opt/puro/disco.img`.
Livro de referência: LFS 13.1-systemd. Versões do Debian dentro do pedido: GCC 14.2, Binutils 2.44, kernel do WSL 6.18.

Falta, ao começar:

1. `/bin/sh` aponta para dash, e o livro exige bash. Só trocar quando a linha Debian não estiver construindo.
2. Rodar o `version-check.sh` do livro e cronometrar o primeiro pacote, para ter o SBU real desta máquina.
3. Escolher o gerenciador de pacotes antes de compilar o sistema (a pesquisa recomenda pacman).

## Compilar em partes

O computador não fica ligado direto, então a compilação precisa poder parar e continuar:

- Compilar um pacote por vez, com um script que marca cada pacote concluído e pula os já feitos ao retomar.
- Pacote interrompido volta ao início, sem perder os anteriores, porque tudo fica no disco do WSL.
- Antes de desligar, é preciso desmontar o disco virtual; ao ligar, montar de novo e rodar o mesmo script.

## Etapas

| Etapa | Entrega | Como aprovar |
|---|---|---|
| P1 | LFS em modo texto, com systemd | Inicia em VM UEFI com login, rede e reinício limpo |
| P2 | Receitas de pacotes reproduzíveis, em git | Reconstrução em chroot limpo passa no mesmo teste |
| P3 | GNOME sem extensões, seguindo o BLFS | Login, sessão, arquivos, rede e som na VM |
| P4 | CarlosUI aproveitada da linha Debian | Dock, barra, Menu Aurora e papéis de parede |
| P5 | ISO live | Boot em BIOS e UEFI |
| P6 | Instalador | Instalação em disco virtual e reinício sem a ISO |
| P7 | Wine, Android e Carlos AI | Cada um testado separadamente |
| P8 | Rotina de segurança | Uma correção real aplicada do aviso até o sistema |

## Riscos

- Sem atualizações prontas: cada aviso de segurança precisa ser aplicado à mão.
- Só depois da P2 vale decidir se o projeto continua: a P1 mostra o tempo real, e a P2, o custo de manutenção.
