# Guia de Documentação BDD

## Quando usar

Crie ou atualize um arquivo em `docs/behavior/` sempre que:
- Um comportamento core do sistema for adicionado ou modificado
- A lógica de um motor (`query_engine.go`, `mutation_engine.go`, `pipeline.go`) mudar
- Um hook built-in tiver seu comportamento alterado
- Uma nova capability for introduzida no YAML ou na infraestrutura

**Um arquivo por funcionalidade core.** Não crie docs por entidade de negócio; documente o comportamento genérico do motor.

## Estrutura Canônica

```markdown
# <Nome da Capability>

## Visão Geral

Uma ou duas frases descrevendo o que essa funcionalidade faz e qual problema resolve.

## Comportamentos

---

### <Nome do Comportamento>

Descrição em prosa do comportamento. Inclua as regras invariantes aqui.

**Regras:**
- Regra objetiva 1
- Regra objetiva 2

#### Cenário: <Nome do Cenário>
**Dado** <pré-condição ou estado inicial>
**Quando** <ação ou evento disparador>
**Então** <resultado esperado>
**E** <resultado adicional, se necessário>
```

## Regras de Escrita

| Elemento | Regra |
|---|---|
| Título do arquivo | kebab-case, corresponde ao componente arquitetural (`query-engine.md`, `hook-pipeline.md`) |
| Seção `### Comportamento` | Agrupa cenários relacionados sob um mesmo aspecto funcional |
| Palavra `Dado` | Estado inicial ou pré-condição que contextualiza o cenário |
| Palavra `Quando` | A ação ou evento que dispara o comportamento |
| Palavra `Então` | O resultado observável esperado |
| Conectivo `E` | Resultado adicional — não use para repetir ou reformular o `Então` |
| Negrito nos conectivos | Sempre `**Dado**`, `**Quando**`, `**Então**`, `**E**` |
| Tom | Objetivo, sem jargão. Legível por qualquer desenvolvedor sem conhecer o código |
| Escopo | Comportamento observável externamente — evite detalhar implementação interna |

## Exemplo Canônico

Extraído de `docs/behavior/query-engine.md`:

```markdown
### Filtragem por Operadores

Campos escalares e campos de relacionamento aceitam filtros com operadores tipados.

**Operadores suportados:** `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `in`, `isNull`

#### Cenário: Filtro com eq
**Dado** registros com diferentes valores de `status`
**Quando** o filtro `{ status: { eq: "ATIVO" } }` é aplicado
**Então** apenas registros com `status = "ATIVO"` são retornados

#### Cenário: Filtro com isNull
**Dado** registros onde alguns têm `deletedAt` nulo e outros não
**Quando** o filtro `{ deletedAt: { isNull: true } }` é aplicado
**Então** apenas registros com `deletedAt IS NULL` são retornados
```

## Quando Atualizar

Ao modificar qualquer comportamento core, localize o cenário correspondente no doc BDD e:

1. **Atualize** o cenário se o comportamento mudou
2. **Adicione** um novo cenário se é um comportamento novo
3. **Remova** cenários de comportamentos que foram eliminados

Os docs BDD devem sempre refletir o comportamento real do sistema — não o comportamento desejado ou histórico.
