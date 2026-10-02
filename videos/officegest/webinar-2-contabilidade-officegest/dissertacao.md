---
titulo: "Webinar #2: Contabilidade OfficeGest"
tema: officegest
sistema: OfficeGest v2.220
publicado: 2020-06-03
link: https://www.youtube.com/watch?v=vW9GhkTXmNU
palavras-chave: [contabilidade, classificação de artigos, plano de contas, contas de terceiros, mercados, contas bancárias, lançamento automático, lançamentos em lote, integração automática, lançamentos recorrentes, declaração periódica de IVA, SAF-T, taxonomias, balancete, balanço, demonstração de resultados, mapas, apuramento de IVA, apuramento de resultados, e-Fatura]
---

# Webinar #2: Contabilidade OfficeGest

> 🔁 **Há um vídeo mais recente sobre o mesmo tema:** [Formação Prática Módulo Contabilidade](../formacao-pratica-modulo-contabilidade/dissertacao.md) (gravado em 2021-09, v3.043). Repete a parametrização com mais detalhe e acrescenta as declarações (Modelo 10), a contabilidade analítica e o reencaminhamento de contas. A secção "O que mudou desde o webinar de 2020" dessa dissertação lista as diferenças. Esta continua a ser a melhor fonte para o botão de contabilização na fatura, o SAF-T e as taxonomias.

> 🔁 **O menu "Importação E-fatura"**, que aqui só se vê fechado, é **aberto** na [Formação Prática Módulo Configuração Geral](../formacao-pratica-modulo-configuracao-geral/dissertacao.md) (gravada em 2021-08, v3.039), secção 2.

| | |
|---|---|
| **Vídeo** | [youtu.be/vW9GhkTXmNU](https://www.youtube.com/watch?v=vW9GhkTXmNU) |
| **Canal** | Officegest (canal oficial) |
| **Apresentador** | Pedro Jordão (nome no ecrã) |
| **Publicado em** | 2020-06-03 |
| **Duração** | 46:37 |
| **Processado em** | 2026-10-01 |
| **Fonte do texto** | Legendas automáticas do YouTube (pt), com muitos erros, **corrigidas pelos ecrãs**. Os nomes de menus e campos abaixo foram lidos nos screenshots |
| **Ecrãs** | 194 capturados em [`ecras/`](ecras/); os mais úteis estão embutidos abaixo |
| **Versão do OfficeGest** | **vr 2.220** (rodapé do menu), em ambiente "Demonstração", exercício A2020 |

> ⚠️ **Vídeo com mais de 6 anos.** Tudo o que está abaixo descreve o OfficeGest **como era em junho de 2020, na versão 2.220**. Trate cada afirmação como **hipótese**, com a forma "segundo o webinar de 2020-06", até ser confirmada no sistema atual. Os screenshots servem para comparar: se o ecrã de hoje for diferente, houve mudança.
>
> ❓ = ponto que nem a fala nem o ecrã deixam claro.

---

## Resumo

É uma formação do canal oficial sobre o **módulo de contabilidade** do OfficeGest, feita como demonstração ao vivo na conta de demonstração. O fio condutor é **parametrizar uma vez para que os documentos de vendas e compras passem sozinhos para a contabilidade**. A ordem é esta:

1. **Classificação de artigos.** Cada artigo tem uma classificação, e essa classificação diz em que contas de venda, compra, IVA e devolução o artigo é lançado, por taxa de IVA e por mercado.
2. **Contas de terceiros.** As contas de clientes (211…) e de fornecedores (221…) são criadas automaticamente.
3. **Contas bancárias e caixa.** Definem a conta de recebimentos e de pagamentos de cada banco.
4. **Lançamentos.** Há três formas de lançar: na própria fatura, em massa pelo ecrã **Lançamentos em lote**, ou por **integração automática diária**, configurada por mês no exercício, com relatório de erros por email. Existem também lançamentos manuais e lançamentos recorrentes.
5. **Declaração periódica de IVA.** Cada campo da declaração soma as contas associadas a ele. A declaração exporta em XML e imprime.
6. **SAF-T e taxonomias.**
7. **Relatórios e Mapas** personalizáveis, exportáveis para Excel.
8. **Apuramento de IVA e de resultados.**

### Onde fica cada coisa (versão 2.220)

Todo o módulo de contabilidade está no menu lateral **Contabilidade**:

- Plano de Contas · Lançamentos · **Lançamentos em lote** · **Apuramento de resultados/I.V.A.** · Centros de Custo · **Declaração periódica** · Exportar
- **Ficheiros de Apoio** → Exercícios · Documentos · Diário · Apuramento · **Classificação de artigos** · **Mercados** · Reencaminhamento de contas · Reencaminhamento de centros de custo · **Lançamentos recorrentes** · **Taxonomias** · **Parâmetros**

Fora dele ficam:

- **Stocks → Ficheiros de Apoio → Famílias**
- **Tabelas de Apoio → Financeiros → Contas Bancárias**
- **Relatórios → Contabilidade** (balancetes, extratos, balanço, demonstração de resultados, mapas)
- **Relatórios → Automáticos**
- **Comunicações AT** → Exportar SAFT-PT · Inventário · Importação E-fatura

---

## 1. Classificação de artigos (≈ 04:00–12:40)

**Caminho:** Contabilidade → Ficheiros de Apoio → **Classificação de artigos**.

![Lista de classificações de artigos](ecras/04-24.jpg)

- A classificação é atribuída **por artigo**, e não por documento. Numa mesma fatura, cada linha pode ir para contas diferentes.
- O OfficeGest traz **um plano de contas próprio** (SNC), e as classificações iniciais vêm feitas sobre ele. Quem usar **um plano de contas seu** tem de refazer as classificações. Importar o SAF-T da contabilidade de outro programa com um plano diferente também traz dificuldades.
- Para criar uma classificação, usa-se o botão de nova classificação. O formulário tem **Classificação** (por exemplo, "[1] Mercadorias"), **IVA** (a taxa) e três separadores:
  - **Vendas:** Conta Venda · Conta IVA Venda · Conta Devolução Venda · Conta Devolução IVA Venda;
  - **Compras:** Conta Compra · Conta IVA Compra · Conta Devolução Compra · Conta Devolução IVA Compra;
  - **Inventário permanente.**
- Em cada separador há uma linha por **mercado**: **Nacional**, **Comunitário** e **Internacional**.

![Classificação "Mercadorias", IVA 23 %, separador Compras](ecras/09-44.jpg)

*Exemplo no ecrã (Mercadorias, 23 %, Compras):*

| Mercado | Conta Compra | Conta IVA Compra | Conta Devolução Compra | Conta Devolução IVA Compra |
|---|---|---|---|---|
| Nacional | 3111131 Taxa Normal – Continente | 24321131 Taxa Normal – Continente | 31711131 Taxa Normal – Continente | 24342231 Taxa Normal – Continente |
| Comunitário | 311213 Compra IC: Taxa Normal | 24321231 Taxa Normal – IC | 317221 Com IVA dedutível | — |
| Internacional | 31133 Isentas | — | 317233 Isentas | — |

Na lista, a mesma classificação nas **vendas, a 23 %, nacional** usa **7111131** (venda) e **24331131** (IVA liquidado).

**Como se atribui a classificação ao artigo:**

- **Por família** (o caminho recomendado para começar): em **Stocks → Ficheiros de Apoio → Famílias**, ao editar a família há um campo **Classificação do artigo**. Os artigos criados nessa família herdam a classificação.

  ![Editar Família com o campo Classificação do artigo](ecras/11-17.jpg)

- **Por artigo:** na ficha do artigo existe o separador **Contabilidade**. A ficha também mostra o **Tipo Artigo** (por exemplo, "Contabilístico") e o **IVA**.

  ![Ficha do artigo com o separador Contabilidade](ecras/11-54.jpg)

## 2. Contas de clientes e fornecedores (≈ 12:15–17:00)

O objetivo é que a conta de terceiro seja **criada automaticamente quando se cria a entidade**. São dois passos.

**Passo 1. Contabilidade → Ficheiros de Apoio → Parâmetros** (ecrã "Configuração", separador **Contas**):

- **Conta Base Clientes C/C = 211** e **Conta Base Forn. C/C = 221**, ambas com **Nº Digs. = 5** e a opção **Criar conta automaticamente**;
- no mesmo ecrã: as contas de descontos e proveitos financeiros (686 e 7822), os arredondamentos (7888 e 68888) e a retenção na fonte nas compras (2422).

![Parâmetros: contas de terceiros](ecras/13-02.jpg)

**Passo 2. Contabilidade → Ficheiros de Apoio → Mercados:** a conta base de clientes e de fornecedores **por mercado**. No ecrã: Nacional **21111 / 22111**, Comunitário **21112**, Internacional **21113 / 22113**.

![Mercados com as contas base](ecras/13-55.jpg)

- **Resultado:** a conta do cliente é a conta base do mercado mais o número do cliente. No ecrã aparecem, por exemplo, **2111100022** (cliente 22, nacional) e **2111100003**.
- Quem importou um plano de contas diferente terá de fazer uma **transferência de contas**.
- **Para entidades que já existem sem conta:** o botão **Criação de contas** abre uma janela com as opções **Clientes** e **Fornecedores** e um intervalo de datas de documentos emitidos, e cria as contas em falta. No exemplo, a resposta foi "Nenhuma conta foi criada", porque já existiam todas.

![Criação de contas](ecras/15-35.jpg)

## 3. Contas bancárias e caixa (≈ 17:00–20:45 e 45:00–46:30)

**Caminho:** **Tabelas de Apoio → Financeiros → Contas Bancárias**.

- Cada conta (no exemplo: CGD, CXC – Caixa Defeito, Millennium BCP) tem, na secção **Contabilidade**, o **Nº Conta Contabilidade (Recebimentos)** e o **Nº Conta Contabilidade (Pagamentos)**. No exemplo: Caixa → **111**, Millennium BCP → **1201**.
- Existe a opção **"Assumir esta conta bancária como gestão de caixa / balcão"**.
- Os recebimentos em numerário vão para a caixa. Os recebimentos por multibanco ou transferência vão para o banco escolhido.

![Conta bancária Millennium BCP com as contas de recebimentos e pagamentos](ecras/17-54.jpg)

- **Banco novo:** primeiro cria-se a conta em **Contabilidade → Plano de Contas → Nova Conta** (o exemplo é a 1202). Depois, na conta bancária, escolhe-se essa conta.
- **Anunciado para "uma próxima versão" (2020):** tratar o TPA ou multibanco como uma conta de caixa própria e transferir para o banco no **fecho do TPA**. **Falta verificar se isto existe hoje.**

## 4. Lançamentos contabilísticos (≈ 20:45–30:15)

### 4.1 Na própria fatura

- Uma fatura emitida (no exemplo, **FT 9999/33**: cliente [22] Pedro, artigo a 23 %, 10,00 € + 2,30 € de IVA) tem no canto superior direito um botão laranja **"Contabili…"** ❓ (o nome está tapado pela imagem da câmara), que faz o lançamento.
- Se faltar conta no artigo, na entidade ou no banco (no caso do recibo), o sistema avisa e não lança.

![Fatura FT 9999/33 com o botão de contabilização](ecras/21-42.jpg)

O lançamento resultante fica no **Diário [50] Vendas**, com o **Documento [51] N/Factura** e a origem FT 9999/33:

| Conta | Título | Débito | Crédito |
|---|---|---|---|
| 7111131 | Taxa Normal – Continente | | 10,00 |
| 24331131 | Taxa Normal – Continente | | 2,30 |
| 2111100022 | Pedro | 12,30 | |

![Lançamento gerado pela fatura](ecras/22-20.jpg)

### 4.2 Em massa: **Lançamentos em lote**

**Caminho:** Contabilidade → **Lançamentos em lote**.

- **Filtros:** Data Lançamento Contabil. ou Data Doc. (desde / até), Diário, Documentos (com atalhos **Vendas**, **Compras** e **Bancos**) e Série de Documentos.
- **Botões:** **Filtrar**, **Validar** e **Processar**.
- A lista mostra os documentos ainda não lançados, com Tipo Doc., Documento, datas, Cód. Diário, Cód. Documento, Descritivo e uma caixa **Lançar**. À direita aparece a **pré-visualização** do lançamento do documento selecionado.
- **Validar** pinta **a vermelho** os documentos com problemas. **Processar** lança os documentos marcados e mostra o resultado, com o número de documentos lançados e a lista de erros.

![Lançamentos em lote](ecras/22-55.jpg)

- **Regra vista no ecrã:** com o exercício A2020 ativo, os documentos de 2018 dão o erro **"Tem de comutar para um exercício compatível"**. O exercício tem de corresponder à data do documento.

![Resultado: 1 documento lançado, erros de exercício incompatível](ecras/25-00.jpg)

### 4.3 Integração automática diária

- **Contabilidade → Ficheiros de Apoio → Exercícios:** cada mês de cada exercício tem o estado (Aberto ou fechado) e uma opção **Integrar**. No exemplo, todos os meses de 2020 estão marcados. Segundo a fala, a integração corre **todos os dias, de madrugada**, e lança os documentos dos meses marcados que ainda não estão na contabilidade.

  ![Exercícios com os meses marcados para integrar](ecras/25-23.jpg)

- Os documentos com contas em falta não são lançados. Os erros vão por email, configurados em **Relatórios → Automáticos** ("Relatórios automáticos por e-mail"), separador **Diário**, secção Contabilidade → **Integração Contabilidade**, onde se escolhe o destinatário (no exemplo, o Administrador).

  ![Relatório automático diário da integração da contabilidade](ecras/32-25.jpg)

### 4.4 Lançamentos manuais e recorrentes

- **Contabilidade → Lançamentos → novo:** Data, Descritivo, Documento, Diário, Origem e Tipo de Lançamento (Normal), e as linhas de conta com débito e crédito. Os botões são **Guardar** e **Associar**.
- **Lançamentos recorrentes** (Contabilidade → Ficheiros de Apoio): cria-se um modelo com uma designação e uma lista de contas (no exemplo, 111 Caixa, 24331111 Taxa Reduzida – Continente e uma conta de fornecedor). Se a conta não existir no exercício, aparece o erro "Não existe essa conta no exercício".

  ![Lançamento recorrente TESTE com as contas](ecras/29-36.jpg)

- No novo lançamento, o botão **Associar** → **"Associar lançamento recorrente"** preenche as contas. Só faltam os valores.

## 5. Declaração periódica de IVA (≈ 30:15–33:20)

**Caminho:** Contabilidade → **Declaração periódica**.

- A lista mostra o Período (por exemplo, "1º Trimestre"), o Ano, **A Pagar**, **A Recuperar** e o Estado (**Aberto** / **Fechado**). A **Nova declaração** pede o ano e o mês ou trimestre.
- A declaração é apresentada **com o aspeto do modelo oficial da AT**. Cada campo tem uma lupa que abre **"Contas do campo N"**: a lista de contas e, para cada uma, **Calcular = Saldo, Débito ou Crédito**. Podem retirar-se contas ou **adicionar** novas.

![Contas associadas ao campo 3](ecras/31-04.jpg)

- **A ligação também se faz pela conta.** Em **Plano de Contas**, cada conta tem os campos **Campo na Declaração do IVA**, **Campo na Declaração do IVA (Anual)** e **Regularização**. É aqui que, segundo a fala, se indicam as contas dos **campos 40 e 41**. Cada conta tem ainda a **Taxa associada**, o **Tipo Conta** (Integração ou Movimento) e o **Código taxonomia**.

  ![Ficha de conta com os campos da declaração de IVA](ecras/32-06.jpg)

- Com as classificações e a integração bem feitas, os campos preenchem-se sozinhos.
- O botão **Finalizar** fecha a declaração. Depois aparecem os botões **Editar**, **Exportar** (gera o ficheiro `declaracao_periodica_….xml` para submeter nas Finanças) e **Imprimir** (PDF).

  ![Declaração finalizada com Editar, Exportar e Imprimir](ecras/32-43.jpg)

- Os **reembolsos** constavam da agenda, mas não foram demonstrados ❓.

## 6. SAF-T e taxonomias (≈ 33:20–36:00)

- **Comunicações AT → Exportar SAFT-PT** ("SAFT-PT: Gerar ficheiro"). Os passos são:
  1. o **formato**: Auditoria, Comunicação de documentos (envio mensal pelo portal das Finanças) ou **Contabilidade**, com a versão 1.04_01 (Portaria n.º 302/2016);
  2. o **período**: ano e **mês**. Segundo a fala, antes só se podia extrair por ano;
  3. o **formato de envio**: Ficheiro, ou Ficheiro & E-Mail.

![Exportar SAF-T, com o menu Comunicações AT aberto](ecras/33-37.jpg)

- No mesmo menu existe **Importação E-fatura** (não foi demonstrada).
- Os contabilistas que submeteram o SAF-T da contabilidade tiveram **erros de taxonomia**. A solução mostrada:
  - em **Contabilidade → Ficheiros de Apoio → Taxonomias** está a tabela (Código, Código SNC Base, Descrição), que depende do regime (por exemplo, microentidades);
  - **"Atualizar plano de contas"** atribui o código de taxonomia a cada conta de movimento. Depois, filtra-se o Plano de Contas pelas contas de movimento **sem** código e completa-se à mão.

![Atualizar plano de contas com os códigos de taxonomia](ecras/35-24.jpg)

## 7. Relatórios (≈ 36:00–38:40)

Os relatórios estão em **Relatórios → Contabilidade**:

- **Balancetes:** Balancete analítico, Balancete razão e Balancete por taxonomia. Filtram-se por exercício, intervalo ou seleção de contas, mês inicial e final e grau, com tipo de impressão Mensal, Acumulado ou Mensal e acumulado. Podem **imprimir-se** ou exportar-se para **Excel**.

  ![Balancete analítico](ecras/36-32.jpg)

- **Extratos:** Extrato de Conta e Extrato Diário. O extrato de uma conta também se abre pelo botão **Extracto** da própria conta, no Plano de Contas.
- **Balanço** e **Demonstração dos resultados por naturezas:** em 2020 calculavam-se por **fórmulas sobre contas** editáveis em cada rubrica, com comparação de dois anos. Foi anunciado que passariam a usar as **taxonomias**. **Falta verificar** como funciona hoje.

## 8. Mapas, novidade em 2020 (≈ 38:40–43:10)

- **Relatórios → Contabilidade → Mapas → Novo mapa:** Designação, **Novo** ou **Baseado em** (um mapa existente), e o número de **Páginas**, **Linhas** e **Colunas**. Cada página vira uma folha do Excel.

  ![Novo mapa](ecras/38-59.jpg)

- O editor funciona como uma folha de cálculo, com texto, formatação e **fórmulas**, por exemplo o saldo de uma conta num intervalo de datas. O botão **Calcular** preenche os valores, e o mapa exporta para Excel.

  ![Editor de mapa com uma fórmula](ecras/42-24.jpg)

## 9. Apuramentos de IVA e de resultados (≈ 43:10–45:00)

- **Contabilidade → Ficheiros de Apoio → Apuramento:** lista os apuramentos configurados, como o **APUR – Apuramento IVA** (conta 24351) e os apuramentos de resultados (resultado operacional, financeiro, corrente, antes de impostos, líquido). Cada um tem as contas a apurar.

  ![Apuramentos configurados](ecras/44-06.jpg)

- **Contabilidade → Apuramento de resultados/I.V.A.**, separadores **IVA** e **Resultados**: escolhe-se o apuramento, a conta, o Diário e o Documento ([70] Apuramento IVA), a data e o período (por exemplo, "2º Trimestre"). O botão **Executar** cria o lançamento de apuramento.

  ![Apuramento de IVA](ecras/43-31.jpg)

---

## O que este vídeo pode responder no projeto winners-group

Perguntas consultadas em 2026-10-02 (revisão; a versão anterior era de 2026-10-01) em: `docs/dependencias-externas.md`, `docs/pendentes.md` e `contabilidade/processo-atual/perguntas-em-aberto.md` do projeto `C:\projetos\winners-group`, lidos por inteiro, mais o registo de vídeos `docs/fontes-videos.md`. A tabela é o retrato desse dia: se as perguntas mudarem, pede-se nova revisão.

Tudo o que está na coluna do meio é **segundo o webinar de 2020-06 (versão 2.220)** e continua **por confirmar no OfficeGest atual**. Os instantes entre parênteses são ecrãs guardados em [`ecras/`](ecras/).

| Pergunta (código e texto no projeto) | O que o vídeo mostra | O que ficou por ver |
|---|---|---|
| **OG-9** — O OfficeGest tem um importador do e-Fatura? | O menu **Comunicações AT** tem três entradas: *Exportar SAFT-PT*, *Inventário* e **Importação E-fatura** ([33:37](ecras/33-37.jpg)). | A entrada **não foi aberta** neste vídeo. ⚠️ **Divergência com o projeto:** o projeto regista que não se sabe o que esta entrada faz. Ela é **aberta e explicada** na [Formação Prática Módulo Configuração Geral](../formacao-pratica-modulo-configuracao-geral/dissertacao.md), secção 2, que o projeto ainda não tem no seu registo de vídeos. |
| **OG-6** — As oficinas têm o módulo DMS (OCR) licenciado? | Só a entrada **Gestão Documental** no menu lateral, visível em quase todos os ecrãs ([01:45](ecras/01-45.jpg)). | Nunca foi aberta. Não se sabe se é o DMS. |
| **C-24** — A equipa usa o lançamento automático ou lança à mão? | **Três formas de lançar** (botão na fatura, *Lançamentos em lote*, integração diária por mês). Novo nesta revisão: (1) a lista *Lançamento de Documentos* já tinha em 2020 **faturas de fornecedor lançadas** ("Factura Fornecedor FAF 9999/22", diário 40) e uma linha "Compras / Despesas", ao lado das vendas ([22:47](ecras/22-47.jpg)), ou seja, as compras passam pelo mesmo mecanismo; (2) os *Lançamentos em lote* têm um atalho **Compras** ([22:55](ecras/22-55.jpg)); (3) o ecrã *Exercícios* tem uma coluna **Colaboradores**: o exercício de 2020 está atribuído a um utilizador e o de 2019 a outros três ([26:51](ecras/26-51.jpg)); (4) a mesma lista já tinha o botão **"Validar lançam…"** (o resto do nome está tapado pela câmara). | O vídeo só demonstra o lançamento de **vendas**; nenhuma compra é lançada à frente da câmara. Se a Winners usa alguma das três formas continua a ser pergunta para a Winners. |
| **C-24**, hora da integração | O formador diz "penso que" é de madrugada. | ⚠️ **Divergência com o projeto:** o projeto regista "de madrugada" como facto. Na fala é uma suposição, e a formação de 2021 diz que o formador não sabe a hora. |
| **C-8** — Qual é o prazo do fecho? Onde se perde mais tempo? | Não responde à pergunta, que é sobre a Winners. Mostra só o que o sistema tem para o fecho: no ecrã *Exercícios*, cada mês tem um estado (**Aberto**) com um ícone de pasta, e o exercício tem uma coluna **Fechado** ("Não") ([25:23](ecras/25-23.jpg)). | Fechar um mês ou um exercício não foi demonstrado. |
| **C-2** — "Classificar por artigos" é atribuir a conta SNC ou o artigo? | A classificação é do **artigo** (pela família ou no separador *Contabilidade* da ficha) e define as contas por **taxa de IVA e por mercado**. A ficha do artigo mostra o **Tipo Artigo "Contabilístico"** ([11:54](ecras/11-54.jpg)), o mesmo tipo que a formação de 2021 explica para as despesas. | Como a Winners trabalha. |
| **C-19** — Que regra se aplica a cascos, rappel e devoluções? | Só as **devoluções**: cada classificação tem *Conta Devolução Compra* e *Conta Devolução IVA Compra* por mercado ([09:44](ecras/09-44.jpg)). O menu tem *Reencaminhamento de contas*, não aberto. | Cascos e rappel: **não responde**. |
| **C-9** — Que impostos são registados no fecho? | Apuramento de IVA (gera um lançamento no diário [70]), declaração periódica com exportação em XML, e nos *Parâmetros* a conta **Retenção na Fonte (Compras) = 2422**, com a opção "Usar retenção no pagamento" desligada ([13:02](ecras/13-02.jpg)). | Segurança Social, PEC/PPC e Modelo 10: **não responde**. |
| **C-11** — Regime de IVA mensal ou trimestral? | A lista de declarações da demo é toda **por trimestre** ([30:32](ecras/30-32.jpg)); a fala diz que pode ser mensal. Os *Parâmetros* têm um separador **"Iva / Abertura"** ([13:02](ecras/13-02.jpg)). | O separador não foi aberto. A formação de contabilidade de 2021 diz que é aí que se escolhe o regime, mas também não o abre. |
| **C-18** — Como são tratados os contratos de leasing/ALD no fecho? | Os *Lançamentos recorrentes* são uma **lista de contas** ([29:36](ecras/29-36.jpg)); ao associar, as linhas entram com valor 0,00 e os valores escrevem-se à mão. Sem agendamento. | Bate com a nota do projeto. Nada de novo. |
| **C-5** — O que é o ficheiro de performance? | *Mapas* (relatório desenhado pelo utilizador, exporta para Excel). Novo nesta revisão: o menu *Relatórios → Contabilidade* já tinha em 2020 **Mapas analíticos**, **Centros de Custo** e *Mapa estado da conta* ([38:45](ecras/38-45.jpg)), e cada linha de lançamento tem uma coluna **Centro Custo** ([22:20](ecras/22-20.jpg)). | *Mapas analíticos* e *Centros de Custo* não foram abertos. |
| **C-21** — O OfficeGest exporta para Excel a lista de compras e o balancete? | O **balancete**: botões *Imprimir* e **Imprimir Excel** ([36:59](ecras/36-59.jpg)); a demonstração de resultados tem os mesmos. | A lista de compras: **não responde** (o relatório de compras não aparece). |
| **C-3** e **C-12** — O que conta como divergência? A equipa verifica o ATCUD? | Só uma pista: nos lançamentos de compras, o descritivo traz o **número do documento no fornecedor**, escrito de formas diferentes ("123456789", "12434", "FT00001") ([22:47](ecras/22-47.jpg)). Confirma, já em 2020, que é texto livre. | ATCUD e QR Code: **não responde** (o vídeo é anterior a ambos). |
| **C-27** — As oficinas fazem o Fecho de TPA? | O formador **anuncia** para uma versão seguinte o multibanco como conta própria e a passagem para o banco no fecho do TPA (≈ 19:10–20:45). | Não é mostrado. Existe na formação de financeira de 2021. |
| **C-26** — Como se registam os movimentos do banco sem documento? | **Não responde.** Há só duas pistas: o campo "Conta Custos Banco Pagam. Auto." nos *Parâmetros*, vazio ([13:02](ecras/13-02.jpg)), e o atalho **Bancos** nos *Lançamentos em lote*. | O menu *Bancos* nunca é aberto. |
| **OG-3** — O OfficeGest tem importação de extratos e reconciliação? | **Não responde.** | — |
| **C-16** — O processamento salarial é feito no OfficeGest? | **Não responde.** O menu *Recursos Humanos* vê-se, mas não é aberto. | — |
| **OG-10** — Que funcionalidades estão licenciadas e em uso? | **Não responde.** A conta do vídeo é uma demonstração, com o aviso de que "algumas funcionalidades serão limitadas" ([01:45](ecras/01-45.jpg)). | — |
| **D-3** — Que funcionalidades nativas a Winners já usa? | Para o inventário: classificação de artigos, criação automática de contas de terceiros, lançamentos em lote, integração automática, lançamentos recorrentes, declaração periódica, SAF-T da contabilidade, taxonomias, mapas e apuramentos. | O uso é pergunta para a Winners. |
| Sem código: **regra do risco irreversível** (citada nas notas do projeto) | O lançamento gerado por uma fatura tem os botões **Novo, Editar, Duplicar, Imprimir e Apagar** ([22:20](ecras/22-20.jpg)), e o formador apaga-o. A lista de lançamentos tem caixas de seleção e um **Apagar** para vários ([22:47](ecras/22-47.jpg)). Uma declaração finalizada volta a ter **Editar**. Novo nesta revisão: "Atualizar plano de contas" (taxonomias) pede confirmação com o aviso **"Esta operação é irreversível"** ([35:27](ecras/35-27.jpg)). | Se um mês fechado impede apagar. |

As restantes perguntas em aberto (OG-4, OG-5, OG-7, OG-8, API-1 a API-3, AT-1 a AT-4, B-1, B-2, COM-1, D-1, D-2 e as perguntas de volume e de âmbito) não são tocadas por este vídeo.

**Perguntas sugeridas** (o vídeo levanta, o projeto ainda não tem):

- Quando uma oficina nova chega com a contabilidade feita noutro programa, o histórico é importado (SAF-T da contabilidade) ou começa-se do zero? O formador avisa que a importação só corre bem se o plano de contas for o do OfficeGest (≈ 05:20–06:30).
- As oficinas usam o **plano de contas do OfficeGest** ou um plano próprio? Com um plano próprio, as classificações de artigos têm de ser refeitas (≈ 04:50–05:50).

**A rever no texto acima** (não corrigido nesta revisão, que só mexe na ligação): a secção 4.3 não refere as colunas **Colaboradores** e **Fechado** do ecrã *Exercícios* e dá a hora da integração como certa; a secção 2 não lista os separadores dos *Parâmetros*; a secção 7 não refere *Mapas analíticos* nem o relatório *Centros de Custo*; a secção 4 não refere o botão "Validar lançam…".

O projeto winners-group **não foi editado**: é ele que decide o que absorve.

## Pontos a verificar no sistema atual

- [ ] Os caminhos de menu acima continuam iguais?
- [ ] A integração automática (Exercícios → Integrar) e o relatório "Integração Contabilidade" ainda existem nestes moldes?
- [ ] O que faz hoje a **Importação E-fatura**, e se serve para a conferência das compras? (OG-9; ver primeiro a secção 2 da Formação Prática Módulo Configuração Geral)
- [ ] O TPA ou multibanco como conta própria, anunciado em 2020, chegou a existir? → Sim, em agosto de 2021 já existia o **Fecho TPA**: ver a secção 9 da [Formação Prática Módulo Financeira](../formacao-pratica-modulo-financeira/dissertacao.md). Falta confirmar no sistema atual.
- [ ] O balanço e a demonstração de resultados já são calculados a partir das taxonomias?
- [ ] A que hora corre a integração automática, e se a hora se pode escolher? (C-24)
- [ ] O ecrã *Exercícios* ainda tem as colunas **Colaboradores** e **Fechado**? Que utilizadores estão em que exercício, em cada oficina? (C-24)
- [ ] O que é a entrada **Gestão Documental** do menu: é o DMS com OCR? (OG-6)
- [ ] O separador **"Iva / Abertura"** dos Parâmetros da contabilidade mostra o regime de IVA de cada oficina? (C-11)
- [ ] O lançamento gerado por uma compra ainda se pode **apagar**, e o que acontece se o mês estiver fechado? (regra do risco irreversível)
- [ ] O que abrem hoje *Mapas analíticos* e o relatório *Centros de Custo*? (C-5)
- [ ] O menu *Ajuda → Registo de Alterações* diz quando cada função entrou (Importação E-fatura, Fecho TPA)? Se sim, data as hipóteses destes vídeos.

## Limites desta versão

- Os **ecrãs** são a fonte mais fiável dos nomes. A **explicação** do porquê vem de legendas automáticas com muitos erros; onde a fala não era clara, ficou a marca ❓.
- O vídeo anuncia uma sessão de perguntas e respostas, mas a gravação termina na demonstração.
