# Projetos de destino

Diz, para cada **assunto**, que projeto as dissertações servem e onde esse
projeto guarda as suas perguntas em aberto. A skill `dissertar-video` lê este
registo antes de rever os ecrãs de um vídeo, para procurar no vídeo o que o
projeto precisa de saber **hoje**.

Os caminhos da coluna "Onde estão as perguntas" são relativos à pasta do
projeto. Um assunto que não serve nenhum projeto fica com "nenhum" na coluna
Projeto, para a skill não voltar a perguntar.

| Assunto | Projeto | Onde estão as perguntas | Registo de vídeos do projeto | Registado em |
|---|---|---|---|---|
| officegest | `C:\projetos\winners-group` | `docs/dependencias-externas.md` · `docs/pendentes.md` · `contabilidade/processo-atual/perguntas-em-aberto.md` | `docs/fontes-videos.md` | 2026-10-02 |

## Como se mantém

- **Assunto novo:** a skill pergunta uma vez se o assunto serve algum projeto e
  acrescenta a linha.
- **O projeto mudou os ficheiros de sítio:** a skill avisa quando um caminho
  deste registo não existe. Corrige-se a linha aqui.
- **Um assunto serve dois projetos:** uma linha por projeto, com o mesmo
  assunto.
- A skill **lê** os projetos de destino; nunca os edita.
