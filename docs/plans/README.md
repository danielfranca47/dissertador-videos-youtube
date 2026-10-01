# docs/plans — Como usar

Camada de **intenção**: melhorias identificadas que ainda não entraram no
ciclo de implementação. Nada aqui é compromisso — é backlog priorizado.

Distinção rápida:

| Diretório | O que é |
|---|---|
| `docs/plans/` | O que **talvez** se faça — melhorias futuras, com prioridade |
| `docs/implementations/` | O que se **está a fazer** — contrato vivo, uma branch por arquivo |
| `docs/architecture/` | O que **já está feito** — espelho do código atual |

---

## De onde vêm os itens

1. **Triagem de graduação** — Passo 5 de
   [`_processo-graduacao-implementacao.md`](../implementations/_processo-graduacao-implementacao.md):
   itens da secção "Ajustes Possíveis" que o utilizador validou como
   não-urgentes.
2. **Observação direta** — uma falha notada ao dissertar um vídeo, ou uma
   ideia que surge numa conversa e não vai ser implementada agora.

---

## Formato

**Nome do arquivo:** `<tema-descritivo>.md`
Ex.: [`melhorias-futuras.md`](melhorias-futuras.md)

```markdown
# Título do tema

> Contexto: de onde veio este documento (ex.: graduação de `<arquivo>.md`).

## M1 — Nome da melhoria

**Prioridade: ALTA / MÉDIA / BAIXA**

Descrição do problema e do que precisa mudar. Citar arquivos ou
comportamentos relevantes se já souber. Se custar dinheiro ou exigir uma
conta, dizer quanto e qual.
```

Enquanto o backlog for pequeno, tudo vive em `melhorias-futuras.md`:
**acrescentar** como novo `M<n>` em vez de criar outro arquivo. Um tema só
ganha arquivo próprio quando juntar três ou mais itens.

---

## Prioridade

Declarada por quem regista o item, ajustável a qualquer momento:

- **ALTA** — corrige algo que já atrapalha o uso, ou desbloqueia outra coisa
- **MÉDIA** — melhoria clara de valor, sem urgência
- **BAIXA** — bom ter; entra se sobrar espaço

Um item pode dizer **o que o faz subir de prioridade** ("sobe para ALTA no
primeiro vídeo sem legendas"). É a forma de adiar sem esquecer.

---

## Como um item sai daqui

Quando o utilizador escolher implementá-lo: segue o ciclo normal de
[`_guia-documentar-implementacao.md`](../implementations/_guia-documentar-implementacao.md)
— Plan Mode primeiro, depois branch + worktree + arquivo de implementação. O
item é removido deste arquivo quando a implementação correspondente é criada
(não quando é graduada), para o backlog não mostrar como pendente algo que já
está em curso.

Arquivos prefixados com `_` são guias permanentes do processo — nunca
deletados na limpeza de planos.
