# Divisão de Tarefas em Checkpoints

Toda feature ou bug de complexidade média ou alta é entregue em **checkpoints funcionais**: pontos da implementação onde o sistema está inteiro, testado e utilizável. Não em um único bloco gigante, nem em commits que só fazem sentido juntos.

Feature trivial (uma função, um ajuste de texto, um bugfix de uma linha) é um checkpoint só — não invente divisão onde não há.

## O que é um checkpoint

Um checkpoint agrupa **uma ou mais tarefas** levantadas na ideação/planejamento e resulta em um estado do sistema que satisfaz, ao mesmo tempo:

- **Build passa** — compila, sobe, instala.
- **Testes passam** — rodados pelo agente localmente e válidos também na CI/CD, sem depender de um checkpoint futuro.
- **Nenhuma funcionalidade existente quebrada** — o que funcionava antes continua funcionando.
- **Revertível isoladamente** — `git revert` do checkpoint devolve um sistema funcional, sem exigir revert de outros checkpoints.
- **Validável manualmente** — existe algo concreto que o usuário que pediu a feature consegue exercitar e conferir (tela, endpoint, comando, log).

Se um dos cinco não se sustenta, o corte está no lugar errado: junte com o checkpoint vizinho ou redivida.

## Durante o planejamento

- **FAÇA**: Agrupe as tarefas em checkpoints, na ordem em que serão implementados, cada um com o critério de validação manual explícito ("como o usuário confere que esse checkpoint está de pé").
- **FAÇA**: Ordene para que os checkpoints iniciais já entreguem algo observável, em vez de deixar tudo visível só no último.
- **NÃO FAÇA**: Criar checkpoint que só existe como etapa interna ("criar as interfaces", "adicionar a coluna") sem nada que o usuário possa validar — isso é tarefa dentro de um checkpoint, não um checkpoint.

## Durante a implementação

- **FAÇA**: Antes de escrever código, pergunte ao usuário se ele quer a entrega **checkpoint por checkpoint** (pausa para validação em cada um) ou **tudo de uma vez** (implementa o plano inteiro e entrega no fim).
- **FAÇA**: Rode build e testes antes de cada commit. Falhou, conserte antes de commitar — commit vermelho não existe.
- **FAÇA**: Um commit por checkpoint (ou uma sequência que só termina com o checkpoint fechado), com mensagem que descreva o comportamento entregue.
- **NÃO FAÇA**: Commitar código com build quebrado, teste quebrado ou funcionalidade quebrada, nem com a justificativa de "o próximo commit conserta".
- **NÃO FAÇA**: Misturar dois checkpoints no mesmo commit — mata a revertibilidade isolada.

Mesmo com "tudo de uma vez", a divisão em checkpoints continua valendo nos commits. O que muda é só se há pausa para validação entre eles.

O teste (mental, não uma etapa a executar): para cada checkpoint, "se este commit fosse revertido, o sistema continuaria funcional?". Se a resposta for não, o corte está errado — redivida antes de commitar. Não faça revert de verdade para conferir.
