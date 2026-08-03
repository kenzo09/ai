# Guideline: PRD

`docs/features/<modulo>/prd.md` — por que esta feature existe, quem usa, que problema resolve.

**Audiência:** PMs, novatos, não-engenheiros. Se o leitor precisa abrir o código para entender o PRD, o PRD falhou.

## Quando rodar

- Módulo novo → sempre ganha PRD
- Feature existente expandiu o escopo → atualize a seção de escopo
- Módulo perdeu responsabilidade → mova o que saiu para "fora de escopo"

**Quando NÃO usar:** módulo puramente técnico sem valor de negócio distinguível (um wrapper de biblioteca, um helper
interno). Nesse caso `reference.md` basta.

## Template

```markdown
# <Feature> — PRD

## Objetivo
Um parágrafo: o problema sendo resolvido.

## Usuários
Quem se beneficia e como.

## Escopo
O que está no escopo. O que está explicitamente fora.

## Comportamentos-chave
Lista com os 3–7 comportamentos mais importantes do ponto de vista de negócio.
```

## Regras

| Regra | Por quê |
|---|---|
| Zero referência a código — sem nome de classe, endpoint, tabela ou env var | A audiência é não-técnica; detalhe técnico vive em `reference.md` |
| "Fora de escopo" é obrigatório quando existe | Ausência de limite é a maior fonte de expectativa errada |
| Comportamentos-chave em linguagem de negócio | Se vira lista de endpoints, virou reference |
| 3–7 comportamentos-chave | Mais que isso, o módulo provavelmente são dois |
| Verificado contra o código | Escopo que a spec prometeu e o código não entregou não entra |

## Erros comuns

| Erro | Correção |
|---|---|
| Copiar o objetivo da spec verbatim | Verifique se o código entrega aquilo; reescreva conforme o que existe |
| PRD que descreve implementação | Descreva o resultado para o usuário, não o mecanismo |
| Módulo novo sem PRD | Todo módulo novo ganha PRD, mesmo curto |
| Listar 20 comportamentos | Agrupe, ou o módulo precisa ser dividido |
