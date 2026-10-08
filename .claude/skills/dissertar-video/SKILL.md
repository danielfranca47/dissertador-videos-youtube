---
name: dissertar-video
description: Transforma um vídeo do YouTube num .md detalhado, com screenshots dos ecrãs demonstrados, para servir de base de conhecimento a projetos do Claude Code. Use sempre que o utilizador colar um link do YouTube (youtube.com ou youtu.be) e pedir para dissertar, documentar, resumir em detalhe, extrair o conhecimento ou "fazer" o vídeo, ou quando pedir para reprocessar ou atualizar um vídeo já processado. Use também quando pedir para rever, atualizar ou voltar a cruzar os vídeos já dissertados com as perguntas atuais de um projeto (por exemplo, "revê os vídeos do OfficeGest com as perguntas atuais"). Use também quando o utilizador apontar para um ficheiro de vídeo no disco (uma gravação de ecrã ou de telemóvel, .mp4 ou outro) e pedir para o transcrever, capturar os ecrãs ou analisar.
argument-hint: <link-do-youtube> [projeto de destino, opcional; por omissão, o do registo videos/projetos-destino.md] | rever <assunto> | <ficheiro-de-video> <pasta de destino fora do git>
---

# Dissertar vídeo do YouTube

Esta skill tem três modos. **Dissertar um vídeo novo** do YouTube são os passos 1 a 5. **Rever a ligação** de vídeos já dissertados, quando as perguntas do projeto de destino mudaram, é a secção "Rever a ligação". **Preparar uma gravação local**, que é um ficheiro no disco e pode ter dados reais, é a secção "Gravação local com dados reais", no fim: tem regras próprias, e os passos 1 a 5 não se aplicam.

O utilizador **não é desenvolvedor** e usa o resultado para aprender um tema que não domina. Por isso, não lhe peças para validar o conteúdo. A prova é o ecrã: os nomes de menus, campos e botões vêm dos screenshots, e não da tua interpretação.

Corre todos os comandos a partir da raiz do projeto (`C:\projetos\dissertador-videos-youtube`), com `PYTHONIOENCODING=utf-8`.

## 1. Extrair dados e transcrição

Antes de correr, escolhe o **assunto** (`--tema`): o sistema ou a área de que o vídeo trata, numa palavra ou duas, por exemplo `officegest`, `claude-code` ou `vendas-b2b`. Vê as pastas que já existem em `videos/` e reutiliza uma se servir, para não criar dois assuntos para a mesma coisa. Se o título e o canal não deixarem claro, pergunta ao utilizador.

```
python scripts/extrair_video.py "<link>" --tema <assunto>
```

- Cria `videos/<assunto>/<titulo-do-video>/` com `metadados.json` e `transcricao.txt` (blocos de ~30 s com o minuto de início). Daqui em diante, `<pasta>` é esta pasta.
- **Código de saída 2 = o vídeo não tem legendas.** Ainda não existe transcrição do áudio. Avisa o utilizador e pergunta se quer seguir só com os ecrãs ou parar.
- Lê `metadados.json` (data, duração, descrição, capítulos) e a transcrição inteira. Num vídeo longo, lê por partes. Tira daqui a estrutura e as explicações. A legenda automática em português de Portugal **erra muito**: nunca copies dela nomes de menus, campos ou pessoas.

## 1b. Saber a quem o vídeo serve

As perguntas do projeto de destino mudam de vídeo para vídeo. Lê-as **agora**, antes de olhar para os ecrãs, porque são elas que dizem o que vale a pena procurar no vídeo.

1. Abre `videos/projetos-destino.md` e procura a linha do assunto. Se o utilizador indicou um projeto no pedido, esse projeto vale para este vídeo, mesmo que o registo diga outra coisa.
2. **O assunto tem projeto:** lê **por inteiro** cada ficheiro da coluna "Onde estão as perguntas" (não pesquises por palavras: uma pergunta reformulada escapa à pesquisa). Lê também o registo de vídeos do projeto, se houver, para saber o que os vídeos anteriores já responderam. Se um caminho do registo não existir, **avisa o utilizador** e procura no projeto para onde o ficheiro foi; não sigas sem ele.
3. **O assunto não está no registo:** pergunta uma vez ao utilizador se o assunto serve algum projeto. Se sim, explora esse projeto (`README.md`, `CLAUDE.md`, `docs/`), encontra onde estão as perguntas em aberto e acrescenta a linha ao registo. Se o projeto não tiver perguntas escritas, regista os documentos que dizem o que ele já sabe. Se não servir nenhum, regista "nenhum".
4. Faz uma **lista de trabalho**: as perguntas ainda em aberto que este vídeo pode tocar, pelo título, pela descrição e pela transcrição, cada uma com o código e o texto **tal como estão no ficheiro**. Junta as pistas que o projeto já anotou sobre este vídeo ou sobre vídeos anteriores (por exemplo, "menu visto mas não aberto").

Se o assunto ficou com "nenhum", salta este passo e o ponto 7 do passo 4.

## 2. Capturar os ecrãs

```
python scripts/capturar_ecras.py videos/<pasta>
```

- Grava `ecras/MM-SS.jpg` e as folhas de miniaturas (9 por folha) em `ecras/folhas/`.
- Se a saída passar de **~250 ecrãs** (mais de ~28 folhas), volta a correr com `--limiar 0.15`. Num vídeo sem demonstração de ecrã (uma palestra, por exemplo), as capturas por minuto chegam.
- Para um instante específico que faltou, usa `--em MM:SS,MM:SS`.

## 3. Rever os ecrãs

1. Vê **todas** as folhas (`ecras/folhas/folha-NN.jpg`) e anota, por minuto, o ecrã e o menu visíveis.
2. Abre em **tamanho real** só os ecrãs-chave: os que mostram um formulário de configuração, uma tabela com valores, o resultado de uma ação, uma mensagem de erro ou o menu aberto. Num vídeo de 45 minutos, cerca de 15 a 25 chegam. O tamanho real gasta muito contexto, por isso escolhe bem.
3. **Os momentos que tocam numa pergunta da lista de trabalho (passo 1b) são sempre ecrãs-chave**, mesmo que pareçam um ecrã banal: abre-os em tamanho real. Se a transcrição fala de um desses temas num intervalo em que as folhas não têm nenhum ecrã, pede-o com `--em`. A captura automática pode saltar minutos inteiros.
4. Procura também a versão do software (rodapé, "Acerca de") e o nome do apresentador no ecrã.

## 4. Escrever `videos/<pasta>/dissertacao.md`

Segue a estrutura de `videos/officegest/webinar-2-contabilidade-officegest/dissertacao.md`, que é o exemplo de referência:

0. **Ficha de busca** (frontmatter YAML, no topo do arquivo): `titulo`, `tema`, `sistema` (com versão, se houver), `publicado`, `link` e `palavras-chave`. As palavras-chave são os **termos que alguém usaria para procurar** o que o vídeo ensina, no vocabulário do assunto (ex.: "declaração periódica de IVA", "lançamentos em lote"). É por elas que outros projetos encontram a dissertação.
1. **Cabeçalho** em tabela: link, canal, apresentador, data de publicação, duração, data de processamento, fonte do texto, número de ecrãs e versão do software (se aparecer).
2. **Aviso de idade:** se o vídeo tiver mais de 12 meses, avisa que tudo é **hipótese datada** ("segundo o vídeo de AAAA-MM") até ser confirmado no sistema atual. Explica a marca ❓.
3. **Resumo:** o fio condutor do vídeo e a lista dos temas.
4. **Mapa** de onde fica cada coisa (menus), quando for um tutorial de software.
5. **Uma secção por tema**, com o intervalo de minutos (≈ MM:SS–MM:SS), o caminho de menu, os campos e os valores lidos no ecrã, e as regras e erros demonstrados. Embute os screenshots que provam cada ponto com `![descrição](ecras/MM-SS.jpg)`. Põe em tabela os valores que aparecem no ecrã.
6. **O que foi anunciado como futuro** no vídeo, marcado com "falta verificar se existe hoje".
7. **Ligação ao projeto de destino** (o do passo 1b). O título é "O que este vídeo pode responder no projeto <nome>". Começa com uma linha a dizer **a data da consulta e os ficheiros lidos** ("Perguntas consultadas em AAAA-MM-DD em: …"), para se saber que a tabela é o retrato desse dia. Depois, uma tabela com uma linha por pergunta da lista de trabalho: o código, o que o vídeo mostra, e o que ficou por ver. **Marca as divergências** com o que o projeto já tem registado. Regras:
   - Só citas um código de pergunta que **leste no ficheiro** nesta sessão. Não deduzas códigos a partir de referências noutros documentos.
   - Uma pergunta da lista de trabalho que o vídeo afinal **não responde** também entra, com "não responde": poupa a quem lê ir procurar.
   - Se o vídeo levanta uma pergunta que o projeto ainda não tem, escreve-a como **pergunta sugerida**, sem lhe inventar código.
   - Se o projeto não tem perguntas escritas, a tabela passa a ser "o que este vídeo acrescenta ao que o projeto já sabe".
   - **Não edites o outro projeto**: ele tem o seu próprio processo para absorver cada vídeo.
8. **Pontos a verificar no sistema atual** (checklist) e **Limites desta versão**.

Regras de escrita:

- Português, em linguagem clara. Mantém os termos exatamente como aparecem no ecrã (incluindo o português de Portugal: "ecrã", "ficheiro", "Factura").
- Escreve a explicação com as tuas palavras. **Não copies a transcrição**; no máximo, uma frase curta entre aspas quando a formulação importar.
- Marca com ❓ o que nem a fala nem o ecrã deixam claro. Não inventes para tapar buracos.
- Não incluas palavras-passe nem dados pessoais que apareçam no ecrã.

## 5. Registar e responder

- Acrescenta (ou atualiza) a linha do vídeo em `videos/fontes-video.md`, o **índice**, na secção do assunto (cria a secção se for um assunto novo). As colunas são: Vídeo (título, canal, versão, duração), Publicado (AAAA-MM), **O que ensina** (os temas numa frase, com as mesmas palavras das palavras-chave) e a ligação para a dissertação. Dentro de cada assunto, ordena do mais recente para o mais antigo.
- Se o vídeo atualiza um tema que já tem dissertação de um vídeo mais antigo, diz na nova dissertação **o que mudou** em relação à anterior, e na anterior acrescenta no topo um aviso a apontar para a mais recente.
- Responde ao utilizador com: o link para o `.md`, a idade do vídeo, os temas cobertos, o que responde no projeto de destino, os pontos a verificar e quanto do vídeo ficou com ❓.
- **Apaga o `video.mp4` no fim, sem perguntar** (cerca de 120 MB por 45 minutos). Só depois de a dissertação estar escrita, de confirmares que todas as imagens que ela embute existem em `ecras/`, e do commit feito. Diz na resposta que o apagaste. Se mais tarde faltar um ecrã, o `capturar_ecras.py --em` volta a descarregar o vídeo.

## Rever a ligação (vídeos já dissertados)

Usa-se quando o utilizador pede para rever os vídeos de um assunto com as perguntas atuais do projeto de destino. **Não é automático**: só a pedido. Reescreve **só** a secção "O que este vídeo pode responder no projeto …" e a checklist "Pontos a verificar no sistema atual" de cada dissertação. O resto do texto não é tocado.

1. **Âmbito.** O pedido diz o assunto (todos os vídeos dele, pelo índice `videos/fontes-video.md`) ou um vídeo em particular. Se não disser, pergunta.
2. **Perguntas atuais.** Faz o passo 1b uma vez para o assunto: lê por inteiro os ficheiros do registo `videos/projetos-destino.md`. Lê também o registo de vídeos do projeto, para saber que vídeos ele já absorveu e que notas tirou de cada um.
3. **Para cada vídeo**, do mais antigo para o mais recente:
   1. Lê a `dissertacao.md` e a `transcricao.txt` da pasta. Faz a lista de trabalho deste vídeo com as perguntas **de hoje**.
   2. Volta aos ecrãs **já guardados** em `ecras/`. Se `ecras/folhas/` existir, revê as folhas; se não, usa os minutos da transcrição e da dissertação para escolher os ecrãs. Abre em tamanho real os que tocam numa pergunta da lista de trabalho, mesmo os que a dissertação não embute: uma pergunta nova pode estar respondida num ecrã que antes não interessava.
   3. **Nunca repitas a captura automática** de um vídeo já dissertado: apaga os ecrãs pedidos à mão que a dissertação embute. Se faltar um instante, pede só esse com `--em MM:SS` (descarrega o vídeo de novo) e apaga o `video.mp4` no fim.
   4. Reescreve a secção de ligação com as regras do ponto 7 do passo 4. A primeira linha passa a ser "Perguntas consultadas em AAAA-MM-DD (revisão; a versão anterior era de AAAA-MM-DD) em: …". Atualiza a checklist: acrescenta os pontos novos e mantém os que continuam por verificar.
   5. Se a revisão mostrar que o **corpo** da dissertação tem um erro ou uma falta, **não o corrijas neste modo**: escreve-o no fim da secção de ligação, numa linha "A rever no texto acima", e diz-o na resposta.
4. **Commit único** em `main`, só com as dissertações revistas: `docs: rever a ligação de <assunto> ao projeto <nome>`. No corpo, uma linha por vídeo com o que mudou.
5. **Responde** com, por vídeo: quantas perguntas a tabela tinha e passou a ter, o que apareceu de novo, as perguntas sugeridas e as divergências. Lembra que o projeto de destino **não foi editado**: é ele que decide o que absorve.

## Gravação local com dados reais

Usa-se quando o pedido aponta para um **ficheiro de vídeo no disco** (uma gravação de ecrã ou de telemóvel) em vez de um link. Estas gravações costumam mostrar dados reais de clientes, por isso as regras são outras. Os passos 1 a 5 **não se aplicam**: aqui a ferramenta só prepara o material (a fala em texto e os ecrãs). A análise escrita é do projeto que a pediu, no sítio e no formato que ele definir.

Regras, antes de correr qualquer comando:

- **Nada da gravação fica nesta pasta nem entra no git.** A pasta de destino é dada pelo projeto que pediu (no winners-group: `C:\projetos\winners-group\dados\gravacoes\<código>`). Os scripts recusam uma pasta versionada com o código de saída 3. Não contornes a recusa: pede outra pasta.
- **O vídeo original nunca é copiado, movido nem apagado.** A regra "apaga o `video.mp4` no fim" é só para vídeos do YouTube.
- **Não acrescentes a gravação a `videos/fontes-video.md`**, não escrevas `dissertacao.md` aqui e não faças commit nesta pasta.
- **O som não sai da máquina, mas o que leres sai.** A transcrição e os ecrãs que abrires são processados pelo serviço da Anthropic. Abre os ecrãs de que precisas, não todos. No que escreveres, não copies NIFs, IBANs nem palavras-passe.

Passos, a correr com os caminhos completos dos scripts (`C:\projetos\dissertador-videos-youtube\scripts\…`) e `PYTHONIOENCODING=utf-8`:

1. **Preparar:**
   ```
   python scripts/preparar_local.py "<ficheiro>" --destino "<pasta>" --titulo "<título>" --gravado AAAA-MM-DD
   ```
   Lê a linha "Som:". Se disser que o som só existe até um certo minuto, **avisa o utilizador logo**: o resto do vídeo só tem imagem, e ele pode ter o ficheiro original com o som inteiro.
2. **Transcrever:**
   ```
   python scripts/transcrever_audio.py "<pasta>"
   ```
   - Se disser que o modelo não está na máquina, corre uma vez `python scripts/transcrever_audio.py --descarregar-modelo` (cerca de 1,6 GB; é o único passo que vai à internet).
   - Demora menos do que a duração do áudio (entre 0,3 e 0,6 vezes, medido em outubro de 2026 num portátil sem placa gráfica; quanto mais silêncio, mais rápido) e deixa o computador lento. Acima de 20 minutos de vídeo, corre em segundo plano e avisa o utilizador de quanto vai demorar.
   - No fim, lê as três medições. **"Frases repetidas" acima de zero** quer dizer texto inventado num silêncio: encontra esses blocos e não os uses. **"Fala"** diz quanto do vídeo tem alguém a falar.
   - `--trecho 33:00-43:00 --saida <nome>.txt` transcreve só uma parte, para um teste rápido.
   - Não uses `--vocabulario` por omissão: no piloto acertou nomes como "OfficeGest" e "fatura-recibo", mas trocou frases inteiras por outras sem sentido e perdeu pontuação. Sem ele, o texto é mais fiel e erra só os nomes: conta com "Office de Edge" por OfficeGest, "fatores recibo" por faturas-recibo, e valores com "R$" que no ecrã são euros.
3. **Capturar os ecrãs:** `python scripts/capturar_ecras.py "<pasta>"`, como no passo 2 de cima. Uma gravação de ecrã com a imagem parada gera poucos ecrãs; pede com `--em` os instantes em que a fala aponta para alguma coisa.
4. **Ler:** a transcrição inteira, as folhas de miniaturas, e em tamanho real os ecrãs-chave. O texto **não separa quem fala**: quando houver duas pessoas, distingue-as pelo conteúdo e, se não der, não atribuas a frase a ninguém. Os nomes de menus e os valores vêm dos ecrãs, não da fala.
5. **Responder** com: onde ficou o material, quanto demorou, quanto do vídeo é fala, e qualquer aviso (som em falta, frases repetidas). O que fazer com o material é do projeto que pediu.
