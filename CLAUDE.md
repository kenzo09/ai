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

# Documentação
@docs/README.md