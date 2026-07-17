# Fechamento das 3 aplicações base — checklist para 100%

> Estado consolidado pós-auditoria Red Team (jun/2026). Princípio acordado:
> **deixar as 3 apps prontas ANTES de tocar o core.** Cada item é classificado:
> 🟦 **código** (Claude faz) · 🟧 **operacional** (Leo faz — ato no mundo) ·
> 🟨 **decisão** (Leo decide) · 🟪 **fase core** (depende da consolidação do núcleo).
>
> Legenda de status: ✅ feito · ⬜ falta · 🔄 em progresso.

---

## 1. previsao-cripto (GarimpoInvestimentos)

**Definição de 100%:** as duas linhas (LLM Fase-1 + edge mecânico V3) produzindo
veredito estatístico honesto, governadas, sem segredo exposto, alimentando o painel.

### Feito (verificado nesta sessão)
- ✅ 🟦 Falhas silenciosas instrumentadas (`config.py`, `__init__.py`, `store/cache.py` ×2, `analyzers/backtest.py`)
- ✅ 🟦 Rename `core/` → `store/` (mata colisão com `predictor_core`)
- ✅ 🟦 Telemetria: Fase-1 emite evento `signal` (paridade com o V3)
- ✅ 🟦 Carimbo do juiz LLM (`provider:modelo:prompt-hash`) — já existia, verificado ligado no history
- ✅ 🟦 V3 veredito pelo pedágio (PSR>0.80 ∧ CI_lower>0 ∧ MaxDD<20%) — já existia, verificado
- ✅ 🟦 Suíte 26/26 verde

### Falta para 100%
- ⬜ 🟧 **Rotacionar a chave Gemini** (está em `GarimpoInvestimentos/.env`, texto plano). P0.
- ⬜ 🟧 Confirmar que a chave **nunca esteve no histórico git** (`git log --all -p -- **/.env`); se esteve, a rotação é obrigatória, não opcional.
- ⬜ 🟧 **Acúmulo de dados no tempo** — a linha LLM só dá correlação madura após semanas (D+7/D+30 dos scores); o V3 precisa de funding/OI acumulados para o backtest GO/NO-GO ter n suficiente. "100%" de pesquisa depende disso.
- 🔄 🟦 **Cobertura de teste do V3** — 🔄 PARCIAL: `circuit_breaker` (7 testes) e `signal_engine.generate_signal` (11 testes) cobertos (suíte 26→44). FALTA: `feature_builder`, `regime_engine` (HMM), `backtest_v3` (lógica GO/NO-GO), `pipeline`/collectors/`vision_ingest` (I/O — mais difícil, exige fixtures).
- ⬜ 🟨 (resolvido) Linha principal = **ambas, lado a lado** — decisão tomada.

---

## 2. predictor-stocks

**Definição de 100%:** veredito real da H1 emitido (M6) sobre dados multi-ano, com
anti-lookahead estrutural e a bateria da guilhotina (Fase -1) passada.

### Feito (verificado nesta sessão)
- ✅ 🟦 Achado 5: série vazia agora dá "SEM DADOS (pipeline vazio)" + warning (não "inconclusivo" disfarçado)
- ✅ 🟦 Achado 6: filtro de mercado à vista (`market_type='010'`) em `universe.py`/`backtest.py` — corta 167k→2.230 tickers (opções/termo fora)
- ✅ 🟦 Achado 1 já defendido no call-site (`diff_sharpe` retorna None p/ não-finito) + core reforçado
- ✅ 🟦 Universo = à vista completo (ações+BDR+ETF) — decisão tomada
- ✅ 🟦 Suíte 95/95 (fora 1 e2e lento)

### Falta para 100%
- ⬜ 🟧 **Ingerir COTAHIST multi-ano** — o DB tem só 2024; sem 252d hist + 252d lookback o backtest dá n=0. **É o desbloqueio principal.**
- ⬜ 🟧 (depois do dado) Rodar o **veredito real da H1** (M6).
- ⬜ 🟦 (depois do dado) **Bateria da guilhotina (Fase -1):** sensibilidade params ±10%, decomposição por regime, remoção dos 5 melhores pregões, robustez a 3 preços + 2× custo. (Código meu; precisa do dado.)
- ⬜ 🟪 **Adotar `replay`** no M4 (anti-lookahead estrutural) — hoje é point-in-time por convenção (`_idx_le`). Depende de endurecer o `replay` no core (vazamento `poc_leak`).
- ❌ ~~Índice no `prices_raw`~~ — CORREÇÃO: o índice `(ticker,date)` JÁ EXISTE (`db.py:38`). A lentidão (~123s) é o padrão O(tickers×datas) do `rank_universe` + construir 2230 séries ajustadas, não índice faltando. Resolver = refactor algorítmico (recalcula mediana em SQL / cacheia séries) — toca lógica sensível, exige autorização do Leo (regra do projeto: perguntar antes).

---

## 3. wc-predictor-v2

**Definição de 100%:** odds reais coletadas pré-apito (a tese de edge inteira),
2ª leva de testes fechada, débitos do core agendados. (Domínio PARKED — produção
`wc-predictor` não se toca; trabalho no shadow `-v2`.)

### Feito (verificado nesta sessão)
- ✅ 🟦 De-fork: métricas de futebol movidas p/ `src/research/score_metrics.py`; core vendorizado restaurado ao canônico (em sincronia)
- ✅ 🟦 Bug do `PARKED` (rename) corrigido no `sync_core` (match por prefixo)
- ✅ 🟦 Auditoria das duplicatas: `net.py`/`obs.py` JUSTIFICADAS (não débito); `bootstrap.py` é o único débito real
- ✅ 🟦 Débitos registrados no `HANDOFF.md`
- ✅ 🟦 Suíte 22/22 verde

### Falta para 100%
- ⬜ 🟧 **🔴 PRIORIDADE Nº1 — odds + casas de aposta.** É o coração: sem odds de qualidade não há CLV, e o CLV é o edge. Operação do **cron pré-apito** (T-72h dos jogos de 2026, passadas até o apito) em rede limpa. Cada jogo iniciado sem coleta = abertura perdida pra sempre.
- ⬜ 🟧 **Limpeza one-time** do cache de odds 2026 + **recoleta de 2022** (preenche Over/Under, ~96s).
- ⬜ 🟧 Ampliar odds históricas (Euro 2024 ut_id=1, Copa América 2024 ut_id=133) — opcional, não bloqueia CLV.
- 🔄 🟦 **2ª leva de pytest** (HANDOFF item 2): ✅ `_find_odds`/`_canon` COBERTO (12 testes — o gap MAIS perigoso, swap de orientação odds↔jogo; suíte 81→93). `frac_to_decimal`/`parse_odds`/`parse_ou`/Elo já eram testados. FALTA confirmar `ci_mean` (provável que test_bootstrap já cubra).
- ⬜ 🟦 **CI/CD com gate de teste** (não de ROI) antes de merge.
- ⬜ 🟪 **Trocar bootstrap iid → Lente 2** (`block_bootstrap_ci` do core) — muda veredito CLV/ROI; fazer só no shadow quando autorizado.

---

## Cross-cutting — bloqueadores comuns às 3 (pauta da fase do core)

- ⬜ 🟪 **Endurecer o `replay`** — `poc_leak.py` prova que `past._data` expõe o futuro; a garantia "anti-lookahead estrutural" é furável. Pré-requisito para a adoção honesta no stocks/wc.
- ⬜ 🟪 **Adoção do `replay`** nos 3 (hoje é código morto — ninguém importa).
- ⬜ 🟪 **`connect` unificado** — decidir o armazenamento: `store/` CSV (cripto) vs SQLite `infra` (stocks). Por demanda real, não especulação.
- ⬜ 🟪 **Consolidar bootstrap** — uma só Lente 2 (hoje wc tem iid próprio).

---

## Resumo executivo do que falta

| App | Falta de CÓDIGO (Claude) | Falta OPERACIONAL (Leo) | Bloqueado por core |
|---|---|---|---|
| cripto | cobertura de teste V3 | rotacionar chave · acúmulo de dados | — |
| stocks | guilhotina Fase-1 · índice DB | **ingerir COTAHIST multi-ano** | replay |
| wc | 2ª leva pytest · CI gate | **operação odds pré-apito** · recoleta 2022 | bootstrap iid→Lente 2 |

**O caminho crítico de cada app é um ato operacional do Leo** (chave / dados / odds).
O código que ainda dá pra fazer sem esperar: cobertura de teste do V3 (cripto),
índice no DB + bateria da guilhotina parametrizada (stocks), 2ª leva de pytest +
CI gate (wc). Nada do core até as 3 estarem fechadas.
