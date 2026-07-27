# Princípios de Design

Estes princípios se aplicam a todo código, independente de linguagem, framework ou paradigma.

## KISS — Keep It Simple, Stupid

Prefira a solução mais simples que resolve o problema corretamente.

- **FAÇA**: Escolha implementações diretas em vez de espertas
- **FAÇA**: Se duas soluções funcionam, escolha a mais fácil de ler e entender
- **NÃO FAÇA**: Adicionar camadas de abstração, padrões ou indireção sem uma necessidade concreta e presente
- **NÃO FAÇA**: Over-engineering para requisitos hipotéticos futuros

## YAGNI — You Aren't Gonna Need It

Implemente apenas o que é necessário **agora**.

- **FAÇA**: Implemente funcionalidades quando forem explicitamente necessárias
- **NÃO FAÇA**: Adicionar hooks, flags, pontos de extensão ou generalização baseados em especulação
- **NÃO FAÇA**: Construir para o "talvez depois" — o requisito futuro pode nunca chegar, ou chegar diferente

## Responsabilidade Única

Cada função, classe ou módulo deve ter **um propósito claro** e um único motivo para mudar.

## Fail Fast (Early Return)

Trate condições de saída antecipada logo no topo da função — não deixe o caminho principal enterrado em uma cadeia de `if/else`.

- **FAÇA**: Verifique a condição inválida ou de borda primeiro e retorne (`return`/`throw`/`continue`) imediatamente
- **FAÇA**: Mantenha o caminho principal ("happy path") no nível de indentação mais raso
- **NÃO FAÇA**: Encadear vários `if/else if/else` quando um guard clause resolve
- **NÃO FAÇA**: Aninhar validações umas dentro das outras
- **NÃO FAÇA**: Usar `else` depois de um `if` que já termina em `return`/`throw`/`continue` — se o `if` sai da função, o que vem depois já é o caminho principal, sem precisar de `else`
