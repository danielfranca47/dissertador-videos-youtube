# Guia: Como Documentar uma Implementação

Este arquivo é um guia de instrução para o Claude. Leia-o antes de criar
qualquer arquivo em `docs/implementations/`.

---

## Quando este guia se aplica

O utilizador pediu para construir ou melhorar algo **na ferramenta** do
dissertador-videos-youtube: os scripts, a skill `dissertar-video` ou as regras
da dissertação. Pode ter dito coisas como:

- "Quero que funcione com vídeos sem legendas"
- "A captura está a gerar ecrãs a mais, devia gerar menos"
- "Voltei a correr a captura e perdi os ecrãs que tinha pedido à mão"

Dissertar um vídeo **não** entra aqui — é uso, não implementação (ver
`CLAUDE.md`, "Usar não é implementar").

Antes de escrever qualquer código, siga os passos abaixo em ordem.

---

## Passo 0 — Diagnóstico em Plan Mode (obrigatório)

**Antes de criar o arquivo ou tocar no código**, entrar em Plan Mode e
responder:

### 1. Essa funcionalidade já existe?

Ler os ficheiros relevantes e verificar se o comportamento pedido já está
implementado, total ou parcialmente. Citar ficheiros e linhas onde encontrou —
ou onde procurou e não encontrou. Verificar também se já está registado em
[`docs/plans/`](../plans/README.md): se estiver, o plano parte do que lá está.

### 2. Se não existe, o que precisa de ser construído?

- Que componente recebe a mudança — o script de extração, o de captura, a
  skill — e mais do que um?
- Que funções são criadas ou alteradas?
- Que vídeo real serve para testar isto? (Com legendas, sem legendas, longo,
  sem demonstração de ecrã…)
- A mudança altera o formato do que fica em `videos/` (`metadados.json`,
  `transcricao.txt`, `ecras/indice.json`, a estrutura da dissertação)? Se sim,
  o que acontece aos vídeos já dissertados?

### 3. Muda a arquitetura recomendada, custa dinheiro ou exige uma conta?

Se sim, a mudança passa pelo agente arquiteto em `C:\projetos\modelos-agents`
antes de ser construída, e o custo sobe ao utilizador **no plano** (ver
`CLAUDE.md`, "Mudança de arquitetura passa pelo arquiteto").

### 4. Quais são os riscos e dependências?

- A mudança pode quebrar algo que já funciona? Onde?
- Pode apagar ou sobrescrever dissertações ou ecrãs já produzidos?
- Há trade-off que o utilizador deva conhecer antes de decidir?
- Há decisão de produto por tomar? (ver `CLAUDE.md`, "Com quem o Claude está
  a falar" — o que sobe e o que não sobe)

**Formato do plano:**

```
## Diagnóstico

### Já existe?
<Sim / Parcialmente / Não> — <explicação com ficheiros e linhas>

### O que precisa de ser construído
<Mudanças agrupadas por componente>

### Riscos e dependências
<"Nenhum" é uma resposta válida>

### Proposta de fases
Fase 1 — <nome> — <objetivo em uma frase>
```

**Aguardar aprovação antes de avançar.**

### O plano é onde as ambiguidades aparecem

Toda lacuna que exija uma escolha deve estar **no plano**, resolvida ou
perguntada. Se nada escrito decide algo, o plano diz qual decisão o Claude vai
tomar e porquê; o utilizador corrige ali, antes de existir código.

**Se uma ambiguidade só aparecer a meio da implementação** e mudar o resultado
visível: parar e resolver nesse momento — decidindo e registando, ou
perguntando se for uma das coisas que sobem. Nunca acumular para o relatório
final: nessa altura o código já está escrito e a pergunta chega como fatura,
não como decisão.

**Se o pedido vier como ordem direta de código** ("implementa a transcrição do
áudio"), o Passo 0 continua obrigatório — é justamente aí que mais protege,
porque um pedido assim costuma esconder várias escolhas que ninguém fechou.

---

## Passo 1 — Criar a branch e nomear o arquivo

### Branch + worktree

Criar a branch **e a worktree que vai com ela** — sempre, mesmo que não haja
outra implementação ativa (ver `CLAUDE.md`, "Estratégia de branch por
implementação": isola a pasta principal, onde os vídeos são dissertados, e
previne colisão entre sessões que nem sabem uma da outra).

**Nome:** `feat/<slug>` ou `fix/<slug>`. O Claude propõe e **pede confirmação**;
depois `EnterWorktree(name="feat/<slug>")`.

> A worktree funciona logo (as bibliotecas estão no Python da máquina), mas a
> `videos/` dela não tem `video.mp4`: um teste ponta a ponta descarrega o vídeo
> de novo. Os resultados de teste ficam na worktree e não são commitados.

### Arquivo

**Formato do nome:** `<slug>.md`

Exemplos: `transcricao-audio-sem-legendas.md`, `skill-global.md`,
`preservar-capturas-manuais.md`

---

## Passo 2 — Estrutura do arquivo

> **Exemplo concreto preenchido:**
> [`_template-implementacao.md`](_template-implementacao.md). Leia-o antes de
> criar o seu — mostra o nível de detalhe esperado.

Seções marcadas com `(*)` são obrigatórias.

```markdown
# <Título descritivo da feature>

**Componente:** <script de extração / script de captura / skill / vários>
**Branch:** `<branch-atual>`
**Status:** Em andamento

---

## Motivação

<Por que o utilizador quer isto? Qual é o comportamento atual e o desejado?
Se houver causa raiz conhecida, descrever aqui.>

---

## Problemas Identificados (estado anterior) (*)

1. **Nome do problema:** descrição + ficheiro/linha onde ocorre.

---

## Abordagem (*)

<Prosa ou diagrama ASCII de como a solução funciona.>

---

## Plano de Implementação (*)

### Fase 1 — <Nome>

**Objetivo:** <uma frase>

| Ficheiro | O que muda |
|---|---|

<Antes/depois de código apenas quando a mudança for não-óbvia.>

---

## Checks de Validação (*)

| Prefixo | O que verifica | Como |
|---|---|---|
| `L` | Lógica pura | Sem internet: chamar a função com uma entrada conhecida e comparar o resultado |
| `E` | Ponta a ponta | Correr o script ou a skill contra um vídeo real do YouTube e olhar para o que saiu em `videos/` |

### Cenário L1 — <Descrição>
- [ ] Entrada
- [ ] Resultado esperado

---

## Ajustes Possíveis Pós-Implementação

<Limitações conhecidas, trade-offs conscientes, o que ficou fora do escopo.>
```

---

## Passo 3 — Ciclo de vida do arquivo

O arquivo **cresce**. Nunca reescrever o que já foi documentado — acrescentar.

### Quando uma fase é implementada

```markdown
### Commits Fase N

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `<hash>` | Descrição resumida |
```

### Antes de pedir validação

Depois do commit, e **antes** de aguardar validação, dois passos obrigatórios:

**1. Escrever o relatório da fase em linguagem simples:**

```markdown
### Relatório da Fase N — o que mudou na prática

**Antes:** <comportamento anterior, 1-2 frases>
**Agora:** <comportamento novo, 1-2 frases>
**Para validar:** <que Cenários cobrem esta fase>
```

Obrigatório mesmo em fases pequenas. Serve dois propósitos: comunicar o impacto
real, e permitir retomar numa conversa nova sem reler o histórico do chat.

**2. Oferecer a validação — sempre com prompt de retomada pronto:**

> "Quer que eu corra os Cenários X agora?
>
> Se preferir depois (aqui ou numa conversa nova), pode colar:
>
> Lê `<arquivo>.md`, secção "Fase N", e executa os testes dos Cenários X."

O prompt de retomada **nunca fica de fora**, e leva os nomes e números reais —
não um placeholder.

### Quando um cenário é testado

```markdown
- [x] <o que foi confirmado>
- **Validado em:** 01/10/2026 — descrição do que foi observado
```

### Quando um teste revela um bug

Acrescentar nova secção no fim (não editar o que já estava escrito), com
problema identificado, causa raiz e correção. A nova fase segue o mesmo ciclo:
commit → relatório → checks → validação.

### Quando a implementação estiver completa

```markdown
**Status:** Todos os cenários validados (01/10/2026)
```

Depois, seguir
[`_processo-graduacao-implementacao.md`](_processo-graduacao-implementacao.md).

---

## Regras de escrita

1. **Registar decisões, não só resultado.** Se uma abordagem foi descartada,
   dizer porquê numa frase.
2. **Causa raiz explícita.** "O bug era X" é mais útil que "o sistema fazia Y
   errado".
3. **Antes/depois de código** apenas quando a mudança é não-óbvia.
4. **Sem histórico acumulado** no texto corrido — isso fica nos commits.
5. **Tabela de ficheiros sempre presente** por fase.
6. **Checks executáveis por alguém sem contexto interno.** Incluir o setup: o
   link do vídeo usado, o comando exato, e o que procurar no resultado.
7. **Nenhum dado inventado.** Um check ponta a ponta usa um vídeo real, com o
   link escrito. Se não houver um vídeo que produza o cenário (por exemplo, um
   vídeo sem legendas), procurar um — não simular o resultado.
8. **O relatório da fase é um relatório, não uma lista de perguntas.** Decisões
   tomadas entram como decisões; só sobe o que cabe nas categorias do
   `CLAUDE.md`. Pedir autorização para o que o fluxo já autoriza — graduar com
   `[⏭️]` justificado, por exemplo — é ruído.
9. **Relatório em linguagem simples por fase, escrito antes de pedir
   validação.**

---

## Ciclo de vida de uma fase

As fases **não são planeadas todas de uma vez**. Cada fase nasce de uma
necessidade concreta: o pedido inicial, ou o resultado dos testes da anterior.

```
Utilizador reporta problema/melhoria
  → Plan Mode (diagnóstico + plano da Fase 1)
  → Utilizador aprova
  → cria branch + worktree, cria o .md, implementa Fase 1 + commit
  → escreve checks + "Relatório da Fase 1"
  → oferece validação + prompt de retomada
      ├─ Sim → corre, regista resultados nos checks
      └─ Não → aguarda

Resultado dos testes
  → marca os checks validados

  Caminho A — tudo ok → graduação
  Caminho B — teste revelou problema → Plan Mode de novo → Fase 2 no mesmo
              arquivo → ciclo repete-se
```

**Regra:** cada fase tem exatamente um commit, e o hash é registado no arquivo
assim que é criado.

---

**Nota:** o arquivo `.md` só é criado após o primeiro plano ser aprovado. O Plan
Mode é o rascunho; o arquivo é o contrato vivo entre o utilizador e o Claude
durante o desenvolvimento da feature.
