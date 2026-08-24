# Prompt — auditoria do PREDICTORS do zero no Codex

Copie o bloco abaixo para uma nova sessão do Codex. A auditoria deve começar sem confiar em conclusões de conversas anteriores.

---

Quero uma **auditoria longa, profunda, evidence-first e do zero** de todo o meu ecossistema PREDICTORS. Não quero que você presuma que README, HANDOFF, comentários, nomes como “canonical/source of truth”, testes verdes ou conclusões anteriores estejam corretos. **Cada afirmação de cada repositório é apenas um claim até ser validada por evidência.**

## Escopo exato

Audite estes seis repositórios e somente estes como ecossistema canônico atual:

1. `leonardosovienski/ecosystem-predictor`
2. `leonardosovienski/core-predictor`
3. `leonardosovienski/predictor-ops`
4. `leonardosovienski/cripto-predictor`
5. `leonardosovienski/brasileirao-predictor`
6. `leonardosovienski/stocks-predictor`

Comece registrando o `main` HEAD SHA de cada um. Não use memória de outro chat como evidência.

## Intenção humana que deve ser tratada separadamente da evidência técnica

A intenção atual é:

- `ecosystem-predictor`, `core-predictor` e `predictor-ops` regem/viabilizam o ecossistema;
- `cripto-predictor`, `brasileirao-predictor` e `stocks-predictor` são os três predictors econômicos;
- Stocks tem como linha científica ativa atual `predictor-rj`; o antigo domínio cross-sectional/fatores é histórico;
- o objetivo econômico final dos três predictors é encontrar oportunidades que possam demonstrar **expectativa de lucro líquido positivo de forma prospectiva e auditável**, sem confundir acurácia/skill preditiva com lucro;
- `NO_OPPORTUNITY` deve ser uma saída válida;
- execução humana/manual não pode ser confundida com performance intrínseca do predictor;
- não dê orientação de investimento/aposta, sizing, ordens ou uso de capital. Esta tarefa é **somente auditoria científica, econômica e de engenharia**.

A intenção acima define **o que o projeto quer ser**, mas não prova que os repositórios realmente implementam isso.

## Regra central da auditoria

Use estas classes em todos os achados:

- `CONFIRMED` — provado por evidência primária/reproduzível;
- `PROVISIONAL` — plausível, mas ainda não reproduzido integralmente;
- `CONFLICT` — duas fontes/evidências contemporâneas incompatíveis;
- `MISSING_EVIDENCE` — claim sem prova suficiente;
- `RISK` — fraqueza metodológica, econômica, operacional ou arquitetural;
- `OPEN_QUESTION` — depende de decisão humana ou dado externo ainda não resolvido.

Não promova claim documental para `CONFIRMED` só porque está em arquivo chamado `CURRENT_STATE`, `HANDOFF`, `CHARTER`, `REPORT`, `FINAL` ou `canonical`.

## O que ler

Faça inventário completo antes de concluir qualquer coisa. Em cada repo, leia e cruze:

- **todos os arquivos Markdown** (`*.md`), distinguindo claramente documento corrente de snapshot histórico/datado;
- README, HANDOFF, charters, ADRs, designs, runbooks, relatórios, erratas e fechamentos;
- `pyproject.toml`, `uv.lock`, requirements, configs YAML/JSON/TOML;
- `.github/workflows/*` e demais automações versionadas;
- código em `src/` e módulos equivalentes;
- testes, fixtures, golden vectors, contract tests e integration tests;
- trial registries, hypothesis registries, scientific state files, attestations, reports e resultados versionados;
- scripts de coleta, serving, backtest, settlement, scheduler e auditoria;
- schemas de banco/ledgers e qualquer amostra de dados versionada que seja relevante;
- commits/PRs recentes quando forem necessários para explicar divergências temporais;
- logs/artefatos de CI quando uma conclusão depender do que realmente foi executado.

Faça busca global por termos e versões que costumam denunciar drift: `NO_GO`, `GO`, `COMPROVADA`, `READY`, `capital`, `profit`, `P&L`, `ROI`, `2.2`, `2.3`, `3.0`, `3.1`, `vendor`, `predictor.plugins`, `source of truth`, `current`, `canonical`, `TODO`, `FIXME`, `legacy`, `deprecated`, `shadow`, `prospective`, `lookahead`, `holdout`.

## Hierarquia de prova

Use a fonte apropriada para cada tipo de claim:

- **escopo/intenção humana:** Charter atual + instrução acima;
- **versão/dependência/runtime:** manifests, lockfiles e artefatos instalados;
- **integração:** código, entry-points, imports e testes reais;
- **operação:** jobs versionados, scheduler/orchestrator, heartbeat/audit logs e CI/runtime observável;
- **resultado científico:** dados usados, código exato, protocolo pré-registrado, relatório produzido e reprodução independente;
- **resultado econômico:** preços/odds conhecidos naquele instante, decisão definida antes do outcome, custos/fricções aplicáveis e settlement prospectivo;
- **documentação:** serve como claim, contexto e provenance; não substitui as fontes acima.

## Auditoria cruzada dos seis

Verifique do zero se a arquitetura afirmada é verdadeira:

- Core é realmente compartilhado e não duplicado/override silenciosamente;
- Ops é realmente usado onde o repo diz usar, e não apenas declarado como dependência;
- os três predictors realmente expõem a superfície canônica do Ecosystem;
- o `predictor.plugins` funciona de verdade em pacote instalado, não só no TOML;
- os contratos do Ecosystem correspondem aos adapters dos três predictors;
- `scientific_status`, `predictive_status`, `economic_status`, `operational_status` e `capital_permission` não misturam semânticas;
- ausência de estado falha fechada;
- `capital_permission` não pode ser promovido por acidente;
- Core não incorporou lógica de domínio indevida;
- Ops não passou a decidir ciência/lucro;
- Ecosystem não está sobrescrevendo a ciência local sem evidência;
- todos os seis podem ser instalados/testados de forma reproduzível a partir do Git, sem depender de estado oculto de uma máquina.

Compare documentação cruzada: se Ecosystem diz uma versão/estado e o domínio diz outra, descubra qual é temporalmente e mecanicamente verdadeiro.

## Auditoria científica dos três predictors

Para **Cripto, Brasileirão e Stocks**, reconstrua hipótese por hipótese. Para cada uma, produza uma linha de evidência contendo:

`hipótese → data/pré-registro → dataset e período → informação disponível as-of → código/ref → baseline → métrica/gate → multiplicidade → resultado → reproducibilidade → status correto`.

Teste especificamente:

- lookahead/leakage e uso de informação publicada após o cutoff;
- data snooping e hipóteses formuladas após observar resultado;
- holdout contaminado;
- seleção de período/universo/survivorship bias;
- tratamento de missing/censura;
- dependência temporal e bootstrap adequado;
- múltiplos testes, DSR/PBO/FDR quando aplicável;
- positive control e negative control;
- poder estatístico/sample size e interpretação correta de resultado inconclusivo;
- calibração, resolução e comparação com baseline apropriado;
- divergência entre modelo de research e modelo de serving;
- qualquer parâmetro/gate mudado depois de olhar o resultado;
- resultados que não possam mais ser reproduzidos porque dados foram perdidos.

Não aceite “passou nos testes” como prova de que uma hipótese funciona. Testes podem apenas provar que o código implementa o comportamento testado.

## Auditoria econômica

Mantenha sempre separado:

`predictor acerta` ≠ `predictor tem edge` ≠ `predictor produz lucro líquido`.

Para qualquer claim econômico, exija cadeia temporal auditável:

`informação disponível → forecast/sinal → preço/odd disponível → decisão definida → outcome → settlement → P&L líquido`.

Sem essa cadeia, classifique o claim econômico como não demonstrado.

Para o Brasileirão, skill contra climatologia não basta: verifique comparação contra preços/odds de mercado apropriados e a coorte prospectiva real.

Para Cripto, reproduza os NO-GOs/hipóteses atuais quando os dados existirem e marque explicitamente qualquer histórico não reproduzível.

Para Stocks/RJ, se a fase atual só testa se fatores antecedem rallies, não a chame de estratégia lucrativa. Verifique separadamente descoberta de sinal temporal e existência ou não de uma camada econômica validada.

Não forneça instruções de execução financeira, apostas, stake/sizing ou ordens. Apenas avalie evidência e metodologia.

## Auditoria operacional

Verifique se o que está versionado reproduz o que o sistema afirma operar:

- jobs/schedulers completos;
- dependências entre refresh de modelo, coleta, forecast, decision, settlement;
- idempotência e retry seguro;
- reconciliação de execução ambígua;
- health/ready reais;
- backup/restore e integridade;
- segredos/redaction;
- versões/hash/provenance das wheels;
- comportamento quando Redis/API/provider falha;
- discrepâncias entre tarefas existentes numa máquina e instaladores versionados;
- qualquer passo manual oculto necessário para manter o predictor funcionando.

## Markdown/documentação

Leia **todo Markdown**, mas não “corrija” história apenas porque está velha. Classifique documentos em:

1. corrente/autoritativo para intenção;
2. corrente, mas apenas claim técnico;
3. snapshot histórico válido para sua data;
4. stale/enganoso porque se apresenta como corrente;
5. contraditório;
6. órfão/deprecado.

Procure especialmente versões, contagens de testes, escopo, status de hipóteses, paths, nomes de plugins, Core/Ops, runtime Python e permissões de capital que estejam duplicados e tenham drift.

## Execução dos testes

Tente executar tudo que for razoavelmente reproduzível:

- sync/install locked;
- Ruff/format;
- Pyright/type checking;
- pytest/coverage;
- build das wheels;
- smoke de wheel fora do checkout;
- contract tests entre Ecosystem e os três plugins;
- testes de container/Compose quando disponíveis;
- scripts de auditoria/read-only;
- backtests/reproduções científicas somente quando os dados necessários estiverem disponíveis e a execução não modificar estado canônico.

Não altere datasets, registries, hypotheses, gates, reports ou outputs canônicos para fazer um teste passar. Se algo depender de segredo/API externa/máquina local, marque a limitação explicitamente.

## Regra de não modificação nesta primeira auditoria

**Primeiro audite. Não corrija nada ainda.**

Não edite código, Markdown, config, trials, dados ou workflows durante a primeira rodada. Quero primeiro um mapa completo do que está certo e errado. Só depois de eu aprovar os achados faremos correções.

## Profundidade / saturação

Não pare na primeira lista de bugs. Faça múltiplas passagens:

1. inventário e leitura total;
2. arquitetura e contratos;
3. ciência e dados;
4. economia;
5. operação/CI;
6. documentação e provenance;
7. auditoria cruzada final.

Continue procurando até ter **duas passagens consecutivas sem novos achados P0/P1 relevantes**. Se não conseguir saturar por limitação de acesso/tempo, diga exatamente o que ficou sem inspecionar.

## Saída obrigatória

Entregue um relatório estruturado com:

1. **HEADs auditados** dos seis repos;
2. **veredito global** sobre a coerência da ideia PREDICTORS;
3. **veredito individual** de cada repo;
4. matriz dos três predictors em `ciência / predição / economia / operação`;
5. **ledger único de inconsistências**, com IDs `INC-001...`, severidade `P0/P1/P2/P3`, classificação, evidência (`arquivo:linha`, commit/artefato quando aplicável), impacto e correção sugerida — mas sem executar a correção;
6. claims importantes **confirmados**;
7. claims **falsos/contraditórios/stale**;
8. evidência **faltante**;
9. resultados que você **reproduziu** e resultados que não conseguiu reproduzir;
10. riscos de leakage, overfitting, data snooping e atribuição econômica;
11. divergências Markdown ↔ código ↔ CI ↔ dados;
12. lista priorizada do que precisaria ser corrigido depois da auditoria;
13. conclusão explícita para cada predictor: `EDGE_DEMONSTRATED`, `PREDICTIVE_ONLY`, `INCONCLUSIVE`, `NO_GO`, ou `INSUFFICIENT_EVIDENCE`, sempre explicando a evidência;
14. conclusão explícita sobre a tese global: a arquitetura realmente ajuda a descobrir/invalidar edge em domínios diferentes ou apenas agrega projetos independentes?

Se encontrar um resultado positivo, tente falsificá-lo antes de aceitá-lo. Se encontrar um NO-GO, verifique se o teste tinha poder suficiente e se a conclusão “não funciona” é justificável. Não procure um resultado bonito; procure o estado verdadeiro.

Comece agora pelo inventário completo dos seis repositórios e registre os HEAD SHAs antes de qualquer interpretação.

---
