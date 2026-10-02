# Ligação a projetos de destino

Como a dissertação de um vídeo fica ligada às perguntas em aberto do projeto
que ela serve: de onde se sabe que projeto é, quando e como as perguntas são
lidas, o que a dissertação escreve sobre elas, e como se põe em dia uma
dissertação antiga.

Os passos que o Claude segue estão na skill
[`dissertar-video`](../../.claude/skills/dissertar-video/SKILL.md) (passo 1b,
passo 3, ponto 7 do passo 4 e secção "Rever a ligação"). Este documento diz o
que esses passos garantem e porquê. Os scripts em `scripts/` não participam:
tudo isto é feito pelo Claude Code na sessão.

---

## As peças

```
link → 1. extrair → 1b. registo de destinos → ler perguntas → lista de trabalho
                                                                   │
                     2. capturar → 3. rever ecrãs (com a lista) ───┤
                                                                   ▼
                                  4. escrever (tabela datada, códigos lidos)
```

| Peça | Onde vive | O que é |
|---|---|---|
| Registo de destinos | [`videos/projetos-destino.md`](../../videos/projetos-destino.md) | Uma linha por assunto: o projeto que o assunto serve, os ficheiros desse projeto com as perguntas em aberto, e o registo de vídeos do projeto, se tiver |
| Lista de trabalho | Só na sessão | As perguntas em aberto que o vídeo pode tocar, com o código e o texto tal como estão no ficheiro, mais as pistas que o projeto já anotou sobre vídeos anteriores |
| Secção de ligação | No fim de cada `dissertacao.md` | "O que este vídeo pode responder no projeto <nome>": a linha com a data da consulta e a tabela, uma linha por pergunta |

---

## O registo de destinos

- A chave é o **assunto** (a pasta em `videos/`). O destino não é guardado em
  cada vídeo: mudar um caminho corrige-se numa linha só.
- Os caminhos da coluna "Onde estão as perguntas" são relativos à pasta do
  projeto de destino.
- Um assunto que serve dois projetos tem uma linha por projeto.
- Um assunto que não serve nenhum projeto fica com "nenhum" na coluna Projeto.
  A linha existe para a skill não voltar a perguntar; com ela, o passo 1b e a
  secção de ligação são saltados.
- Um projeto sem perguntas escritas regista os documentos que dizem o que ele
  já sabe. A tabela da dissertação passa a ser "o que este vídeo acrescenta ao
  que o projeto já sabe".
- Um assunto sem linha faz a skill perguntar **uma vez** se serve algum
  projeto, e a resposta fica gravada.
- Um projeto indicado no pedido vale para esse vídeo, mesmo que o registo diga
  outra coisa.

Acrescentar ou corrigir uma linha do registo é **uso** da ferramenta, não
implementação (ver `CLAUDE.md`, "Usar não é implementar").

---

## Regras da leitura das perguntas

- **Por inteiro, nunca por pesquisa de palavras.** Uma pergunta reformulada ou
  criada no próprio dia escapa à pesquisa. O custo é mais leitura por vídeo.
- **Antes de rever os ecrãs.** As perguntas decidem que ecrãs se abrem em
  tamanho real e que instantes se pedem à mão: um momento que toca numa
  pergunta da lista de trabalho é sempre ecrã-chave, mesmo que pareça banal.
- **Caminho do registo que não existe:** a skill avisa e procura para onde o
  ficheiro foi. Não segue sem ele. O registo só descobre que o outro projeto
  mudou os ficheiros de sítio quando a leitura falha.
- **Só leitura.** O dissertador nunca edita o projeto de destino. Esse projeto
  tem o seu próprio processo para absorver cada vídeo.

---

## O que a secção de ligação garante

- A primeira linha diz a **data da consulta e os ficheiros lidos**. A tabela é
  o retrato desse dia, não o estado atual do projeto.
- Só aparecem códigos de pergunta **lidos no ficheiro** nessa sessão. Um código
  visto numa referência noutro documento não conta.
- Uma pergunta da lista de trabalho que o vídeo não responde entra com "não
  responde".
- Uma pergunta que o vídeo levanta e o projeto não tem entra como "pergunta
  sugerida", sem código inventado.
- As divergências com o que o projeto já registou são marcadas.

---

## Rever a ligação de vídeos já dissertados

Só acontece **a pedido** ("revê os vídeos do <assunto> com as perguntas
atuais"), para um assunto inteiro ou para um vídeo.

- Reescreve **só** a secção de ligação e a checklist "Pontos a verificar no
  sistema atual". O corpo da dissertação fica igual.
- Um erro ou uma falta do corpo visto durante a revisão **não é corrigido**:
  fica numa linha "A rever no texto acima", no fim da secção de ligação.
- A primeira linha da secção passa a dizer a data da revisão e a da versão
  anterior. Os pontos antigos da checklist que continuam por verificar
  mantêm-se.
- Trabalha com a transcrição e os ecrãs **já guardados**. Abre também ecrãs que
  a dissertação não embute.
- **Nunca repete a captura automática** de um vídeo já dissertado: apagaria os
  ecrãs pedidos à mão que a dissertação embute. Um instante em falta pede-se
  sozinho, com `--em`. É uma proteção por regra escrita na skill, não pelo
  script (ver M3 em [`melhorias-futuras.md`](../plans/melhorias-futuras.md)).
- As folhas de miniaturas não estão no git. Num vídeo sem `ecras/folhas/`, os
  ecrãs a abrir escolhem-se pelos minutos da transcrição e da dissertação.
- Termina num commit único em `main`, só com as dissertações revistas:
  `docs: rever a ligação de <assunto> ao projeto <nome>`.

---

## Limites conhecidos

- Rever um assunto inteiro numa só conversa é pesado: cada vídeo pede a
  transcrição inteira e vários ecrãs em tamanho real.
- Os ecrãs pedidos à mão não constam de `ecras/indice.json`; só se sabe que
  existem olhando para a pasta.
