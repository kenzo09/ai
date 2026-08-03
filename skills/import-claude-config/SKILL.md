---
name: import-claude-config
description: Use when the user gives a public GitHub repo URL and wants its .claude/ config (skills, agents, hooks, rules, CLAUDE.md) installed or merged into the current project
---

# Importando Config do Claude a Partir do GitHub

## Visão Geral

Busca a árvore do diretório `.claude/` de um repositório público do GitHub via GitHub REST API (sem `git clone`, sem baixar histórico git local) e reporta cada arquivo como NEW, CONFLICT ou IDENTICAL comparando com o `.claude/` do projeto atual. Você então aplica as mudanças, perguntando ao usuário antes de sobrescrever qualquer coisa.

Os scripts usam apenas a stdlib do Python (`urllib`, sem dependência de `curl`/`bash`/`mktemp`), então rodam da mesma forma em Linux, macOS e Windows — em qualquer lugar onde `python3` (ou `python` no Windows, se `python3` não estiver no PATH) esteja disponível.

O script nunca escreve dentro do diretório `.claude/` real — ele só baixa para um diretório temporário de staging e reporta. Copiar para o lugar definitivo é um passo separado e deliberado, para que conflitos nunca sejam sobrescritos silenciosamente.

## Quando Usar

- O usuário cola/nomeia um repositório público do GitHub ("owner/repo" ou URL completa) e pede para trazer as skills, agents, hooks, rules ou CLAUDE.md dele.
- O usuário quer sincronizar/atualizar um setup `.claude/` local existente a partir de um repositório que acompanha.

Não serve para: repositórios privados que exigem auth além de um `GITHUB_TOKEN` pessoal, ou repositórios que não usam o layout `.claude/` (veja Layouts fora do padrão abaixo).

## Workflow

1. **Interprete a entrada.** Normalize para `owner/repo`. Remova `https://github.com/` se receber a URL completa. Pergunte ao usuário apenas se a string do repositório for genuinamente ambígua.

2. **Liste o que está disponível antes de baixar qualquer coisa:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/list_claude_tree.py <owner/repo> [ref] [subpath]
   ```
   (use `python` em vez de `python3` se for o que resolve na máquina atual, ex.: alguns setups Windows)
   - `ref` — deixe vazio (`""`) para resolver automaticamente a branch default do repositório.
   - `subpath` — default é `.claude`, que normalmente cobre CLAUDE.md, skills/, agents/, hooks/ e rules/ numa listagem só (todos ficam aninhados abaixo dele no layout padrão).

   Isso imprime cada entrada de primeiro nível abaixo do subpath (ex.: `DIR .claude/skills/ (7 files)`) com os filhos imediatos indentados (ex.: nomes individuais de skills, arquivos de agents). Se reportar "No files found", veja Layouts fora do padrão abaixo.

3. **Pergunte ao usuário o que importar** — tudo, ou entradas específicas da listagem (ex.: "só as skills `foo` e `bar`, e o CLAUDE.md" vs "tudo"). Não assuma "importar tudo" por default; a listagem existe justamente para o usuário escolher.

4. **Rode o script de fetch com os paths selecionados:**
   ```
   python3 ~/.claude/skills/import-claude-config/scripts/fetch_claude_config.py <owner/repo> [ref] [root_subpath] [target_dir] [selected...]
   ```
   - `root_subpath` — mesmo valor usado em `subpath` no passo 2 (default `.claude`).
   - `target_dir` — default é `./.claude` (o projeto atual). Rode a partir da raiz do projeto.
   - `selected...` — um ou mais paths da listagem que o usuário escolheu (ex.: `.claude/skills/foo .claude/CLAUDE.md`). Omita completamente para importar tudo abaixo de `root_subpath`.

   Defina `GITHUB_TOKEN` no ambiente antes se bater no rate limit não autenticado do GitHub (60 req/h).

5. **Leia o relatório.** A saída termina com linhas como:
   ```
   NEW       skills/foo/SKILL.md
   CONFLICT  agents/bar.md
   IDENTICAL rules/baz.md
   STAGING_DIR=/tmp/tmp.XXXXXX
   ```

6. **Aplique as entradas NEW e IDENTICAL** copiando direto de `STAGING_DIR/.claude/<path>` para `target_dir/<path>` (IDENTICAL não precisa de cópia, já é igual). Use suas ferramentas de arquivo (leia o arquivo em staging, escreva no path de destino) em vez de um comando de cópia específico de shell — assim o passo funciona igual em qualquer SO. Não precisa perguntar — não há nada a perder.

7. **Para todo CONFLICT, pergunte ao usuário antes de mexer** — mostre o path e ofereça: sobrescrever com a versão remota, manter a versão local, ou ver um diff primeiro (leia `STAGING_DIR/.claude/<path>` e `target_dir/<path>` e compare). Nunca sobrescreva conflitos em lote sem confirmação por arquivo (ou um "sobrescreve tudo" explícito).

8. **Limpeza:** delete `STAGING_DIR` depois que tudo for aplicado (é um diretório temporário do SO de qualquer forma — seguro deixar se deletar for inconveniente na plataforma atual).

## Layouts fora do padrão

Se o passo 2 reportar "No files found under .claude/", o repositório de origem pode não usar o layout padrão (ex.: `skills/`, `hooks/` no nível raiz em vez de aninhados sob `.claude/`). Não adivinhe — pergunte ao usuário qual(is) subpath(s) buscar, então rode o script uma vez por subpath com um `target_dir` correspondente (ex.: `subpath=skills`, `target_dir=.claude/skills`).

## Erros Comuns

| Erro | Por que está errado |
|---|---|
| Usar `git clone` em vez do script | Baixa o histórico completo e tudo mais do repositório; o script busca só a subárvore relevante via GitHub API + URLs raw dos arquivos. |
| Rodar o fetch direto, sem listar primeiro | Tira do usuário a chance de escolher um subconjunto; sempre rode `list_claude_tree.py` e pergunte antes do `fetch_claude_config.py`. |
| Sobrescrever arquivos CONFLICT automaticamente | Destrói edições locais sem volta. Sempre pergunte primeiro. |
| Assumir que existe uma pasta `.claude/` | Alguns repositórios usam layout próprio (veja Layouts fora do padrão) — confira a saída do script antes de assumir. |
| Esquecer de limpar o `STAGING_DIR` | Deixa diretórios temporários para trás; delete depois de aplicar as mudanças (fica no temp do SO, então deixar não é danoso, só desleixo). |
