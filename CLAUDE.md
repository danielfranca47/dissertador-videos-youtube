# Dissertador de vídeos do YouTube

Transforma um vídeo do YouTube num `.md` detalhado, com os ecrãs demonstrados,
para servir de base de conhecimento a outros projetos do Claude Code (o
primeiro é o `C:\projetos\winners-group`, com os vídeos do OfficeGest).

O utilizador usa as dissertações para aprender temas que não domina. Por isso
o conteúdo de um vídeo entra sempre como **hipótese datada**, e a prova é o
ecrã, não a legenda. Como usar, e as regras da dissertação, estão no
[`README.md`](README.md) e na skill
[`dissertar-video`](.claude/skills/dissertar-video/SKILL.md).

A arquitetura foi recomendada pelo agente "Arquiteto de Soluções de IA" em
`C:\projetos\modelos-agents\briefings\2026-10-01-dissertador-videos-youtube.md`:
fluxo fixo e não agente; scripts Python para a parte determinística; o próprio
Claude Code lê as imagens e escreve o `.md`, sem chave de API da Anthropic.

---

## Usar não é implementar

Há dois tipos de trabalho nesta pasta, e só um deles passa pelo fluxo abaixo.

| Trabalho | Exemplo | Como se faz |
|---|---|---|
| **Usar** a ferramenta | Dissertar um vídeo, reprocessar um vídeo, corrigir o texto de uma dissertação | Direto na pasta principal, pela skill `dissertar-video`. Sem Plan Mode, sem branch. No fim, um commit em `main` só com a pasta desse vídeo e o índice: `docs: dissertar <título do vídeo>` |
| **Mudar** a ferramenta | Alterar `scripts/`, a skill `dissertar-video`, ou as regras da dissertação | Workflow de Implementação, abaixo |

Se um vídeo revelar uma falha da ferramenta (ecrãs a mais, legenda que não é
encontrada, um passo da skill que não serve), terminar o vídeo como der,
registar a falha em [`docs/plans/`](docs/plans/README.md) e dizê-lo na
resposta. Não corrigir a ferramenta a meio de um vídeo.

---

## Com quem o Claude está a falar

O utilizador **não é programador**. Lê tudo o que o Claude escreve, mas não
avalia código — avalia consequência: o que a ferramenta passa a fazer, o que
isso muda para quem a vai usar, e o que falta decidir.

### O que o Claude decide sozinho

Tudo o que tenha resposta derivável do que já existe — README, skill, código,
`docs/`, o briefing do arquiteto, ou bom senso de engenharia:

- estrutura de ficheiros, nomes, bibliotecas, ordem de implementação
- que abordagem usar quando nada escrito decide mas o domínio decide
- como resolver um conflito de merge
- se um check pode ficar `[⏭️]` e a implementação graduar — a regra já está
  escrita, não precisa de nova autorização

Nestes casos: **decidir, registar no contrato vivo, e reportar.** "Decidi X
porque Y" é um relatório. "Prefere X ou Y?", com X e Y escritos em vocabulário
de código, é passar a conta a quem não a pode pagar.

### O que sobe para o utilizador

Três coisas, e mais nada:

1. **Decisão de produto** — o que a ferramenta deve fazer ou o que a
   dissertação deve conter, quando há mais de uma resposta defensável e a
   escolha muda o que o utilizador vê.
2. **Decisão de negócio** — prioridade, escopo, e tudo o que custe dinheiro ou
   exija criar uma conta num serviço (a transcrição paga do áudio, por exemplo).
3. **Risco irreversível** — perda de dissertações ou de ecrãs já produzidos, ou
   algo que não dá para desfazer.

### Mudança de arquitetura passa pelo arquiteto

Uma mudança que altere a recomendação do briefing (trocar a fonte da
transcrição, introduzir um serviço pago, passar de fluxo fixo a agente) é
levada ao agente arquiteto em `C:\projetos\modelos-agents` **antes** de
construir, na fase de plano. O que sobe ao utilizador é a recomendação dele em
linguagem simples, com o custo e a consequência — não o debate técnico.

### Como perguntar, quando é mesmo preciso

- **No plano, não no fim.** Ambiguidade que muda o resultado e aparece a meio
  da implementação: parar e resolver ali. Nunca acumular para o relatório
  final — nessa altura o código já está escrito e a pergunta chega como
  fatura, não como decisão.
- **Uma pergunta de cada vez**, sem nome de ficheiro, variável ou código
  interno.
- **Sempre com recomendação e default:** "Vou seguir por X, que me parece
  melhor porque Y — diga se prefere Z."
- **A consequência em termos de uso, não de código.**

---

## Onde vive cada tipo de documento

| Diretório | O que é | Ciclo |
|---|---|---|
| `videos/` | O **produto**: dissertações, ecrãs e o índice `fontes-video.md` | Cresce a cada vídeo dissertado |
| `docs/plans/` | O que **talvez** se faça — backlog com prioridade | Entra por triagem ou observação; sai ao virar implementação |
| `docs/implementations/` | O que se **está a fazer** — contrato vivo, 1 branch por arquivo | Nasce após Plan Mode aprovado; morre na graduação |
| `docs/architecture/` | O que **já está feito** — espelho do código atual | Criado/atualizado na graduação |
| `docs/decisoes.md` | Decisões transversais, com data e motivo | Cronológico, nunca reescrito |

---

## Workflow de Implementação

Todo pedido de nova funcionalidade ou correção não-trivial **na ferramenta**
segue este ciclo. Os guias estão em `docs/implementations/`.

```
1. Plan Mode (obrigatório antes de qualquer código)
   → ler _guia-documentar-implementacao.md
   → diagnóstico: já existe? o que construir? riscos?
   → aguardar aprovação do utilizador

2. Criar a branch + worktree (feat/<slug> ou fix/<slug>)
   → propor o nome e pedir confirmação antes de criar
   → criar docs/implementations/<slug>.md

3. Implementar fase a fase
   → cada fase = 1 commit; hash registado no .md logo após o commit
   → relatório da fase em linguagem simples + oferta de validação, sempre com
     prompt de retomada pronto para colar

4. Validar os checks
   → marcar [x] com data; teste que revela problema vira nova fase (Plan Mode
     novamente)

5. Graduação (só quando TODOS os checks estão [x] ou [⏭️] justificados)
   → seguir _processo-graduacao-implementacao.md
   → migrar o que é arquitetural para docs/architecture/
   → triar "Ajustes Possíveis" → docs/implementations/ ou docs/plans/
   → git rm do arquivo + commit único de graduação
```

### Regras críticas

- **Nunca avançar para código sem plano aprovado.** Um pedido em forma de ordem
  direta ("implementa a transcrição do áudio") não dispensa o Passo 0 — é
  justamente aí que ele mais protege, porque um pedido assim costuma esconder
  várias escolhas que ninguém fechou.
- **Nunca graduar com checks `[ ]` em aberto.** `[⏭️]` justificado é permitido.
- **O arquivo .md é o contrato vivo da feature.**
- **Cada fase tem exatamente 1 commit.**
- **O commit não é o fim da fase.** O relatório em linguagem simples faz parte
  do fecho.

### Como se valida neste projeto

Não há testes automáticos. A validação é manual até existirem, e tem dois
níveis (ver a tabela de checks no guia):

- **Lógica (`L`)** — funções que se verificam sem internet, chamadas
  diretamente com uma entrada conhecida. A única verificação automática que
  existe hoje é `python -m py_compile scripts/*.py` (o código abre sem erro).
- **Ponta a ponta (`E`)** — correr o script ou a skill contra um vídeo real do
  YouTube e olhar para o que saiu. O vídeo de referência é o `vW9GhkTXmNU`
  (OfficeGest, webinar #2), já dissertado em `videos/officegest/`.

Correr os comandos a partir da raiz, com `PYTHONIOENCODING=utf-8`.

---

## Git workflow

Após cada fase concluída, criar um commit na branch da implementação antes de
encerrar a resposta.

### Estratégia de branch por implementação

Cada implementação vive na sua própria branch **e na sua própria worktree** —
sempre, mesmo quando é a única ativa. Isso existe para que a pasta principal
nunca seja tocada por trabalho de implementação (é nela que os vídeos são
dissertados), e para que duas sessões do Claude nunca colidam na mesma pasta
sem saber uma da outra.

**Onde vivem:** `.claude/worktrees/<tipo>/<slug>` — coberto pelo `.gitignore`.
`git worktree list` é a fonte de verdade do que está ativo; só a pasta
principal na lista significa nada em andamento.

**Criação:** depois do plano aprovado, `EnterWorktree(name="feat/<slug>")`.

> **O que a worktree tem e não tem.** As bibliotecas (`yt-dlp`, Pillow) estão
> instaladas no Python da máquina, por isso a worktree funciona logo, sem
> instalar nada. Mas a `videos/` dela só tem o que está no git: não tem
> `video.mp4`. Um teste ponta a ponta dentro da worktree descarrega o vídeo de
> novo e escreve na `videos/` **da worktree** — o que é o desejado: o resultado
> de um teste não se mistura com as dissertações reais, e desaparece com a
> worktree. Não commitar esses resultados de teste.

> **Sem remoto configurado.** `.claude/settings.json` define
> `worktree.baseRef: "head"` — a branch nasce do `main` local. Enquanto não
> houver remoto, a graduação termina no merge local, sem push.

> **Fallback:** se `EnterWorktree` recusar com "not in a git repository"
> (acontece quando a sessão arrancou antes do repo existir), criar à mão:
> `git worktree add .claude/worktrees/<tipo>/<slug> -b <tipo>/<slug> main`
> e depois `EnterWorktree(path=...)`.

**Quando graduada:** `ExitWorktree(action="keep")` → `git merge` local na branch
que a originou → `git worktree remove` + `git branch -d`. Merges sempre
sequenciais.

**Limpeza automática:** toda nova conversa que inspecionar `git worktree list`
remove worktrees cuja branch já esteja mergeada e sem mudanças pendentes. Se
houver trabalho não commitado, **não remover nada** — avisar o que ficou.

**Resolução de conflitos:** trabalho autónomo do Claude. Processo em
`docs/implementations/_guia-resolucao-conflitos.md`; ler sempre que um merge
reportar conflito. Única exceção para pausar: risco irreversível de perda de
dados. Depois de qualquer merge com conflito, escrever um relatório simples: o
que conflitou, o que cada lado queria, o que foi decidido, como reverter.

### Convenção de mensagem

Conventional Commits — `feat:`, `fix:`, `docs:`, `chore:`. No corpo: ficheiros
alterados, o que mudou em cada um, e a motivação.

### Regras

- Commitar sempre na branch da implementação em curso; vídeos dissertados vão
  direto para `main` (ver "Usar não é implementar")
- **Nunca** `--amend` em commits já publicados
- `git add` nos ficheiros específicos — nunca `git add -A`
- Sem alteração de ficheiros (apenas leitura/análise), **não criar commit**
- Nunca commitar `video.mp4`, folhas de miniaturas ou ficheiros `.env`
