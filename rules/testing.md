# Testes

Todo teste responde a uma pergunta: **o que o usuário perde se isso quebrar?** Sem resposta, o teste não deveria existir. Confiança vem de poucos testes que atravessam o sistema de verdade, não de muitos que exercitam peças isoladas.

A meta deste repositório é uma suíte que cabe na cabeça: pequena, rápida, e onde uma falha vermelha significa "o produto quebrou", não "alguém renomeou um campo".

## Ordem de preferência

Pare no primeiro nível que dá confiança real sobre o comportamento:

1. **E2E** — exercita o sistema pela borda que o usuário usa (UI, API, CLI). É o teste mais valioso: é o único que prova que as partes integram.
2. **Integração** — quando a borda completa não é alcançável (dependência externa sem sandbox, ambiente caro), cubra o maior pedaço real que der.
3. **Unidade** — último recurso, só quando a lógica é crítica **e** o caso é inalcançável de fora.

"Inalcançável de fora" significa combinação que não dá para provocar pela borda: matriz grande de casos de cálculo, fronteira de segurança (authz, path traversal, redaction), classificação de erro que decide retry versus perda de dado. "É mais fácil testar isolado" não conta.

- **FAÇA**: Cubra toda feature core por um teste de fora, no nível em que o usuário a percebe.
- **FAÇA**: Ao corrigir um bug, deixe um teste que falharia antes do fix — no nível mais alto que consiga reproduzi-lo.
- **NÃO FAÇA**: Criar teste de unidade para um método só porque ele existe.
- **NÃO FAÇA**: Testar detalhe de implementação que muda sem afetar comportamento observável.

## O que não merece teste

- **NÃO FAÇA**: Testar getter, wrapper que só delega, serialização que só valida anotação de struct, enum, helper trivial.
- **NÃO FAÇA**: Escrever teste cujo setup é majoritariamente mock: você está testando os mocks.
- **NÃO FAÇA**: Duplicar num nível abaixo um caso que o teste de fora já cobre.
- **NÃO FAÇA**: Perseguir número de cobertura. Cobertura de linha não é critério; "essa feature core tem teste?" é.
- **NÃO FAÇA**: Escrever teste para o quality gate passar. Se o gate exige cobertura que o escopo acima não justifica, isso é um problema do gate: declare em voz alta em vez de encher a suíte.

## Custo de manutenção

Todo teste é código que alguém vai manter. A suíte só permanece útil se encolher com a mesma facilidade com que cresce.

- **FAÇA**: Remova teste micro ao encontrá-lo, mesmo que esteja passando. Deletar é contribuição.
- **FAÇA**: Antes de criar um arquivo novo, veja se um teste existente deveria cobrir mais um caso. Uma tabela de casos por conceito vale mais que um arquivo por método.
- **FAÇA**: Mantenha a suíte rápida o bastante para rodar inteira antes de cada commit. Se não roda, ela está grande demais ou acoplada demais à infra.
- **NÃO FAÇA**: Conviver com teste intermitente. Conserte ou delete no mesmo trabalho: falha que o time aprende a ignorar destrói o valor de todas as outras.

## Testabilidade é design

- **FAÇA**: Projete fluxo crítico de negócio (pagamento, autenticação, precificação) para que um cenário completo seja reproduzível sem mock elaborado nem setup manual extenso.
- **FAÇA**: Trate fluxo crítico difícil de testar de fora como sinal de acoplamento ruim: resolva o acoplamento, não desça de nível para contornar.
- **FAÇA**: Declare em voz alta feature core sem teste de fora. É lacuna a registrar, não a compensar com uma pilha de testes de unidade.

## Evidência visual de execução

Evidência visual do resultado rodando (**imagem ou vídeo**) é a prova, para quem pediu, de que o que foi solicitado existe e funciona. Sem ela, a entrega é só uma afirmação.

- **FAÇA**: Ao fechar uma implementação (testes passando, antes de anunciar entrega, commit ou MR), **pergunte ao usuário** se ele quer gerar a evidência. Rode só se ele pedir; silêncio ou "ok" não é "sim".
- **FAÇA**: Se a skill `test-evidence` estiver disponível, use-a para a mecânica de captura. Se não estiver, capture com o que a stack oferecer (screenshot do navegador, gravação de tela, print do cliente HTTP) e combine com o usuário onde o arquivo mora.
- **FAÇA**: Antes de dizer que terminou, confirme que há captura cobrindo cada caminho prometido.
- **NÃO FAÇA**: Apresentar diff, log de build ou saída transcrita **no lugar** da captura pedida: nada disso prova execução.
- **NÃO FAÇA**: Montar suíte E2E automatizada só para gerar evidência onde a stack não comporta. A evidência é obrigatória, o spec automatizado não.

Se capturar for de fato impossível no ambiente, isso é bloqueio a declarar junto da entrega, não licença para trocar o formato por texto.

## O teste é a especificação do comportamento

Comportamento observável se registra em teste, não em prosa. Um cenário escrito em markdown não roda, não falha e não avisa quando deixa de ser verdade; o teste, sim.

- **FAÇA**: Nomeie o teste pelo comportamento de negócio que ele protege, não pela função que ele chama. O nome é a documentação.
- **FAÇA**: Ao encontrar cenário de comportamento documentado em prosa, converta em teste e apague o texto. Dois registros da mesma verdade divergem; o que roda é o que fica.
- **NÃO FAÇA**: Escrever a descrição de um comportamento em doc esperando que ela substitua o teste. Doc cobre arquitetura, integração, capacidade e regra core (ver `rules/documentation.md`); comportamento é teste.

O teste do teste: se ele falhar amanhã, você consegue dizer o que o usuário perdeu? Se a resposta é "nada perceptível", delete.
