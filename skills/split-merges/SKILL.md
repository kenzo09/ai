---
name: split-merges
description: Use when a feature branch (or a set of sibling-repo branches sharing one ticket) grew too large to review as one merge request and must be split into smaller, independently mergeable MRs, or when a previous split is in progress and the next slice must be cut. Triggers on "quebrar em MRs menores", "separar esse WIP", "dividir a branch", "MR grande demais", "split this branch", "o diff está gigante", and on any diff stat with hundreds of files against the base branch. Do not use for a small single-topic branch; open the MR directly.
---

# Dividir branch grande em MRs pequenos

Um WIP grande vira uma sequência de MRs que cada um compila, passa nos testes e pode ser revisado
e revertido sozinho. O produto desta skill é um **handoff** (`assets/handoff-template.md`) que
outro agente ou pessoa pega e executa sem refazer a análise. Escreva-o antes de cortar qualquer coisa.

**Princípio central:** mapear dependências primeiro, cortar depois. Cada MR nasce de uma worktree
limpa da branch base, recebe só os arquivos do seu tema e é verificado por inteiro antes do próximo.

## Processo

### 1. Medir antes de opinar

Por repositório envolvido:

```bash
git fetch origin <base>
git log --oneline origin/<base>..HEAD | wc -l          # commits à frente
git log --oneline HEAD..origin/<base> | wc -l          # commits atrás (drift da base)
git diff --stat origin/<base>...HEAD | tail -1
git show --stat --format='%h %s' <cada commit>          # quão temático é cada um
```

Descubra repositórios irmãos com a mesma branch. Uma mudança que atravessa dois repos é **um** MR
lógico, com o mesmo nome de branch nos dois.

### 2. Decidir a mecânica: cherry-pick ou recomposição

- Commits limpos, um tema cada → `git cherry-pick` na ordem.
- Commits entrelaçados (o comum) → **recompor a partir do estado final**: copiar os arquivos do
  tema com `git checkout <branch-wip> -- <paths>` para a worktree do MR. Registre a decisão no handoff.

### 3. Mapear temas e dependências

- Agrupe os arquivos do diff por tema (pasta nova, módulo movido, migration, feature de tela).
- Para cada pacote/módulo novo, liste o que ele importa dos outros temas (`grep` de imports). O grafo
  de imports define a ordem mínima.
- Liste os **arquivos tangenciados**: os que carregam hunks de mais de um tema (composition root,
  registro de rotas, locales, docs de visão geral, lockfile, migration compartilhada). Cada um
  precisa de um plano de "só o hunk do MR".
- Procure **quebras cruzadas**: contrato removido num repo que o outro ainda consome, endpoint
  renomeado, tipo compartilhado que mudou. Elas fixam a ordem de merge e deploy entre repos. Quando
  a única saída é código que **não existe no WIP** (adaptador de compatibilidade, endpoint mantido
  como projeção), isso entra no escopo do MR como decisão marcada para quem pediu, não como surpresa.

### 4. Verificar o drift da base

A base andou desde o fork. Confira, no mínimo:

- **Migrations**: numeração colide com algo novo na base? Uma migration do WIP mistura temas?
  Cada MR leva migration própria, renumerada depois da última da base, com `down` só do seu tema.
- **Arquivos que o merge da base "desfez"**: `git diff origin/<base> -- <arquivo>` em arquivos do
  diff que não pertencem a nenhum tema; deleções grandes de teste são suspeitas.
- **Arquivos gerados** (lockfile, snapshots, specs gerados): só entram no MR que causa a mudança.

### 5. Ordenar e cortar

1. A dependência decide a ordem mínima; entre independentes, primeiro refactors do que já existe
   na base, depois features novas.
2. Corte grosso: um MR precisa passar nos cinco critérios (build, testes, sem quebra acidental,
   revertível sozinho, validável por quem pediu). Se um corte não passa, junte com o vizinho.
3. Dê a cada MR um sufixo breve (`feature/<TICKET>-<sufixo>`), o(s) repo(s), o escopo por arquivo,
   de quem depende e como o time confere que está de pé.
4. O que sobrou sem tema (chore, gitignore, fix não relacionado) vira lista de **sobras** com destino
   sugerido, nunca fica implícito.

### 6. Escrever o handoff

Use `assets/handoff-template.md`. Salve em `docs/handoff/` (ou onde o repo guarda handoffs) e
garanta que o caminho está no `.gitignore` quando for artefato de planejamento. Idioma: o do repo
para handoffs (pt-BR por padrão). O handoff referencia commits, diffs e outros docs por caminho ou
hash; não repete o que já está neles.

### 7. Executar o primeiro MR e realimentar o handoff

O primeiro corte prova a receita. Depois dele, preencha no handoff as seções **Estado**,
**Receita que funcionou** e **Armadilhas encontradas** com o que de fato aconteceu (comandos exatos,
colisões, ajustes manuais). Cada MR seguinte atualiza o Estado com o ponto exato em que parou:
só em worktree, pushado, MR aberto (link), mergeado. Um MR grande dentro da sequência
pode ganhar handoff próprio, linkado na tabela.

## Receita por MR

```bash
git worktree add <dir-worktrees>/<sufixo> -b feature/<TICKET>-<sufixo> origin/<base>
cd <dir-worktrees>/<sufixo>
git checkout <branch-wip> -- <dirs inteiros e arquivos novos do tema>
git rm -r <o que o tema remove>
git show <branch-wip>:<path> > <novo-path>           # arquivo que muda de nome
# arquivos tangenciados: aplicar só os hunks do tema com replace exato (uma ocorrência), não git apply parcial
# build + testes do repo (inteiro no modo rápido, completo nos pacotes tocados)
git add -A && git status --short                     # revisar; commit só com autorização de quem pediu
```

Worktree em vez de `checkout -b` no lugar: o WIP original fica intacto para consulta enquanto
o MR é montado, e dois MRs podem ser preparados em paralelo.

## Erros comuns

| Erro | Correção |
|---|---|
| Uma sequência por repositório (A1..A7, C1..C6) | Uma tabela só; mudança multi-repo é uma linha com o mesmo nome de branch nos repos |
| Handoff de 300+ linhas em prosa | Tabela de MRs + escopo detalhado por MR; prosa só onde há decisão |
| Sem seção de Estado | Quem retoma precisa saber o que já foi mergeado, aberto, ou está em worktree |
| Cherry-pick de commit "refactor" | Recompor a partir do estado final; o commit mistura temas |
| Planejar sem medir o drift da base | Numeração de migration e testes desfeitos só aparecem comparando com `origin/<base>` atual |
| Migration do WIP levada inteira no primeiro MR que precisa dela | Recortar: uma migration por tema, renumerada |
| Arquivo tangenciado levado inteiro | Só o hunk do tema; o resto volta no MR dono |
| Sobras espalhadas pelos MRs | Seção própria com destino explícito |
