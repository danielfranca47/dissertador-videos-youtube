# Gravações locais

Como a ferramenta trata um **ficheiro de vídeo que está no disco**, em vez de
um link do YouTube: de onde vem o texto, para onde vai a saída e o que o
código garante. Estas gravações costumam mostrar dados reais, e é isso que
explica quase todas as regras.

A recomendação de arquitetura está em
`C:\projetos\modelos-agents\briefings\2026-10-08-dissertador-gravacoes-locais.md`.

---

## O que a ferramenta faz e o que não faz

Faz: a fala em texto, com os minutos, e os ecrãs. Tudo na própria máquina, e
tudo gravado numa pasta que o projeto de destino indica.

Não faz: a análise escrita. Não escreve `dissertacao.md`, não acrescenta a
gravação a `videos/fontes-video.md` e não gera commit nesta pasta. O que
fazer com o material é do projeto que o pediu.

```
ficheiro de vídeo no disco (fica onde está)
   │
   ▼
scripts/preparar_local.py ───► <pasta>/metadados.json
   │
   ▼
scripts/transcrever_audio.py ► <pasta>/transcricao.txt
   │
   ▼
scripts/capturar_ecras.py ───► <pasta>/ecras/ + ecras/folhas/
```

Os passos, as regras de uso e o que dizer ao utilizador estão na secção
"Gravação local com dados reais" da skill
[`dissertar-video`](../../.claude/skills/dissertar-video/SKILL.md).

---

## Os metadados de uma gravação local

`preparar_local.py` grava um `metadados.json` com chaves próprias. É por
elas que os outros scripts sabem que não estão perante um vídeo do YouTube.

| Chave | O que é |
|---|---|
| `origem` | Sempre `"local"`. É o que o `transcrever_audio.py` exige |
| `ficheiro` | Caminho completo do vídeo original. É o que o `capturar_ecras.py` usa para decidir que não descarrega nada |
| `id` | O nome da pasta de destino |
| `titulo`, `gravado` | Dados pelo utilizador; por omissão, o nome do ficheiro e a data de modificação |
| `duracao`, `segundos`, `resolucao` | Lidos com o `ffprobe`. A resolução já conta com a rotação dos clipes de telemóvel |
| `tem_som`, `segundos_de_som` | Se há faixa de som e até onde vai |
| `legenda` | Vazio até à transcrição. Depois guarda o motor, o modelo, o tempo de processamento, os segundos de fala e as frases repetidas |

Um vídeo do YouTube continua a ter `link` e não tem `ficheiro` nem `origem`.

---

## A transcrição

| | |
|---|---|
| Motor | `faster-whisper`, no processador, com quantização `int8` |
| Modelo | `large-v3-turbo` por omissão (`--modelo` troca) |
| Idioma | Fixo em português |
| Silêncios | Filtro de silêncio ligado; cada bloco é transcrito sem olhar para o texto do anterior, para uma frase inventada num silêncio não se propagar |
| Som | Lido com o `ffmpeg` para a memória, a 16 kHz e num só canal. Uma gravação de 2 horas ocupa cerca de 450 MB de memória |
| Saída | `transcricao.txt`, no formato das legendas do YouTube: blocos de ~30 s com o minuto de início, montados por `extrair_video.agrupar` |
| Progresso | Uma linha e uma gravação do texto parcial a cada 5 minutos de áudio |

`--trecho A-B` corta o som nesse intervalo; os minutos do texto continuam a
ser os do vídeo. `--vocabulario` passa uma lista de termos ao modelo em
todos os blocos (`hotwords`). Não é usado por omissão.

**O que se mediu** (outubro de 2026, AMD Ryzen 5 5500U, 6 núcleos, sem placa
gráfica): entre 0,3 e 0,6 vezes a duração do áudio. Quanto mais silêncio,
mais rápido.

**O que se sabe da qualidade:** as frases são fiéis e não apareceram
repetições nem texto inventado nos silêncios. Os nomes próprios e os termos
do ofício saem mal escritos, e os valores podem trazer o símbolo de outra
moeda. A lista de vocabulário corrige os nomes à custa de trocar frases
inteiras. O texto não separa quem fala.

No fim, o script imprime três medições, e a skill manda lê-las: o tempo
sobre a duração, a percentagem de fala, e quantas vezes a mesma frase
apareceu três vezes seguidas.

---

## O que o código garante

Estas regras estão no código porque não podem depender de alguém se lembrar.

1. **A saída só vai para fora do git.** `preparar_local.fora_do_git` aceita
   uma pasta que esteja fora de qualquer repositório ou que o repositório
   ignore (`git check-ignore`). Os três scripts chamam
   `exigir_fora_do_git` quando a origem é local, e terminam com o código 3
   se a pasta for versionada.
2. **A transcrição não usa a rede.** `transcrever_audio.py` define
   `HF_HUB_OFFLINE=1` antes de carregar a biblioteca e abre o modelo só a
   partir do disco.
3. **Descarregar o modelo é um comando à parte:**
   `transcrever_audio.py --descarregar-modelo`. É o único que vai à
   internet. O modelo (cerca de 1,6 GB) fica na pasta de cache do Hugging
   Face do utilizador, fora desta pasta.
4. **Nenhum script copia, move ou apaga o vídeo original.**
5. **Um trecho sem som não rebenta:** termina com uma mensagem e o código 2.

Códigos de saída: 0 correu; 1 uso errado ou ficheiro em falta; 2 não há som
ou o modelo não está na máquina; 3 pasta de destino recusada.

---

## O que só a skill garante

- A gravação não entra no índice nem gera commit nesta pasta.
- O utilizador é avisado logo quando o som acaba antes da imagem.
- No que se escreve a partir da gravação não entram NIFs, IBANs nem
  palavras-passe.
- **O som e o vídeo não saem da máquina, mas o que o Claude Code lê sai.** A
  transcrição e os ecrãs abertos são processados pelo serviço da Anthropic.

---

## Quando deixa de ser fiável

- **O vídeo foi movido ou mudou de nome.** Os metadados guardam o caminho
  completo. Uma captura nova ou um `--em` falham; prepara-se a pasta de
  novo, e o registo da transcrição mantém-se.
- **`segundos_de_som` menor do que `segundos`.** A transcrição só cobre a
  parte com som. O resto do vídeo tem ecrãs e não tem texto.
- **O projeto de destino mudou o seu `.gitignore`.** Uma pasta que era
  aceite pode passar a ser recusada, e o contrário.
- **`HF_HUB_OFFLINE` tem de ser definido antes de a biblioteca ser
  carregada.** Mover essa linha para depois do `import` desliga a garantia
  sem dar erro.
- **Repetir a captura automática apaga os ecrãs pedidos à mão**, tal como
  nos vídeos do YouTube (melhoria M3 do backlog).
