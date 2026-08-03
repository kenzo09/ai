# Guideline: BDD

Documente comportamentos observáveis do sistema como cenários BDD em `docs/features/<modulo>/bdd.md`. Cenários
descrevem o que o sistema faz visto de fora — não como faz internamente.

## Quando rodar

Crie ou atualize um doc BDD sempre que:
- Uma regra de negócio é introduzida ou muda
- Um contrato de API, política de autorização ou regra de validação de dados muda
- Um fluxo técnico transversal (auth, multi-tenancy, pipeline de importação) muda
- Uma nova área de domínio é introduzida

**Quando NÃO usar:** CRUD rotineiro sem invariantes ou regras especiais. Se todo campo é opcional e qualquer valor é
aceito, não há nada comportamental a documentar.

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

Um `bdd.md` por módulo, dentro da pasta do módulo:

```
docs/features/
  auth/
    bdd.md
  school-resolution/
    bdd.md
  payments/
    bdd.md                    # arquivo único enquanto couber
    bdd/                      # vira pasta quando passa de 3 unidades distintas
      checkout.md
      refunds.md
      subscription-billing.md
```

**Quebre em `bdd/` quando** o módulo cresce para 3 ou mais unidades de comportamento que um dev consultaria de forma
independente. Nomeie os arquivos internos pelo comportamento específico (`checkout.md`, não `payments-checkout.md` — a
pasta já fornece o namespace). Junte quando os cenários são finos demais para existirem sozinhos.

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

Use o idioma do projeto: Dado/Quando/Então ou Given/When/Then, nunca misturados.

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

## Rastreabilidade Cenário ↔ Teste

Todo cenário documentado tem um teste que o exercita. Um cenário sem teste é uma afirmação não verificada sobre o
sistema.

**Convenção:** o nome do teste repete o nome do cenário, e o arquivo/suíte de teste corresponde ao arquivo BDD.

```
docs/features/student-management/bdd.md   →  suíte "Student Management"
  #### Cenário: Matrícula duplicada na mesma escola
                    ↓
  it("matrícula duplicada na mesma escola", ...)
```

Se o projeto já tem outra convenção de nomes de teste, siga a do projeto — o que importa é que dê para ir do cenário ao
teste (e vice-versa) sem adivinhar. Ferramenta de BDD executável (Cucumber, Behave, SpecFlow) é opcional: teste comum
com nome espelhado cumpre o papel.

O teste deve seguir a estrutura do cenário: `Dado` → setup, `Quando` → a ação, `Então`/`E` → as asserções. Uma
asserção por `Então`/`E`.

### Ao validar doc contra teste

Percorra o arquivo BDD e, para cada cenário, localize o teste:

| Situação | O que fazer |
|---|---|
| Cenário sem teste | Escreva o teste. Se ele falhar, o sistema não faz o que a doc afirma — decida se é bug ou doc desatualizada |
| Teste sem cenário | Se cobre comportamento observável, documente o cenário; se cobre detalhe interno, deixe fora do BDD |
| Cenário e teste discordam | Verifique o comportamento real no código antes de mudar qualquer um dos dois |
| Cenário que ninguém pretende testar | Remova o cenário — o BDD documenta comportamento verificável, não intenção |

**Nunca** ajuste o teste para passar sem antes decidir qual lado está errado. Um teste alinhado a uma doc errada só
torna o erro permanente.

## Mantendo os Docs Atualizados

Ao modificar qualquer comportamento, localize o cenário correspondente e:

1. **Atualize** — se o comportamento mudou
2. **Adicione** — se é comportamento novo sem cenário existente
3. **Remova** — se o comportamento foi eliminado

Docs BDD devem refletir o **comportamento atual real** do sistema — não o comportamento desejado ou histórico.
