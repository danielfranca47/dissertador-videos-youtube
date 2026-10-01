# Guia: Como Resolver Conflitos de Merge

> Referenciado por [`CLAUDE.md`](../../CLAUDE.md), secção "Estratégia de
> branch por implementação" → "Resolução de conflitos". Ler sempre que um
> `git merge` (Passo 8 de
> [`_processo-graduacao-implementacao.md`](_processo-graduacao-implementacao.md))
> reportar conflito.

---

## Por que este guia existe

O utilizador não vai decidir qual lado de um conflito manter — nem é essa a
expectativa. **Claude resolve todo conflito sozinho, sempre**, usando os
critérios abaixo, e só depois explica em português simples o que aconteceu, o
que foi decidido e como reverter. Não há passo de "aguardar decisão do
utilizador" no meio do processo — a única exceção está na secção 5.

---

## 0. Configuração (já aplicada neste repositório)

```bash
git config merge.conflictStyle zdiff3
```

Inclui o **ancestral comum** nos marcadores — a versão do trecho antes de
qualquer branch mexer nele:

```
<<<<<<< HEAD (branch atual)
...conteúdo da branch atual...
||||||| (ancestral comum)
...conteúdo original...
=======
...conteúdo da branch que está sendo mergeada...
>>>>>>> feat/nome-da-branch
```

Sem isso só se vê "lado A" e "lado B", sem saber a intenção original de cada
um — com o ancestral visível dá para distinguir mudanças complementares
(mecânico) de contraditórias (comportamento). É configuração local, não
versionada: cada clone precisa rodar o comando uma vez.

---

## 1. Ao detectar o conflito

- `git status` — lista os arquivos em conflito (`both modified`)
- `git diff --name-only --diff-filter=U` — só os conflitantes
- `git diff --ours -- <arquivo>` / `git diff --theirs -- <arquivo>` — isola o
  que cada lado mudou em relação ao ancestral

---

## 2. Classificar o conflito

### Mecânico

O git não juntou automaticamente por proximidade no arquivo, mas as mudanças
**não se contradizem** — duas funções novas na mesma área, dois imports
próximos, duas linhas numa tabela markdown no mesmo ponto.

**Resolução:** manter as duas, remover os marcadores.

### Comportamento / regra

As duas branches mudaram a **mesma regra, valor ou cálculo** de forma
incompatível. Exemplos concretos neste projeto:

- Duas branches mudam a mesma constante de captura (`LIMIAR_CENA`,
  `INTERVALO_MAXIMO`, `DISTANCIA_MINIMA`) com valores diferentes
- Duas branches mudam a ordem de preferência das legendas, ou de onde vem o
  texto quando não há legendas
- Duas branches alteram a mesma regra da dissertação na skill (o aviso de
  idade, quando usar ❓, de onde vêm os nomes de menus)
- Duas branches mudam o formato do mesmo ficheiro em `videos/`
  (`metadados.json`, `indice.json`) — ver secção 6

**Regra:** a classificação decide qual critério da secção 3 usar — não decide
se Claude pausa. Ambos são resolvidos sozinho, sem exceção fora da secção 5.

---

## 3. Heurística de decisão (conflitos de comportamento)

Aplicar esta ordem até um critério decidir:

1. **Segurança/conservadorismo primeiro.** Preferir o que falha de forma mais
   segura: o que não apaga ecrãs nem dissertações já produzidos, o aviso que
   aparece em mais casos, a regra que marca mais coisas como hipótese ou ❓ em
   vez de as afirmar. É mais fácil relaxar uma regra estrita depois do que
   descobrir que uma dissertação afirmou algo que o vídeo não mostrava.
2. **Intenção mais recente vence.** Se nenhum lado é claramente mais seguro,
   desempatar pelo commit mais recente
   (`git log -1 --format=%cI <hash>` de cada lado).
3. **Se a mudança tem impacto em custo** (chamadas a um serviço pago) e os
   critérios 1–2 não resolvem com confiança — **ainda assim resolver**, pelo
   lado que gasta menos, mas marcar com destaque no relatório pós-merge (7.2)
   para o utilizador poder corrigir com uma frase.

---

## 4. Resolver

1. Editar aplicando a escolha (mecânico: manter as duas; comportamento:
   aplicar a heurística)
2. `git add <arquivo>`
3. Validar (7.1) antes de finalizar
4. `git commit` (finaliza o merge)
5. Escrever o relatório pós-merge (7.2) — obrigatório, mesmo em conflitos
   triviais

### Nunca fazer

- `git checkout --ours/--theirs <arquivo>` sem entender o que se descarta —
  descarta um lado inteiro; só depois de a heurística decidir que um lado
  inteiro perde mesmo
- Commitar com marcadores de conflito no arquivo
- `--no-verify` para forçar o commit do merge

### Se a resolução ficar confusa tecnicamente

`git merge --abort` volta ao estado anterior sem risco. Usar sempre que a
resolução não estiver clara, e replanejar. Abortar não é falha — é a opção
segura em dúvida técnica genuína.

---

## 5. Quando ainda assim pausar (exceção)

Única situação: **risco real e irreversível de perda de dados**, onde nenhuma
das duas opções é claramente segura — tipicamente duas versões diferentes de
lógica que apaga ou sobrescreve ficheiros em `videos/`.

Mesmo aí, a pergunta é concreta, não-técnica, e já vem com uma opção padrão:

> "Encontrei um conflito envolvendo [o quê, em termos simples]. Não dá para
> saber com segurança qual versão está certa sem arriscar o que já foi
> produzido. Vou seguir com [opção X] a menos que prefira [opção Y] — pode
> confirmar?"

Fora deste caso, **não pausar** — resolver, validar e reportar depois.

---

## 6. Casos especiais deste repositório

> Esta secção é a que mais rende ser mantida à medida que o projeto cresce:
> cada vez que um conflito custar a decidir, acrescentar aqui o caso e o
> critério usado.

- **`videos/fontes-video.md` e as pastas de vídeos** — um vídeo dissertado em
  `main` enquanto uma branch estava aberta acrescenta linhas ao índice. É
  sempre mecânico: manter todas as linhas, pela ordem do índice (do mais
  recente para o mais antigo dentro de cada assunto). Uma branch de
  implementação não deve trazer dissertações de teste; se trouxer, o lado de
  `main` vence.
- **Formato dos ficheiros em `videos/`** — se as duas branches mudaram o mesmo
  campo de `metadados.json` ou de `indice.json`, o conflito é sobre o que os
  vídeos já dissertados e os outros projetos podem assumir. Tratar como
  comportamento, nunca mecânico, e destacar no relatório.
- **A skill e os scripts descrevem o mesmo passo** — se uma branch mudou um
  script e a outra mudou o passo da skill que o chama, o git pode não reportar
  conflito nenhum e o resultado ficar incoerente. Depois de qualquer merge que
  toque `scripts/` ou a skill, reler os dois lado a lado.
- **Funções puras** — duas funções novas: mecânico. Mesma função alterada dos
  dois lados: comportamento.
- **`docs/architecture/*.md`** — não juntar os dois textos linha a linha.
  Reescrever a secção afetada como espelho do estado atual do código
  pós-merge — mesma regra do processo de graduação.
- **`docs/implementations/<arquivo>.md`** — cada implementação tem a própria
  branch, então normalmente não há conflito. Se acontecer, tende a ser
  mecânico: o padrão do guia é sempre *acrescentar* secções de fase, nunca
  reescrever.
- **`CLAUDE.md` e `docs/plans/`** — se as duas branches acrescentaram regras ou
  itens diferentes, manter os dois.

---

## 7. Validar e relatar

### 7.1 Validar antes de finalizar

- Se o merge tocou código: correr `python -m py_compile scripts/*.py` antes do
  commit final. Não há testes automáticos, por isso, se o conflito foi de
  comportamento, repetir à mão o check do arquivo de implementação que cobre a
  área em conflito. Conflitos resolvidos sem erro do git ainda podem quebrar
  comportamento — **conflito semântico**: o merge "abre" mas o resultado não
  faz o que nenhuma das duas branches pretendia.
- Buscar marcadores esquecidos:
  `grep -rn "<<<<<<<\|=======\|>>>>>>>" <arquivos-resolvidos>`

### 7.2 Relatório obrigatório pós-merge

Depois de qualquer merge com conflito, escrever sempre um resumo em português
simples, sem jargão de código:

1. **O que conflitou** — em que área, numa frase, em termos de uso e não de
   ficheiros
2. **O que cada lado tentava fazer** — sem mostrar código
3. **O que foi decidido e por quê** — qual critério da secção 3 foi usado
4. **Como reverter** — normalmente basta pedir; Claude cuida da mecânica

Este relatório substitui a pergunta prévia — é como o utilizador mantém
controlo sobre o resultado sem precisar entender o processo técnico.

---

## 8. Prevenção

- Branches curtas — já é regra (graduação assim que os checks passam)
- Merges sempre sequenciais, nunca simultâneos
- Branch aberta há muito tempo: sincronizar periodicamente com a original
  (merge da original nela) — conflitos pequenos e frequentes são mais fáceis
  que um grande no fim
