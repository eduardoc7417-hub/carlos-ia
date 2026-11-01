# Projeto: Carlos OS Puro

Você vai trabalhar no Carlos OS Puro, a versão em Linux From Scratch (LFS) do projeto Carlos OS Aurora. Responda em português do Brasil, de forma curta.

**Repositório:** https://github.com/eduardoc7417-hub/carlos-ia

Leia primeiro: `docs/carlos-os-puro.md`, `STATUS.md`, `TESTES.md`, `ROADMAP.md`, `CLAUDE.md` e `reports/`. Não refaça pesquisas já salvas sem necessidade.

## O que já existe

Linha Debian (continua sendo feita em outro ambiente, não mexa nela):

- Debian sid, GNOME 51, live-build e instalador Calamares
- CarlosUI: dock, barra e menus translúcidos, Menu Aurora e 14 papéis de parede originais (`tools/gen-art.py`)
- Carlos AI Lite e Pro e Otimizador Carlos (`carlos-ai/`)
- Wine e Waydroid integrados à ISO
- Instalação testada em disco virtual, em UEFI no QEMU, até a ISO 0.8
- A ISO 0.9 está em desenvolvimento, com Btrfs e pontos de restauração; ela ainda não foi testada

Carlos OS Puro: **nada foi compilado**. Existe só o plano. Referência: LFS 13.1-systemd. Confira se há versão estável mais nova.

## Objetivo

Construir o Carlos OS Puro nas etapas P1 a P8 de `docs/carlos-os-puro.md`, uma por vez. A primeira entrega é a **P1: LFS em modo texto com systemd, iniciando em VM UEFI, com login, rede e reinício limpo.**

## Onde compilar

Quero usar o meu Google Colab, por ser uma máquina mais potente que a minha. Eu rodo as células no Colab e colo o resultado aqui; você entrega os scripts pelo GitHub. Antes de compilar, verifique de verdade:

1. CPU, RAM, disco livre, permissões e tempo de sessão.
2. Se o ambiente permite `chroot`, `mount`, dispositivo loop e `/dev/kvm`, que o livro LFS e o teste de boot podem exigir.
3. Se a compilação longa é permitida pelas regras do meu plano do Colab.

Se algo faltar, me diga o que encontrou e proponha uma alternativa. Não invente contornos que violem as regras do serviço.

## Compilação em partes (obrigatório)

Sessões do Colab podem cair a qualquer momento, então:

- Compile um pacote por vez, com um script que marca cada pacote concluído e pula os já feitos ao retomar.
- Salve o progresso e os logs fora da sessão, no meu Google Drive, em uma pasta só do projeto, e confira se dá para restaurar.
- Antes de começar, explique como retomar depois de uma queda e teste isso.
- Cronometre o primeiro pacote e me passe o tempo estimado real.

## Regras

1. **Não invente resultados.** Registre em `TESTES.md` só o que foi executado.
2. **Segurança:** nunca peça minha senha nem coloque tokens, chaves ou credenciais em arquivos, logs ou commits. Quando precisar de login, deixe que eu faça.
3. **Discos:** só use disco virtual. Nunca formate nada real, nem apague arquivos sem me perguntar.
4. **Git:** trabalhe na branch `carlos-os-puro`. Não faça push na `main` nem force push, e me peça confirmação antes de publicar.
5. **Marcas e licenças:** não use fontes, logos, ícones ou papéis de parede da Apple ou da Microsoft. Mantenha os avisos de licença.
6. **Decisões:** escolha o gerenciador de pacotes antes de compilar o sistema (a pesquisa recomenda pacman) e registre o motivo.
7. **Limite honesto:** um LFS não recebe atualizações prontas. Registre esse custo a cada etapa e me diga, depois da P2, se vale continuar.

## Ao fim de cada etapa, informe

O que foi feito, o que foi testado, o que funcionou, o que falhou, o que falta e o próximo passo.

## Primeira tarefa agora

Não compile ainda. Leia os arquivos, verifique o Colab e me entregue: o resultado das verificações, um plano curto e como retomar depois de uma queda. Depois, aguarde minha confirmação.
