# Mapa Geral de Arquitetura

Guia de navegação dos documentos de arquitetura. Use este ficheiro para decidir
qual doc ler antes de trabalhar numa área, e se deve atualizar um existente ou
criar um novo.

Para a visão global de componentes, ver [`_mapa-sistema.md`](_mapa-sistema.md).

---

## Documentos existentes e áreas cobertas

| Documento | Área | Atualizar quando... |
|---|---|---|
| [`ligacao-projetos-destino.md`](ligacao-projetos-destino.md) | Como a dissertação se liga às perguntas do projeto que serve: registo de destinos, leitura das perguntas, secção de ligação datada, revisão a pedido | Mudar o registo `videos/projetos-destino.md`, o passo 1b da skill, as regras da secção de ligação ou o modo "rever a ligação" |

Os docs de arquitetura são criados na **graduação** de implementações — não
antecipadamente. Um doc aqui é sempre um espelho de código que já existe e foi
validado, nunca uma intenção.

Onde vive o que ainda não tem doc de arquitetura:

| Tipo de informação | Onde vive hoje |
|---|---|
| Contexto, perfil do utilizador, fluxo de trabalho | [`CLAUDE.md`](../../CLAUDE.md) da raiz |
| Como usar a ferramenta e as regras da dissertação | [`README.md`](../../README.md) |
| Os passos que o Claude segue ao dissertar um vídeo | [`.claude/skills/dissertar-video/SKILL.md`](../../.claude/skills/dissertar-video/SKILL.md) |
| O que cada script faz e os seus parâmetros | O comentário no topo de cada ficheiro em `scripts/` |
| A recomendação de arquitetura original | `C:\projetos\modelos-agents\briefings\2026-10-01-dissertador-videos-youtube.md` |
| Decisões transversais | [`docs/decisoes.md`](../decisoes.md) |
| Features em construção | `docs/implementations/` |
| Melhorias futuras priorizadas | `docs/plans/` |

---

## Quando criar um doc novo

Na graduação de uma implementação, quando o Passo 3 de
[`_processo-graduacao-implementacao.md`](../implementations/_processo-graduacao-implementacao.md)
concluir que a feature introduz uma área de responsabilidade sem doc existente
— regra prática: mais de 3 conceitos distintos ou mais de 5 ficheiros
envolvidos.

Candidatos prováveis neste projeto, pela ordem em que deve crescer:

- **Extração e transcrição** — de onde vem o texto do vídeo, por que ordem se
  tentam as fontes, e como a dissertação marca a fonte. Nasce quando a
  transcrição do áudio for implementada: passa a haver duas fontes e uma regra
  entre elas.
- **Captura de ecrãs** — como se decide o que é um ecrã novo, o que cada
  constante controla, e o que distingue uma captura automática de uma manual.
- **Formato da base de conhecimento** — o que fica em `videos/`, e o que os
  outros projetos podem assumir ao lê-la. Nasce quando a skill passar a ser
  usada a partir de outras pastas. O registo de destinos, que também vive em
  `videos/`, já está em `ligacao-projetos-destino.md`.

**Formato:** `docs/architecture/<slug>.md` + uma linha na tabela acima.

---

## Regra de escrita dos docs de arquitetura

- Espelho do **estado atual** do código — enxuto e confiável
- Sem histórico ("antes era X, agora é Y") — isso fica no git log
- Ao atualizar, reescrever a secção afetada, não acrescentar parágrafos
