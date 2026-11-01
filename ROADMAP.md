# Roteiro

## Versão 0.9: a mais completa até aqui

Objetivo pedido pelo usuário: mudar a arquitetura onde for preciso e melhorar tudo. Nada disto foi feito ainda.

1. **Segurança e arquitetura:** Btrfs com pontos de restauração antes de atualizar, atualizações testadas e repositório com data fixa.
2. **Desempenho:** compressão de memória (zram), perfis de vidro, ajustes do Otimizador e medições no i5-4570 real.
3. **Instalador:** funcionar sem internet, BIOS e UEFI, dual boot testado em VM e apresentação corrigida.
4. **Visual:** tela de boot Aurora, tema de janelas, ícones próprios e ampliação do dock.
5. **Compatibilidade:** `.exe` com dois cliques, Android com instalação de apps e loja de aplicativos.
6. **Carlos AI:** Pro testada e melhores respostas em português.
7. **Lançamento:** pacote de código-fonte, para publicar a ISO em dia com a licença.

Ordem pedida pelo usuário: terminar a 0.8 e fazer a 0.9 em Debian. O Carlos OS Puro em LFS (`docs/carlos-os-puro.md`) fica para depois, só com as ferramentas preparadas.

## Fases

Uma fase por vez; cada uma só termina com teste real (`TESTES.md`).

1. **Sistema mínimo:** boot em BIOS e UEFI no QEMU. Concluído na ISO 0.1.1.
2. **Ambiente gráfico:** base sid com data fixa, GNOME 51, login e aplicativos básicos.
3. **CarlosUI:** tema próprio, dock, barra superior, ícones, vários papéis de parede próprios e
   Vidro Aurora em três perfis (econômico, equilibrado, avançado).
4. **Carlos AI Lite:** modelo pequeno, local e offline, integrado ao sistema, com a Pro como opção na mesma arquitetura.
   **Otimizador Carlos:** serviço leve e sem modelo, com ajustes reversíveis (memória, energia, inicialização).
   A IA só abre sob demanda para explicar e sugerir, e mudanças fora da lista segura pedem autorização.
5. **ISO instalável:** sessão live, instalador e teste de reinicialização.
6. **Compatibilidade de apps (opcional):** Android com Waydroid e programas .exe com Wine.
   **Pacote Cleo (nome a confirmar):** escritório e editor de vídeo com nome próprio, sobre projetos livres
   como LibreOffice e Shotcut ou Kdenlive, respeitando licenças e marcas. Não testado.
   **Programação:** VS Code como instalação opcional pelo repositório oficial da Microsoft, sem incluir na ISO.
   O Visual Studio completo só existe para Windows; só tentar pelo Wine, sem garantia. Não testado.
7. **Otimização:** medições no i5-4570 real e em outros computadores.
8. **Carlos AI Pro:** modelos maiores e aceleração por GPU.
9. **Lançamento:** licenças, atualizações, revisão jurídica e identidade final.

Pendências de verificação: suporte das extensões ao GNOME 51, relato de travamento com User Themes no 51,
`binder` no kernel para o Waydroid, licença do tradutor ARM e Vulkan na HD 4600.
