---
name: parallel-batches
description: Use after an implementation plan is written and approved, to execute it with the maximum number of subagents working at the same time instead of one implementer at a time. Maps task dependencies, groups independent tasks into parallel batches and drives the dispatch as tech lead. Triggers on "roda o plano em paralelo", "paraleliza o plano", "quebra em lotes", "quantos agentes der", "executa em lote", "não quero um agente por vez", "run the plan in parallel". Do not use for a trivial change or a plan with fewer than three tasks: dispatch directly.
---

# Execução do plano em lotes paralelos

Você é o **líder técnico** de um time de subagents. Seu trabalho aqui não é implementar: é manter o time ocupado. Agente parado é tempo jogado fora, e serialização desnecessária é a forma mais cara de desperdício.

**Anuncie no início:** "Usando a skill parallel-batches para executar o plano em lotes paralelos."

## Onde esta skill entra

Depois do `superpowers:writing-plans` fechar o plano e você escolher o método de execução, **esta skill substitui o loop de execução**. Ela não altera nem depende de nenhum arquivo do superpowers.

```
brainstorming → writing-plans → [ parallel-batches ]  ← você está aqui
```

**Substituição explícita:** o `superpowers:subagent-driven-development` instrui "never dispatch multiple implementation subagents in parallel". Enquanto esta skill está ativa, essa linha **não vale** — ela é a decisão oposta, tomada de propósito. O que o superpowers protegia com a serialização (conflito de edição e review por tarefa) esta skill protege com escopo de arquivo disjunto e review na convergência do lote.

Não invoque as duas ao mesmo tempo. Se a serialização for o que você quer, use o `subagent-driven-development` e ignore esta skill.

## 1. Mapa de dependências

Leia o plano inteiro antes de despachar qualquer coisa. Para cada tarefa, pergunte de que ela precisa para **começar** — não de que ela precisa para *terminar*. A maioria das dependências aparentes é de término, e dependência de término não bloqueia o início.

A pergunta padrão não é "dá para paralelizar isso?". É **"por que isso ainda está em série?"**. Toda serialização precisa de uma justificativa nomeada, e só existem três:

1. **Dependência de saída**: a tarefa B precisa do que A produziu para começar.
2. **Mesmo arquivo**: as duas editam o mesmo arquivo.
3. **Estado compartilhado**: banco, fixture, porta, recurso único.

Sem uma das três, vai junto.

Monte a tabela antes de qualquer dispatch:

| # | Tarefa | Arquivos (exclusivos) | Precisa para começar | Lote |
|---|---|---|---|---|
| 1 | ... | ... | — | L1 |
| 2 | ... | ... | contrato da 1 | L2 |

## 2. Abrir mais trabalho

Antes de aceitar o mapa, ataque-o. Cada item abaixo tira tarefa da fila serial:

- **Casca do desbloqueador**: se o que destrava o lote é caro, entregue primeiro só a **casca** — assinatura, tipo, interface vazia, migration sem uso. O lote inteiro libera e o miolo vira mais uma tarefa paralela.
- **Quebre tarefa grande**: uma tarefa de cinco arquivos que ocuparia um agente por muito tempo geralmente é três tarefas de arquivos disjuntos. Eixos de corte: por arquivo, por camada, por endpoint, por caso de teste, por entidade.
- **Trabalho de segunda classe não existe**: teste, documentação, tipos, fixtures, migration e ajuste de chamadores são tarefas do lote, não apêndice de quem escreveu o código. São as vagas mais fáceis de preencher.
- **Extraia o detalhe disputado**: se B só depende de um detalhe de A, tire esse detalhe para uma tarefa própria e mande A e B juntas.
- **Mesmo arquivo não é veto imediato**: antes de serializar, veja se dá para fatiar o arquivo, extrair o trecho disputado, ou mandar um agente fazer a mudança estrutural e os outros trabalharem em cima. Só serialize quando nenhum desses couber.

Prefira um lote grande a dois lotes pequenos em sequência.

## 3. Despachar

- **Todos na mesma mensagem.** Um dispatch por resposta roda em série e o plano paralelo não vale nada.
- **Dimensione pelo trabalho disponível**, não por um número confortável. Dez tarefas independentes são dez subagents.
- **Escopo fechado por agente.** Escopo vago é a causa número um de colisão. Cada brief carrega:

```
Tarefa: <a tarefa do plano, copiada inteira>
Arquivos que você pode tocar: <lista exaustiva>
Arquivos que NÃO são seus: <os dos irmãos do lote>
Contratos com que você conta: <assinaturas e tipos já existentes ou entregues no lote anterior>
Restrições globais: <a seção Global Constraints do plano>
Não commite. Não despache subagents. Devolva: o que mudou e o que ficou pendente.
```

- **Nada de contexto herdado.** O subagent recebe o brief construído, nunca o histórico da sessão.
- **Redistribua enquanto o lote roda.** Terminou antes e existe tarefa do próximo lote já destravada, despache — ocioso não espera o lote inteiro fechar.

### Review

O review acontece na **convergência do lote**, não por tarefa: um reviewer sobre o diff junto do lote. É a troca consciente que compra o paralelismo.

Exceção nomeada: tarefa de risco alto (dinheiro, autenticação, migration destrutiva, concorrência) leva **reviewer próprio despachado junto com ela**, no mesmo lote. Não vale a pena economizar seat aí.

### Batch de mesma forma

Quando o plano lista várias tarefas que são o mesmo edit pequeno repetido em arquivos diferentes (a mesma constante, o mesmo campo, o mesmo one-liner), **não abra um agente por arquivo**: um brief só, listando todos, e um diff só para revisar.

## 4. Convergir

Ao fim de cada lote, antes de abrir o próximo:

- `git status` e `git log`: subagent extrapola escopo e commita mesmo com instrução explícita em contrário.
- Build e testes rodam **uma vez sobre o resultado junto** do lote, não por tarefa isolada.
- Costura de bordas é trabalho do líder, não de mais um subagent. Integre você mesmo o que os agentes deixaram desalinhado.
- Só então commite, seguindo a rule `checkpoints.md`: o lote convergido fecha um checkpoint, ou se junta ao lote seguinte até fechar um.

## O limite

Paralelismo é meio, não meta. Coordenar custa: escopo escrito, integração, revisão do que voltou. Em tarefa pequena esse custo passa do ganho — aí faça em sequência e siga. O limite é esse, e só esse. Não use "é mais simples em série" como atalho para não mapear a dependência.

Quando os cinco critérios de checkpoint e o lote maior colidem, **os critérios ganham**: junte menos tarefas e aceite o corte.

## Idioma dos artefatos

Esta skill roda em subagents que não herdam a tabela de idiomas do `CLAUDE.md`. Portanto: resposta ao usuário e mapa de lotes em **pt-BR**; briefs de dispatch, código e mensagens de commit em **en-US**.
