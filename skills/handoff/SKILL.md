---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Escreva um documento de handoff resumindo a conversa atual para que um agente novo possa continuar o trabalho. Salve em `docs/handoff/` na raiz do projeto (crie a pasta se não existir), com nome de arquivo descritivo. Garanta que `docs/handoff/` esteja no `.gitignore` — se não estiver, adicione (criando o `.gitignore` caso não exista).

Inclua uma seção "skills sugeridas" no documento, nomeando quais skills o próximo agente deve invocar via ferramenta Skill.

Não duplique conteúdo já registrado em outros artefatos (specs, plans, ADRs, issues, commits, diffs). Referencie-os por caminho ou URL.

Redija qualquer informação sensível, como chaves de API, senhas ou dados pessoais identificáveis.

Se o usuário passar argumentos, trate-os como descrição do foco da próxima sessão e adapte o documento a isso.
