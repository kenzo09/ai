# Testes

Testabilidade é parte do design, não um afterthought — principalmente para fluxos críticos de negócio.

## Fluxos críticos

- **FAÇA**: Projete fluxos críticos de negócio (pagamento, autenticação, cálculo de preço, etc.) para que um cenário completo seja fácil de reproduzir num teste, sem mock elaborado nem setup manual extenso.
- **FAÇA**: Se um fluxo crítico é difícil de testar, trate isso como sinal de acoplamento ruim — resolva o acoplamento, não pule o teste.

## Unidade vs E2E

- **FAÇA**: Priorize testes E2E focados nos critérios de aceite do produto (o que é observável de fora) para os fluxos críticos.
- **FAÇA**: Use teste de unidade para lógica isolada e não trivial (cálculo, parser, regra de validação) que compensa isolar do resto.
- **NÃO FAÇA**: Criar teste de unidade para todo método só porque ele existe — isso infla a suíte sem aumentar confiança real.
- **NÃO FAÇA**: Testar detalhe de implementação que muda sem afetar o comportamento observável.

O teste: cada teste deve responder "o que quebra, do ponto de vista do produto, se essa lógica falhar?". Se a resposta é "nada perceptível", o teste não paga o custo de manutenção.
