# CLAUDE.md

Diretrizes de comportamento para reduzir erros comuns de LLM ao codificar. Mescle com instruções específicas do projeto conforme necessário.

## Idioma

Responda sempre em pt-BR, independentemente do idioma da pergunta, do código ou dos arquivos envolvidos.

## 1. Simplicidade primeiro

Código mínimo que resolve o problema. Nada especulativo.

- Sem abstrações para uso único, sem "flexibilidade" ou configuração que não foi pedida.
- Sem tratamento de erro para cenários impossíveis.
- Prefira reutilizar algo que já existe no projeto/linguagem/stdlib antes de escrever código novo.
- Se escreveu 200 linhas e dava pra ser 50, reescreva.

## 2. Suposição em vez de trava

Ambiguidade não trava o trabalho:

- Escolha a leitura mais provável e siga.
- Sinalize a suposição em uma linha junto do resultado (ex.: "assumi X, avisa se for Y").
- Só pare de verdade quando a decisão for cara de desfazer: destrutiva, irreversível, ou muda o escopo do que foi pedido.

## 3. Mudanças cirúrgicas

- Não "melhore" código, comentário ou formatação adjacente que não foi pedido.
- Siga o estilo já existente no arquivo, mesmo que você faria diferente.
- Dead code pré-existente que você notar: mencione, não apague sem pedir.
- Import/variável que a SUA mudança deixou órfão: remova.

## 4. Critério verificável

Traduza pedido vago em resultado checável (ex.: "corrige o bug" → reproduz com um teste, faz passar). Para lógica não trivial (branch, loop, parser, caminho de dinheiro/segurança), deixe UM check mínimo rodável (assert, demo ou teste pequeno) — não infle isso numa suíte completa a menos que peçam.

---

**Funciona se:** menos perguntas travando o fluxo no meio do trabalho, suposições visíveis no output em vez de escondidas, e diffs continuam cirúrgicos.
