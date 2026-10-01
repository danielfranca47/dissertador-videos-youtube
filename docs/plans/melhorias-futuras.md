# Melhorias futuras do dissertador

> Contexto: M1 e M2 são o que ficou por fazer no fim da construção inicial
> (01/10/2026), quando as três primeiras fases — texto, ecrãs e skill — foram
> concluídas e testadas no vídeo do OfficeGest. M3 foi notado ao ler o código
> durante a instalação do fluxo de trabalho, no mesmo dia.

---

## M1 — Transcrever o áudio de vídeos sem legendas

**Prioridade: BAIXA** — sobe para **ALTA** no primeiro vídeo sem legendas que
o utilizador queira dissertar.

**O que acontece hoje.** Quando o vídeo não tem legendas (nem manuais nem
automáticas), `scripts/extrair_video.py` grava só os dados do vídeo e termina
com o código de saída 2. A skill avisa e pergunta se o utilizador quer seguir
só com os ecrãs ou parar. Sem a fala, a dissertação perde as explicações e
fica reduzida ao que se vê.

**O que precisa mudar.** Quando não houver legendas, descarregar o áudio,
transcrevê-lo e gravar o mesmo `transcricao.txt` em blocos de ~30 s, para o
resto do fluxo não notar a diferença. A dissertação tem de dizer, na "fonte do
texto", que veio de transcrição de áudio.

**Recomendação do arquiteto** (briefing de 01/10/2026): usar a Whisper API da
OpenAI, e só neste caso. A máquina não tem placa gráfica, o que afasta a
alternativa de correr o Whisper localmente.

**Custo e o que exige do utilizador:**

- Cerca de **US$ 0,36 por hora de vídeo** (US$ 0,006 por minuto). Confirmar o
  preço em vigor no plano — este é o de 01/10/2026.
- **Criar uma conta na OpenAI e uma chave de API**, com um método de
  pagamento. É o único passo que só o utilizador pode fazer.
- A chave fica num ficheiro `.env` nesta pasta, que o `.gitignore` já exclui.

**A fechar no plano, antes de construir:**

- O que fazer com vídeos longos: a API tem um limite de tamanho por ficheiro
  de áudio, por isso um vídeo de mais de uma hora provavelmente tem de ser
  cortado em partes. Confirmar o limite atual.
- Se a skill transcreve sem perguntar ou mostra antes o custo estimado
  ("este vídeo tem 1h20, vai custar cerca de US$ 0,48 — sigo?"). Recomendação
  inicial: mostrar o custo e pedir confirmação, porque é a única parte da
  ferramenta que gasta dinheiro.
- Que vídeo real, sem legendas, serve para o teste ponta a ponta.

Como muda a origem do texto e introduz um serviço pago, passa pelo arquiteto
na fase de plano (ver `CLAUDE.md`, "Mudança de arquitetura passa pelo
arquiteto"). A recomendação de base já existe; falta fechar os pontos acima.

---

## M2 — Usar a skill a partir de qualquer projeto

**Prioridade: MÉDIA**

**O que acontece hoje.** A skill `dissertar-video` vive em
`.claude/skills/dissertar-video/` desta pasta, por isso só aparece com o
Claude Code aberto aqui. Para dissertar um vídeo enquanto se trabalha noutro
projeto (no `winners-group`, por exemplo), é preciso abrir outra janela nesta
pasta.

**O que precisa mudar.** Instalar a skill como skill global, em
`~/.claude/skills/`, para o utilizador poder colar um link em qualquer projeto.

**O que não é tão simples como copiar a pasta:**

- **Os resultados continuam a vir para aqui.** A skill já manda correr os
  comandos a partir de `C:\projetos\dissertador-videos-youtube`, e os scripts
  gravam sempre em `videos/` desta pasta. Convém que continue assim, para o
  índice `videos/fontes-video.md` ser um só — mas a skill tem de o dizer com
  caminhos completos, e não relativos, em todos os passos.
- **Autorização para escrever fora do projeto aberto.** A partir de outro
  projeto, o Claude Code vai pedir autorização para escrever nesta pasta.
  Decidir se a instalação trata disso ou se fica só explicado.
- **Duas cópias da skill.** A instalação global é uma cópia. Se a skill for
  alterada aqui e a cópia não for atualizada, as duas divergem. O
  `C:\projetos\dev-flow-work-creator` resolve o mesmo problema com um
  `install.ps1` que volta a copiar; seguir esse padrão. Decidir também se a
  cópia desta pasta se mantém — com as duas presentes, a skill aparece em
  duplicado quando o Claude Code é aberto aqui.
- **O commit depois de dissertar** (`CLAUDE.md`, "Usar não é implementar") é
  uma regra desta pasta. A partir de outro projeto o Claude não a lê, por isso
  tem de passar para dentro da skill.

Não custa dinheiro nem exige contas. Não muda a arquitetura recomendada.

---

## M3 — Repetir a captura apaga os ecrãs pedidos à mão

**Prioridade: BAIXA**

**O que acontece hoje.** Repetir a captura de um vídeo (com `--limiar 0.15`,
por exemplo, quando saíram ecrãs a mais) começa por apagar todas as imagens de
`ecras/`, incluindo as que tinham sido pedidas à mão com `--em`
(`scripts/capturar_ecras.py:147-148`). Se a dissertação já embutia uma dessas
imagens, fica com a imagem em falta, sem aviso. As capturas manuais também não
entram em `ecras/indice.json` (`scripts/capturar_ecras.py:139-145`), por isso
nada regista que foram pedidas.

**O que precisa mudar.** Registar no índice que uma captura foi pedida à mão, e
poupá-la quando a captura automática for repetida.

Ainda não causou nenhuma perda. O arquivo
[`_template-implementacao.md`](../implementations/_template-implementacao.md)
usa este problema como exemplo de como se documenta uma implementação — o
exemplo é ilustrativo, a correção **não foi feita**.

**Atualização (2026-10-02).** O risco deixou de ser teórico: a dissertação de
`videos/officegest/formacao-pratica-modulo-contabilidade/` embute três capturas
pedidas à mão (`18-40.jpg`, `37-20.jpg` e `1-17-05.jpg`; foram pedidas cinco,
com `18-25.jpg` e `1-18-25.jpg`). Repetir a captura desse vídeo deixa a
dissertação com três imagens em falta. **Sobe para MÉDIA** na primeira vez que
for preciso repetir a captura de um vídeo já dissertado.

---

## M4 — O yt-dlp avisa que vai deixar de funcionar sem um "motor de JavaScript"

**Prioridade: MÉDIA**

> Contexto: observado ao dissertar o vídeo `dwB0syVcAvg`, em 2026-10-02.

**O que acontece hoje.** Ao pedir os dados de um vídeo, o `yt-dlp` escreve o
aviso "No supported JavaScript runtime could be found (…) YouTube extraction
without a JS runtime has been deprecated, and some formats may be missing". O
vídeo foi extraído e descarregado sem problema (legendas, metadados e imagem),
por isso hoje não há consequência.

**O risco.** O aviso diz que este modo está a ser abandonado. Numa versão
futura do `yt-dlp`, ou quando o YouTube mudar, a extração pode falhar ou
descarregar o vídeo com pior imagem, o que prejudica a leitura dos ecrãs.

**O que precisa mudar.** Instalar na máquina o motor que o `yt-dlp` pede (o
`deno`, gratuito) e acrescentá-lo aos requisitos do `README.md`. Detalhe em
<https://github.com/yt-dlp/yt-dlp/wiki/EJS>.

Não custa dinheiro nem exige contas. Não muda a arquitetura recomendada.
**Sobe para ALTA** no dia em que um vídeo falhar a extração por este motivo.

**Nota menor, do mesmo vídeo.** A saída do `capturar_ecras.py` traz centenas de
linhas de progresso do descarregamento antes do resumo. Não atrapalha o
resultado, só a leitura.
