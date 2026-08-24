# Predictor ecosystem

Este repositório é a plataforma agregadora e a fonte de governança do PREDICTORS; não é um monorepo dos domínios.

## Fonte de autoridade

Para retomar o trabalho, leia nesta ordem:

1. [ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md) — **decisão humana canônica** sobre composição, papéis, objetivo econômico e regras de autoridade;
2. [ECOSYSTEM_MECHANICAL_STATE.md](ECOSYSTEM_MECHANICAL_STATE.md) — inventário mecânico corrente dos seis projetos canônicos;
3. [ECOSYSTEM_HANDOFF_2026-08-23.md](ECOSYSTEM_HANDOFF_2026-08-23.md) — handoff corrente após P0 e a reconciliação mecânica;
4. [PENDENCIAS_ABERTAS.md](PENDENCIAS_ABERTAS.md) — pendências e registros históricos que ainda exigem interpretação temporal;
5. o README/HANDOFF/charter do repositório que será analisado;
6. Git, código, dados e execução observável no ref correspondente.

`ECOSYSTEM_CURRENT_STATE.md` e o antigo `ECOSYSTEM_HANDOFF.md` permanecem preservados como snapshots históricos da linha anterior.

**Regra:** inventário mecânico não define escopo humano; documentação não transforma claim em fato; CI verde não comprova validade científica nem lucro.

## Composição canônica atual

A composição vigente possui **seis projetos**:

| Repositório | Papel |
|---|---|
| `ecosystem-predictor` | governança, registry, gateway, scheduler, storage e visão agregada |
| `core-predictor` | contratos científicos, temporais, métricas e contratos econômicos compartilhados |
| `predictor-ops` | execução operacional, idempotência, observabilidade, reconciliação e controles de runtime |
| `cripto-predictor` | predictor econômico de cripto |
| `brasileirao-predictor` | predictor econômico de mercados do Brasileirão |
| `stocks-predictor` | predictor econômico de ações; domínio ativo atual `predictor-rj` |

`cs-predictor`, `f1-predictor`, `lol-predictor`, `wc-predictor`, `nba-predictor` e outros repositórios preservados são históricos, referência ou trabalho fora do escopo canônico atual. Eles não são apagados e seus resultados históricos continuam válidos para a data em que foram produzidos.

## Objetivo global

Os três predictors econômicos — Cripto, Brasileirão e Stocks — existem para produzir recomendações baseadas somente em informação disponível no momento da decisão que possam demonstrar **expectativa de lucro líquido positivo de forma prospectiva e auditável**.

```text
dados disponíveis
      ↓
previsão / sinal
      ↓
recomendação
      ↓
execução humana
      ↓
settlement
      ↓
P&L líquido auditável
```

A execução pode ser otimizada ou automatizada no futuro. Hoje, automação não é requisito para validar edge. `NO_OPPORTUNITY` é uma saída válida.

Melhora de accuracy, RPS, Brier, log-loss, correlação, um backtest bruto positivo, CI verde ou identificação retrospectiva de rally **não equivalem a lucro**.

## Arquitetura

```text
                  ┌───────────────────────────────┐
                  │       ecosystem-predictor     │
                  │ governança / gateway / visão  │
                  └───────────────┬───────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
     core-predictor 2.3.x                    predictor-ops 3.1.x
   contratos/medição/tempo                 execução/operação/auditoria
              │                                       │
              └───────────────────┬───────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     cripto-predictor   brasileirao-predictor   stocks-predictor
              │                   │                   │
              └──────────── predictors econômicos ───┘
```

O Core já define a cadeia econômica portátil:

```text
ProbabilisticForecast → MarketQuote → EconomicDecision → ExecutionRecord → SettlementRecord
```

O Core não decide sizing, risco ou autorização de capital. O Ops não julga hipótese nem rentabilidade. O Ecosystem não inventa previsão nem reclassifica ciência local sem evidência.

## Estados globais

Os predictors devem ser descritos em eixos separados:

- `scientific_state`;
- `predictive_state`;
- `economic_state`;
- `operational_state`;
- `capital_permission`.

A semântica completa está em [ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md).

## Inventário mecânico atual

A fonte corrente é [ECOSYSTEM_MECHANICAL_STATE.md](ECOSYSTEM_MECHANICAL_STATE.md), gerada a partir de `audit/canonical-ecosystem-facts.json` e validada por `scripts/sync_canonical_ecosystem_facts.py`.

A primeira fotografia dos seis já evidencia uma divergência estrutural importante: `stocks-predictor` continua sem `pyproject.toml`, sem runtime Python declarado no manifest e com Core legado vendorizado, enquanto Cripto e Brasileirão consomem Core 2.3/Ops 3.1 de forma moderna. Isso é registrado como drift; não é corrigido por inferência.

O snapshot de nove repositórios de 2026-08-17 em [ECOSYSTEM_CURRENT_STATE.md](ECOSYSTEM_CURRENT_STATE.md) continua histórico e não é mais o inventário mecânico corrente dos seis.

## Comandos oficiais deste repositório

```bash
uv sync --locked --all-extras --python 3.13
uv run ruff check src tests scripts
uv run ruff format --check src tests scripts
uv run pyright
uv run coverage run -m pytest -q
uv run python scripts/sync_canonical_ecosystem_facts.py --offline-check
uv build
```

Para comparar explicitamente os seis HEADs remotos com o snapshot:

```bash
uv run python scripts/sync_canonical_ecosystem_facts.py --check
```

Compose, container, segurança e smokes são definidos em [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Limites

Este repositório governa a arquitetura e a interpretação do estado global, mas não substitui a evidência dos domínios. Nenhuma mudança documental autoriza capital real. Promoção econômica exige evidência específica do predictor e decisão humana explícita.
