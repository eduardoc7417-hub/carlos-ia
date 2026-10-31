# Roteiro

Uma fase por vez; cada uma só termina com teste real (`TESTES.md`).

1. **Sistema mínimo:** boot em BIOS e UEFI no QEMU. Concluído na ISO 0.1.1.
2. **Ambiente gráfico:** base sid com data fixa, GNOME 51, login e aplicativos básicos.
3. **CarlosUI:** tema próprio, dock, barra superior, ícones, vários papéis de parede próprios e
   Vidro Aurora em três perfis (econômico, equilibrado, avançado).
4. **Carlos AI Lite:** modelo pequeno, local e offline.
5. **ISO instalável:** sessão live, instalador e teste de reinicialização.
6. **Compatibilidade de apps (opcional):** Android com Waydroid e programas .exe com Wine.
7. **Otimização:** medições no i5-4570 real e em outros computadores.
8. **Carlos AI Pro:** modelos maiores e aceleração por GPU.
9. **Lançamento:** licenças, atualizações, revisão jurídica e identidade final.

Pendências de verificação: suporte das extensões ao GNOME 51, relato de travamento com User Themes no 51,
`binder` no kernel para o Waydroid, licença do tradutor ARM e Vulkan na HD 4600.
