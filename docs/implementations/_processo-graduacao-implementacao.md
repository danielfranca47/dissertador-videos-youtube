# Processo de Graduação: Implementação → Arquitetura

Quando um arquivo de `docs/implementations/` está **completo e validado**, o
seu conteúdo é "graduado" para os docs de arquitetura em `docs/architecture/`.

Isto garante que os docs de arquitetura são sempre um espelho do código real,
e que os arquivos de implementação — documentos de trabalho temporários — são
limpos quando já não são necessários.

---

## Quando executar

Executar quando **todas** estas condições forem verdadeiras:

1. O arquivo tem `**Status:** Todos os cenários validados`
2. Todos os checks obrigatórios estão `[x]` (checks pulados com justificativa
   `[⏭️]` são aceitáveis)
3. Não há fases adicionais abertas

Se algum check ainda estiver `[ ]`, o arquivo **não está pronto**.

---

## Passo 1 — Identificar que áreas foram afetadas

Ler o arquivo de implementação e listar as áreas alteradas. Usar
[`_mapa-sistema.md`](../architecture/_mapa-sistema.md) como referência.

| A implementação afetou... | Área no mapa |
|---|---|
| `scripts/extrair_video.py`, ou de onde vem o texto do vídeo | Extração e transcrição |
| `scripts/capturar_ecras.py`, ou como se escolhem os ecrãs | Captura de ecrãs |
| A skill `dissertar-video`, ou as regras da dissertação | Escrita da dissertação |
| O que fica em `videos/` e como outro projeto o encontra | Formato da base de conhecimento |

---

## Passo 2 — Ler os docs de arquitetura relevantes

Ler [`_overview.md`](../architecture/_overview.md) para identificar quais
documentos cobrem as áreas do Passo 1. Ler cada doc relevante **na íntegra**
antes de alterar — o objetivo é perceber o que já está documentado e o que
falta.

---

## Passo 3 — Decidir: atualizar existente ou criar novo

### Atualizar um doc existente quando:
- A implementação altera ou estende uma área já coberta
- É uma nova funcionalidade dentro de um domínio existente

**Como atualizar:** reescrever apenas as secções afetadas. Sem parágrafos de
"antes era X, agora é Y" — sem histórico de implementação no corpo. O
resultado é um espelho do código atual, enxuto e confiável.

### Criar um novo doc quando:
- A implementação introduz uma área de responsabilidade sem doc existente
- A feature é grande demais para caber como secção (regra prática:
  >3 conceitos distintos ou >5 arquivos envolvidos)

**Formato:** `docs/architecture/<slug>.md`
**Atualizar** `_overview.md` com uma linha na tabela.
**Atualizar** `_mapa-sistema.md` se a mudança acrescenta um script, um serviço
externo ou um tipo de ficheiro em `videos/` que ainda não está mapeado.

---

## Passo 4 — Fazer as atualizações

**Checklist antes de fechar:**
- [ ] Todos os novos comportamentos e regras estão refletidos?
- [ ] `_mapa-sistema.md` precisa de novo script, serviço ou tipo de ficheiro?
- [ ] `_overview.md` precisa de nova linha na tabela?
- [ ] Algum doc ficou desatualizado (algo que era verdade deixou de ser)?
- [ ] O `README.md` e a skill `dissertar-video` continuam a dizer a verdade
      sobre como se usa a ferramenta? (Requisitos, comandos, o que acontece
      com vídeos sem legendas.)
- [ ] Houve decisão transversal — um custo aceite, um serviço adotado, uma
      regra da dissertação alterada? Se sim, entra em
      [`docs/decisoes.md`](../decisoes.md).

---

## Passo 5 — Triagem de "Ajustes Possíveis"

Antes de deletar o arquivo, verificar a secção final de sugestões não
implementadas (`## Ajustes Possíveis Pós-Implementação` ou equivalente). Se
não existir ou estiver vazia, saltar para o Passo 6.

**Por quê:** esta secção acumula boas sugestões que seriam perdidas ao
deletar o arquivo, sem nenhuma decisão explícita. Este passo garante que nada
é descartado silenciosamente.

1. **Extrair e listar** cada sugestão como item numerado, em linguagem simples.
2. **Perguntar ao utilizador quais são válidos.** Aceitar "todos", "nenhum"
   ou lista específica. Itens descartados ficam de fora, sem registo.
3. **Para cada item validado, perguntar a prioridade:**
   - **Urgente** → novo arquivo em `docs/implementations/`, criado seguindo
     [`_guia-documentar-implementacao.md`](_guia-documentar-implementacao.md)
     com `**Status:** Aguardando Plan Mode`. Isto **não substitui** o Plan
     Mode obrigatório — a implementação real só começa depois do diagnóstico.
     Referenciar a origem na Motivação: "Surgiu como 'Ajuste possível' na
     graduação de `<arquivo>.md`."
   - **Não-urgente** → registar em `docs/plans/` com prioridade declarada
     ALTA/MÉDIA/BAIXA (ver [`docs/plans/README.md`](../plans/README.md))
4. **Confirmar** o resumo (item → destino) antes de prosseguir.

---

## Passo 6 — Deletar o arquivo de implementação

```bash
git rm docs/implementations/<nome-do-arquivo>.md
```

**O que NÃO precisa migrar:**
- Histórico de fases e diagnósticos — pertence ao git log
- Trechos de código antes/depois — visível no git diff
- Notas de testes com datas — ficam nos commits
- "Ajustes Possíveis" — já tratados no Passo 5

**O que SIM precisa migrar:**
- Regras e comportamentos não-óbvios (por exemplo: de onde vem o texto quando
  não há legendas, e como isso fica marcado na dissertação)
- O formato do que fica em `videos/`, e o que outros projetos assumem sobre ele
- Custos, limites e contas de serviços externos
- Variáveis de ambiente e invariantes — as afirmações do tipo "quando X
  acontece, Y deixa de ser confiável", que ninguém redescobre lendo o código

---

## Passo 7 — Commit único

Um único commit com tudo: docs atualizados, docs criados, arquivo(s) de
implementação removido(s).

```
docs: graduar <nome-da-feature> → atualizar architecture

- <arquivo>.md: <o que foi atualizado>
- <outro>.md: criado (nova área: <descrição>)
- Removido: docs/implementations/<arquivo>.md (todos os testes validados)
```

---

## Passo 8 — Merge de volta

Depois do commit de graduação, fechar a branch e a worktree (ver `CLAUDE.md`,
"Estratégia de branch por implementação"):

1. `ExitWorktree(action="keep")` — volta a sessão para a pasta principal (ou,
   se a implementação era aninhada, para a worktree da branch pai), deixando
   worktree e branch intactas por enquanto.
2. Nessa pasta: `git merge` local da branch da implementação na branch que a
   originou — sem PR.
3. Validar na pasta principal: `python -m py_compile scripts/*.py`.
4. Limpeza final: `git worktree remove .claude/worktrees/<tipo>/<slug>` +
   `git branch -d <branch>`.

> **Sem remoto.** Este repositório só existe neste computador, por isso não há
> `git push`. Se um dia for configurado um remoto, acrescentar o push entre os
> passos 3 e 4, e retirar `worktree.baseRef` de `.claude/settings.json`.

Merges são sempre **sequenciais**, nunca simultâneos. Se duas branches
estiverem prontas ao mesmo tempo, mergear uma primeiro; só depois a segunda,
resolvendo ali qualquer conflito (ver
[`_guia-resolucao-conflitos.md`](_guia-resolucao-conflitos.md)).

---

## Manutenção deste processo

Se o processo mudar (nova convenção de naming, novo tipo de doc, novo passo),
atualizar este arquivo para refletir o padrão atual.
