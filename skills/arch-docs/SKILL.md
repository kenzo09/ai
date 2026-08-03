---
name: arch-docs
description: Use when a repository lacks a single macro architecture document, when someone new needs one page showing actors, internal components and external dependencies, or when an existing architecture overview may have drifted from the current code.
---

# Documentação de Arquitetura Macro

## Visão Geral

Produz **um artefato**: `docs/architecture/overview.md` — o sistema inteiro em uma página, um diagrama mais o mínimo de
texto ao redor.

**Princípio central:** toda aresta do diagrama e toda linha das tabelas sai de uma leitura do código. Integração que
você não encontrou no código não entra no desenho.

Este doc responde "o que é este sistema e de quem ele depende". Não responde "como implementar X" — isso é referência
técnica, outro artefato.

## Quando Usar

- O repositório não tem nenhuma visão macro do sistema
- Alguém precisa entender o sistema inteiro sem ler o código
- Uma nova integração externa, um novo datastore ou um novo ponto de entrada foi adicionado
- Suspeita de que o overview existente descreve um sistema que já não é o atual

**Não use para:** detalhar um módulo (isso é referência), registrar uma decisão (isso é ADR), ou descrever
comportamento observável (isso é BDD).

## Criar vs Atualizar

Antes de qualquer coisa, verifique se o artefato já existe.

| Estado | Ação |
|--------|------|
| Não existe | Cria com todas as seções obrigatórias |
| Existe | Verifica cada afirmação contra o código atual, corrige o que divergiu, **preserva seções extras que alguém adicionou** |

Ao atualizar, não reescreva o que já está correto. Mude o que está errado ou faltando e relate ao usuário, em uma
linha por item, o que divergia.

## Passos

### 1. Mapeie os pontos de entrada

Procure controllers, handlers de rota, consumers de fila, comandos de CLI, jobs agendados, handlers de webhook.
Cada um corresponde a um ator ou a uma aresta de entrada. Anote também qual autenticação cada um exige — atores
diferentes costumam entrar por portas diferentes.

### 2. Leia o composition root

O arquivo onde as dependências são registradas (DI container, factory de app, módulo de bootstrap) é o inventário mais
confiável de dependências externas. Ele revela com o que o sistema de fato se comunica — mais do que qualquer README.

### 3. Leia cada client de integração

Para cada dependência externa, abra a implementação do client e anote:

- transporte e endereço/rota/tópico
- política de retry, timeout, circuit breaker
- **o que acontece no erro** — propaga, devolve valor vazio, ou é suprimido

O tratamento de erro é o item que dá substância ao doc e o mais fácil de supor sem verificar. Se não localizou,
registre `não verificado` na tabela em vez de inferir.

### 4. Leia a configuração

Arquivos de config e variáveis de ambiente revelam dependências que o código esconde atrás de abstração, e mostram o
que muda entre ambientes.

### 5. Verifique antes de desenhar

Antes de escrever o diagrama, para cada aresta pretendida confirme que existe uma chamada no código. Aresta sem origem
verificada é removida, não desenhada com ressalva.

## Estrutura obrigatória do artefato

Nesta ordem, sem seções a mais nem a menos (seções extras só ao atualizar um doc que já as tinha):

1. **Título e essência** — um ou dois parágrafos: o que o sistema faz e a característica macro que define sua forma.
   Por exemplo: ausência de estado, orientação a eventos, datastore único, papel de proxy
2. **Diagrama** — um bloco mermaid, o centro do doc
3. **Componentes** — tabela do que roda dentro do limite do sistema
4. **Fluxo principal** — o caminho mais comum, em bloco de texto curto
5. **Dependências e o que acontece quando falham** — tabela de criticidade e comportamento na falha
6. **Pontos de atenção** — restrições e invariantes não óbvias que quebram o sistema quando violadas
7. **Links** — para os docs de detalhe

## Template

````markdown
# Arquitetura Macro

<Uma ou duas frases: o que o sistema faz.>

<Um parágrafo com a característica que define a forma do sistema e o que ela implica.>

```mermaid
flowchart LR
    %% ---------- Atores ----------
    <ator1>([<Nome><br/><qualificação>])
    <ator2>([<Nome>])

    %% ---------- Nosso sistema ----------
    subgraph sist["<Nome do Sistema>"]
        <comp1>[<Componente><br/><tecnologia>]
        <comp2>[<Componente><br/><responsabilidade>]
        <store>[(<Datastore><br/><o que guarda>)]
    end

    %% ---------- Externos ----------
    <ext1>[<Sistema Externo><br/><o que fornece>]
    <ext2>[<Sistema Externo><br/><o que fornece>]

    %% ---------- Integrações ----------
    <ator1> -->|<protocolo> <rota><br/><auth>| <comp1>
    <comp1> --> <comp2>
    <comp2> -->|<protocolo><br/><retry/timeout>| <ext1>
    <comp2> --> <store>
    <comp1> -.->|<chamada eventual>| <ext2>

    %% ---------- Estilos ----------
    classDef externo fill:#f5f5f5,stroke:#999,stroke-dasharray:4 3,color:#333
    classDef dados fill:#e8f0fe,stroke:#4285f4,color:#000
    classDef assinc fill:#fff4e5,stroke:#f59e0b,color:#000
    class <ext1>,<ext2> externo
    class <store> dados
```

## Componentes

| Componente | O que é | Nota |
|------------|---------|------|
| **<Nome>** | <uma linha> | <o detalhe não óbvio> |

## Fluxo principal

```
<ponto de entrada>
  → <passo>
  → <passo>
  → <resultado>
```

<Uma linha sobre o caminho alternativo relevante, se houver.>

## Dependências e o que acontece quando falham

| Dependência | Criticidade | Comportamento na falha |
|-------------|-------------|------------------------|
| **<Nome>** | <Crítica / Degradável / Necessária na inicialização> | <o que o código faz: retry, exceção, valor vazio> |

## Pontos de atenção

- **<Restrição ou invariante, em negrito.>** <Consequência de violá-la.>

---

<Links para os docs de detalhe.>
````

## Convenções do diagrama

| Elemento | Sintaxe | Uso |
|----------|---------|-----|
| Ator | `nome([Rótulo])` | Quem inicia uma interação |
| Componente | `nome[Rótulo]` | Unidade que roda dentro do sistema |
| Datastore | `nome[(Rótulo)]` | Banco, cache, bucket |
| Fila / tópico | `nome{{Rótulo}}` | Comunicação assíncrona |
| Aresta síncrona | `-->` | Chamada direta |
| Aresta eventual | `-.->` | Fallback, caminho de exceção, chamada condicional |

- `<br/>` na segunda linha do rótulo para tecnologia ou responsabilidade
- Label de aresta traz protocolo, rota/tópico e política (`retry 3x`, `timeout 2s`)
- Limite do sistema em `subgraph` — o que está dentro é responsabilidade da equipe; o que está fora, de terceiros
- `classDef externo` em tudo que está fora; `dados` em datastores; `assinc` em filas

## Limites

Um diagrama grande demais para caber na tela perde a função de comunicar. Se passar de ~15 nós, o desenho está no
nível errado: agrupe componentes internos ou mova detalhe para os docs de nível abaixo.

O doc inteiro cabe em uma leitura de poucos minutos. Ele aponta para o detalhe, não o contém.

## Erros comuns

| Erro | Correção |
|------|----------|
| Desenhar a arquitetura que o README descreve | O README pode estar desatualizado; a fonte é o código |
| Inferir uma integração pelo nome de um pacote | Confirme que existe chamada, não só dependência declarada |
| Supor o comportamento na falha | Leia o tratamento de erro; se não localizou, registre `não verificado` |
| Repetir na tabela de componentes o que o diagrama já diz | A tabela existe para o detalhe **não** óbvio no desenho |
| Detalhar um componente a ponto de se tornar doc de módulo | Isso é referência técnica, outro artefato |
| Reescrever o doc inteiro numa atualização | Corrija o que divergiu, preserve o resto |
| Diagrama com 30 nós | Agrupe ou desça de nível |

## Integração com outros docs

Este artefato é o topo. Abaixo dele:

- **Referência técnica** — contratos, config, pontos de manutenção
- **ADR** — por que uma decisão foi tomada
- **BDD** — comportamento observável

Ao criar ou atualizar o overview, adicione-o ao índice de documentação do repositório. Se o repositório usa a skill
`live-docs`, ela é quem organiza o resto da estrutura.
