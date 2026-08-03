# ai-toolkit

Toolkit pessoal de configuração para o Claude Code. Agents, skills e regras de design que uso na maioria dos meus projetos, pra manter o mesmo comportamento consistente em qualquer repo onde eu instalar.

## Estrutura

```
agents/    # personas dedicadas para tarefas específicas (docs, arquitetura, spec)
rules/     # regras de design que valem para qualquer código, independente de linguagem
skills/    # skills reutilizáveis (import de config, docs vivas, BDD)
CLAUDE.md  # diretrizes gerais de comportamento do agente
```

## Como usar num projeto

Duas formas de trazer isso pra um projeto:

1. **Manual** — copie `agents/`, `rules/`, `skills/` e `CLAUDE.md` para dentro do `.claude/` do projeto alvo.
2. **Via skill** — de dentro do projeto alvo, use a skill `import-claude-config` (deste próprio repo) apontando para `kenzo09/ai`. Como o layout aqui não segue o padrão `.claude/` (as pastas ficam na raiz), rode com `subpath` vazio — veja a seção "Non-standard layouts" do `SKILL.md` da própria skill.

## Agents

| Agent | Persona | Output |
|---|---|---|
| `overview` | Especialista em Documentação Técnica / Arquiteto Sênior | `docs/OVERVIEW.md` — Design Doc completo |
| `design` | Arquiteto de Soluções Principal | `docs/ARCHITECTURE.md` — diagramas Mermaid (flowchart, sequence, ERD, C4, state) |
| `spec` | Analista de Sistemas / Engenheiro de Requisitos | `docs/specs/[modulo].md` — regras de negócio + cenários BDD |
| `api-docs` | Arquiteto de APIs / Technical Writer | `docs/API_REFERENCE.md` — spec de endpoints REST |

Todos seguem o mesmo protocolo: entrevistam o desenvolvedor antes de gerar o artefato final, não geram nada enquanto faltar informação crítica.

## Rules

- **`design-principle.md`** — KISS, YAGNI, Responsabilidade Única e Early Return (guard clauses no topo da função, sem `else` desnecessário, sem cadeia de `if/else if`).
- **`documentation.md`** — toda feature nova precisa de doc mínima; bugfix só atualiza a doc se o comportamento documentado mudou (não quando a doc já previa o certo e só o código estava errado).
- **`task-breakdown.md`** — feature média/complexa entregue em checkpoints funcionais: build e testes verdes, nada quebrado, revertível isoladamente e validável à mão pelo usuário.
- **`testing.md`** — fluxos críticos de negócio precisam ser fáceis de testar; priorizar E2E nos critérios de aceite do produto, unidade só onde compensa, sem inflar a suíte.

## Skills

| Skill | Quando usar |
|---|---|
| `import-claude-config` | Puxar o `.claude/` de um repo público do GitHub (skills, agents, rules, CLAUDE.md) pro projeto atual |
| `bdd-docs` | Documentar comportamentos observáveis em BDD sempre que uma regra de negócio, autorização ou fluxo técnico muda |
| `live-docs` | Converter specs/plans/issues em documentação viva (PRD, ADR, BDD, reference) fiel ao código atual, não à intenção original |

## CLAUDE.md

Diretrizes gerais de comportamento — simplicidade por padrão, assumir em vez de travar em ambiguidade, mudanças cirúrgicas, critério verificável — e a regra de sempre responder em pt-BR. Feito pra funcionar sozinho, mesmo em projetos sem plugins extras instalados.
