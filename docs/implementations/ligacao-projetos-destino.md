# Ligar cada dissertação às perguntas atuais do projeto que ela serve

**Componente:** skill `dissertar-video` e documentação (os scripts não mudam)
**Branch:** `feat/ligacao-projetos-destino`
**Status:** Todos os cenários validados (02/10/2026)

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

### Commits Fase 1

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `7cc8d61` | Registo de destinos, passo 1b na skill, ecrãs-chave guiados pelas perguntas, tabela de ligação datada |

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

**Decidido ao implementar:**

- O modo de rever **não repete a captura automática** de um vídeo já
  dissertado, porque apagaria os ecrãs pedidos à mão (M3). Um instante em
  falta pede-se sozinho, com `--em`.
- O modo de rever **não corrige o corpo** da dissertação. Se encontrar um erro
  ou uma falta no texto, escreve-o numa linha "A rever no texto acima" e
  di-lo na resposta. Motivo: o utilizador escolheu uma revisão que mexe só na
  ligação; alargar o âmbito em silêncio tirava-lhe essa garantia.
- A primeira linha da secção revista diz a data da revisão **e** a da versão
  anterior, para se ver que houve revisão.
- Um commit único por revisão, com todas as dissertações revistas.

### Commits Fase 2

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `645379e` | Modo "rever a ligação" na skill; README, CLAUDE.md, decisões e nota em M3 |

### Relatório da Fase 2 — o que mudou na prática

**Antes:** a tabela de ligação de um vídeo já dissertado ficava para sempre
como estava no dia em que foi escrita. Para a pôr em dia era preciso pedir a
correção vídeo a vídeo, sem regra de como.
**Agora:** basta pedir "revê os vídeos do OfficeGest com as perguntas atuais".
A ferramenta lê as perguntas de hoje, volta à transcrição e aos ecrãs
guardados de cada vídeo e reescreve só a tabela de ligação e a lista de pontos
a verificar, com a data nova. O README, o CLAUDE.md e o registo de decisões
explicam o registo de destinos e este pedido.
**Para validar:** Cenário E2, e o ramo "nenhum" do Cenário L2.

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

- [x] Os três ficheiros de perguntas do winners-group e o
      `docs/fontes-videos.md` são lidos por inteiro
- [x] Sai uma lista de trabalho com códigos e textos iguais aos dos ficheiros
- **Validado em:** 02/10/2026 — lidos os quatro ficheiros (268, 71, 81 e 41
  linhas). A leitura completa encontrou as perguntas C-26 e C-27, criadas no
  próprio dia, que a leitura parcial do vídeo `7UlDwks9BgQ` não tinha visto, e
  confirmou que o COM-1 existe (estava nas últimas linhas, que não tinham sido
  lidas).

### Cenário L2 — Assunto novo (Fase 1)

Setup: seguir o passo 1b para um assunto sem linha no registo (por exemplo
`claude-code`).

- [x] A skill pergunta uma vez se o assunto serve algum projeto
- [x] A resposta "serve um projeto" fica gravada no registo
- [x] A resposta "nenhum" fica gravada no registo
- **Validado em:** 02/10/2026 — o utilizador respondeu "serve um projeto", sem
  indicar qual; usou-se `C:\projetos\modelos-agents` como alvo do teste. A
  exploração não encontrou perguntas escritas e registou `README.md`,
  `CLAUDE.md` e `briefings/` como "o que o projeto já sabe". A linha de teste
  foi apagada no fim. **O ramo "nenhum" não foi exercitado**; fica para a
  validação da Fase 2.
- **Ramo "nenhum" validado em:** 02/10/2026 (com a Fase 2) — para o assunto
  `claude-code`, sem linha no registo, com a resposta "não serve nenhum
  projeto" dada pelo utilizador no pedido do teste. Ficou gravada a linha
  `| claude-code | nenhum | — | — | 2026-10-02 |`. Numa segunda passagem pelo
  passo 1b, a linha é encontrada e o passo é saltado sem nova pergunta. A
  linha de teste foi apagada no fim; `git diff` do registo vazio.

### Cenário L3 — Ficheiro do registo em falta (Fase 1)

Setup: trocar na worktree um caminho da linha `officegest` por um que não
existe e seguir o passo 1b.

- [x] A skill avisa e procura o ficheiro, em vez de seguir sem ele
- **Validado em:** 02/10/2026 — com `docs/pendentes-antigo.md` no registo, a
  verificação deu "não existe" e a procura no projeto encontrou
  `docs/pendentes.md`. Registo reposto.

### Cenário E1 — Vídeo novo, ponta a ponta (Fase 1)

Setup: na worktree, dissertar `https://www.youtube.com/watch?v=vW9GhkTXmNU`
com a skill nova (a pasta já existe; a captura descarrega o vídeo de novo). O
resultado **não é commitado**.

- [x] A secção de ligação começa com a data da consulta e os ficheiros lidos
- [x] Todos os códigos citados existem nos ficheiros do winners-group
- [x] Há pelo menos uma linha "não responde" ou a lista de trabalho ficou toda
      respondida
- **Validado em:** 02/10/2026 — extração e captura repetidas na worktree (194
  ecrãs, iguais aos que estavam no histórico), as 22 folhas revistas e 8 ecrãs
  abertos em tamanho real por tocarem numa pergunta. Os 19 códigos citados
  estão definidos nos ficheiros do winners-group e as 8 imagens existem
  (verificado por script). A tabela passou de 4 para 15 linhas.
- **O que as perguntas fizeram encontrar** e a dissertação de 01/10 não tinha:
  a coluna **Colaboradores** e o estado **Fechado** no ecrã Exercícios (C-24,
  C-8), as compras já lançadas na lista de lançamentos (C-24), o separador
  "Iva / Abertura" e a retenção na fonte nos Parâmetros (C-11, C-9), os
  botões do lançamento (regra do risco irreversível), "Imprimir Excel" no
  balancete (C-21) e os Mapas analíticos no menu (C-5).
- **Desvio em relação ao setup:** só a secção de ligação e a checklist foram
  reescritas; o corpo da dissertação (secções 1 a 9) foi reaproveitado, porque
  esta implementação não muda a forma de o escrever. O resultado foi
  descartado da worktree, como previsto.

### Cenário E2 — Rever a ligação (Fase 2)

Setup: na worktree, pedir "revê os vídeos do OfficeGest com as perguntas
atuais".

- [x] `git diff` mostra alterações só na secção de ligação e na checklist de
      cada `dissertacao.md`
- [x] Cada secção revista tem a nova data de consulta
- **Validado em:** 02/10/2026 — revistas as quatro dissertações do assunto
  `officegest`, da gravação mais antiga para a mais recente. Lidos por inteiro
  os quatro ficheiros do winners-group (268, 71, 81 e 41 linhas), as quatro
  transcrições e as 22 folhas do webinar (os outros três vídeos não têm folhas
  no git); 41 ecrãs abertos em tamanho real, vários que as dissertações não
  embutem. Nenhuma captura foi repetida e nenhum vídeo foi descarregado.
  Conferido por script: em cada ficheiro, o texto até ao título da secção de
  ligação e de "Limites desta versão" em diante é **igual ao do commit**; as
  quatro secções começam por "Perguntas consultadas em 2026-10-02 (revisão…)";
  todos os códigos citados estão definidos nos ficheiros do winners-group;
  todas as imagens ligadas existem; nenhum ponto antigo das checklists se
  perdeu; o winners-group não foi tocado.

  | Dissertação | Linhas da tabela | Pontos da checklist |
  |---|---|---|
  | Webinar #2 (2020) | 4 → 20 | 5 → 12 |
  | Configuração Geral (2021) | 13 → 22 | 10 → 15 |
  | Financeira (2021) | 9 → 13 | 9 → 13 |
  | Contabilidade (2021) | 11 → 20 | 12 → 16 |

- **O que a revisão encontrou** e as versões anteriores não tinham:
  o winners-group ainda não registou o vídeo de Configuração Geral, o único
  que abre o menu "Importação E-fatura" (OG-9); as operações bancárias do
  vídeo de financeira aparecem nos Lançamentos em lote do vídeo de
  contabilidade e falham por falta da conta do banco (C-26); registos
  "Fechado" que mostram um botão Apagar, contra a nota do projeto; o
  emparelhamento à mão da reconciliação não confere datas (OG-3). Cada
  dissertação ganhou uma linha "A rever no texto acima" com as faltas do corpo
  que a revisão viu e não corrigiu.
- **Decidido ao validar:**
  - Três das quatro tabelas antigas não tinham data de consulta. Como "data da
    versão anterior" usou-se a data "Processado em" do cabeçalho.
  - A ordem "do mais antigo para o mais recente" seguiu a data de **gravação**
    (três dos vídeos têm a mesma data de publicação).
  - Códigos de pergunta já respondida no projeto (OG-1, OG-2, C-1, C-25) saíram
    das tabelas; o que estava preso a eles passou para a pergunta em aberto
    onde o projeto o arrumou, ou para "pergunta sugerida".
  - **O resultado não foi commitado**, pela regra dos testes na worktree. Ao
    contrário do E1, é trabalho que vale a pena aproveitar: as quatro
    dissertações revistas ficam por commitar na worktree, para serem levadas
    para `main` na graduação como a primeira revisão real
    (`docs: rever a ligação de officegest ao projeto winners-group`), se o
    utilizador não preferir descartá-las.

---

## Ajustes Possíveis Pós-Implementação

- **As quatro dissertações existentes** mantêm a tabela antiga, sem data de
  consulta, até serem revistas a pedido (Fase 2).
- **(02/10, da validação do E2) A revisão de um assunto inteiro é pesada.**
  Quatro vídeos pediram quatro transcrições inteiras e 41 ecrãs em tamanho
  real numa só conversa. Com mais vídeos por assunto, convém a skill sugerir a
  revisão **vídeo a vídeo** ou em lotes pequenos.
- **(02/10, idem) Versão anterior sem data.** A skill manda escrever "a versão
  anterior era de AAAA-MM-DD" e não diz de onde tirar a data quando a tabela
  antiga não a tem. Usou-se a data de processamento; falta escrevê-lo na skill.
- **(02/10, idem) Revisão no mesmo dia.** Quando a versão anterior é do próprio
  dia, a linha "revisão; a versão anterior era de" repete a data e não diz o
  que mudou. Acrescentou-se à mão "feita com leitura parcial".
- **(02/10, idem) "Do mais antigo para o mais recente"** não diz se é pela data
  de publicação ou de gravação.
- **(02/10, da validação do L2) Linha "nenhum".** O registo e a skill só dizem
  o que vai na coluna Projeto; as outras colunas ficaram com "—". O modo de
  rever não diz o que fazer quando o assunto pedido está registado como
  "nenhum".
- **(02/10, da validação do E2) Capturas à mão fora do `indice.json`.** 16
  ecrãs pedidos à mão nos três vídeos de 2021 existem em `ecras/` mas não
  constam do índice. Já é o M3 de `docs/plans/melhorias-futuras.md`; fica aqui
  porque o modo de rever depende desses ecrãs.
- **O registo depende do outro projeto não mudar os ficheiros de sítio.** A
  skill avisa quando um caminho falha, mas não o descobre antes.
- **Usar a skill a partir de outro projeto** continua a ser o M2 de
  `docs/plans/melhorias-futuras.md`; esta implementação não o resolve.
