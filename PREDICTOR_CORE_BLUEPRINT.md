# predictor_core — Blueprint & Contrato da Plataforma

> **⚠️ HISTÓRICO / SUPERSEDED (marcado em 2026-07-17, Onda 5 da reintegração
> do ecossistema).** Este documento descreve a PROPOSTA original do core,
> escrita quando ele ainda não existia ("Status: proposta (design). Não
> implementado."). O core foi implementado desde então e está em produção na
> versão `1.3.1-ga-20260716`, consumido por 8 domínios via vendoring
> (`sync_core.py`). A fonte de verdade atual sobre o que o core realmente é e
> faz é **[`predictor_core/README.md`](predictor_core/README.md)** e
> **[`predictor_core/CHANGELOG.md`](predictor_core/CHANGELOG.md)** — não este
> arquivo. O conteúdo abaixo é preservado como registro histórico da decisão
> original (o "porquê" de várias escolhas de design ainda é válido), não como
> descrição do estado atual do código. Onde este documento e o código
> divergirem, o código prevalece.

> **Status original (na época em que foi escrito):** proposta (design). **Não implementado.**
> **Mandato original:** auditoria — este documento NÃO altera o código dos três domínios.
> Ele define o contrato que `wc-predictor`, `predictor-stocks` e `previsao-cripto`
> passarão a respeitar quando a refatoração for autorizada.
> **Base empírica:** auditoria interna dos 3 projetos (16/06/2026) + dissecação
> medida do QuantConnect/LEAN (código real lido, não suposto — ver Apêndice A).

---

## 0. A tese e o princípio único

Os três projetos são **três instâncias de um mesmo sistema**. O `predictor_core` é a
espinha compartilhada — o "pedágio da verdade" pelo qual nenhum domínio gera um
relatório sem passar.

**O bug que o core existe para curar:** em cada projeto, o invariante mais sagrado é
hoje garantido por **disciplina humana, não por máquina** — paridade train/serve (wc),
parâmetros congelados (stocks), juiz-único do LLM (cripto). O core converte cada um
desses em **invariante de arquitetura**: algo que o código impede, não que o
programador promete.

Regra de extração: o core só recebe uma peça quando um domínio a **exige de fato**.
Nada de generalização especulativa. O que é específico de um domínio fica nele.

---

## 1. Camada de dados desacoplada (o Contrato de Dados)

**Problema curado:** hoje cada domínio mistura "lidar com a rede" (timeouts, rate
limits de CoinGecko/SerpAPI/Sofascore, bloqueio de IP corporativo) com "rodar o
modelo". Uma falha de rede contamina o backtest.

**O contrato:** separação física entre **baixar** e **servir**.

```
[rede limpa / cron]            [offline / determinístico]
  download + retry  ──►  lago local (SQLite WAL + cache TTL)  ──►  domínio consome
  (resiliente, sujo)        (idempotente, congelado)              (nunca toca a rede)
```

- **O modelo nunca fala com a rede.** Ele lê só o lago local. Rede vive no cron.
- **`core.infra.connect(path)`** — unifica WAL + `busy_timeout` + migração idempotente.
  Resolve a divergência atual (wc usa `busy_timeout=30000`+`synchronous=NORMAL`; o core
  do stocks usa `5000`+`row_factory=Row`). **Decisão:** um só `connect`, parametrizado.
- **`core.net`** — retry com backoff exponencial; 404 não re-tenta; cache hit nunca
  dispara rede. (Generaliza o `net.py` do wc e o `core/retry.py` do cripto.)
- **`core.cache`** — TTL real com carimbo de origem (lição do cripto: `setdefault` no
  `cached_at` para não renovar o TTL para sempre). **Invariante temporal:** dado de
  evento futuro (odds de fixture, preço de hoje) **nunca** entra no cache de disco —
  só evento liquidado é cacheável (lição do wc; senão o cache congela um preço velho).

**Não-objetivo (Trilho B):** worker .NET / websockets / streaming. O volume real
(barras diárias, odds de jogo, REST) não justifica. Reavaliar só sob o gatilho do §7.

---

## 2. Anti-lookahead estrutural — "Feed, don't query"

**Lição medida do LEAN (`Slice.cs`, ver Apêndice A):** o anti-lookahead não é um
teste, é **inversão de controle**. O motor *empurra* o corte de tempo atual para o
algoritmo; o futuro simplesmente não existe na memória do passo. O `Slice` é
read-only e entregue sequencialmente — espiar o amanhã é **fisicamente impossível**,
não "proibido por convenção".

**Contraste com o que o stocks planejou:** um teste post-hoc `exec_ts > signal_ts`.
Isso pega o lookahead *depois* de ele acontecer. A inversão o torna *inalcançável*.

**Primitiva do core:**

```python
def replay(history, asof_handler, *, freeze=True):
    """Reexecuta a história ponto-a-ponto. Para cada asof, ENTREGA ao handler
    apenas o estado <= asof (uma fatia congelada). O handler NÃO recebe acesso
    à série completa — não tem como consultar asof+1.

    history     : sequência ordenada por tempo (imutável).
    asof_handler: callable(slice_ate_asof) -> decisão. Vê só o passado.
    freeze      : a fatia é read-only; mutação levanta erro.
    Retorna o ledger de decisões, cada uma carimbada com seu asof.
    """
```

A função de sinal de cada domínio (`factor` do stocks, `predict` do wc, o prompt do
cripto) passa a ser um `asof_handler`. Ela deixa de fazer `df.loc[:hoje]` (onde o
lookahead entra por um off-by-one) e passa a **receber** a fatia. O teste
`exec_ts > signal_ts` continua como cinto-e-suspensório, mas a garantia agora é
estrutural.

---

## 3. O pedágio de duas lentes (o gate de significância)

**Princípio:** nenhum relatório sai sem **(a) um nulo pré-registrado declarado** e
**(b) um intervalo de significância** provando que está fora dele. O core impõe a
*forma*; o domínio fornece o *nulo*.

### Lente 1 — PSR (paramétrica, fórmula fechada, barata) — *roubada do LEAN*

Probabilistic Sharpe Ratio (Bailey & López de Prado 2012). Pune **não-normalidade**
(assimetria + curtose) e tamanho de amostra. Custo ~zero → **primeira barreira**: se
não passa aqui, nem gaste ciclo no bootstrap.

```python
def probabilistic_sharpe_ratio(returns, benchmark_sharpe=0.0):
    """P(Sharpe verdadeiro > benchmark_sharpe), corrigido por skew/curtose e n.
    Verbatim do LEAN (Apêndice A), reimplementado em stdlib:
        est_std = sqrt((1 - skew*SR + ((kurt-1)/4)*SR^2) / (n-1))
        PSR     = Phi((SR_obs - benchmark_sharpe) / est_std)
    LIMITE CONHECIDO: assume i.i.d. — NÃO corrige autocorrelação. Por isso existe a Lente 2.
    """
```

### Lente 2 — Block bootstrap pareado (não-paramétrica, pesada) — *o juiz definitivo*

Assume o fardo que o PSR ignora: **autocorrelação** (blocos) e **dependência cross**
(reamostragem conjunta ativo↔benchmark). Uma única assinatura generalizada serve aos
três domínios — e é **retrocompatível** com a API congelada no M0 do stocks (só alarga
o tipo da unidade reamostrada de `float` para qualquer unidade).

```python
def block_bootstrap_ci(units, statistic, *, block_length=21, n_boot=10_000,
                       confidence=0.95, seed=42, method="moving"):
    """IC empírico de uma estatística arbitrária sobre série temporal.

    units     : lista ORDENADA NO TEMPO. Cada unidade é um escalar (ex.: CLV por
                aposta) OU uma tupla pareada (ex.: (ret_estrategia, ret_benchmark)).
    statistic : callable(list[unit]) -> float. Desempacota a unidade.
    method    : "moving" (blocos fixos) | "stationary" (Politis-Romano, L~Geom).
    Retorna (lo, hi, distribuicao_bootstrap).

    INVARIANTE DE CORREÇÃO (a única que importa):
        reamostre BLOCOS de UNIDADES (linhas no tempo) — NUNCA colunas independentes.
        É isso que preserva cross-correlação (dentro da unidade) E autocorrelação
        (entre unidades do bloco). Bootstrapar colunas separado infla o IC da
        diferença e empurra o veredito para "inconclusivo" falso.
    """
```

### Injeção do nulo por domínio (o core impõe a forma, o domínio dá o nulo)

| Domínio | Nulo (H0) | Estatística | Lentes aplicáveis |
|---|---|---|---|
| wc | CLV médio ≤ 0 (não antecipa o mercado) | `mean(clv)` | só Lente 2 (CLV não é Sharpe) |
| stocks | Sharpe_estrat − Sharpe_bench ≤ 0 | `sharpe(a) - sharpe(b)` sobre pares | **PSR (triagem) + Lente 2 pareada (juiz)** |
| cripto | Spearman(score, ret_fwd) ≤ 0; e excesso-sobre-BTC ≤ 0 | `spearman(score, ret)` | só Lente 2 (Spearman não é Sharpe) |

> **Precisão honesta:** o PSR é uma lente **específica de Sharpe**. Onde a estatística
> não é um Sharpe (CLV no wc, Spearman no cripto), o pedágio roda **só a Lente 2**. A
> "validação em dois estágios" se aplica plenamente ao stocks; nos outros, o bootstrap
> é a barreira única — e suficiente.

### Adaptadores (uma linha por domínio)

```python
# stocks — diferença de Sharpe (par reamostrado JUNTO)
block_bootstrap_ci(list(zip(ret_estrat, ret_bench)),
                   lambda b: sharpe([u[0] for u in b]) - sharpe([u[1] for u in b]))

# cripto — Spearman com significância (par no tempo)
block_bootstrap_ci(list(zip(scores, ret_fwd)),
                   lambda b: spearman([u[0] for u in b], [u[1] for u in b]))

# wc — CLV médio vs 0 (unidade = escalar; chama como hoje)
block_bootstrap_ci(clv_por_aposta, statistic=mean)
```

### Aceite mecânico do pedágio (propriedades, não leitura de código)

(a) cobertura AR(1) série única: IC 95% cobre a verdade em 95%±2pp;
(b) comprimento médio de bloco ≈ L; (c) índices reamostrados ~uniformes;
(d) reprodutível com seed; (e) caso sintético onde o iid subestima a largura e o
block acerta;
**(f) [o que faltava] COBERTURA PAREADA:** sobre ≥500 pares AR(1) positivamente
correlacionados com diferença-de-estatística conhecida, o IC 95% cobre em 95%±2pp.
Um bootstrap que reamostra colunas separado **falha aqui de forma detectável**.

---

## 4. Bifurcação de IA: Modo A vs Modo B

O cripto provou que "IA é read-only" não serve para todos. O core reconhece **dois
modos**, com contratos diferentes.

### Modo A — IA como analista (wc, stocks)
A matemática interpretável gera o sinal. A IA é **observadora read-only**: narra o
ledger, explica divergências modelo-vs-mercado, triagem de quarentena como *sugestão*.
- **NUNCA** escreve no banco. **NUNCA** entra no caminho de cálculo do sinal.
- Saída = artefato consultivo em `reports/ai/` com data, **descartável** (deletar o
  módulo não pode quebrar teste nenhum).
- Enforçado por **fronteira de processo**, não por comentário: o módulo analista roda
  sem credencial de escrita no banco (read-only connection).

### Modo B — LLM como modelo (cripto)
O LLM **é** o modelo (o `opportunity_score`). Então sofre a **mesma tortura
estatística** que uma regressão sofreria:
- passa pelo **pedágio** (§3) como qualquer sinal — forward, contra o nulo, com IC;
- forward-only honesto (previsão registrada ANTES do preço futuro existir — já é assim);
- **carimbo obrigatório do juiz** no envelope de reprodutibilidade (§5): provider +
  modelo + hash do prompt. Sem isso, um bump de modelo mistura dois juízes no mesmo
  histórico e o backtest os pooled como um só estimador.

> O core não escolhe o modo — o domínio declara. Mas o core **recusa** emitir relatório
> de um sinal Modo B que não esteja embrulhado no envelope de reprodutibilidade.

---

## 5. Reprodutibilidade & esteira de sincronização

### Envelope de reprodutibilidade (toda execução)
- `run_id` (timestamp UTC + prefixo do config_hash, ordenável e único),
- `config_hash`, `code_version` (git short HEAD),
- **Modo B:** + `judge_version` (provider/modelo/prompt-hash).
- **Furo a fechar:** `code_version` retorna `'unknown'` na cópia de rede limpa (sem
  `.git`). **Correção:** carimbar a versão num arquivo no momento do sync/deploy e ler
  como fallback. O ledger forward (a anti-tautologia) não pode gravar versão anônima.

### Congelamento de parâmetros (machine-enforced, não duplicado)
- Separar **params congelados** (H1-FROZEN) de **params operacionais** (db_path, seed).
- **Golden hash do subconjunto congelado**, asserido em teste — uma fonte de verdade,
  em vez de duplicar os valores no config e no teste (hoje o tripwire do stocks duplica;
  um implementador apressado pode "consertar o teste" e o lacre evapora).
- `config_hash` passa a hashear **só o subconjunto relevante** por domínio (hoje wc e
  stocks divergem: escopo e `ensure_ascii` diferentes → mesma peça, hashes diferentes).

### `sync_core.py` como mini-CI (o pedágio do próprio core)
- Copia o core para `vendor/predictor_core/` + carimba `VERSION` (versão + data).
- **Verificação de hash de assinatura**: aborta se o vendor tiver diff não levado a
  upstream (evita "evolução por demanda" perdida) **e** se a cópia local não bater com
  o hash canônico do core (evita alguém adulterar o núcleo dentro de um domínio para
  mascarar um resultado ruim).
- Vendoring, **não** `pip install` (EDR corporativo quarentena venv; e o core não pode
  ser dependência global mutável). Contêiner só se o EDR permitir; senão `--target`.

### Telemetria (semente do painel unificado)
- `core.obs.emit_metric(domain, name, value, run_id)` grava eventos **estruturados**
  (não log textual): `CLV_edge`, `PSR`, `bootstrap_IC`, `score_calibração`,
  `H1_confidence`. O painel lê desses eventos. (OTel completo é Trilho B.)

---

## 6. O que cada domínio herda (mapa de refatoração) + ordem

| Domínio | Herda do core / dos pares |
|---|---|
| wc-predictor | Lente 2 (troca o bootstrap iid) · seed no simulador · simulador amostrar da grid (com Dixon-Coles) · "feed don't query" no backtest (curar a paridade train/serve: backtest e serving consomem a MESMA janela) |
| predictor-stocks | pedágio de 2 lentes (PSR+pareado) no M5 · "feed don't query" no M4 (anti-lookahead estrutural) · fechar custo/rebalance do benchmark antes do M3 · golden hash do frozen |
| previsao-cripto | Lente 2 (significância que falta) · métricas **relativas** (excesso sobre BTC, não retorno absoluto) · carimbo do juiz · instrumentar degradação silenciosa do `except Exception` |
| todos | envelope de reprodutibilidade · `connect`/`net`/`cache` unificados · emit_metric |

### Sequência (Trilho A)
1. **P0 (hoje):** rotacionar chaves do Garimpo que viveram em commits (history = comprometido).
2. **Contrato do core** + resolver divergências (`connect`, `config_hash`).
3. **Pedágio de 2 lentes no core** (PSR + bootstrap pareado generalizado) ← peça de
   maior alavancagem: cura significância de stocks **e** cripto de uma vez.
4. `sync_core` com verificação de hash.
5. Herança cruzada + envelope de reprodutibilidade.
6. Telemetria estruturada.
7. **Terminar o stocks (M1→M6) já consumindo o core consolidado.**

### Gatilho do Trilho B (escrito, não "nunca")
`.NET worker` / `k8s` / `Azure Key Vault+OpenAI` / `OTel completo` disparam quando
**qualquer um** for verdade: capital real alocado · 2º operador no time · usuário
externo consumindo · um feed que **de fato** exija websocket/baixa-latência. Antes
disso é aprendizado de ferramenta, não arquitetura de produção da carga atual.

---

## 7. Fronteira / não-objetivos

- Este é um **instrumento de medição metodológica** (TCC + projeto de longo prazo),
  não recomendação de investimento. Operação com dinheiro real está fora do escopo.
- Este documento é **proposta**: não autoriza tocar no código dos três repos. A
  refatoração começa quando o contrato for aprovado.
- Veredito comparativo vs LEAN é **unidimensional e honesto**: a plataforma ganha em
  *ceticismo estatístico* (autocorrelação + pareamento); o LEAN ganha em *realismo de
  execução* (slippage, impacto, corporate actions) e cobertura. Arenas diferentes.

---

## Apêndice A — Achados medidos no LEAN (base empírica, código real lido)

1. **`PortfolioStatistics.cs`** computa ~19 métricas, **todas estimativa pontual**,
   EXCETO uma: `ProbabilisticSharpeRatio`. → nossa hipótese ("só pontual") era **meio
   errada**; corrigida pela medição.
2. **`Statistics.ProbabilisticSharpeRatio` (verbatim):**
   `est_std = sqrt((1 - skew*SR + ((kurt-1)/4)*SR^2)/(n-1))`;
   `PSR = Normal.CDF((SR_obs - benchmark_sharpe)/est_std)`. Toma **benchmark escalar**
   (não série pareada); **assume i.i.d.** (sem correção de autocorrelação). → cobre
   não-normalidade, NÃO cobre autocorrelação nem pareamento. Daí as duas lentes serem
   **complementares**, não concorrentes.
3. **`TrackingError`** já constrói a série de diferença `algo[i]-bench[i]` e para na
   volatilidade dela — está a um passo do bootstrap e não dá.
4. **`StatisticsBuilder.cs`**: só agrega pontual (total + rolling 1/3/6/12m); o nulo
   está **presente** na arquitetura (benchmark é input de Beta/Alpha/IR/PSR) mas **não
   é imposto como portão** — o ceticismo é delegado ao usuário.
5. **`Slice.cs`**: anti-lookahead **estrutural** — read-only, entregue sequencialmente
   pelo engine; "slices futuros não existem no passo atual". A joia que vira o §2.

*Fonte: QuantConnect/Lean @ master, lido em 16/06/2026.*
