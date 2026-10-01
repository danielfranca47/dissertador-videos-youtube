---
name: dissertar-video
description: Transforma um vídeo do YouTube num .md detalhado, com screenshots dos ecrãs demonstrados, para servir de base de conhecimento a projetos do Claude Code. Use sempre que o utilizador colar um link do YouTube (youtube.com ou youtu.be) e pedir para dissertar, documentar, resumir em detalhe, extrair o conhecimento ou "fazer" o vídeo, ou quando pedir para reprocessar ou atualizar um vídeo já processado.
argument-hint: <link-do-youtube> [projeto de destino, opcional]
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
3. Procura também a versão do software (rodapé, "Acerca de") e o nome do apresentador no ecrã.

## 4. Escrever `videos/<pasta>/dissertacao.md`

Segue a estrutura de `videos/officegest/webinar-2-contabilidade-officegest/dissertacao.md`, que é o exemplo de referência:

0. **Ficha de busca** (frontmatter YAML, no topo do arquivo): `titulo`, `tema`, `sistema` (com versão, se houver), `publicado`, `link` e `palavras-chave`. As palavras-chave são os **termos que alguém usaria para procurar** o que o vídeo ensina, no vocabulário do assunto (ex.: "declaração periódica de IVA", "lançamentos em lote"). É por elas que outros projetos encontram a dissertação.
1. **Cabeçalho** em tabela: link, canal, apresentador, data de publicação, duração, data de processamento, fonte do texto, número de ecrãs e versão do software (se aparecer).
2. **Aviso de idade:** se o vídeo tiver mais de 12 meses, avisa que tudo é **hipótese datada** ("segundo o vídeo de AAAA-MM") até ser confirmado no sistema atual. Explica a marca ❓.
3. **Resumo:** o fio condutor do vídeo e a lista dos temas.
4. **Mapa** de onde fica cada coisa (menus), quando for um tutorial de software.
5. **Uma secção por tema**, com o intervalo de minutos (≈ MM:SS–MM:SS), o caminho de menu, os campos e os valores lidos no ecrã, e as regras e erros demonstrados. Embute os screenshots que provam cada ponto com `![descrição](ecras/MM-SS.jpg)`. Põe em tabela os valores que aparecem no ecrã.
6. **O que foi anunciado como futuro** no vídeo, marcado com "falta verificar se existe hoje".
7. **Ligação a um projeto** (se o utilizador indicar um, ou se for óbvio, como o OfficeGest → `C:\projetos\winners-group`): lê o que esse projeto já sabe (docs, perguntas em aberto) e faz uma tabela "o que este vídeo pode responder", **marcando as divergências** com o que lá está. **Não edites o outro projeto**: o utilizador aponta-o depois para a dissertação.
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
