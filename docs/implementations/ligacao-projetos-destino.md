# Ligar cada dissertação às perguntas atuais do projeto que ela serve

**Componente:** skill `dissertar-video` e documentação (os scripts não mudam)
**Branch:** `feat/ligacao-projetos-destino`
**Status:** Em andamento

---

## Motivação

A dissertação termina com uma tabela "o que este vídeo pode responder no
projeto X". O utilizador reparou que, no winners-group, as perguntas são
reformuladas, ganham hipóteses e nascem novas a cada vídeo, e quis saber se a
ferramenta as consulta atualizadas. Não consultava: lia uma parte, no fim, e
nunca mais voltava.

Comportamento desejado (02/10/2026, utilizador):

1. As perguntas do projeto de destino são lidas **atualizadas** e orientam o
   que se procura no vídeo, "pois dependendo da deficiência e necessidade podem
   estar sujeitos a serem buscadas outras ou mais ou menos informações".
2. Isto serve **qualquer projeto**, não só o OfficeGest / winners-group.
3. Os vídeos já dissertados são revistos **a pedido**, e não sozinhos
   (escolha do utilizador entre três opções, no plano).

---

## Problemas Identificados (estado anterior) (*)

1. **Destino escrito como exemplo:** o ponto 7 do passo 4 da skill dizia "se o
   utilizador indicar um, ou se for óbvio, como o OfficeGest →
   `C:\projetos\winners-group`". Nenhum registo dizia que projeto serve cada
   assunto, nem onde estão as perguntas dele.
2. **Leitura parcial:** sem lista de ficheiros, o Claude escolhia o que ler. No
   vídeo `7UlDwks9BgQ` leu `docs/dependencias-externas.md` por inteiro e só
   pesquisou por palavras em `docs/pendentes.md` e em
   `contabilidade/processo-atual/perguntas-em-aberto.md`. Citou os códigos C-9,
   C-24 e COM-1 a partir de referências, sem ler o texto dessas perguntas.
3. **Perguntas lidas tarde:** só eram precisas no passo 4 (escrever), por isso
   não influenciavam o passo 3 (que ecrãs abrir, que instantes pedir à mão).
4. **Tabela sem data de consulta:** nada dizia de quando era o retrato.
5. **Sem forma de rever** a ligação de um vídeo já dissertado.

---

## Abordagem (*)

Um registo em `videos/projetos-destino.md` diz, por assunto, que projeto o
vídeo serve e que ficheiros desse projeto têm as perguntas. A skill ganha um
passo logo a seguir à extração ("1b. Saber a quem o vídeo serve") que lê esses
ficheiros por inteiro e produz uma lista de trabalho. Essa lista orienta a
revisão dos ecrãs e é a base da tabela de ligação, que passa a levar a data da
consulta.

```
link → 1. extrair → 1b. registo de destinos → ler perguntas → lista de trabalho
                                                                   │
                     2. capturar → 3. rever ecrãs (com a lista) ───┤
                                                                   ▼
                                  4. escrever (tabela datada, códigos lidos)
```

**Descartado:** guardar o destino dentro de cada `metadados.json`. Obrigava a
mexer no script de extração e repetia a mesma informação em todos os vídeos do
assunto; mudar um caminho exigia editar todos.

**Descartado:** a skill escrever no projeto de destino. O winners-group já tem
o seu processo para absorver cada vídeo (`docs/fontes-videos.md`), com um
commit por vídeo. Duas mãos a escrever no mesmo sítio dariam conflitos.

**Decidido sem perguntar:**

- O registo vive em `videos/`, ao lado do índice: faz parte do produto e é o
  que outro projeto vê primeiro.
- Um projeto sem perguntas escritas regista os documentos que dizem o que ele
  já sabe, e a tabela passa a ser "o que este vídeo acrescenta".
- Uma pergunta que o vídeo levanta e o projeto ainda não tem entra como
  "pergunta sugerida", sem código inventado.

---

## Plano de Implementação (*)

### Fase 1 — Registo de destinos e perguntas atuais nos vídeos novos

**Objetivo:** a skill sabe que projeto consultar por assunto, lê as perguntas
por inteiro antes de rever os ecrãs, e data a tabela de ligação.

| Ficheiro | O que muda |
|---|---|
| `videos/projetos-destino.md` (novo) | Registo assunto → projeto → ficheiros de perguntas → registo de vídeos do projeto, com a linha do `officegest` |
| `.claude/skills/dissertar-video/SKILL.md` | Passo novo "1b. Saber a quem o vídeo serve"; no passo 3, os momentos que tocam numa pergunta são ecrãs-chave; o ponto 7 do passo 4 passa a exigir data de consulta, códigos lidos no ficheiro, "não responde" e "pergunta sugerida"; `argument-hint` atualizado |
| `docs/implementations/ligacao-projetos-destino.md` (novo) | Este contrato |

### Relatório da Fase 1 — o que mudou na prática

**Antes:** ao dissertar um vídeo, o Claude escolhia sozinho o que ler do
projeto de destino, lia-o só no fim, e a tabela de ligação não dizia de quando
era. Fora do OfficeGest, a ligação só acontecia se o utilizador indicasse o
projeto no pedido.
**Agora:** cada assunto tem o seu projeto e os seus ficheiros de perguntas
registados. A skill lê essas perguntas por inteiro logo depois de extrair o
vídeo, usa-as para decidir que ecrãs abrir e que instantes pedir, e escreve a
tabela com a data da consulta e só com códigos que leu. Num assunto novo,
pergunta uma vez que projeto serve e guarda a resposta.
**Para validar:** Cenários L1, L2, L3 e E1.

### Fase 2 — Rever a ligação dos vídeos antigos a pedido

**Objetivo:** pedir "revê os vídeos do OfficeGest com as perguntas atuais"
reescreve só a secção de ligação e a checklist de cada dissertação do assunto.

| Ficheiro | O que muda |
|---|---|
| `.claude/skills/dissertar-video/SKILL.md` | Modo "rever a ligação"; descrição da skill passa a cobrir esse pedido |
| `README.md` | "Como usar" (rever a ligação) e "Como outro projeto usa estas dissertações" (registo de destinos) |
| `CLAUDE.md` | Tabela "Usar não é implementar": rever a ligação é uso |
| `docs/decisoes.md` | Entrada datada |
| `docs/plans/melhorias-futuras.md` | Nota em M3: o modo de rever pode pedir mais capturas à mão |

*(Por implementar.)*

---

## Checks de Validação (*)

| Prefixo | O que verifica | Como |
|---|---|---|
| `L` | Lógica pura | Sem internet: seguir o passo da skill com uma entrada conhecida e comparar o resultado |
| `E` | Ponta a ponta | Correr a skill contra um vídeo real do YouTube e olhar para o que saiu em `videos/` |

Os scripts não mudam. `python -m py_compile scripts/*.py` só confirma que nada
se partiu.

### Cenário L1 — Assunto registado (Fase 1)

Setup: na worktree, seguir o passo 1b da skill para o assunto `officegest`.

- [ ] Os três ficheiros de perguntas do winners-group e o
      `docs/fontes-videos.md` são lidos por inteiro
- [ ] Sai uma lista de trabalho com códigos e textos iguais aos dos ficheiros

### Cenário L2 — Assunto novo (Fase 1)

Setup: seguir o passo 1b para um assunto sem linha no registo (por exemplo
`claude-code`).

- [ ] A skill pergunta uma vez se o assunto serve algum projeto
- [ ] A resposta fica gravada no registo, incluindo "nenhum"

### Cenário L3 — Ficheiro do registo em falta (Fase 1)

Setup: trocar na worktree um caminho da linha `officegest` por um que não
existe e seguir o passo 1b.

- [ ] A skill avisa e procura o ficheiro, em vez de seguir sem ele

### Cenário E1 — Vídeo novo, ponta a ponta (Fase 1)

Setup: na worktree, dissertar `https://www.youtube.com/watch?v=vW9GhkTXmNU`
com a skill nova (a pasta já existe; a captura descarrega o vídeo de novo). O
resultado **não é commitado**.

- [ ] A secção de ligação começa com a data da consulta e os ficheiros lidos
- [ ] Todos os códigos citados existem nos ficheiros do winners-group
- [ ] Há pelo menos uma linha "não responde" ou a lista de trabalho ficou toda
      respondida

### Cenário E2 — Rever a ligação (Fase 2)

Setup: na worktree, pedir "revê os vídeos do OfficeGest com as perguntas
atuais".

- [ ] `git diff` mostra alterações só na secção de ligação e na checklist de
      cada `dissertacao.md`
- [ ] Cada secção revista tem a nova data de consulta

---

## Ajustes Possíveis Pós-Implementação

- **As quatro dissertações existentes** mantêm a tabela antiga, sem data de
  consulta, até serem revistas a pedido (Fase 2).
- **O registo depende do outro projeto não mudar os ficheiros de sítio.** A
  skill avisa quando um caminho falha, mas não o descobre antes.
- **Usar a skill a partir de outro projeto** continua a ser o M2 de
  `docs/plans/melhorias-futuras.md`; esta implementação não o resolve.
