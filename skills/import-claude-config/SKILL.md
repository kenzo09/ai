---
name: import-claude-config
description: Use when the user gives a public GitHub repo URL and wants its .claude/ config (skills, agents, hooks, rules, CLAUDE.md) installed or merged into the current project
---

# Importando Config do Claude a Partir do GitHub

## Visão Geral

Busca a árvore do diretório `.claude/` de um repositório público do GitHub via GitHub REST API (sem `git clone`, sem baixar histórico git local) e reporta cada arquivo como NEW, IDENTICAL, EOL-ONLY ou CONFLICT comparando com o `.claude/` do projeto atual. Você então aplica as mudanças, perguntando ao usuário antes de sobrescrever qualquer coisa.

**O destino é sempre o `.claude/` do projeto em que você está** — o diretório de trabalho atual. Nunca `~/.claude/` nem qualquer config global. O `fetch_claude_config.py` recusa (exit 2) um `target_dir` que resolva fora do cwd; se o usuário quiser instalar global, ele precisa pedir isso explicitamente, e aí a cópia é feita por você fora do script.

Os scripts usam apenas a stdlib do Python (`urllib`, sem dependência de `curl`/`bash`/`mktemp`), então rodam da mesma forma em Linux, macOS e Windows. Invoque com `python3`; se não resolver (comum no Windows), use `python`.

O script nunca escreve dentro do diretório `.claude/` real — ele só baixa para um diretório temporário de staging e reporta. Copiar para o lugar definitivo é um passo separado e deliberado, para que conflitos nunca sejam sobrescritos silenciosamente.

## Quando Usar

- O usuário cola/nomeia um repositório público do GitHub ("owner/repo" ou URL completa) e pede para trazer as skills, agents, hooks, rules ou CLAUDE.md dele.
- O usuário quer sincronizar/atualizar um setup `.claude/` local existente a partir de um repositório que acompanha.

Não serve para: repositórios privados que exigem auth além de um `GITHUB_TOKEN` pessoal, nem para instalar config global em `~/.claude/`.

Repos que não usam o layout `.claude/` **são suportados** — veja Layouts fora do padrão abaixo.

## Workflow

1. **Interprete a entrada.** Normalize para `owner/repo`. Remova `https://github.com/` se receber a URL completa. Pergunte ao usuário apenas se a string do repositório for genuinamente ambígua.

2. **Liste o que está disponível antes de baixar qualquer coisa:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/list_claude_tree.py <owner/repo> [ref] [subpath]
   ```
   - `ref` — deixe vazio (`""`) para resolver automaticamente a branch default do repositório.
   - `subpath` — default é `.claude`, que normalmente cobre CLAUDE.md, skills/, agents/, hooks/ e rules/ numa listagem só (todos ficam aninhados abaixo dele no layout padrão). Passe `"."` para listar a **raiz do repo** — use isso quando `.claude/` vier vazio. Passe `"."` e não `"/"`: o Git Bash no Windows reescreve um `/` sozinho no path de instalação do Git.

   Isso imprime cada entrada de primeiro nível abaixo do subpath (ex.: `DIR .claude/skills/ (7 files)`) com os filhos imediatos indentados (ex.: nomes individuais de skills, arquivos de agents). Se reportar "No files found", veja Layouts fora do padrão abaixo.

3. **Pergunte ao usuário o que importar** — tudo, ou entradas específicas da listagem (ex.: "só as skills `foo` e `bar`, e o CLAUDE.md" vs "tudo"). Não assuma "importar tudo" por default; a listagem existe justamente para o usuário escolher.

4. **Rode o script de fetch com os paths selecionados:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/fetch_claude_config.py <owner/repo> [ref] [root_subpath] [target_dir] [selected...]
   ```
   - `root_subpath` — mesmo valor usado em `subpath` no passo 2 (default `.claude`).
   - `target_dir` — default `.claude`. **Sempre relativo, sempre dentro do projeto atual**; rode a partir da raiz do projeto. Path que resolva fora do cwd é recusado com exit 2 — se isso acontecer, você errou o destino, não force com path absoluto.
   - `selected...` — um ou mais paths da listagem que o usuário escolheu (ex.: `.claude/skills/foo .claude/CLAUDE.md`). Omita completamente para importar tudo abaixo de `root_subpath`.

   Defina `GITHUB_TOKEN` no ambiente antes se bater no rate limit não autenticado do GitHub (60 req/h).

5. **Leia o relatório.** A saída termina com linhas como:
   ```
   NEW       skills/foo/SKILL.md
   CONFLICT  agents/bar.md
   IDENTICAL rules/baz.md
   EOL-ONLY  scripts/qux.py
   STAGING_DIR=/tmp/tmp.XXXXXX
   ```
   | Status | O que fazer |
   |---|---|
   | `NEW` | Copiar. Sem perguntar. |
   | `IDENTICAL` | Nada — já é igual byte a byte. |
   | `EOL-ONLY` | Nada — mesmo conteúdo, só CRLF vs LF. Não é conflito, não pergunte, não copie. |
   | `CONFLICT` | Diferença real de conteúdo → passo 7. |

6. **Copie só as entradas NEW**, de `STAGING_DIR/<root_subpath>/<path>` para `target_dir/<path>`. Não precisa perguntar — não há nada a perder. Use `shutil.copy` num `python -c` — **`copy`, não `copyfile`**: o `copyfile` descarta o bit de execução e um hook importado deixa de rodar no Linux/macOS. O que não serve é comando de cópia específico de shell (`cp`, `copy`, `robocopy`), que quebra a portabilidade entre SOs. Para arquivos grandes prefira a cópia via stdlib a ler+escrever, que gasta contexto sem motivo.

7. **Para todo CONFLICT, pergunte ao usuário antes de mexer** — mostre o path e ofereça: sobrescrever com a versão remota, manter a versão local, mesclar as duas, ou ver um diff primeiro (compare `STAGING_DIR/<root_subpath>/<path>` com `target_dir/<path>`). Nunca sobrescreva conflitos em lote sem confirmação por arquivo (ou um "sobrescreve tudo" explícito). Mostre o diff junto da pergunta quando o arquivo for pequeno — poupa uma ida e volta.

8. **Limpeza:** delete `STAGING_DIR` depois que tudo for aplicado (é um diretório temporário do SO de qualquer forma — seguro deixar se deletar for inconveniente na plataforma atual).

## Layouts fora do padrão

Se o passo 2 reportar "No files found under .claude/", o repo não usa o layout padrão — em geral tem `skills/`, `rules/`, `CLAUDE.md` na raiz em vez de aninhados sob `.claude/`.

1. Rode a listagem de novo com `subpath="."` para ver a raiz do repo.
2. Mostre o que existe e pergunte o que importar (passo 3 continua valendo).
3. **Rode o fetch uma vez por subpath**, sempre mapeando para dentro do `.claude/` do projeto:

   | `root_subpath` (repo) | `target_dir` (projeto) |
   |---|---|
   | `skills` | `.claude/skills` |
   | `rules` | `.claude/rules` |
   | `agents` | `.claude/agents` |
   | `hooks` | `.claude/hooks` |
   | `CLAUDE.md` | `.claude` |

   A regra: `target_dir` é `.claude/` + o mesmo nome do subpath. Exceção são arquivos soltos na raiz (`CLAUDE.md`), onde `target_dir` é só `.claude` — o script já resolve o nome do arquivo.

Skills que o repo tem mas já estão instaladas globais e idênticas: não duplique no projeto, só diga que foram ignoradas.

## Depois de aplicar

Duas coisas que fazem o import parecer pronto sem estar — verifique e reporte em uma linha cada:

- **`rules/*.md` não carregam sozinhos.** Só entram em contexto se algum `CLAUDE.md` referenciar com `@rules/...`. Se importou rules, ofereça adicionar os imports.
- **`.claude/` num repo git.** Confira se está no `.gitignore`; se não estiver, avise que os arquivos vão aparecer como untracked e deixe o usuário decidir entre commitar (config do time) ou ignorar (config pessoal).

## Erros Comuns

| Erro | Por que está errado |
|---|---|
| Usar `git clone` em vez do script | Baixa o histórico completo e tudo mais do repositório; o script busca só a subárvore relevante via GitHub API + URLs raw dos arquivos. |
| Rodar o fetch direto, sem listar primeiro | Tira do usuário a chance de escolher um subconjunto; sempre rode `list_claude_tree.py` e pergunte antes do `fetch_claude_config.py`. |
| Importar para `~/.claude/` em vez do projeto | Esta skill instala no projeto atual. O `~/.claude/` já existir e o `.claude/` do projeto não existir **não** é motivo pra mudar de destino — o script cria o que faltar. Só vá pro global se o usuário pedir com essas palavras. |
| Passar `target_dir` absoluto pra contornar o exit 2 | O exit 2 é o script te avisando que o destino está errado. Corrija o destino, não o contorne. |
| Sobrescrever arquivos CONFLICT automaticamente | Destrói edições locais sem volta. Sempre pergunte primeiro. |
| Tratar `EOL-ONLY` como conflito | Só CRLF vs LF; o conteúdo é o mesmo. Perguntar sobre isso gasta o tempo do usuário à toa. |
| Assumir que existe uma pasta `.claude/` | Alguns repositórios usam layout próprio (veja Layouts fora do padrão) — confira a saída do script antes de assumir. |
| Esquecer de limpar o `STAGING_DIR` | Deixa diretórios temporários para trás; delete depois de aplicar as mudanças (fica no temp do SO, então deixar não é danoso, só desleixo). |
