# Guideline: Reference Técnica

`docs/features/<modulo>/reference.md` — os contratos que desenvolvedores dependem. Curto, escaneável, verificado
contra o código atual.

**Audiência:** quem vai consumir ou manter o módulo. Ao contrário do PRD, aqui nome de código é obrigatório.

## Quando rodar

- Um endpoint, comando de CLI, evento ou assinatura pública mudou
- Uma env var foi adicionada, renomeada ou removida
- Um código/formato de erro mudou
- Auditoria: suspeita de que o reference lista contratos que já não existem

## O que entra

| Seção | Conteúdo |
|---|---|
| Interface pública | Endpoints, comandos, eventos publicados/consumidos, funções exportadas |
| Configuração | Env vars: nome exato, obrigatória ou não, default, o que acontece se faltar |
| Erros | Código/status, condição que dispara, mensagem |
| Pontos de manutenção | Onde mexer para o tipo de mudança mais comum neste módulo |

Nada de tutorial, nada de justificativa (isso é ADR), nada de cenário (isso é BDD).

## Verificação obrigatória

Cada linha do reference sai de uma leitura do código, não da spec:

- **Env vars:** confirme o nome exato nos arquivos de config do projeto (`.env*`, config loader, `CLAUDE.md`, README) e
  no ponto onde o código lê a variável. Nome de env var é o item que mais diverge entre spec e código.
- **Endpoints:** confirme rota, método e auth no handler, não no doc antigo.
- **Erros:** confirme código e mensagem no ponto onde o erro é levantado.

Contrato que você não localizou no código sai do doc — não fica com ressalva.

## Erros comuns

| Erro | Correção |
|---|---|
| Reference listando env vars desatualizadas | Verifique o nome no ponto de leitura do código |
| Copiar a assinatura que a spec propôs | Use a assinatura atual do código |
| Reference virando tutorial | Contrato, não guia de uso |
| Explicar por que o contrato é assim | Isso é ADR |
| Manter endpoint removido "por compatibilidade do doc" | Doc reflete o que existe hoje |
