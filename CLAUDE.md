Diretrizes de comportamento para reduzir erros comuns de LLM ao codificar. Mescle com instruções específicas do projeto conforme necessário.

# Idioma

O idioma de cada saída é definido pelo tipo de artefato produzido — nunca pelo idioma da solicitação, do código ou dos arquivos envolvidos. Siga a tabela:

| Artefato | Idioma |
|---|---|
| Resposta ao usuário (chat) | pt-BR |
| Specs | pt-BR |
| Handoffs | pt-BR |
| Plans | en-US |
| MR/PR (título e descrição) | pt-BR |
| Mensagem de commit (título e corpo) | en-US |
| Código (identificadores, strings técnicas) | en-US |
| Comentários e documentação inline | pt-BR |
| Chaves e valores em JSON/YAML | en-US |
| Qualquer artefato não listado | pt-BR |

Artefato aninhado mantém o idioma do próprio artefato: uma mensagem de commit citada numa resposta de chat permanece em en-US.

# 1. Simplicidade primeiro

Código mínimo que resolve o problema. Nada especulativo.

- Sem abstrações para uso único, sem "flexibilidade" ou configuração que não foi pedida.
- Sem tratamento de erro para cenários impossíveis.
- Prefira reutilizar algo que já existe no projeto/linguagem/stdlib antes de escrever código novo.
- Se escreveu 200 linhas e dava pra ser 50, reescreva.

# 2. Suposição em vez de trava

Ambiguidade não trava o trabalho:

- Escolha a leitura mais provável e siga.
- Sinalize a suposição em uma linha junto do resultado (ex.: "assumi X, avisa se for Y").
- Só pare de verdade quando a decisão for cara de desfazer: destrutiva, irreversível, ou muda o escopo do que foi pedido.

# 3. Mudanças cirúrgicas

- Não "melhore" código, comentário ou formatação adjacente que não foi pedido.
- Siga o estilo já existente no arquivo, mesmo que você faria diferente.
- Dead code pré-existente que você notar: mencione, não apague sem pedir.
- Import/variável que a SUA mudança deixou órfão: remova.

# 4. Critério verificável

Traduza pedido vago em resultado checável (ex.: "corrige o bug" → reproduz com um teste, faz passar). Para lógica não trivial (branch, loop, parser, caminho de dinheiro/segurança), deixe UM check mínimo rodável (assert, demo ou teste pequeno) — não infle isso numa suíte completa a menos que peçam.

# 5. Documentação
@docs/README.md