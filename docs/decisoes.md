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
