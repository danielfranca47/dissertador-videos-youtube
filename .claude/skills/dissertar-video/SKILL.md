---
name: dissertar-video
description: Transforma um vídeo do YouTube num .md detalhado, com screenshots dos ecrãs demonstrados, para servir de base de conhecimento a projetos do Claude Code. Use sempre que o utilizador colar um link do YouTube (youtube.com ou youtu.be) e pedir para dissertar, documentar, resumir em detalhe, extrair o conhecimento ou "fazer" o vídeo, ou quando pedir para reprocessar ou atualizar um vídeo já processado.
argument-hint: <link-do-youtube> [projeto de destino, opcional; por omissão, o do registo videos/projetos-destino.md]
---

# Dissertar vídeo do YouTube

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
