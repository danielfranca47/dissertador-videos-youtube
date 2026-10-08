# Decisões

Decisões transversais do projeto, com data e motivo. Cronológico: acrescentar
no fim, nunca reescrever. Uma decisão que muda entra como nova entrada que
refere a anterior.

---

## 01/10/2026 — Arquitetura inicial

Fluxo fixo, e não um agente. Scripts Python para a parte que dá sempre o mesmo
resultado; o próprio Claude Code lê as imagens e escreve a dissertação, sem
chave de API da Anthropic. O conteúdo de um vídeo entra como hipótese datada.

**Motivo:** recomendação do agente arquiteto, em
`C:\projetos\modelos-agents\briefings\2026-10-01-dissertador-videos-youtube.md`.

---

## 01/10/2026 — Adoção do fluxo de trabalho de implementação

Instalado a partir de `C:\projetos\dev-flow-work-creator` (skill
`fluxo-implementacao`), no nível completo: Plan Mode obrigatório, uma branch e
uma worktree por implementação, contrato vivo em `docs/implementations/`,
graduação para `docs/architecture/`, e a regra do que sobe ao utilizador na
variante "não é programador".

### Adaptado a este projeto

- **Usar não é implementar.** Dissertar um vídeo é o uso normal da ferramenta e
  não passa pelo fluxo: faz-se na pasta principal e termina num commit em
  `main`. Só mudar os scripts, a skill ou as regras da dissertação é que exige
  plano e branch. **Motivo:** sem esta distinção, cada vídeo colado pediria um
  plano e uma branch, e o fluxo passaria a atrapalhar aquilo para que o projeto
  serve.
- **Checks `L` e `E`.** Lógica pura (verificável sem internet) e ponta a ponta
  (contra um vídeo real). **Motivo:** é o que este projeto consegue verificar.
- **Mudança de arquitetura passa pelo arquiteto**, na fase de plano.
  **Motivo:** o utilizador não é programador e quer as decisões de arquitetura
  validadas por esse agente.

### Deixado de fora, e porquê

| O que | Motivo | Quando reconsiderar |
|---|---|---|
| Checks de interface (`U`) e teste pelo browser | A ferramenta não tem interface | Se vier a ter uma |
| Checks bloqueados por terceiros (`I`), marca `DEPENDE-…` no código e documento de perguntas em aberto | Não há nenhum sistema externo com perguntas por responder: o YouTube é lido pelo `yt-dlp`, sem contrato nem conta | Se a transcrição paga (M1) trouxer dúvidas que só o fornecedor responde |
| Análise de sprint e planos semanais | O backlog tem três itens | Com um backlog a sério |
| Versionamento por feature (vN) | Nada é distribuído em versões | Se a skill passar a ser instalada noutras máquinas |
| Comandos slash próprios do fluxo | Nascem de repetição observada; ainda nenhuma implementação passou pelo fluxo | Depois de três ou quatro implementações |
| `git push` na graduação | O repositório só existe neste computador | Quando houver um remoto |
| Promessa de validação automática | Não há testes; a validação é manual e o texto di-lo | Quando existirem testes |

---

## 01/10/2026 — O que entra no histórico de versões

Entram o código, a skill, a documentação e, de cada vídeo, a dissertação, a
transcrição, os dados e **os ecrãs**. Ficam de fora o `video.mp4` e as folhas
de miniaturas.

**Motivo:** os ecrãs são a prova que a dissertação embute; sem eles o `.md`
fica com imagens em falta. O vídeo e as folhas voltam a gerar-se com um
comando.

**Custo aceite:** cada vídeo acrescenta ao histórico cerca de 25 MB de imagens,
e cada worktree traz uma cópia delas. **Reconsiderar** quando a pasta `.git`
passar de 1 GB ou criar uma worktree se tornar lento — a saída é tirar os
ecrãs do histórico e passar a guardá-los só na pasta.

**Atenção:** o histórico de versões não é uma cópia de segurança. Está no
mesmo disco que os ficheiros; se o disco falhar, perde-se tudo.

---

## 02/10/2026 — O vídeo descarregado é apagado no fim de cada dissertação

Antes, a skill perguntava se podia apagar o `video.mp4`. Passa a apagá-lo
sempre, sem perguntar, depois de a dissertação estar escrita, as imagens
embutidas confirmadas e o commit feito. Os dois vídeos que existiam foram
apagados nesta data.

**Motivo:** decisão do utilizador. Depois de o conteúdo estar dissertado, o
vídeo não compensa o espaço (214 MB num vídeo de 1 h 27), e a pergunta
repetia-se em todos os vídeos com a mesma resposta.

**Custo aceite:** pedir um ecrã extra mais tarde obriga a descarregar o vídeo
de novo, e deixa de ser possível se o vídeo sair do YouTube. Os ecrãs já
capturados não se perdem: estão na pasta e no histórico.

**Como foi feito:** alteração de uma linha na skill e outra no `README.md`,
direta em `main`, sem passar pelo fluxo de implementação, por ser uma regra de
uso já decidida pelo utilizador e sem escolhas por fechar.

---

## 02/10/2026 — Cada assunto tem um projeto de destino, e as perguntas dele são lidas atualizadas

A dissertação passa a ser escrita com as perguntas em aberto do projeto que
serve lidas **por inteiro e antes de rever os ecrãs**. O registo
`videos/projetos-destino.md` diz, por assunto, que projeto é e onde estão as
perguntas. A tabela de ligação leva a data da consulta. Os vídeos já
dissertados são revistos **a pedido**, reescrevendo só essa tabela e a
checklist.

**Motivo:** o utilizador reparou que o winners-group reformula e cria perguntas
a cada vídeo, e que o que se procura num vídeo depende do que falta saber
nesse dia. No vídeo `7UlDwks9BgQ` a leitura tinha sido parcial e não viu duas
perguntas criadas no próprio dia. O utilizador quer também usar a ferramenta
com outros projetos.

**Escolha do utilizador:** rever os vídeos antigos só a pedido, em vez de
sozinho a cada vídeo novo (demorava cada vez mais) ou de nunca (deixava as
tabelas antigas desatualizadas).

**Mantido:** a ferramenta só lê o projeto de destino. Quem decide o que entra
nas perguntas é esse projeto.

**Custo aceite:** cada vídeo gasta mais leitura (os ficheiros de perguntas
inteiros), e o registo deixa de estar certo se o outro projeto mudar os
ficheiros de sítio; a skill avisa quando isso acontece.

---

## 08/10/2026 — Gravações locais: a fala é transcrita na própria máquina

A ferramenta passa a aceitar um ficheiro de vídeo do disco e a transcrever a
fala no computador, com o `faster-whisper` e o modelo `large-v3-turbo`, sem
rede. A saída vai para uma pasta fora do git, indicada pelo projeto que pede
a análise. Nada dessas gravações fica nesta pasta.

**Motivo:** o winners-group tem gravações de ecrã com dados reais de
clientes, que não podem passar pelo YouTube nem por um serviço de
transcrição externo.

**Revê a entrada de 01/10** só neste ponto. A recomendação de então afastava
a transcrição local por a máquina não ter placa gráfica. O que mudou foi a
regra, e não a máquina: com dados reais, o serviço externo deixou de ser
opção. Recomendação do arquiteto, com revisão crítica, em
`C:\projetos\modelos-agents\briefings\2026-10-08-dissertador-gravacoes-locais.md`.

**Medido no piloto:** entre 0,3 e 0,6 vezes a duração do áudio, contra a
estimativa de 1 a 1,5 vezes.

**Escolha do utilizador:** transcrever sem lista de vocabulário. O texto fica
com as frases fiéis e erra só os nomes próprios ("Office de Edge" por
OfficeGest); com a lista acerta os nomes e troca frases inteiras.

**Custo aceite:** os nomes e os valores confirmam-se sempre nos ecrãs; o
texto não separa quem fala; e o texto e os ecrãs que o Claude Code lê são
processados pelo serviço da Anthropic, embora o som e o vídeo não saiam da
máquina.

**Em aberto:** para vídeos públicos do YouTube sem legendas (M1), a escolha
entre o serviço pago e a transcrição local fica por fazer, agora com o
tempo medido.
