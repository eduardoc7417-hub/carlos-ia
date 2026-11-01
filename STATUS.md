# Status real

Atualizado em 2026-10-31. Estados: planejado, em desenvolvimento, implementado, testado, aprovado.

| Componente | Estado | Observação |
|---|---|---|
| ISO 0.7 (sid, GNOME 51, CarlosUI) | Testado em VM | Live e instalação em UEFI no QEMU (`TESTES.md`) |
| Instalador (Calamares) | Testado em VM | Instalação em UEFI; BIOS não testado. Precisa de internet para instalar o GRUB |
| CarlosUI: dock, barra, vidro, Menu Aurora | Em desenvolvimento | Sem ícones próprios, perfis de vidro nem ampliação do dock |
| Papéis de parede (8 Aurora e 6 Flor) | Implementado | Na ISO; seleção nas Configurações não testada |
| Carlos AI | Em desenvolvimento | Lite respondeu uma pergunta no sistema instalado; Pro não testada |
| Otimizador Carlos | Em desenvolvimento | Serviço ativo no sistema instalado; ajustes reais não avaliados |
| Programas .exe (Wine) | Em desenvolvimento | Bloco de Notas de 64 bits abriu na VM; integrado à ISO 0.8, não testada |
| Apps Android (Waydroid) | Em desenvolvimento | Android abriu na VM; integrado à ISO 0.8, não testada; imagem baixada com consentimento |
| Pacote Cleo, VS Code | Planejado | Não testados |
| Computador real | Planejado | Só QEMU até agora; rede, áudio e fluidez sem teste |

## Defeitos conhecidos

- A imagem de apresentação do instalador aparece em branco durante a instalação.
- A base sid muda com frequência: a ISO final precisa fixar a data do repositório.
- A distribuição pública da ISO exige oferecer o código-fonte dos pacotes GPL; isso ainda não foi resolvido.
