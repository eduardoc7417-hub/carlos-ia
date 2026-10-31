# Decisão de base

Data: 2026-10-31. Substitui as decisões anteriores por Ubuntu 26.04 e Linux From Scratch.

## Pedido

Base Linux leve, sem Ubuntu e sem mostrar a base no uso normal do sistema.

## Decisão

**Debian 13 "Trixie" (estável), a partir de instalação mínima com debootstrap, e ISO gerada com live-build.**

- 13.7 é a atualização mais recente, de 2026-09-12; o fim de vida é 2028-08-09 e o LTS vai até 2030-06-30
  ([lançamentos](https://www.debian.org/releases/)).
- Só entram os pacotes escolhidos, sem o conjunto padrão de apps do GNOME.
- Atualizações de segurança continuam vindo do Debian, sem manutenção manual como no LFS.

## Efeito na interface

O Debian estável traz **GNOME Shell 48.7**, não o 50 ([pacote](https://packages.debian.org/stable/gnome-shell)).
A pesquisa em `reports/` verificou extensões para o GNOME 50, então cada uma precisa ser conferida
novamente para o 48. O desempenho no sistema Debian também ainda não foi medido.

## O que deixa de mostrar a base

- Nome e logos em boot, login, tela "Sobre", instalador e Plymouth.
- `/etc/os-release`, `/etc/issue`, menu do GRUB e papéis de parede.
- Pacotes de marca do Debian: substituir, sempre que a dependência permitir.

## O que continua existindo

- Textos de licença e créditos: obrigatórios e mantidos, inclusive o código-fonte exigido pela GPL.
- Rastros técnicos no terminal: `apt`, `dpkg`, versões de pacote e `ID_LIKE=debian`, necessários para
  compatibilidade e atualizações.
- Repositórios Debian na configuração do sistema.

A menção à base fica apenas em "Licenças e créditos", sem sugerir ligação com o projeto Debian.
A [política de marcas](https://www.debian.org/trademark) proíbe usar a marca como nome de produto e pede
aviso de não afiliação. Ela não trata diretamente da remoção de marcas; dúvidas vão para
trademark@debian.org ou para um advogado se o sistema for distribuído publicamente.

## Marcos até a primeira ISO

1. Instalar WSL2 com Debian no Windows (administrador e reinício). **Bloqueia todo o resto.**
2. Preparar live-build e QEMU no WSL. O live-build ainda precisa ser validado nesse ambiente.
3. Gerar uma ISO mínima e testar o boot no QEMU. Sem KVM aninhado no Windows 10, o QEMU deve usar
   emulação por software: serve para boot e instalação, não para avaliar fluidez. A fluidez é
   medida no i5-4570 real.
4. Adicionar GNOME, marca própria e instalador Calamares.
5. Testar boot, instalação e reinicialização em VM, depois no i5-4570 real.
6. Publicar nome, tamanho, SHA-256 e resultados dos testes.
