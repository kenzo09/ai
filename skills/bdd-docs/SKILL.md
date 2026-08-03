---
name: bdd-docs
description: Use when a behavior is added, modified, or removed — whether business logic, authorization rules, API contracts, or core technical flows. Also use when reviewing whether existing BDD docs reflect the current system after a code change.
---

# Documentação BDD

## Visão Geral

Documente comportamentos observáveis do sistema como cenários BDD em `docs/bdd/`. Um arquivo por unidade de comportamento (componente, fluxo ou domínio). Cenários descrevem o que o sistema faz visto de fora — não como faz internamente.

## Quando Usar

Crie ou atualize um doc BDD sempre que:
- Uma regra de negócio é introduzida ou muda
- Um contrato de API, política de autorização ou regra de validação de dados muda
- Um fluxo técnico transversal (auth, multi-tenancy, pipeline de importação) muda
- Uma nova área de domínio é introduzida

**Quando NÃO usar:** CRUD rotineiro sem invariantes ou regras especiais. Se todo campo é opcional e qualquer valor é aceito, não há nada comportamental a documentar.

## O Que Documentar

Dois tipos de conteúdo pertencem aos docs BDD:

**Comportamentos de negócio** — regras visíveis a usuários e stakeholders:
- Regras de validação (campos obrigatórios, formatos, restrições de unicidade)
- Autorização (quem pode fazer o quê, sob quais condições)
- Invariantes de domínio (ex.: número de matrícula único por escola, não globalmente)
- Regras de workflow (criação transacional de múltiplos registros, sucesso parcial na importação)

**Comportamentos técnicos** — regras invisíveis ao usuário, mas contratuais para desenvolvedores:
- Fluxos de token de auth (como um token do provedor A se torna um token válido para o sistema B)
- Resolução de tenant (como o sistema determina a qual tenant uma request pertence)
- Regras de fallback e default (o que acontece quando uma claim está ausente)
- Contratos de resposta de erro (qual status code, qual mensagem, sob qual condição)

## Organização de Arquivos

```
docs/bdd/
  auth-middleware.md          # Domínio em arquivo único
  school-resolution.md
  student-management.md
  payments/                   # Pasta quando um domínio tem 3+ arquivos distintos
    checkout.md
    refunds.md
    subscription-billing.md
```

**Use uma pasta quando** um domínio cresce para 3 arquivos ou mais. Nomeie a pasta com o nome do domínio (`payments/`, `notifications/`, `access-control/`). Mantenha os arquivos internos nomeados pelo comportamento específico (`checkout.md`, não `payments-checkout.md` — a pasta já fornece o namespace).

**Um arquivo por unidade de comportamento.** Divida quando um arquivo cobre dois conceitos distintos que um dev consultaria de forma independente. Junte quando os cenários são finos demais para existirem sozinhos.

## Estrutura Canônica

```markdown
# <Nome do Componente ou Fluxo>

## Visão Geral

Uma ou duas frases: o que isso faz e qual problema resolve.

## Comportamentos

---

### <Nome do Grupo de Comportamento>

Texto descrevendo o comportamento. Declare regras invariantes aqui.

**Regras:**
- Regra objetiva 1
- Regra objetiva 2

#### Cenário: <Nome do Cenário>
**Dado** <precondição ou estado inicial>
**Quando** <ação ou evento que dispara>
**Então** <resultado observável esperado>
**E** <resultado adicional, se necessário>
```

## Regras de Escrita

| Elemento | Regra |
|---|---|
| Nome do arquivo | kebab-case correspondente à unidade de comportamento |
| `### Grupo de Comportamento` | Agrupa cenários relacionados sob um mesmo aspecto funcional |
| `**Dado**` | Estado inicial ou precondição — define o contexto |
| `**Quando**` | A ação ou evento que dispara o comportamento |
| `**Então**` | O resultado esperado observável |
| `**E**` | Resultado adicional — nunca repita nem reescreva o `Então` |
| Conectivos em negrito | Sempre em negrito: `**Dado**`, `**Quando**`, `**Então**`, `**E**` |
| Tom | Objetivo, sem jargão. Legível sem conhecer o código |
| Escopo | Comportamento observável externamente — sem detalhes de implementação |

## Exemplo Canônico

```markdown
### Unicidade de Matrícula

O número de matrícula é único por escola, não globalmente. O mesmo número pode existir em escolas diferentes.

**Regras:**
- Se `enrollment_number` for informado, deve ser único dentro da escola
- `enrollment_number` é opcional; ausência não viola nenhuma regra

#### Cenário: Matrícula duplicada na mesma escola
**Dado** um aluno com matrícula "2024001" já cadastrado na escola A
**Quando** um novo aluno com matrícula "2024001" é cadastrado na escola A
**Então** retorna erro 409 "enrollment_number is already in use at this school"

#### Cenário: Mesma matrícula em escolas diferentes
**Dado** um aluno com matrícula "2024001" cadastrado na escola A
**Quando** um aluno com matrícula "2024001" é cadastrado na escola B
**Então** o cadastro é aceito normalmente
```

## Mantendo os Docs Atualizados

Ao modificar qualquer comportamento, localize o cenário correspondente e:

1. **Atualize** — se o comportamento mudou
2. **Adicione** — se é comportamento novo sem cenário existente
3. **Remova** — se o comportamento foi eliminado

Docs BDD devem refletir o **comportamento atual real** do sistema — não o comportamento desejado ou histórico.
