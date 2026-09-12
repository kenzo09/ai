---
name: test-evidence
description: Use when about to claim a delivery is done, finished, working or ready (an endpoint, page, flow, fix or feature someone else will check), and visual proof of it running has not been captured yet. Also use when choosing how to capture (Playwright MCP, Swagger, Postman, DevTools, curl in a terminal), when redacting secrets or personal data before a screenshot, when delegating capture to a subagent, or when verifying that .evidence/ covers every promised path. Triggers on "evidência", "evidência visual", "print", "screenshot", "prova que funciona", "capturar a tela", "terminei", "está pronto".
---

# Evidência de Teste

Prova visual de que o que foi entregue roda de verdade. Quem exercita o fluxo e captura é o agente,
antes de dizer que terminou: a evidência é para quem pediu conferir sem ter que acreditar.

**Princípio central:** evidência é imagem ou vídeo. Texto que descreve execução não é evidência, é
afirmação. Se os arquivos entregues não incluem pelo menos um `.png`, `.jpg`, `.gif`, `.webm` ou
`.mp4`, a evidência não foi produzida.

## O que conta

| Conta como evidência | Não conta |
|---|---|
| Print do Swagger / Postman / Insomnia / DevTools | `.json` de resposta salvo na pasta |
| Print do terminal com o comando e a resposta visíveis | Bloco de log colado na resposta do chat |
| Screenshot do Playwright MCP | Saída de `curl` transcrita sem o print |
| Vídeo do fluxo (`.webm`, `.mp4`) | Diff, log de build, descrição do que foi feito |

A ferramenta é livre; o formato não. Rodar `curl` é legítimo para *disparar*, mas entregar o texto dele
sem a captura não é evidência. Esses arquivos são complemento, e complemento sozinho não prova
execução.

Print de terminal vale tanto quanto print de Swagger. Se dirigir a UI está custando caro, o terminal
resolve; o que não pode é o custo virar motivo para não haver imagem nenhuma.

## Como capturar

1. **Redija primeiro.** Segredo e dado pessoal saem *antes* do disparo (ver seção abaixo).
2. **Exercite o fluxo no sistema real.** Com tela, o MCP do Playwright é a primeira opção: navegue,
   preencha, dispare a request, leia rede e console, tire o screenshot. Sem tela, ele também serve
   para disparar a chamada, assim como Swagger ou `curl` num terminal fotografado.
3. **Capture o caminho feliz.** E quando o pedido envolve erro ou validação, o caminho de erro
   também.
4. **Deixe a prova legível na imagem.** Para API: endpoint, status, corpo, e a parte da resposta que
   prova o comportamento. Para página: o estado final da tela.
5. **Salve em `.evidence/<assunto>/`**, um arquivo por caminho prometido, com nome que diz o que é
   (`create-201.png`, `duplicate-409.png`).
6. **Confira antes de entregar.** `ls .evidence/<assunto>/` e verifique que há imagem ou vídeo
   cobrindo *cada* caminho prometido. Essa conferência é a última coisa antes da entrega.

Console limpo faz parte da prova. Captura com erro no console ou request vermelha sem tratamento não
serve. 4xx/5xx que o próprio teste provocou de propósito é esperado: aponte qual é e por quê.

## Redação: antes, nunca depois

Imagem não se edita com `sed`. Redija na origem, no DOM antes do screenshot, no payload antes do
disparo:

- Nome, e-mail, documento, telefone: ambiente de dev costuma responder com conta real.
- Token, chave, senha: o Swagger imprime o bearer inteiro no bloco `curl`.

## Delegação

Ao delegar a captura a um subagente, mande o formato exigido dentro do prompt. Delegação não
transfere a regra: se o subagente devolver só texto, a evidência continua não existindo, e quem
entrega responde por isso.

Ao pedir revisão da entrega, inclua "existe imagem ou vídeo de cada caminho prometido?" como item
verificável: critério que não entra no prompt do revisor não é conferido por ninguém.

## Erros comuns

| Erro | Correção |
|---|---|
| Screenshot com bearer ou e-mail real visível | Redigir no DOM antes de capturar |
| Uma imagem só, do caminho feliz, quando o pedido era validação | Uma por caminho prometido |
| Dizer "terminei" e listar `.evidence/` depois | A conferência vem antes da frase |

## Quando capturar é impossível

Bloqueio real de ambiente (sem browser, sem acesso, SSO que barra automação) é um bloqueio a declarar
em voz alta junto da entrega, não licença para substituir o formato por texto e seguir como se a
regra tivesse sido cumprida. Peça ao usuário o que falta (autenticar a sessão, liberar acesso) em vez
de entregar sem prova.
