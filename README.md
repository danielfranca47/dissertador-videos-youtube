# Dissertador de vídeos do YouTube

Transforma um vídeo do YouTube num `.md` detalhado, que serve de base de conhecimento para projetos do Claude Code. Também prepara gravações que estão no disco (transcrição feita no computador e ecrãs), para outro projeto as analisar.

A recomendação de arquitetura está em `C:\projetos\modelos-agents\briefings\2026-10-01-dissertador-videos-youtube.md`; a das gravações locais, em `C:\projetos\modelos-agents\briefings\2026-10-08-dissertador-gravacoes-locais.md`.

## Como usar

Abra o Claude Code nesta pasta e cole o link do vídeo, ou escreva:

```
/dissertar-video <link-do-youtube> [projeto de destino]
```

A skill [`.claude/skills/dissertar-video`](.claude/skills/dissertar-video/SKILL.md) faz os passos abaixo pela ordem certa e escreve a dissertação com as regras de data e de hipótese.

### Para que projeto é o vídeo

Cada **assunto** pode servir um projeto. O registo [`videos/projetos-destino.md`](videos/projetos-destino.md) diz qual, e onde esse projeto guarda as suas perguntas em aberto. Antes de olhar para os ecrãs, a skill lê essas perguntas por inteiro, para procurar no vídeo o que o projeto precisa de saber nesse dia. A dissertação termina com uma tabela "o que este vídeo pode responder", com a data em que as perguntas foram consultadas.

- **Assunto novo:** a skill pergunta uma vez que projeto ele serve (pode ser nenhum) e guarda a resposta no registo.
- **Outro projeto só para um vídeo:** indique-o no pedido, depois do link.
- A skill **só lê** o projeto de destino; nunca o edita.

### Rever os vídeos antigos quando as perguntas mudam

As perguntas de um projeto mudam, e a tabela de cada dissertação é o retrato do dia em que foi escrita. Para a pôr em dia, peça:

```
revê os vídeos do <assunto> com as perguntas atuais
```

A skill volta à transcrição e aos ecrãs já guardados de cada vídeo do assunto e reescreve **só** a tabela de ligação e a lista de pontos a verificar. O resto da dissertação não muda. Só acontece a pedido.

### Os passos, se quiser correr à mão

1. Extrair os dados e a transcrição do vídeo:
   ```
   python scripts/extrair_video.py <link-do-youtube> --tema <assunto>
   ```
   Cria `videos/<assunto>/<titulo-do-video>/` com `metadados.json` e `transcricao.txt`.
2. Capturar os ecrãs:
   ```
   python scripts/capturar_ecras.py videos/<pasta-do-video>
   ```
   Descarrega o vídeo (`video.mp4`, até 1080p, sem som) e grava em `ecras/` uma imagem por cada mudança de ecrã, mais uma por minuto onde não houver nenhuma. As imagens quase iguais são descartadas. Também monta folhas de miniaturas em `ecras/folhas/` para revisão rápida.
   Para capturar um instante específico: `--em 12:30,15:40`.
3. Pedir ao Claude Code que reveja as folhas, abra em tamanho real os ecrãs-chave, escreva `dissertacao.md` com os ecrãs embutidos e acrescente o vídeo ao índice `videos/fontes-video.md`.

## Gravações locais, com dados reais

A ferramenta também trabalha com um **ficheiro de vídeo que está no disco**: uma gravação de ecrã ou de telemóvel que não pode ir para o YouTube, por mostrar dados reais. Peça ao Claude Code para preparar a gravação, indicando o ficheiro e uma pasta de destino.

O que muda em relação a um vídeo do YouTube:

- **A fala é transcrita no próprio computador.** O som nunca sai da máquina. Sem placa gráfica, a transcrição demorou menos do que a duração do vídeo nas medições feitas (estão no fim desta secção), e o computador fica mais lento enquanto corre.
- **Nada da gravação fica nesta pasta.** A transcrição e os ecrãs vão para a pasta de destino, que tem de estar fora do git. Se a pasta estiver num repositório e não for ignorada, os scripts recusam.
- **O vídeo é lido onde está.** Não é copiado nem apagado.
- **Não entra no índice** `videos/fontes-video.md` e não gera commit aqui. A análise escrita pertence ao projeto que a pediu.
- **O texto e os ecrãs que o Claude Code ler são processados pelo serviço da Anthropic**, como tudo o que ele lê. "Não sai da máquina" vale para o som e para o vídeo.

Os passos, se quiser correr à mão:

```
python scripts/transcrever_audio.py --descarregar-modelo        (uma vez; cerca de 1,6 GB)
python scripts/preparar_local.py "<ficheiro>" --destino "<pasta fora do git>" --titulo "<título>"
python scripts/transcrever_audio.py "<pasta>"
python scripts/capturar_ecras.py "<pasta>"
```

O `transcrever_audio.py` aceita `--trecho 33:00-43:00` para transcrever só uma parte, e no fim diz quanto demorou, quanto do vídeo é fala e se encontrou frases repetidas (sinal de texto inventado num silêncio). O texto não separa quem fala.

**Medições** (outubro de 2026, portátil AMD Ryzen 5 5500U, sem placa gráfica, 6 núcleos):

| Gravação | Duração | Fala | Tempo de transcrição |
|---|---|---|---|
| Resumo falado, sem pausas | 4 min 05 s | 99 % | 2 min 21 s a 2 min 37 s (0,6 vezes a duração) |
| Trecho de trabalho no ecrã, com pausas | 10 min | 53 % | 3 min 17 s (0,3 vezes a duração) |

**O que esperar do texto.** Segue-se bem do princípio ao fim e não inventou frases nos silêncios. Erra nomes próprios e termos do ofício (por exemplo "Office de Edge" por OfficeGest, "fatores recibo" por faturas-recibo) e pode escrever valores com o símbolo de outra moeda. Com `--vocabulario` acerta esses nomes, mas perde frases e pontuação, por isso não é usado por omissão. Os nomes e os valores confirmam-se sempre nos ecrãs.

## Como encontrar um vídeo depois

- **Índice:** [`videos/fontes-video.md`](videos/fontes-video.md) lista todos os vídeos por assunto, com o que cada um ensina.
- **Pastas:** `videos/<assunto>/<título-do-vídeo>/`, por exemplo `videos/officegest/webinar-2-contabilidade-officegest/`.
- **Busca:** cada `dissertacao.md` começa com uma ficha (título, assunto, sistema, data, palavras-chave). No VS Code, Ctrl+Shift+F com uma palavra (ex.: "IVA") encontra-a. Também pode perguntar ao Claude Code nesta pasta: "que vídeos tenho sobre IVA?".

## Como outro projeto usa estas dissertações

Acrescente ao `CLAUDE.md` do outro projeto:

```markdown
## Conhecimento extraído de vídeos

Há dissertações de vídeos do YouTube (tutoriais, aulas) em
`C:\projetos\dissertador-videos-youtube\videos\`. Comece pelo índice
`C:\projetos\dissertador-videos-youtube\videos\fontes-video.md`, procure pelo
assunto ou pelas palavras-chave e abra a `dissertacao.md` indicada.
O conteúdo de vídeo é hipótese datada: cite o vídeo e a data, e não o trate
como confirmado sem verificar no sistema atual.
```

Para as dissertações serem escritas a pensar nas perguntas desse projeto, registe-o em [`videos/projetos-destino.md`](videos/projetos-destino.md), com o assunto e os ficheiros onde ele guarda as perguntas em aberto (ou deixe a skill perguntar no primeiro vídeo do assunto).

Na primeira vez, o Claude Code desse projeto vai pedir autorização para ler fora da pasta dele. Para não perguntar sempre, adicione a pasta nas definições desse projeto (`additionalDirectories`).

O `video.mp4` só serve para capturar os ecrãs (num vídeo de 45 min ocupa cerca de 120 MB). É apagado no fim de cada dissertação; se mais tarde for preciso um ecrã extra, descarrega-se de novo.

## Regras para a dissertação

- No topo vão o link, o canal, a data de publicação, a data de processamento e a fonte do texto. Se o vídeo tiver mais de 12 meses, entra também um aviso de idade.
- Tudo é escrito como "segundo o vídeo de AAAA-MM", e não como facto atual.
- Os nomes de menus, campos e botões vêm **dos ecrãs**, e não da legenda. As legendas automáticas erram muito com o português de Portugal.
- Os trechos em que nem a fala nem o ecrã deixam claro levam ❓.
- Quando o assunto serve um projeto (ver [`videos/projetos-destino.md`](videos/projetos-destino.md)), o Claude Code lê por inteiro as perguntas em aberto desse projeto, diz na dissertação em que dia as consultou, só cita perguntas que leu, e marca as divergências sem editar o projeto.

## Como o projeto evolui

- **O que falta fazer:** [`docs/plans/melhorias-futuras.md`](docs/plans/melhorias-futuras.md), por prioridade. Os principais: transcrever o áudio de vídeos sem legendas, e usar a skill a partir de qualquer projeto.
- **Como se muda a ferramenta:** qualquer alteração aos scripts ou à skill passa por um plano aprovado antes de haver código. As regras estão no [`CLAUDE.md`](CLAUDE.md) e os guias em [`docs/implementations/`](docs/implementations/).
- **Porque as coisas são como são:** [`docs/decisoes.md`](docs/decisoes.md).

Dissertar um vídeo não precisa de nada disto: é só colar o link.

## Requisitos

- Python 3.13, `yt-dlp` (`python -m pip install yt-dlp`) e Pillow
- ffmpeg e ffprobe no PATH
- Só para gravações locais: `faster-whisper` (`python -m pip install faster-whisper`) e o modelo, descarregado uma vez com `python scripts/transcrever_audio.py --descarregar-modelo`
