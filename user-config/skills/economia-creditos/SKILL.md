---
name: economia-creditos
description: Reduz o gasto de créditos na conversa. Usar quando o usuário pedir para economizar créditos, tokens ou uso, ou digitar /economia-creditos.
---

# Economia de créditos

Manter estas regras até o fim da conversa. Elas nunca justificam declarar algo como feito sem verificar.

## Respostas

- Responder em poucas frases, sem repetir o pedido, sem resumo do que já foi dito e sem listas de opções.
- Fazer a tarefa direto quando o caminho for claro; perguntar só o que realmente muda o resultado.
- Se a mensagem do usuário vier cortada, pedir a frase inteira em uma linha e parar.

## Ferramentas

- Não criar subagentes nem fazer pesquisa profunda, salvo pedido explícito.
- Fazer pesquisa na web só se a resposta depender dela: no máximo uma busca e uma ou duas páginas.
- Antes de pesquisar, procurar o que já está salvo no projeto (`CLAUDE.md`, `docs/`, `reports/`).
- Ler só o trecho necessário dos arquivos; usar busca antes de abrir arquivos grandes.
- Limitar a saída de comandos, mostrando só o final dos logs ou as linhas de erro.
- Não reler arquivos recém-editados nem repetir uma verificação cujo resultado não mudou.
- Em tarefas longas, rodar em segundo plano e não consultar o andamento repetidamente.

## Conversa longa

Quando a etapa atual terminar e a conversa já estiver longa, salvar o estado no `CLAUDE.md` do projeto e
recomendar uma única vez que o usuário abra uma conversa nova.
