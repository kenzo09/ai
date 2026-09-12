# Divisão de Tarefas

Planejar uma feature de complexidade média ou alta é tomar duas decisões, **nesta ordem**:

1. **O que pode correr junto**: o mapa de dependências e os lotes de subagents paralelos.
2. **Onde ficam os cortes funcionais**: os checkpoints que agrupam esses lotes.

A ordem importa: quem corta checkpoint primeiro e só depois procura paralelismo produz plano serializado, porque cada corte que já existe vira uma barreira artificial. Quem mapeia dependência primeiro descobre o quanto pode correr junto e só então escolhe onde parar.

Feature trivial (uma função, um ajuste de texto, um bugfix de uma linha) não tem lote nem checkpoint. Não invente divisão onde não há.

## Primeiro: paralelismo dos subagents

O ganho de tempo está aqui, e ele desaparece se a divisão for feita depois.

- **FAÇA**: Comece pelo mapa de dependências: para cada tarefa, de que ela precisa para *começar*. Tarefas que não dependem umas das outras formam um lote paralelo; deixe o lote explícito no plano, não implícito na ordem da lista.
- **FAÇA**: Resolva primeiro o que destrava mais tarefas (contrato, tipo, schema, assinatura, migration) e depois dispare o resto junto. Maximizar o lote é decisão de ordenação, tomada antes de existir checkpoint.
- **FAÇA**: Despache um subagent por tarefa do lote, todos na mesma mensagem. Só o que é de fato independente: arquivos disjuntos, sem estado compartilhado, nenhuma precisa da saída da outra.
- **FAÇA**: Confira `git status` e `git log` depois de cada lote: subagent extrapola escopo e commita mesmo com instrução explícita em contrário.
- **FAÇA**: Convirja antes de fechar o checkpoint: build e testes rodam uma vez sobre o resultado junto do lote, não por tarefa isolada.
- **NÃO FAÇA**: Paralelizar tarefas que editam o mesmo arquivo: o conflito custa mais que o ganho.
- **NÃO FAÇA**: Paralelizar por paralelizar em tarefa pequena: coordenar custa mais que fazer em sequência.

## Depois: checkpoints

Checkpoint é onde o sistema fica inteiro, testado e utilizável: o ponto onde vale commitar. Ele agrupa **um ou mais lotes** e resulta em um estado que satisfaz, ao mesmo tempo:

- **Build passa**: compila, sobe, instala.
- **Testes passam**: rodados pelo agente localmente e válidos também na CI/CD, sem depender de um checkpoint futuro.
- **Nenhuma quebra acidental**: refactor e evolução podem mudar comportamento de propósito; o que não pode é quebra por descuido nem migração pela metade. Se o comportamento muda, a mudança está completa dentro do checkpoint: chamadores, testes e doc ajustados junto, e a quebra declarada na mensagem de commit.
- **Revertível isoladamente**: `git revert` do checkpoint devolve um sistema funcional, sem exigir revert de outros checkpoints.
- **Validável manualmente**: existe algo concreto que o usuário que pediu a feature consegue exercitar e conferir (tela, endpoint, comando, log).

Se um dos cinco não se sustenta, o corte está no lugar errado: junte com o checkpoint vizinho ou redivida.

- **FAÇA**: Corte tão **grosso** quanto os cinco critérios permitirem. Checkpoint fino demais parte lote paralelo em dois e serializa o que podia correr junto.
- **FAÇA**: Dê a cada checkpoint o critério de validação manual explícito ("como o usuário confere que esse checkpoint está de pé").
- **FAÇA**: Ordene para que os checkpoints iniciais já entreguem algo observável, em vez de deixar tudo visível só no último.
- **NÃO FAÇA**: Criar checkpoint que só existe como etapa interna ("criar as interfaces", "adicionar a coluna") sem nada que o usuário possa validar. Isso é tarefa dentro de um checkpoint, não um checkpoint.

## Quando os dois colidem

Paralelismo decide a ordem; os cinco critérios decidem onde para. Quando um lote maior só cabe num checkpoint que não passa nos cinco, **os critérios ganham**: junte menos tarefas e aceite o corte. "Estava paralelo" não é justificativa para commit com build quebrado, teste vermelho ou migração pela metade.

## Durante a implementação

- **FAÇA**: Antes de escrever código, pergunte ao usuário se ele quer a entrega **checkpoint por checkpoint** (pausa para validação em cada um) ou **tudo de uma vez** (implementa o plano inteiro e entrega no fim).
- **FAÇA**: Rode build e testes antes de cada commit. Falhou, conserte antes de commitar. Commit vermelho não existe.
- **FAÇA**: Um commit por checkpoint (ou uma sequência que só termina com o checkpoint fechado), com mensagem que descreva o comportamento entregue.
- **NÃO FAÇA**: Commitar código com build quebrado, teste quebrado ou funcionalidade quebrada, nem com a justificativa de "o próximo commit conserta".
- **NÃO FAÇA**: Misturar dois checkpoints no mesmo commit: mata a revertibilidade isolada.

Mesmo com "tudo de uma vez", a divisão em checkpoints continua valendo nos commits. O que muda é só se há pausa para validação entre eles.

O teste (mental, não uma etapa a executar): para cada checkpoint, "se este commit fosse revertido, o sistema continuaria funcional?". Se a resposta for não, o corte está errado. Redivida antes de commitar. Não faça revert de verdade para conferir.
