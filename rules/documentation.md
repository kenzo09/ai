# Documentação de Features e Bugfixes

Código e documentação não podem divergir. Toda mudança de comportamento observável merece uma decisão explícita sobre a doc: nunca um "esqueceu de atualizar".

## Escopo: o que a doc cobre

A doc cobre **os aspectos core de tecnologia e de negócio**: o que o sistema promete, a decisão arquitetural que sustenta essa promessa, o contrato que alguém de fora consome e a armadilha que faz o leitor errar. Nada além disso.

- **FAÇA**: Documente o comportamento core no nível em que ele é observável (endpoint, campo de YAML, step, regra de autorização, invariante).
- **FAÇA**: Prefira apagar a explicar duas vezes. Um assunto tem um lugar canônico; os outros documentos linkam para ele.
- **FAÇA**: Remova doc micro ao encontrá-la. Micro é: detalhe de implementação interna que o consumidor não vê, narrativa de mudança ("antes era X, agora é Y"), post-mortem de bug, enumeração exaustiva de campo trivial e qualquer texto que só repita o que o código já diz com clareza.
- **NÃO FAÇA**: Documentar estrutura interna de pacote, nome de função privada ou passo-a-passo de refactor: isso vira ADR quando é decisão, e nada quando é só código.
- **NÃO FAÇA**: Deixar uma feature core sem nenhum registro do que ela faz, para quem, e por quê.
- **NÃO FAÇA**: Referenciar em doc commitável arquivos de planejamento (specs/plans/handoffs); eles são gitignored e o link nasce quebrado.

## Feature nova

- **FAÇA**: Documente minimamente toda feature core nova antes de considerar o trabalho concluído, mesmo que seja só um PRD curto ou uma seção em doc existente.
- **FAÇA**: Ao fechar uma implementação (testes passando, antes de anunciar entrega, commit ou MR), **pergunte ao usuário** se ele quer gerar a documentação com a skill `live-docs`. Rode só se ele pedir; silêncio ou "ok" não é "sim".

## Bugfix

Antes de tocar na doc, compare o que ela já dizia com o comportamento depois do fix:

- **Doc já descrevia o comportamento correto, só o código estava errado** → conserte o código; a doc já estava certa, nada a mudar nela.
- **O fix muda o comportamento que a doc descrevia** (mesmo que a doc só documentasse o bug) → atualize a doc para refletir o comportamento novo.
- **A regra de negócio mudou de verdade** (não é só correção, é decisão nova) → atualize a doc.

O teste: se alguém lesse só a doc hoje, ela bateria com o que o sistema faz depois da mudança? Se não, ajuste.

## Como

Use a skill `live-docs` para decidir qual artefato criar ou atualizar (arquitetura, PRD, BDD, ADR) e onde ele mora. Para focar num tipo só, passe o tipo como argumento: `live-docs bdd`.
