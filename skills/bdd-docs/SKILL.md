---
name: bdd-documentation
description: Use when a behavior is added, modified, or removed — whether business logic, authorization rules, API contracts, or core technical flows. Also use when reviewing whether existing BDD docs reflect the current system after a code change.
---

# BDD Documentation

## Overview

Document observable system behaviors as BDD scenarios in `docs/bdd/`. One file per behavioral unit (component, flow, or domain). Scenarios describe what the system does from the outside — not how it does it internally.

## When to Use

Create or update a BDD doc whenever:
- A business rule is introduced or changes
- An API contract, authorization policy, or data validation rule changes
- A cross-cutting technical flow (auth, multi-tenancy, import pipeline) changes
- A new domain area is introduced

**When NOT to use:** Routine CRUD with no invariants or special rules. If every field is optional and any value is accepted, there is nothing behavioral to document.

## What to Document

Two types of content belong in BDD docs:

**Business behaviors** — rules visible to users and stakeholders:
- Validation rules (required fields, formats, uniqueness constraints)
- Authorization (who can do what, under what conditions)
- Domain invariants (e.g., enrollment number unique per school, not globally)
- Workflow rules (transactional creation of multiple records, partial success on import)

**Technical behaviors** — rules invisible to users but contractual for developers:
- Auth token flows (how a token from provider A becomes a valid token for system B)
- Tenant resolution (how the system determines which tenant a request belongs to)
- Fallback and default rules (what happens when a claim is missing)
- Error response contracts (which status code, which message, under which condition)

## File Organization

```
docs/bdd/
  auth-middleware.md          # Single-file domain
  school-resolution.md
  student-management.md
  payments/                   # Folder when a domain has 3+ distinct files
    checkout.md
    refunds.md
    subscription-billing.md
```

**Use a folder when** a domain grows to 3 or more files. Name the folder after the domain (`payments/`, `notifications/`, `access-control/`). Keep files inside named by the specific behavior (`checkout.md`, not `payments-checkout.md` — the folder provides the namespace).

**One file per behavioral unit.** Split when a file covers two distinct concepts that a developer would look up independently. Merge when scenarios are too thin to stand alone.

## Canonical Structure

```markdown
# <Component or Flow Name>

## Visão Geral

One or two sentences: what this does and what problem it solves.

## Comportamentos

---

### <Behavior Group Name>

Prose describing the behavior. State invariant rules here.

**Regras:**
- Objective rule 1
- Objective rule 2

#### Cenário: <Scenario Name>
**Dado** <precondition or initial state>
**Quando** <triggering action or event>
**Então** <expected observable result>
**E** <additional result, if needed>
```

## Writing Rules

| Element | Rule |
|---|---|
| Filename | kebab-case matching the behavioral unit |
| `### Behavior Group` | Groups related scenarios under one functional aspect |
| `**Dado**` | Initial state or precondition — sets the context |
| `**Quando**` | The action or event that triggers the behavior |
| `**Então**` | The observable expected result |
| `**E**` | Additional result — never repeat or rephrase `Então` |
| Bold connectives | Always bold: `**Dado**`, `**Quando**`, `**Então**`, `**E**` |
| Tone | Objective, jargon-free. Readable without knowing the code |
| Scope | Externally observable behavior — no implementation details |

## Canonical Example

```markdown
### Unicidade de Matrícula

O número de matrícula é único por escola, não globalmente. O mesmo número pode existir em escolas diferentes.

**Regras:**
- Se `enrollment_number` for informado, deve ser único dentro da escola
- `enrollment_number` é opcional; ausência não viola nenhuma regra

#### Cenário: Matrícula duplicada na mesma escola
**Dado** um aluno com matrícula "2024001" já cadastrado na escola A
**Quando** um novo aluno com matrícula "2024001" é cadastrado na escola A
**Então** retorna erro 409 "enrollment_number is already in use at this school"

#### Cenário: Mesma matrícula em escolas diferentes
**Dado** um aluno com matrícula "2024001" cadastrado na escola A
**Quando** um aluno com matrícula "2024001" é cadastrado na escola B
**Então** o cadastro é aceito normalmente
```

## Keeping Docs Current

When modifying any behavior, locate the corresponding scenario and:

1. **Update** — if the behavior changed
2. **Add** — if it is new behavior with no existing scenario
3. **Remove** — if the behavior was eliminated

BDD docs must reflect the system's **actual current behavior** — not desired or historical behavior.
