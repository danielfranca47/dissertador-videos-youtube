# Gravações locais: transcrever na máquina e capturar ecrãs de um ficheiro do disco

**Componente:** vários (dois scripts novos, script de captura, skill)
**Branch:** `feat/gravacoes-locais` (worktree em `.claude/worktrees/feat/gravacoes-locais`)
**Status:** Todos os cenários validados (08/10/2026)

---

## Motivação

O projeto winners-group tem 8 gravações (6 de ecrã, 2 de telemóvel; 3h43) de
um contabilista a fazer o fecho mensal de um cliente real. São ficheiros no
disco, não têm legendas e mostram dados reais, por isso não podem passar pelo
YouTube nem por um serviço de transcrição externo. A ferramenta só aceitava
links do YouTube e só sabia tirar a fala das legendas do YouTube.

O desejado: dado um ficheiro de vídeo e uma pasta de destino fora do git, a
ferramenta produz a fala em texto, com os minutos, e os ecrãs, tudo na
própria máquina. A análise escrita fica para o projeto que a pediu.

Pedido a partir da Fase 5 de
`C:\projetos\winners-group\docs\implementations\contabilidade-contexto-e-treinamento.md`.

---

## Problemas Identificados (estado anterior)

1. **Só links do YouTube:** `scripts/extrair_video.py` lê tudo com o
   `yt-dlp` a partir de um link e não aceita um ficheiro.
2. **Sem legendas, sem texto:** o mesmo script termina com o código 2 quando
   não há legendas. A transcrição do áudio estava no backlog (M1), com um
   serviço pago como recomendação.
3. **A captura descarrega sempre o vídeo:** `scripts/capturar_ecras.py`
   chamava `descarregar(metadados["link"], …)` sem alternativa.
4. **Tudo ia para `videos/`, que está no git:** não havia forma de mandar a
   saída para fora do repositório, nem nada que impedisse dados reais de
   entrarem no histórico.
5. **As miniaturas eram esticadas para uma proporção fixa**, o que deforma
   um clipe de telemóvel gravado ao alto.

---

## Abordagem

```
ficheiro de vídeo no disco (fica onde está)
   │
   ▼
scripts/preparar_local.py ───► <pasta>/metadados.json
   │                            recusa pasta versionada; avisa se o som acaba antes da imagem
   ▼
scripts/transcrever_audio.py ► <pasta>/transcricao.txt (blocos de ~30 s)
   │                            sem rede; mede tempo, fala e frases repetidas
   ▼
scripts/capturar_ecras.py ───► <pasta>/ecras/ + folhas (lê o ficheiro local)
   │
   ▼
o Claude Code lê e o projeto de destino escreve a análise
```

- **Motor:** faster-whisper com o modelo `large-v3-turbo`, no processador
  (int8), com filtro de silêncio e sem condicionar no texto anterior, para
  uma frase inventada num silêncio não se repetir.
- **O som é lido com o `ffmpeg`** para a memória, a 16 kHz. Assim o trecho
  (`--trecho`) é um simples corte, e os minutos do texto continuam a ser os
  do vídeo.
- **Regras no código:** a pasta de destino tem de estar fora do git
  (`preparar_local.fora_do_git`, usada pelos três scripts quando a origem é
  local); a transcrição define `HF_HUB_OFFLINE=1` antes de carregar a
  biblioteca e usa só ficheiros locais; descarregar o modelo é um comando à
  parte.
- **O caminho do YouTube não muda.** `extrair_video.py` não foi tocado; em
  `capturar_ecras.py`, o que decide é a chave `ficheiro` nos metadados.
- **Mudança de arquitetura validada pelo arquiteto**, com revisão crítica:
  `C:\projetos\modelos-agents\briefings\2026-10-08-dissertador-gravacoes-locais.md`.
  Revê a recomendação de 01/10 só para dados reais: o que mudou foi a regra
  (o som não pode sair da máquina), não a máquina.
- **Descartado:** o serviço da OpenAI (o som sairia da máquina); seguir sem
  transcrição (perdem-se as explicações faladas); `whisper.cpp` com a placa
  gráfica integrada (mais rápido, instalação mais frágil); `openai-whisper`
  (mais lento no processador).
- **Descartado:** tapar NIFs no texto transcrito. Os NIFs estão sobretudo
  nos ecrãs, e tapar só o texto daria uma segurança falsa.
- **Descartado:** usar o `transcrever_audio.py` já para vídeos do YouTube
  sem legendas (M1). O vídeo que a captura descarrega não traz som, e a
  escolha entre serviço pago e transcrição local para vídeos públicos é
  outra decisão. Fica em "Ajustes Possíveis".

---

## Plano de Implementação

### Fase 1 — Ficheiro local e transcrição na máquina

**Objetivo:** preparar, transcrever e capturar os ecrãs de um ficheiro de
vídeo local, com a saída fora do git.

| Ficheiro | O que muda |
|---|---|
| `scripts/preparar_local.py` | Novo. Lê duração, resolução e som com o `ffprobe`; grava `metadados.json` na pasta de destino; recusa pasta versionada (código 3); avisa quando o som acaba antes da imagem |
| `scripts/transcrever_audio.py` | Novo. Transcreve sem rede, em blocos de ~30 s; `--trecho`, `--saida`, `--vocabulario`, `--modelo`, `--threads`; `--descarregar-modelo` à parte; mede tempo, fala e frases repetidas e regista-os nos metadados |
| `scripts/capturar_ecras.py` | Lê o ficheiro local quando os metadados o indicam, sem descarregar; exige pasta fora do git nesse caso; miniaturas com a proporção do vídeo |
| `.claude/skills/dissertar-video/SKILL.md` | Terceiro modo: "Gravação local com dados reais" |
| `README.md` | Secção "Gravações locais, com dados reais"; requisitos novos |
| `CLAUDE.md` | Linha nova em "Usar não é implementar": usar numa gravação local não gera commit nesta pasta |

Decisões tomadas ao construir:

- **Os metadados de uma gravação local têm `origem: "local"` e `ficheiro`**
  (o caminho completo) em vez de `link`. Os de um vídeo do YouTube não
  mudam.
- **Sem lista de vocabulário por omissão.** No piloto, com a lista o modelo
  escreveu "e-Fatura" com a maiúscula certa, mas trocou pontos por vírgulas
  e perdeu uma frase curta. A opção `--vocabulario` fica disponível.
- **Preparar de novo uma pasta já transcrita mantém o registo da
  transcrição** nos metadados.
- **Um trecho sem som termina com uma mensagem e o código 2**, em vez de um
  erro. Apareceu no piloto: uma das gravações só tem som até aos 22 minutos.

### Commits Fase 1

| # | Commit | O que foi implementado |
|---|---|---|
| 1 | `c9654e6` | Preparação de um ficheiro local, transcrição na máquina, captura a partir do ficheiro local, modo novo na skill e documentação de uso |

### Relatório da Fase 1 — o que mudou na prática

**Antes:** a ferramenta só trabalhava com links do YouTube e só tinha texto
quando o YouTube tinha legendas. Uma gravação com dados reais não tinha
como ser tratada.
**Agora:** dá-se um ficheiro de vídeo e uma pasta fora do git, e a
ferramenta devolve a fala em texto, com os minutos, e os ecrãs. O som não
sai da máquina, o vídeo não é copiado nem apagado, e nada fica nesta pasta.

O que o piloto mediu, num portátil sem placa gráfica:

- **Tempo:** 0,58 a 0,64 vezes a duração numa gravação só de fala (4 min
  05 s em 2 min 21 s a 2 min 37 s) e 0,33 vezes num trecho com pausas (10
  min em 3 min 17 s). A estimativa do plano era de 1 a 1,5 vezes.
- **Silêncios:** no trecho de 10 minutos, só 53 % era fala, e não apareceu
  nenhuma frase repetida três vezes seguidas.
- **Fidelidade:** o texto segue-se do princípio ao fim e bate com a nota
  que o utilizador tinha tirado desse momento e com os valores que se veem
  no ecrã.
- **Limitação:** erra nomes próprios e termos do ofício ("Office de Edge"
  por OfficeGest, "fatores recibo" por faturas-recibo) e escreveu valores
  em euros com "R$". Com a lista de vocabulário acerta os nomes, mas troca
  frases inteiras por outras sem sentido. O utilizador decidiu a 08/10
  seguir sem a lista; os nomes confirmam-se nos ecrãs.
- **Ecrãs:** a 2560 pontos, os valores de uma folha de Excel leem-se sem
  erro em tamanho real (oito linhas conferidas com os ficheiros
  verdadeiros, em duas folhas).
- **Achado nos dados:** uma das 8 gravações (a da conferência, de 63
  minutos) só tem som até aos 22 minutos. O script passou a avisar disso ao
  preparar o ficheiro.

**Para validar:** Cenários L1 a L4 e E1 a E4 (todos corridos a 08/10/2026).

---

## Checks de Validação

| Prefixo | O que verifica | Como |
|---|---|---|
| `L` | Lógica pura | Sem internet: chamar a função com uma entrada conhecida e comparar o resultado |
| `E` | Ponta a ponta | Correr os scripts contra uma gravação real (em `C:\projetos\winners-group\docs\ops\ref-arquivos\`, fora do git) ou contra um vídeo real do YouTube |

Os checks `E1` a `E3` usam gravações com dados reais. Este arquivo regista
as medições, e não o conteúdo.

### Cenário L1 — Os scripts abrem sem erro
- [x] `python -m py_compile scripts/extrair_video.py scripts/capturar_ecras.py scripts/preparar_local.py scripts/transcrever_audio.py` termina com o código 0
- **Validado em:** 08/10/2026 — código 0, antes e depois da correção do trecho sem som

### Cenário L2 — Blocos de 30 segundos e contagem de repetições
- [x] `agrupar([(0,'a'),(12,'b'),(31,'c'),(45,'d'),(3700,'e')])` devolve `['[00:00] a b', '[00:31] c d', '[1:01:40] e']`
- [x] `repeticoes` devolve 1 para `x x x y x x`, 2 para `x x x x z z z` e 0 para uma lista vazia
- **Validado em:** 08/10/2026 — os dois resultados saíram como escrito

### Cenário L3 — A pasta de destino tem de estar fora do git
- [x] `fora_do_git` é falso para uma pasta dentro de `videos/` desta ferramenta e para `docs/` do winners-group
- [x] É verdadeiro para `dados/gravacoes/G4` do winners-group (ignorada), para uma subpasta que ainda não existe dentro de `dados/`, e para uma pasta fora de qualquer repositório
- [x] `preparar_local.py` com destino em `docs/` do winners-group termina com o código 3 e não cria a pasta
- **Validado em:** 08/10/2026 — os cinco casos deram o esperado; a recusa escreveu a mensagem, saiu com 3 e a pasta não foi criada

### Cenário L4 — A transcrição não usa a rede
- [x] Com `HTTP_PROXY` e `HTTPS_PROXY` apontados para um endereço morto (`http://127.0.0.1:9`), a transcrição corre até ao fim
- **Validado em:** 08/10/2026 — as cinco transcrições do piloto correram assim, todas até ao fim. **Não verificado:** o tráfego de rede medido por fora do processo; o que se provou é que a biblioteca não precisou da rede

### Cenário E1 — Gravação G4 inteira (4 min 05 s, fala contínua)
Setup: `preparar_local.py "<…>\Videos_IA\Resumo_Conferencia_E-fatura.mp4" --destino C:\projetos\winners-group\dados\gravacoes\G4`, depois `transcrever_audio.py` sem e com `--vocabulario`, e `capturar_ecras.py`.
Termos fixados antes de correr: e-Fatura, OfficeGest, fatura, NIF, conferência, lançamento, contabilidade, fornecedor, nota de crédito, extrato, reconciliação, Excel.
- [x] Demora até 1,5 vezes a duração do áudio
- [x] Zero frases repetidas três vezes seguidas
- [x] Os termos fixados que são ditos aparecem bem escritos
- [x] A captura lê o ficheiro local sem descarregar nada e grava os ecrãs na pasta de destino
- **Validado em:** 08/10/2026 — três corridas: 2 min 21 s e 2 min 37 s sem vocabulário, 2 min 35 s com (0,58 a 0,64 vezes a duração); 99 % de fala; zero repetições. Ditos e bem escritos: e-Fatura (sem vocabulário, "e-fatura"), fatura, conferência, lançamento, contabilidade, fornecedores, extrato, Excel. Não foram ditos: OfficeGest, NIF, nota de crédito, reconciliação. Com vocabulário: a maiúscula de "e-Fatura" certa, pontos trocados por vírgulas e uma frase curta perdida. A captura demorou 26 s e guardou 2 ecrãs (a imagem está quase sempre parada)

### Cenário E2 — Dez minutos de uma gravação longa, com pausas
Setup: `preparar_local.py` da G6 (`Reconciliacao_bancaria-002.mp4`, 1 h 56) e `transcrever_audio.py <pasta> --trecho 36:00-46:00 --saida transcricao-trecho-36-46.txt`.
O plano previa a G2 dos 33:00 aos 43:00; a G2 não tem som nesse intervalo (ver a Fase 1), por isso o trecho passou para a G6, onde o utilizador tem uma nota aos 41 minutos.
- [x] Demora até 1,5 vezes a duração do trecho
- [x] Zero frases repetidas três vezes seguidas
- [x] O texto à volta dos 41 minutos bate com a nota do utilizador desse momento
- [x] Os minutos do texto são os do vídeo (começam em 36:00)
- [⏭️] Os termos fixados que são ditos aparecem bem escritos
- **Validado em:** 08/10/2026 — 3 min 17 s para 9 min 59 s (0,33 vezes), com e sem vocabulário; 53 % de fala; zero repetições. Entre os 39:06 e os 40:40 o texto descreve faturas do fim do mês anterior cujo movimento no banco aparece dias depois, que é a nota do utilizador. Os blocos vão de 36:00 a 45:17
- **Termos, não cumprido à letra:** sem vocabulário, "OfficeGest" saiu "Office de Edge" e "faturas-recibo" saiu "fatores recibo"; com vocabulário saem certos, mas três frases ficam trocadas por outras sem sentido. O critério media a grafia dos nomes, e o que a análise precisa é de frases fiéis. **Decisão do utilizador (08/10/2026):** seguir sem vocabulário. A limitação está escrita no `README.md` e na skill

### Cenário E3 — Os ecrãs de 2560 pontos leem-se
- [x] Num ecrã de folha de Excel aberto em tamanho real, quatro linhas lidas batem com o ficheiro de Excel verdadeiro
- **Validado em:** 08/10/2026 — feito em duas folhas: o ecrã da G4 a 01:48 (folha de conferência, quatro linhas) e o da G6 aos 41:00 (folha de reconciliação, quatro linhas). Números de documento, datas e valores iguais aos dos ficheiros

### Cenário E4 — O caminho do YouTube continua a funcionar
Setup: na worktree, `extrair_video.py "https://www.youtube.com/watch?v=vW9GhkTXmNU" --tema officegest` e `capturar_ecras.py` na pasta desse vídeo.
- [x] A extração e a captura terminam sem erro
- [x] Os ecrãs gerados são os mesmos que estão no git (`git status` na pasta do vídeo), tirando os pedidos à mão, que a captura automática apaga (M3)
- **Validado em:** 08/10/2026 — 88 blocos de legenda e 194 ecrãs, em 190 s; `git status` em `videos/` sem nenhuma diferença (este vídeo não tem ecrãs pedidos à mão). O `video.mp4` do teste foi apagado da worktree

---

## Ajustes Possíveis Pós-Implementação

1. **Vídeos do YouTube sem legendas (M1):** o `transcrever_audio.py` pode
   servir, com um passo que descarregue o som. Falta decidir, para vídeos
   públicos, entre o serviço pago e a transcrição local, com o tempo medido
   aqui.
2. **Usar a placa gráfica integrada** (`whisper.cpp` com Vulkan): só se o
   volume de gravações crescer a ponto de o tempo de máquina pesar.
3. **Separar quem fala:** o texto junta as vozes. Só vale a pena se as
   análises mostrarem que faz falta.
4. **Retomar uma transcrição interrompida:** o texto é gravado a cada 5
   minutos de áudio, mas uma nova corrida recomeça do início.
5. **Recortar uma zona do ecrã** ao pedir um instante com `--em`, para
   letra muito pequena. No piloto não fez falta.
