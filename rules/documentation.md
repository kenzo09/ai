# Documentação

Doc é código que ninguém compila: ela só se paga quando responde uma pergunta que o leitor não consegue responder lendo o repositório. Documentar demais causa o mesmo dano que não documentar: quando metade do texto está obsoleta, o leitor para de confiar no conjunto inteiro.

A meta é um punhado de documentos que alguém lê inteiro na primeira semana e ainda acha verdadeiros no ano seguinte.

## Escopo: o que merece doc

- **FAÇA**: Documente **arquitetura do sistema** — o que roda dentro do limite, quem entra e por onde.
- **FAÇA**: Documente **integrações externas** — com quem o sistema fala, por qual transporte, e o que acontece quando o outro lado falha.
- **FAÇA**: Documente **capacidades** — o que o sistema entrega ao usuário, em linguagem de negócio.
- **FAÇA**: Documente **regras de negócio core** — a regra que custa dinheiro, dado ou confiança quando violada.
- **FAÇA**: Documente **peças críticas e invariantes não-óbvias** — o que quebra quando alguém mexe sem saber.
- **FAÇA**: Registre **decisão arquitetural com tradeoff real** como ADR: o valor está no porquê, não no quê.
- **FAÇA**: Prefira apagar a explicar duas vezes. Um assunto tem um lugar canônico; os outros linkam para ele.

## O que não merece doc

- **NÃO FAÇA**: Documentar estrutura interna de pacote, função privada ou detalhe de implementação que o consumidor não vê.
- **NÃO FAÇA**: Escrever narrativa de mudança ("antes era X, agora é Y"), post-mortem de bug ou passo-a-passo de refactor. Isso é histórico de commit, não doc.
- **NÃO FAÇA**: Descrever cenário de comportamento em prosa (Dado/Quando/Então e afins). Comportamento se prova com teste; em markdown ele apodrece em silêncio e passa a mentir com cara de contrato. Se vale descrever, vale um teste no lugar.
- **NÃO FAÇA**: Enumerar campo trivial ou repetir o que o código já diz com clareza.
- **NÃO FAÇA**: Referenciar em doc commitável arquivos de planejamento (specs/plans/handoffs); eles são gitignored e o link nasce quebrado.
- **NÃO FAÇA**: Deixar uma capacidade core sem nenhum registro do que ela faz, para quem, e por quê.

**FAÇA**: Ao encontrar doc que caiu nessa lista, delete. Apagar é entrega, não perda.

## Artefato visual

Uma imagem explica arquitetura melhor que mil palavras — mas uma imagem binária não tem diff, ninguém revisa no MR e ela envelhece sem que nada acuse.

- **FAÇA**: Use **diagrama como texto** (mermaid no próprio markdown) como padrão. Versionável, revisável, editável por quem encostar no código.
- **FAÇA**: Recorra a binário (png, jpg, mp4) ou HTML só quando o texto não consegue expressar: captura de UI real, gravação de fluxo, desenho fora do alcance de qualquer sintaxe de diagrama.
- **FAÇA**: Antes de commitar o primeiro binário, configure o repositório para arquivo grande (`git lfs track "docs/**/*.png"`) e registre no `.gitattributes`. Sem isso, o peso fica no clone de todo mundo para sempre: mantenha o diagrama em texto e avise o usuário.
- **NÃO FAÇA**: Commitar imagem que só reproduz o que uma tabela de cinco linhas já diz.

Evidência visual de execução é outra coisa e segue outra regra (ver `rules/testing.md`): ela prova uma entrega para quem pediu, não documenta o sistema, e por isso não vira doc commitável por padrão.

## O que dispara doc

A doc descreve o **estado esperado do sistema**, nunca o caminho até ele. A pergunta certa nunca é "o que eu mexi?", e sim "o que o sistema promete hoje é diferente do que a doc diz?".

- **FAÇA**: Atualize a doc quando uma capacidade, integração, regra de negócio core ou decisão arquitetural **passa a ser outra**: feature nova, evolução, mudança de escopo, integração trocada, regra renegociada.
- **FAÇA**: Registre capacidade core nova antes de considerar o trabalho concluído. Uma seção em doc existente costuma bastar; arquivo novo só quando o assunto não tem dono.
- **NÃO FAÇA**: Documentar bugfix. Bug é código transitório que nunca deveria ter existido: a doc já descrevia o comportamento correto, e o fix apenas faz o sistema alcançá-la. Nada a mudar.
- **NÃO FAÇA**: Confundir evolução com bug. Se o comportamento anterior era o combinado e alguém decidiu mudá-lo, isso é mudança de escopo e a doc muda junto.
- **NÃO FAÇA**: Criar doc para mudança que não altera nenhuma capacidade, integração, regra core ou decisão arquitetural.
- **FAÇA**: Ao fechar uma implementação (testes passando, antes de anunciar entrega, commit ou MR), **pergunte ao usuário** se ele quer gerar a documentação. Rode só se ele pedir; silêncio ou "ok" não é "sim".

O único caso em que um bugfix toca a doc é quando a **doc estava errada**: ela descrevia o comportamento bugado como se fosse o esperado. Aí não se documenta o fix, corrige-se a doc para o comportamento correto — que continua sendo o estado atual, não um relato do que aconteceu.

## Como

Se a skill `live-docs` estiver disponível, use-a para decidir qual artefato criar ou atualizar (arquitetura, PRD, ADR) e onde ele mora; para focar num tipo só, passe o tipo como argumento: `live-docs architecture`. Sem a skill, siga a estrutura que o repositório já usa.

O teste: se alguém lesse só a doc hoje, ela bateria com o que o sistema faz? Se não, ajuste ou apague — manter é a única opção errada.
