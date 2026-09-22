# ai-toolkit

Toolkit pessoal de configuração para o Claude Code. Agents, skills e regras que uso na maioria dos meus projetos, pra manter o mesmo comportamento consistente em qualquer repo onde eu instalar.

## Estrutura

```
agents/    # personas dedicadas para tarefas específicas (review e execução de simplificação)
rules/     # regras que valem para qualquer código, independente de linguagem ou framework
skills/    # skills reutilizáveis (docs vivas, evidência, briefing visual, split de MR, import de config)
etc/       # configs auxiliares que não são do Claude Code (lint, statusline)
CLAUDE.md  # diretrizes gerais de comportamento do agente
```

## Como usar num projeto

Duas formas de trazer isso pra um projeto:

1. **Manual**: copie `agents/`, `rules/`, `skills/` e `CLAUDE.md` para dentro do `.claude/` do projeto alvo.
2. **Via skill**: de dentro do projeto alvo, use a skill `import-claude-config` (deste próprio repo) apontando para `kenzo09/ai`. Como o layout aqui não segue o padrão `.claude/` (as pastas ficam na raiz), rode com `subpath` igual a `.`; veja a seção "Layouts fora do padrão" do `SKILL.md` da própria skill.

## Agents

| Agent | Modelo | Papel |
|---|---|---|
| `code-review-planner` | opus | Review focado só em over-engineering (não em correção nem segurança). Não aplica nada: produz um handoff em `docs/handoff/` com os itens verificados e classificados em Simples/Médio/Complexo |
| `code-review-executor` | sonnet | Aplica um handoff de simplificação ao código, na granularidade pedida, e deixa o handoff atualizado pra próxima execução saber o que já foi feito |

Os dois são complementares e nenhum faz o papel do outro: o planner escreve a lista, o executor executa.

## Rules

- **`documentation.md`**: doc enxuta que cobre só arquitetura, integrações, capacidades, regras de negócio core, peças críticas e decisões com tradeoff real; comportamento se prova com teste, não com prosa; diagrama como texto (mermaid) por padrão, binário só com LFS configurado; doc reflete o estado esperado do sistema, então bugfix não gera doc.
- **`checkpoints.md`**: feature média/complexa entregue em checkpoints funcionais: build e testes verdes, nada quebrado, revertível isoladamente e validável à mão pelo usuário. Decide **onde o trabalho para**; a skill `parallel-batches` decide em que ordem ele corre.
- **`testing.md`**: suíte enxuta em que falha vermelha significa "o produto quebrou"; E2E primeiro, integração quando a borda não é alcançável, unidade só para caso crítico inalcançável de fora; cobertura não é critério; deletar teste micro é contribuição; o teste é a especificação do comportamento.

## Skills

| Skill | Quando usar |
|---|---|
| `handoff` | Compactar a conversa atual num documento de handoff pra outro agente continuar |
| `import-claude-config` | Puxar o `.claude/` de um repo público do GitHub (skills, agents, rules, CLAUDE.md) pro projeto atual |
| `live-docs` | Skill central de documentação: cria e mantém só a doc que se paga (arquitetura, PRD, ADR), verificada contra o código. Guidelines por tipo em `references/`. Aceita argumento pra focar num tipo: `/live-docs architecture` |
| `parallel-batches` | Executar um plano já aprovado com o máximo de subagents ao mesmo tempo: mapa de dependências, lotes paralelos, briefs de escopo fechado e convergência por lote. Entra depois do `superpowers:writing-plans` e substitui o loop serial do `subagent-driven-development` |
| `playwright-skill` | Automação de browser com Playwright: detecta o dev server, escreve o script e roda (screenshot, formulário, login, responsividade, links) |
| `split-merges` | Quebrar uma branch (ou branches irmãs de um ticket) grande demais em MRs pequenos e independentes: mapeia dependências, ordena os cortes e gera o handoff em `docs/handoff/` que outro agente executa. Template em `assets/` |
| `test-evidence` | Capturar evidência visual (Playwright, Swagger, Postman, DevTools, curl) antes de declarar uma entrega pronta, com redação de dados sensíveis |
| `visual-briefing` | Explicar um módulo, feature, branch ou sistema (qualquer linguagem ou arquitetura) numa página HTML visual, com lente Negócio/Técnico. Artifact no Claude Code, `.html` nos outros harnesses. Template em `assets/` |

## etc

Configs que não são do Claude Code e não entram no `.claude/` do projeto:

- **`.golangci.yml`**: configuração de lint para projetos Go.
- **`ccstatusline-config.json`**: configuração da statusline do Claude Code.

## CLAUDE.md

Define o idioma de cada artefato pelo **tipo do artefato**, nunca pelo idioma da solicitação ou do código: chat, specs e handoffs em pt-BR; plans, commits e código em en-US. Importa `docs/README.md` para as diretrizes de documentação do projeto alvo.
