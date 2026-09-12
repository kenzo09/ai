# Testes

Testabilidade é parte do design, não um afterthought, principalmente para fluxos críticos de negócio.

## Escopo: o que a suíte cobre

A suíte cobre **as features core**: o que o produto promete e o que quebra o negócio se falhar. Nada além disso. Suíte enxuta que roda rápido e falha por motivo real vale mais que suíte grande onde ninguém sabe o que uma falha significa.

- **FAÇA**: Cubra toda feature core por um teste que a exercita de fora (E2E, integration ou smoke), no nível em que o usuário a percebe.
- **FAÇA**: Teste de unidade **só para caso muito crítico**: algoritmo com regra de negócio não óbvia, cálculo, fronteira de segurança (authz, anti-SSRF, path traversal, redaction de segredo), classificação de falha que decide retry/perda de dado. Se não é crítico, o teste de fora já basta.
- **FAÇA**: Remova teste micro ao encontrá-lo. Micro é: round-trip de JSON/YAML que só valida tag de struct, getter, `String()`, parse de enum, helper trivial, wrapper que só delega, e qualquer caso já coberto por um teste de fora.
- **FAÇA**: Prefira uma tabela de casos num arquivo por conceito a um arquivo por tipo/método.
- **NÃO FAÇA**: Buscar cobertura por número. Cobertura de linha não é critério; "essa feature core tem teste?" é.
- **NÃO FAÇA**: Manter teste que só falha quando alguém renomeia um campo interno.

Esse escopo vale igualmente para o que **não** existe: feature core sem teste de fora é lacuna a declarar em voz alta, não a compensar com uma pilha de testes de unidade.

## Fluxos críticos

- **FAÇA**: Projete fluxos críticos de negócio (pagamento, autenticação, cálculo de preço, etc.) para que um cenário completo seja fácil de reproduzir num teste, sem mock elaborado nem setup manual extenso.
- **FAÇA**: Se um fluxo crítico é difícil de testar, trate isso como sinal de acoplamento ruim: resolva o acoplamento, não pule o teste.

## Unidade vs E2E

- **FAÇA**: Priorize testes E2E focados nos critérios de aceite do produto (o que é observável de fora) para os fluxos críticos.
- **FAÇA**: Use teste de unidade só quando a lógica é crítica **e** isolá-la é a única forma de exercitar o caso (ver *Escopo* acima).
- **NÃO FAÇA**: Criar teste de unidade para todo método só porque ele existe: isso infla a suíte sem aumentar confiança real.
- **NÃO FAÇA**: Testar detalhe de implementação que muda sem afetar o comportamento observável.

## Evidência visual de execução

Evidência visual do resultado rodando (**imagem ou vídeo**) é a prova, para quem pediu, de que o que foi solicitado existe e funciona. Sem ela, a entrega é só uma afirmação. Por isso ela é sempre **oferecida** no fecho da implementação; gerar ou dispensar é decisão do usuário.

- **FAÇA**: Use a skill `test-evidence` na hora de capturar: ela traz a mecânica (Playwright, redação de segredo antes do print, o que conta como captura, delegação a subagente).
- **FAÇA**: Ao fechar uma implementação (testes passando, antes de anunciar entrega, commit ou MR), **pergunte ao usuário** se ele quer gerar a evidência com a skill `test-evidence`. Rode só se ele pedir; silêncio ou "ok" não é "sim".
- **FAÇA**: Quando o usuário pedir a evidência, antes de dizer que terminou liste `.evidence/` e confirme que há imagem ou vídeo cobrindo cada caminho prometido.
- **NÃO FAÇA**: Apresentar diff, log de build, JSON salvo em arquivo ou saída transcrita **no lugar** da captura pedida: nada disso prova execução.
- **NÃO FAÇA**: Criar suíte E2E de Playwright onde a stack não comporta: a evidência é obrigatória, o spec automatizado não.

Se o usuário pediu a evidência e capturar for de fato impossível no ambiente, isso é um bloqueio a declarar em voz alta junto da entrega, não uma licença para substituir o formato por texto e seguir como se o pedido tivesse sido atendido.

## BDD documentado vira teste

Cenário BDD documentado é critério de aceite, não texto decorativo. Se não existe teste correspondente, ninguém sabe se a doc ainda é verdade.

- **FAÇA**: Implemente um teste para todo cenário BDD documentado: o teste é a prova de que o cenário descreve o sistema real.
- **FAÇA**: Ao mexer num cenário documentado, ajuste o teste correspondente no mesmo trabalho; ao mexer no teste, confira o cenário.
- **FAÇA**: Se cenário e teste divergem, decida qual está errado antes de "consertar" qualquer um dos dois: pode ser doc desatualizada ou pode ser bug.
- **NÃO FAÇA**: Documentar cenário de comportamento que você não pretende cobrir com teste: se não vale um teste, não vale um cenário.
- **NÃO FAÇA**: Documentar cenário micro só para ter o par teste↔cenário; a correspondência vale nos dois sentidos: cenário fora do core não deveria existir, e por isso não gera teste.

Use a skill `live-docs bdd` para a convenção de rastreabilidade entre cenário e teste.

O teste: cada teste deve responder "o que quebra, do ponto de vista do produto, se essa lógica falhar?". Se a resposta é "nada perceptível", o teste não paga o custo de manutenção.
