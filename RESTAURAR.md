# Como continuar depois de formatar

Estado em 2026-10-31: ISO mínima gerada (só modo texto, sem interface nem instalador).
O teste de boot pode não ter terminado antes do backup: confira se existe `out/boot-bios.log` e `out/boot-uefi.log`,
ou repita o teste.

## 1. Restaurar os arquivos

1. Baixe esta pasta do Drive para `C:\Users\carlos\Downloads\Carlos-OS-Aurora`.
2. Para a economia de créditos, copie `user-config\CLAUDE.md` para `C:\Users\carlos\.claude\` e
   `user-config\skills\economia-creditos` para `C:\Users\carlos\.claude\skills\`.

## 2. Reinstalar as ferramentas

O WSL, o Debian e as ferramentas não ficam no backup. Abra o PowerShell como administrador e rode o comando abaixo.
Reinicie, rode de novo se o Debian não instalar, e crie o usuário `carlos` em minúsculas.

    wsl --install -d Debian

Depois, instale as ferramentas de construção:

    wsl.exe -d Debian -u root -- sh /mnt/c/Users/carlos/Downloads/Carlos-OS-Aurora/tools/setup-host.sh

## 3. Continuar com o Claude

Abra uma conversa nova na pasta `Carlos-OS-Aurora`. O `CLAUDE.md` traz as decisões e os próximos marcos. Diga:

    Continue o Carlos OS Aurora pelo CLAUDE.md e pelo RESTAURAR.md. Confirme o boot da ISO mínima e siga para o GNOME.

## Antes de formatar

- Confira no Drive se a pasta foi enviada por completo, inclusive a ISO.
- O pendrive `CARLOS_OS_A` (E: e F:) não faz parte do backup. Não o formate se quiser manter o trabalho anterior.
- O `.iso` pode ser conferido com o hash em `out/*.sha256`.
