# Template do handoff de divisão

Copie o esqueleto abaixo para `docs/handoff/<AAAA-MM-DD>-<ticket>-split-mrs.md`. O que está entre
`<>` é placeholder; os comentários `<!-- -->` dizem o que cada seção precisa carregar e saem do
arquivo final. Mantenha a ordem das seções: quem retoma lê Estado primeiro, depois a tabela.

Tamanho: a tabela de MRs cabe numa tela e concentra a decisão; o escopo detalhado cresce com o
número de arquivos tangenciados (um repo com poucos MRs fica em ~100 linhas, dois repos com sete MRs
em ~250). Prosa só onde há uma decisão a explicar.

---

```markdown
# Handoff — Separação do WIP `<branch>` em MRs pequenos

## Contexto

<!-- Uma frase: qual branch, quais repos, contra qual base. Depois a medida. -->

A branch `<branch>` (<repos>) acumulou um WIP grande contra `<base>`:

| Repo | Commits | Diff vs `origin/<base>` | Base à frente |
|---|---|---|---|
| `<repo-1>` | <n> (`<primeiro>`..`<último>`) | <n> arquivos, +<ins> / −<del> | <n> commits |
| `<repo-2>` | ... | ... | ... |

<!-- A decisão de mecânica e o motivo, em 2–3 linhas: cherry-pick ou recomposição pelo estado final. -->

Regras fixadas:

- Cada MR nasce de uma **worktree nova de `origin/<base>`**, em `<dir-worktrees>/<sufixo>`.
  Branch `<prefixo>/<TICKET>-<sufixo>`, sufixo breve.
- Mudança que envolve mais de um repo: worktree e branch **com o mesmo nome** em todos.
- Ordem: dependência primeiro; entre independentes, refactors do que já existe antes de features novas.
- <!-- Regras de commit/MR do repo: formato de mensagem, quem autoriza commit, label, target. -->

## Estado

<!-- Atualize a cada MR. Quem retoma lê isto primeiro. -->

### Feito

<!-- Um bloco por MR já cortado, com o ponto exato em que parou: só em worktree (não pushado),
     pushado, MR aberto (link), mergeado. Branch, hash do commit, escopo em 2–3 linhas (o detalhe
     está na mensagem de commit e no MR; não repita). Worktree ainda aberta ou já fechada. -->

### Pendente, na ordem proposta

| # | Sufixo | Repos | Escopo | Depende de |
|---|---|---|---|---|
| <n> | `<sufixo>` | <repos> | <o que entra, em uma linha; link para handoff próprio se houver> | <#s ou —> |

<!-- Uma linha por MR. Mudança multi-repo é UMA linha. A coluna "Depende de" cita só dependência
     real (import, contrato, migration) ou conflito de arquivo tangenciado, e diz qual. -->

### Sobras sem MR próprio

<!-- Chores, gitignore, lockfile, fix não relacionado, arquivo desfeito pelo merge da base.
     Cada item com destino sugerido: "junta no MR n", "MR mínimo próprio", "descartar". -->

- <item> — <destino e motivo em meia linha>

## Escopo detalhado por MR

<!-- Um parágrafo ou bloco de bullets por MR pendente: arquivos que nascem, que somem, que são
     tangenciados (e qual hunk levar), migration própria (nome e conteúdo), testes, docs, e a
     validação manual ("como o time confere que está de pé"). Mudança de comportamento observável
     ou breaking change vem marcada. Código que não existe no WIP mas o corte exige (adaptador de
     compatibilidade para o repo irmão) vem marcado como decisão para quem pediu. -->

**<n> — `<sufixo>` (<repos>).** <escopo>

## Receita para montar um MR

<!-- Comandos que valem para todos os MRs deste repo/stack. Depois do primeiro MR, substitua pelo
     que de fato funcionou, com os comandos exatos de build e teste. -->

1. `git fetch origin <base>` e `git worktree add <dir-worktrees>/<sufixo> -b <prefixo>/<TICKET>-<sufixo> origin/<base>` em cada repo envolvido.
2. `git checkout <branch-wip> -- <paths>` para o que é 100% do MR; `git rm -r` do que morre; `git show <branch-wip>:<path> > <path>` para arquivo que muda de nome.
3. Arquivos tangenciados: aplicar só os hunks do MR com substituição exata (uma ocorrência), não `git apply` parcial.
4. Docs e configs compartilhadas: cada MR acrescenta só a sua linha/exemplo.
5. Verificação: <comandos de build e teste do repo, rápido no todo e completo nos pacotes tocados>.
6. Revisar `git status`, commit conforme a regra do repo, push com `-u`, abrir MR contra `<base>`.

## Armadilhas encontradas

<!-- Preencha a partir do primeiro MR executado e a cada MR seguinte. Fato + como contornar,
     uma bullet por armadilha. Exemplos típicos: numeração de migration colidindo com a base,
     migration do WIP misturando temas, arquivo de i18n flat/desordenado, alias de build que um
     teste novo exige, helper que já entrou num MR anterior, teste que o merge da base desfez. -->

- **<armadilha>.** <o que aconteceu e como contornar>
```
