# Mapa do Sistema — Arquitetura Geral

Visão global dos componentes: o que existe hoje e o que está previsto. Ler
antes de trabalhar numa área desconhecida, ou para perceber onde uma mudança
vai ter impacto.

Para saber qual **doc de arquitetura** ler por área, ver
[`_overview.md`](_overview.md). Para o contexto e o fluxo de trabalho, ver
[`CLAUDE.md`](../../CLAUDE.md) na raiz — este ficheiro não o repete.

**Estado:** fase inicial, a funcionar. As três fases iniciais (texto, ecrãs e
skill) estão concluídas, e a dissertação é escrita com as perguntas atuais do
projeto que serve. Há quatro vídeos dissertados, todos do OfficeGest. A
ferramenta também prepara gravações que estão no disco, com a fala
transcrita na própria máquina. Vídeos do YouTube sem legendas ainda não têm
transcrição. Não há testes automáticos.

---

## Como as peças se encadeiam

```
link do YouTube
   │
   ▼
scripts/extrair_video.py ──► metadados.json + transcricao.txt
   │                          (código de saída 2 = vídeo sem legendas)
   ▼
videos/projetos-destino.md ► que projeto o assunto serve; as perguntas em
   │                          aberto desse projeto são lidas por inteiro
   ▼
scripts/capturar_ecras.py ─► video.mp4 + ecras/MM-SS.jpg + ecras/indice.json
   │                          + ecras/folhas/ (miniaturas para revisão)
   ▼
Claude Code, pela skill dissertar-video
   lê a transcrição, revê as folhas, abre os ecrãs-chave em tamanho real
   (os que tocam numa pergunta do projeto são sempre ecrãs-chave)
   │
   ▼
dissertacao.md  +  uma linha em videos/fontes-video.md
```

A pedido, a skill também **revê a ligação** de vídeos já dissertados às
perguntas de hoje, sem repetir a extração nem a captura. O detalhe está em
[`ligacao-projetos-destino.md`](ligacao-projetos-destino.md).

Há um segundo caminho, para **gravações locais** (ficheiros no disco, que
podem ter dados reais). Não passa pelo YouTube nem deixa nada nesta pasta:

```
ficheiro de vídeo no disco
   │
   ▼
scripts/preparar_local.py ───► metadados.json numa pasta fora do git
   │
   ▼
scripts/transcrever_audio.py ► transcricao.txt (feita na máquina, sem rede)
   │
   ▼
scripts/capturar_ecras.py ───► ecras/ + ecras/folhas/ (lê o ficheiro local)
   │
   ▼
o projeto que pediu escreve a sua análise
```

O detalhe está em [`gravacoes-locais.md`](gravacoes-locais.md).

Os scripts fazem a parte que dá sempre o mesmo resultado. Ler imagens e
escrever é feito pelo próprio Claude Code na sessão, sem chave de API.

---

## Componentes

### `scripts/`

Python 3.13, sem ambiente virtual: `yt-dlp`, Pillow e `faster-whisper`
instalados no Python da máquina; `ffmpeg` e `ffprobe` no PATH.

| Ficheiro | Responsabilidade |
|---|---|
| `extrair_video.py` | Lê os dados do vídeo com o `yt-dlp`, escolhe a melhor legenda (manual antes de automática; idioma do vídeo, depois pt-PT, pt, pt-BR, en), agrupa a fala em blocos de ~30 s e cria a pasta `videos/<assunto>/<título>/` |
| `capturar_ecras.py` | Descarrega o vídeo sem som (até 1080p), deteta mudanças de ecrã com o `ffmpeg`, garante pelo menos uma captura por minuto, descarta imagens quase iguais e monta as folhas de miniaturas. Com `--em`, extrai instantes pedidos à mão. Numa gravação local lê o ficheiro onde ele está, sem descarregar |
| `preparar_local.py` | Regista os dados de um ficheiro de vídeo do disco numa pasta de destino. Recusa uma pasta versionada e avisa quando o som acaba antes da imagem |
| `transcrever_audio.py` | Transcreve na máquina a fala de uma gravação local, sem rede, em blocos de ~30 s. Mede o tempo, a fala e as frases repetidas. Descarregar o modelo é um comando à parte |

### `.claude/skills/dissertar-video/`

| Ficheiro | Responsabilidade |
|---|---|
| `SKILL.md` | Os passos, pela ordem certa, que o Claude segue ao receber um link: escolher o assunto, extrair, ler as perguntas do projeto de destino, capturar e rever os ecrãs, escrever a dissertação com as regras de data e de hipótese, e atualizar o índice. Tem um segundo modo, "rever a ligação", para vídeos já dissertados, e um terceiro, "gravação local com dados reais", que só prepara o material e não deixa nada nesta pasta |

A skill só é carregada com o Claude Code aberto nesta pasta.

---

## Dados

Tudo o que a ferramenta produz a partir do YouTube fica em
`videos/<assunto>/<título-do-vídeo>/`. Não há base de dados. O que produz a
partir de uma gravação local (`metadados.json`, `transcricao.txt`, `ecras/`)
fica **fora desta pasta e fora do git**, na pasta que o projeto de destino
indicar.

| Ficheiro | O que é | No git? |
|---|---|---|
| `metadados.json` | Link, título, canal, data de publicação, duração, capítulos, origem da legenda | Sim |
| `transcricao.txt` | A fala em blocos de ~30 s com o minuto de início | Sim |
| `ecras/MM-SS.jpg` | Um ecrã por mudança relevante — são a prova que a dissertação embute | Sim |
| `ecras/indice.json` | Lista dos ecrãs, com o instante e a origem de cada um | Sim |
| `ecras/folhas/` | Miniaturas, 9 por folha, só para revisão | Não — voltam a gerar-se |
| `video.mp4` | O vídeo descarregado, só para capturas extra | Não — ~120 MB por 45 min, volta a descarregar-se |
| `dissertacao.md` | O resultado: o que o vídeo ensina, com ficha de busca no topo | Sim |

Na raiz de `videos/`, dois ficheiros valem para todos os vídeos:

| Ficheiro | O que é | No git? |
|---|---|---|
| `fontes-video.md` | O índice de todos os vídeos, por assunto. É por ele que os outros projetos entram | Sim |
| `projetos-destino.md` | O registo que diz, por assunto, que projeto as dissertações servem e onde esse projeto guarda as perguntas em aberto | Sim |

### Fontes externas

| Fonte | Para quê | Conta ou custo |
|---|---|---|
| YouTube, através do `yt-dlp` | Dados do vídeo, legendas e o próprio vídeo | Nenhum |
| Ficheiros de perguntas do projeto de destino, noutra pasta da máquina | Saber o que procurar no vídeo e preencher a secção de ligação | Nenhum. Só leitura |
| Hugging Face, através do `faster-whisper` | Descarregar uma vez o modelo de transcrição (cerca de 1,6 GB). A transcrição em si corre sem rede | Nenhum |

O `yt-dlp` deixa de funcionar de tempos a tempos, quando o YouTube muda. O
primeiro passo perante um erro de extração é atualizá-lo:
`python -m pip install -U yt-dlp`.

---

## Quem consome

| Projeto | Como |
|---|---|
| `C:\projetos\winners-group` | Lê as dissertações do assunto `officegest`. A instrução a colar no `CLAUDE.md` do projeto consumidor está no [`README.md`](../../README.md). Usa também os scripts para preparar as suas gravações locais, com a saída em `dados/gravacoes/` desse projeto |

A relação tem dois sentidos: o consumidor lê as dissertações, e o dissertador
lê as perguntas em aberto do consumidor, pelos caminhos de
`videos/projetos-destino.md`. O dissertador nunca edita o projeto consumidor:
a dissertação marca as divergências, e o utilizador aponta o outro projeto
para ela.

---

## Previsto, ainda não existe

À medida que o sistema crescer, cada novo componente entra nas tabelas acima
na graduação da implementação que o criou.

| Componente | Estado |
|---|---|
| Transcrição do áudio para vídeos do YouTube sem legendas | No backlog — [`melhorias-futuras.md`](../plans/melhorias-futuras.md), M1. Para gravações locais já existe |
| Skill disponível a partir de qualquer projeto | No backlog — [`melhorias-futuras.md`](../plans/melhorias-futuras.md), M2 |

---

## Manutenção

Este ficheiro é atualizado nos Passos 3 e 4 de
[`_processo-graduacao-implementacao.md`](../implementations/_processo-graduacao-implementacao.md),
sempre que uma implementação graduada acrescenta um script, um serviço externo
ou um tipo de ficheiro. Um mapa que mente é pior do que um mapa que não existe.
