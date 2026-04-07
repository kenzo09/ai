# Design Principles

These principles apply to all code regardless of language, framework, or paradigm.

## KISS — Keep It Simple, Stupid

Prefer the simplest solution that correctly solves the problem.

- **DO**: Choose straightforward implementations over clever ones
- **DO**: If two solutions work, pick the one easier to read and reason about
- **DON'T**: Add abstraction layers, patterns, or indirection without a concrete, present need
- **DON'T**: Over-engineer for hypothetical future requirements

## YAGNI — You Aren't Gonna Need It

Only implement what is required **right now**.

- **DO**: Implement features when they are explicitly needed
- **DON'T**: Add hooks, flags, extension points, or generalization based on speculation
- **DON'T**: Build for "maybe later" — the future requirement may never come, or arrive differently

## SOLID Principles

### Single Responsibility
Each function, class, or module must have **one clear purpose** and one reason to change.

### Open/Closed
Entities should be **open for extension, closed for modification**.  
Extend behavior by adding new code, not by changing existing stable code.

### Dependency Inversion
High-level modules must not depend on low-level modules.  
Both must depend on **abstractions** (interfaces/contracts), not concrete implementations.

## Fail Fast

Validate preconditions and detect errors **as early as possible**.  
Raise or surface errors immediately when an invalid state is detected — do not defer or silently swallow failures.
