# Documentação de Features e Bugfixes

Código e documentação não podem divergir. Toda mudança de comportamento observável merece uma decisão explícita sobre a doc — nunca um "esqueceu de atualizar".

## Feature nova

- **FAÇA**: Documente minimamente toda feature nova antes de considerar o trabalho concluído — mesmo que seja só um PRD curto ou uma seção em doc existente.
- **NÃO FAÇA**: Deixar uma feature sem nenhum registro do que ela faz, para quem, e por quê.

## Bugfix

Antes de tocar na doc, compare o que ela já dizia com o comportamento depois do fix:

- **Doc já descrevia o comportamento correto, só o código estava errado** → conserte o código; a doc já estava certa, nada a mudar nela.
- **O fix muda o comportamento que a doc descrevia** (mesmo que a doc só documentasse o bug) → atualize a doc para refletir o comportamento novo.
- **A regra de negócio mudou de verdade** (não é só correção, é decisão nova) → atualize a doc.

O teste: se alguém lesse só a doc hoje, ela bateria com o que o sistema faz depois da mudança? Se não, ajuste.

## Como

Use a skill `live-docs` para decidir qual artefato criar ou atualizar (PRD, ADR, BDD, reference) e onde ele mora.
