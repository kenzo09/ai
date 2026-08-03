# Guideline: ADR

`docs/adrs/NNN-<titulo>.md` — um ADR por decisão arquitetural. Documenta **por que** uma decisão não-óbvia foi tomada.

**Criar apenas quando:** a decisão tem tradeoffs reais e mantenedores futuros questionariam. Decisão óbvia ou sem
alternativa viável não é ADR.

**Numeração:** inteiros sequenciais, zero-padded em 3 dígitos (`001`, `002`, …). Antes de criar, liste `docs/adrs/`
para descobrir o próximo número — não assuma.

## Quando rodar

- Uma escolha de tecnologia, padrão ou limite arquitetural foi feita entre alternativas concorrentes
- Uma decisão anterior foi substituída → novo ADR + marca o antigo como `Substituído por ADR-XXX`
- Auditoria retroativa: existe no código uma decisão que ninguém consegue explicar

**Quando NÃO usar:** registro de o que foi planejado (isso é a spec), descrição de comportamento (BDD), ou contrato
técnico (reference).

## Template

```markdown
# ADR-NNN: <Título>

**Status:** Aceito | Substituído por ADR-XXX
**Data:** YYYY-MM-DD
**Feature:** <módulo>

## Contexto
Que situação forçou esta decisão?

## Decisão
O que foi decidido.

## Consequências
O que isso habilita, o que previne, o que dificulta.
```

## Regras

| Regra | Por quê |
|---|---|
| Um ADR por decisão, não por spec | Uma spec pode conter zero ou várias decisões |
| ADR nunca é reescrito, é substituído | O histórico de raciocínio é o valor do artefato |
| "Consequências" inclui o que ficou pior | ADR que só lista vantagens é justificativa, não registro |
| Contexto descreve a restrição, não a solução | Sem a força que motivou, a decisão parece arbitrária |
| Data é a da decisão, não a da escrita do doc | Migração retroativa usa a data do commit/spec original |

## Erros comuns

| Erro | Correção |
|---|---|
| Criar ADR para toda spec | Apenas decisões não-óbvias com tradeoffs reais |
| Editar um ADR aceito porque a decisão mudou | Crie um novo e marque o antigo como substituído |
| ADR sem alternativa descartada | Se não havia alternativa, não havia decisão |
| Duplicar número existente | Liste `docs/adrs/` antes de nomear o arquivo |
