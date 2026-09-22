---
name: visual-briefing
description: Use when someone asks to explain, present or brief a module, feature, branch, WIP, pull/merge request, service or whole system to others, in any language, framework or architecture, and the answer should be a visual page rather than chat text. Also use when asked for an explainer, overview, onboarding page, architecture walkthrough or "o que mudou" summary aimed at technical and business readers. Triggers on "gerar um artefato para explicar", "explicar o módulo", "explicar o que foi feito na branch", "briefing das mudanças", "visão de arquitetura", "apresentar para o time", "explainer".
---

# Visual Briefing

Uma página HTML que explica um assunto de software para dois públicos ao mesmo tempo: quem decide
(negócio) e quem mexe (técnico). O visual carrega a explicação; o texto é o mínimo para entender.

**Princípio central:** a página sempre nasce do [`assets/template.html`](assets/template.html). O design já está
decidido lá (tokens, tipografia, componentes, tema claro/escuro, lente Negócio/Técnico). O trabalho
de cada caso é **levantar fatos e escolher componentes**, não inventar design.

## Saída

| Harness | Entrega |
|---|---|
| Claude Code com a ferramenta `Artifact` | Publicar como Artifact (seguir o contrato da própria ferramenta, inclusive `quickstart` antes do primeiro publish) |
| Outro harness com ferramenta própria de página publicada | Publicar por ela, seguindo o contrato dela |
| Qualquer outro | Um arquivo `.html` autocontido no disco, com o caminho informado ao usuário. O template não tem invólucro (o Artifact coloca o dele), então envolva o conteúdo assim: |

```html
<!doctype html>
<html lang="[idioma do usuário]">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- <title>, <link> das fontes e <style> do template -->
</head>
<body>
<!-- .bar, <main> e <script> do template -->
</body>
</html>
```

Sempre gerar a página. Resumo no chat não substitui o artefato.

## Processo

1. **Fixar o assunto.** Qual módulo, mudança ou feature, quais sistemas entram,
   e para quem é a página. Só pergunte se o pedido não disser e o código não resolver.
2. **Levantar fatos.**
   - Assunto com mais de um sistema e harness com subagentes: um subagente de exploração por
     sistema, todos disparados juntos.
   - Assunto de um módulo só: leia você mesmo.
   - Em qualquer caso, só leitura: nada de modificar nem commitar.

   Peça (ou levante) um resumo denso e estruturado, com nomes exatos:
   - o que é e para quem serve;
   - fluxo principal, passo a passo;
   - interfaces (rotas, comandos, eventos, tabelas);
   - estados;
   - números reais (diff stat, contagens);
   - documentação de decisão (o formato que o projeto usar: ADR, RFC, PRD, wiki);
   - riscos e lacunas;
   - status de cada entrega, nos termos do fluxo que o projeto usa (revisão, merge, release, deploy).

   Se o assunto é uma mudança, compare com a linha de base no controle de versão que o projeto
   usa (no git: `git diff --stat base...HEAD` e `git log base..HEAD`). Sem controle de versão,
   compare com o que o usuário apontar como "antes".
3. **Conferir o que decide.** Um fato que vira risco na página, ou dois subagentes que se
   contradizem: leia a fonte você mesmo. O que não der para confirmar entra marcado como
   "a verificar".
4. **Escolher os componentes** pela tabela abaixo. Entram só as seções que o assunto tem.
5. **Montar a partir do template.**
   - Copie sem mudar nada: o `<link>` das fontes, o `<style>`, o `.lens` e o `<script>`.
   - Refaça os links do `.nav`: um link por seção que a página tiver.
   - Troque todo o conteúdo de `<main>`.
   - Troque o `<title>`: um nome de 2 a 4 palavras, específico do assunto.
   - Traduza para a língua do usuário todo rótulo de interface do template (nav, lente,
     `aria-label`, eyebrows, legenda, níveis de risco).
   - Todo texto entre `[colchetes]` é um slot: vira fato levantado ou o elemento sai.
   - Remova o comentário-guia do topo.
6. **Entregar.**
   - Publique ou salve a página.
   - No chat, em até 6 linhas: o link ou caminho, o que a página cobre e os achados que merecem
     ação.

## Componentes

| O assunto tem… | Componente do template |
|---|---|
| Uma tese: o que muda ou para que serve | `.hero`: `.tags` (referência da entrega no rastreador do projeto, se houver; versão; estado), `h1` com a tese, `.sub`, `.stats` com 3 ou 4 números reais |
| Uma mudança | `.ba`: antes → depois. Para um módulo sem mudança, use problema → solução |
| Mais de um componente conversando | `.diagram`: SVG em colunas (atores → interfaces → serviços → externos), com `.legend` |
| Uma sequência real (requisição, pipeline, onboarding) | `.flow .step`, com `.call` para a chamada exata |
| Estados de domínio | `.life .pill` (`.d` rascunho/pendente, `.p` ativo/ok, `.x` encerrado) |
| Um recurso ou sistema a descrever | `.grid .box`: `h3`, `.biz-line` e detalhe em `table` ou `.chips` |
| Uma magnitude com partes (linhas, custo, volume) | `.diffbar` com `flex` igual ao valor real, mais `.drow` |
| Riscos ou pendências | `.risks .risk` com `.sev.h`, `.m`, `.l` ou `.doc`, da mais grave para a menos grave |
| Entregas em andamento | `.deliveries .delivery` com uma `.pill` de status |

Assunto que não cabe em nenhum componente: crie o bloco novo com os mesmos tokens e as mesmas
classes de base (`.box`, `.chip`, `.pill`). Não mude a paleta nem as fontes.

## Contrato do texto

- Cada bloco tem **uma** frase de negócio sempre visível (`.biz-line`, `.lead` ou o `p` do card).
  Todo detalhe técnico vai num elemento com `class="tech"`: ele some na lente Negócio.
- A lente Negócio precisa ser lida sozinha, sem depender de nada que ela esconde.
- Frases curtas, voz ativa, na língua do usuário. Nomes, rotas e caminhos em `code`, exatamente
  como estão no código.
- Números, nomes e status saem do levantamento. Um dado sem fonte não entra.
- Numeração só onde a ordem é real: o `.flow` sim, as seções não.

## Diagrama

- Use as classes do SVG do template (`.n`, `.nb`, `.ni`, `.t`, `.s`, `.c`, `.e`, `.ed`, `.em`,
  `.lbl`, `.lbd`). Elas ficam no `<style>` da página, escopadas em `.diagram`, e servem para
  todos os diagramas. As cores vêm dos tokens, então o diagrama funciona nos dois temas.
- Não coloque `<style>` dentro do SVG: a regra vaza para a página inteira. Uma variante nova
  (por exemplo, nó tracejado) vira uma classe `.diagram .x` no `<style>` da página, feita com os
  tokens.
- Os marcadores (`#ar`, `#ard`, `#arm`) só são definidos no primeiro SVG. Os outros diagramas
  usam os mesmos ids, sem repetir o `<defs>`.
- Destaque (`.nb`) só o que é o assunto da página.
- Ligações: `.e` para o fluxo principal, `.ed` (tracejada) para o caminho alternativo ou de
  desenvolvimento, `.em` para autenticação ou referência.
- Rótulo de ligação é curto: a rota ou o verbo.
- Mantenha `min-width` no SVG e o `overflow-x:auto` do `.diagram`: no celular ele rola, a página
  não.

## Erros comuns

| Erro | Correção |
|---|---|
| Redesenhar paleta, fonte ou layout "para este caso" | O template é o design. Mude só o conteúdo |
| Parágrafos explicativos | Troque por um componente: tabela, chips, passo, diagrama |
| Lente Negócio vazia ou quebrada | Toda seção precisa de uma frase visível sem `.tech` |
| Seção que o assunto não tem ("Status" de um módulo estável) | Apague a seção |
| Afirmar o que só um subagente disse | Confira na fonte ou marque "a verificar" |
| Entregar só o resumo no chat | A página é a entrega; o chat só aponta para ela |
