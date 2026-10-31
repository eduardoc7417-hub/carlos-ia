# Carlos AI: especificação inicial

Estado em 2026-10-31: **nada implementado, baixado ou medido.** Depende da base funcional do sistema.
Dados marcados como "a verificar" ou "a medir" não devem ser tratados como resultado.

## Ordem de trabalho

1. Concluir a base funcional do Carlos OS Aurora.
2. Desenvolver o Carlos AI Lite como componente independente.
3. Testar o Lite no i5-4570 real e estabilizar.
4. Só então iniciar o Carlos AI Pro.

## Requisitos do Lite

- Offline após a instalação dos componentes.
- Execução na CPU, com llama.cpp.
- Modelo de 0,5B a 1B de parâmetros, com quantização de 4 bits quando compatível.
- Carregado sob demanda: nenhum serviço de IA ativo durante o boot.
- Interface GNOME com janela de conversa, campo de pergunta, histórico local opcional,
  botão para apagar conversas, indicador de carregamento e configurações de desempenho.
- Suporte ao português brasileiro.
- Nenhum comando administrativo automático. Toda alteração de arquivo ou configuração exige
  autorização do usuário.

## Mecanismo de inferência

llama.cpp: licença MIT, suporte a AVX2 e servidor compatível com a API da OpenAI
([repositório](https://github.com/ggml-org/llama.cpp)). O suporte a AVX2 no i5-4570 será confirmado no teste.

## Modelos candidatos

| Modelo | Licença | Tamanho Q4 | RAM | Velocidade | Qualidade pt-BR |
|---|---|---|---|---|---|
| Qwen2.5 0.5B | Apache 2.0 em fontes secundárias; confirmar no arquivo LICENSE original | a verificar | a medir | a medir | a medir |
| Gemma 3 270M | a verificar (abaixo da faixa pedida) | a verificar | a medir | a medir | a medir |
| Outros de 0,5B a 1B | a pesquisar | a verificar | a medir | a medir | a medir |

SmolLM2 1.7B está acima da faixa pedida. Nenhum modelo foi escolhido: a decisão depende dos testes abaixo.

## Teste de seleção

Executar cada candidato no i5-4570, sem outras cargas pesadas, e registrar versão do llama.cpp,
hash do modelo, threads e parâmetros.

- **Velocidade:** tokens por segundo na geração e no processamento do prompt, com pelo menos 3 repetições.
- **Tempo:** do carregamento até o primeiro token.
- **Memória:** pico de RSS do processo.
- **Disco:** tamanho do arquivo do modelo.
- **Qualidade:** conjunto fixo de perguntas em pt-BR sobre fatos gerais, ajuda com o sistema, explicação
  de erros, redação e instruções passo a passo; avaliar com critérios escritos antes da execução.
- **Segurança:** resposta deve ser apresentada como sugestão e o usuário deve conseguir recusar qualquer ação.

## Arquitetura proposta

```
Carlos AI (GTK4 + libadwaita)
   |  API local, apenas no computador do usuário
llama-server (serviço de usuário do systemd, iniciado sob demanda, encerrado por inatividade)
   |
modelo GGUF em diretório próprio, com verificação de SHA-256
```

- A interface e o mecanismo ficam em processos separados: uma falha do modelo não derruba o GNOME Shell.
- O serviço não recebe privilégios de administrador e, na primeira versão, não acessa ferramentas do sistema.
- Uma futura ação proposta pela IA será apenas um pedido: o aplicativo mostra o que vai mudar, o usuário
  autoriza, e operações administrativas passam pelo polkit.
- O histórico fica desativado até o usuário ativá-lo, é salvo só localmente e pode ser apagado.
- Sem telemetria e sem conexão de rede em uso normal.
- Um arquivo de perfil define modelo, contexto, threads e backend. Assim, o Pro pode ser adicionado sem
  reescrever a interface.

## ISO

Decisão provisória: **o modelo fica fora da ISO e é um download opcional**, com hash verificado. Motivos:
mantém a ISO menor, evita gastar disco de quem não usa a IA e permite trocar de modelo sem gerar outra ISO.
O aplicativo e o llama.cpp podem ir na ISO, pois não afetam o boot quando inativos. Rever se o objetivo
passar a ser IA funcional logo após uma instalação sem internet; nesse caso, oferecer uma edição maior.

## Carlos AI Pro (somente arquitetura)

Modelos de 3B a 8B ou maiores, aceleração por GPU compatível, contexto maior, assistência de programação
e integrações adicionais. Não implementar antes de estabilizar o Lite. A HD 4600 não é alvo de aceleração
até haver medição.

## Entregas pendentes

1. Modelo recomendado
2. Licença de distribuição
3. Tamanho em disco
4. Consumo de RAM
5. Velocidade medida
6. Código e instruções de instalação
7. Testes realizados
