# Preservar as capturas manuais quando a captura é repetida

> **Este arquivo é um exemplo, não uma implementação real.** Mostra o nível de
> detalhe esperado num arquivo de `docs/implementations/`. O problema descrito
> existe mesmo no código e está registado em
> [`docs/plans/melhorias-futuras.md`](../plans/melhorias-futuras.md) (M3), mas
> **nada disto foi construído**: os commits, as datas e os resultados dos
> checks abaixo são ilustrativos.

**Componente:** script de captura (`scripts/capturar_ecras.py`)
**Branch:** `fix/preservar-capturas-manuais`
**Status:** Todos os cenários validados (exemplo)

---

## Motivação

Quando a captura automática gera ecrãs a mais, a skill manda repetir com
`--limiar 0.15`. Quando falta um instante, manda pedir esse instante com
`--em 12:30`. O problema aparece quando as duas coisas acontecem pela ordem
errada: se alguém pede um instante à mão e depois repete a captura, o ecrã
pedido à mão desaparece sem aviso — e a dissertação que já o embutia fica com
uma imagem partida.

Comportamento desejado: repetir a captura substitui só o que a captura
automática produziu; o que foi pedido à mão fica.

---

## Problemas Identificados (estado anterior) (*)

1. **A repetição apaga tudo:** `scripts/capturar_ecras.py:147-148` apaga todos
   os `.jpg` de `ecras/` antes de recomeçar, sem distinguir a origem.
2. **As capturas manuais não ficam registadas:** o ramo `--em`
   (`scripts/capturar_ecras.py:139-145`) grava a imagem mas não a acrescenta a
   `ecras/indice.json`. Nada no disco diz que aquela imagem foi pedida à mão.

---

## Abordagem (*)

O `indice.json` passa a ser a fonte de verdade sobre a origem de cada ecrã. O
ramo `--em` regista cada captura com `"origem": "manual"`. Ao repetir a
captura automática, o script lê o índice anterior, guarda as entradas manuais,
apaga só as restantes, e no fim junta as manuais ao índice novo, por ordem de
instante.

**Descartado:** guardar as capturas manuais numa subpasta `ecras/manuais/`.
Seria mais simples de implementar, mas mudaria o caminho das imagens, e as
dissertações já escritas embutem `ecras/MM-SS.jpg`. Uma mudança que parte
ligações em documentos já entregues não compensa.

---

## Plano de Implementação (*)

### Fase 1 — Registar a origem manual e preservá-la

**Objetivo:** repetir a captura deixa de apagar os ecrãs pedidos com `--em`.

| Ficheiro | O que muda |
|---|---|
| `scripts/capturar_ecras.py` | O ramo `--em` acrescenta a entrada ao `indice.json` com origem `manual`; a limpeza inicial poupa os arquivos com essa origem; o índice final junta as duas listas |
| `.claude/skills/dissertar-video/SKILL.md` | Passo 2: dizer que as capturas pedidas com `--em` sobrevivem à repetição |

### Commits Fase 1

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `a1b2c3d` | Origem `manual` no índice e limpeza seletiva |

### Relatório da Fase 1 — o que mudou na prática

**Antes:** pedir um ecrã à mão e depois repetir a captura apagava o ecrã
pedido, e a dissertação ficava com uma imagem em falta.
**Agora:** os ecrãs pedidos à mão ficam. Repetir a captura só troca os que a
captura automática tinha escolhido.
**Para validar:** Cenários L1 e E1.

---

## Checks de Validação (*)

| Prefixo | O que verifica | Como |
|---|---|---|
| `L` | Lógica pura | Sem internet: chamar a função com uma entrada conhecida e comparar o resultado |
| `E` | Ponta a ponta | Correr o script ou a skill contra um vídeo real do YouTube e olhar para o que saiu em `videos/` |

### Cenário L1 — O índice junta manuais e automáticas por ordem de instante

Setup: um índice com duas entradas manuais (02:10 e 15:00) e três automáticas
(00:05, 08:00, 20:00).

- [x] O índice final tem as cinco, pela ordem 00:05, 02:10, 08:00, 15:00, 20:00
- [x] As duas manuais mantêm `"origem": "manual"`
- **Validado em:** (exemplo) — resultado igual ao esperado

### Cenário E1 — Repetir a captura mantém o ecrã pedido à mão

Setup: vídeo `https://www.youtube.com/watch?v=vW9GhkTXmNU`, já extraído.

```
python scripts/capturar_ecras.py videos/officegest/webinar-2-contabilidade-officegest
python scripts/capturar_ecras.py videos/officegest/webinar-2-contabilidade-officegest --em 12:30
python scripts/capturar_ecras.py videos/officegest/webinar-2-contabilidade-officegest --limiar 0.15
```

- [x] `ecras/12-30.jpg` existe depois do terceiro comando
- [x] `ecras/indice.json` tem a entrada 12:30 com origem `manual`
- [ ] ~~As folhas de miniaturas mostram o ecrã 12-30~~ → falhou, ver Fase 2
- **Validado em:** (exemplo) — o ecrã ficou, mas não aparecia em nenhuma folha

---

## Fase 2 — As folhas de miniaturas ignoravam as capturas manuais

**Nasceu do Cenário E1.** O ecrã pedido à mão sobrevivia, mas não aparecia nas
folhas de miniaturas — e é pelas folhas que a skill revê o vídeo. Na prática o
ecrã existia e ninguém o via.

**Causa raiz:** as folhas eram montadas a partir da lista de capturas
automáticas da execução corrente (`scripts/capturar_ecras.py:173`), e não a
partir do índice final já com as manuais.

**Objetivo:** as folhas mostram tudo o que está no índice.

| Ficheiro | O que muda |
|---|---|
| `scripts/capturar_ecras.py` | As folhas passam a ser montadas a partir do índice final; o ramo `--em` volta a montar as folhas depois de acrescentar a captura |

### Commits Fase 2

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `d4e5f6a` | Folhas montadas a partir do índice final |

### Relatório da Fase 2 — o que mudou na prática

**Antes:** um ecrã pedido à mão ficava guardado mas não aparecia nas folhas de
revisão.
**Agora:** aparece na folha, no lugar certo pela ordem dos minutos, assim que é
pedido.
**Para validar:** Cenário E2.

### Cenário E2 — O ecrã manual aparece na folha

Setup: o mesmo do E1, depois do terceiro comando.

- [x] A folha que cobre o minuto 12 mostra a miniatura `12-30`
- [x] Pedir outro instante com `--em 15:40` atualiza a folha sem repetir a captura inteira
- **Validado em:** (exemplo) — miniatura presente em `folha-05.jpg`

---

## Ajustes Possíveis Pós-Implementação

- **Não há forma de remover uma captura manual** a não ser apagar o arquivo e
  a linha do índice à mão. Um `--remover 12:30` resolveria.
- **Vídeos capturados antes desta mudança** não têm a origem `manual` no
  índice: a primeira repetição ainda apaga as capturas manuais antigas. Só
  afeta o vídeo do OfficeGest, que não tem nenhuma.
