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

## Evidência visual de execução

Toda API ou página entregue vem com evidência visual do resultado rodando — foto ou vídeo. Quem roda é o agente, antes de dizer que terminou; a evidência é a prova, para quem pediu, de que o que foi solicitado existe e funciona. Sem evidência, a entrega é só uma afirmação.

**O formato é imagem ou vídeo. Sempre — inclusive para API.** Se os arquivos entregues não incluem pelo menos
um `.png`, `.jpg`, `.gif`, `.webm` ou `.mp4`, a evidência não foi produzida.

**A ferramenta é livre; o formato não.** Swagger, Postman ou Insomnia, DevTools, Playwright disparando a
requisição, ou o próprio terminal com `curl` — qualquer meio serve, desde que o resultado apareça numa
captura. Um print do terminal mostrando o comando e a resposta é evidência tão válida quanto um print do
Swagger. O que não é evidência é o mesmo conteúdo entregue **fora** de uma imagem: um `.json` salvo na pasta,
um bloco de log colado na resposta, a saída transcrita.

- **FAÇA**: Exercite o fluxo entregue no sistema real e capture o resultado. O MCP do Playwright é a primeira opção quando há tela — navegue, preencha, dispare a request, tire o screenshot ou grave o vídeo, leia rede e console. Para API, ele também serve para disparar a chamada e capturar o resultado.
- **FAÇA**: Para API, a captura mostra a chamada real com o request e a resposta legíveis na imagem — o endpoint, o status, o corpo e a parte da resposta que prova o comportamento. Para página, o estado final da tela.
- **FAÇA**: Escolha o meio que torne a captura mais legível para quem vai conferir, e o mais barato de operar. Se dirigir a UI está custando caro, um print do terminal resolve — o que não pode é o custo virar motivo para não haver imagem nenhuma.
- **FAÇA**: Capture o caminho feliz e, quando o pedido envolve erro ou validação, também o caminho de erro.
- **FAÇA**: Redija dado pessoal e segredo **antes** de capturar — nome, e-mail, documento, token, chave. Ambiente de desenvolvimento costuma responder com conta real, e o Swagger imprime o bearer inteiro no bloco `curl`. Redija na origem (no DOM, antes do screenshot), nunca depois: imagem não se edita com `sed`.
- **FAÇA**: Antes de dizer que terminou, liste os arquivos de `.evidence/` e confirme que há imagem ou vídeo cobrindo cada caminho prometido. Essa conferência é a última coisa antes da entrega.
- **FAÇA**: Ao delegar a captura, mande junto o formato exigido. Delegação não transfere a regra — se o subagente devolver só texto, a evidência continua não existindo, e quem entrega responde por isso.
- **FAÇA**: Ao pedir revisão da entrega, inclua "existe imagem ou vídeo de cada caminho?" como item verificável. Critério que não entra no prompt do revisor não é conferido por ninguém.
- **NÃO FAÇA**: Apresentar diff, log de build ou descrição do que foi feito como evidência — nada disso prova execução.
- **NÃO FAÇA**: Entregar corpo JSON salvo em arquivo, log de terminal ou saída transcrita **no lugar** da captura. Rodar `curl` é legítimo; entregar o texto dele sem o print não é. Esses arquivos são complemento, e complemento sozinho não prova execução.
- **NÃO FAÇA**: Entregar captura com erro no console ou request vermelha sem tratar — console limpo faz parte da prova. Erro de recurso 4xx/5xx que o próprio teste provocou de propósito é esperado: aponte qual é e por quê.
- **NÃO FAÇA**: Criar suíte E2E de Playwright onde a stack não comporta — a evidência é obrigatória, o spec automatizado não.

Se capturar for de fato impossível no ambiente, isso é um bloqueio a declarar em voz alta junto da entrega —
não uma licença para substituir o formato por texto e seguir como se a regra tivesse sido cumprida.

## BDD documentado vira teste

Cenário BDD documentado é critério de aceite, não texto decorativo. Se não existe teste correspondente, ninguém sabe se a doc ainda é verdade.

- **FAÇA**: Implemente um teste para todo cenário BDD documentado — o teste é a prova de que o cenário descreve o sistema real.
- **FAÇA**: Ao mexer num cenário documentado, ajuste o teste correspondente no mesmo trabalho; ao mexer no teste, confira o cenário.
- **FAÇA**: Se cenário e teste divergem, decida qual está errado antes de "consertar" qualquer um dos dois — pode ser doc desatualizada ou pode ser bug.
- **NÃO FAÇA**: Documentar cenário de comportamento que você não pretende cobrir com teste — se não vale um teste, não vale um cenário.

Use a skill `live-docs bdd` para a convenção de rastreabilidade entre cenário e teste.

O teste: cada teste deve responder "o que quebra, do ponto de vista do produto, se essa lógica falhar?". Se a resposta é "nada perceptível", o teste não paga o custo de manutenção.
