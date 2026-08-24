# Predictor ecosystem

Este repositório é a plataforma agregadora e a fonte de governança do PREDICTORS; não é um monorepo dos domínios.

## Fonte de autoridade

Para retomar o trabalho, leia nesta ordem:

1. [ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md) — **decisão humana canônica** sobre composição, papéis, objetivo econômico e regras de autoridade;
2. [PREDICTOR_CONTRACT.md](PREDICTOR_CONTRACT.md) — contrato canônico dos predictors e dos estados globais;
3. [ECOSYSTEM_MECHANICAL_STATE.md](ECOSYSTEM_MECHANICAL_STATE.md) — inventário mecânico corrente dos seis projetos canônicos;
4. [ECOSYSTEM_HANDOFF_2026-08-24.md](ECOSYSTEM_HANDOFF_2026-08-24.md) — continuidade corrente após P0/P1;
5. o README/HANDOFF/current-state/charter do repositório que será analisado;
6. Git, código, dados e execução observável no ref correspondente.

`ECOSYSTEM_CURRENT_STATE.md`, `ECOSYSTEM_HANDOFF.md`, `ECOSYSTEM_HANDOFF_2026-08-23.md` e demais fechamentos datados permanecem preservados como snapshots históricos. Eles não redefinem o estado atual quando divergem do Charter, do contrato, do código ou de evidência mais recente.

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

O Core define a cadeia econômica portátil:

```text
ProbabilisticForecast → MarketQuote → EconomicDecision → ExecutionRecord → SettlementRecord
```

O Core não decide sizing, risco ou autorização de capital. O Ops não julga hipótese nem rentabilidade. O Ecosystem não inventa previsão nem reclassifica ciência local sem evidência.

## Estados e contrato global

Os predictors são descritos em eixos separados:

- `scientific_status`;
- `predictive_status`;
- `economic_status`;
- `operational_status`;
- `capital_permission`.

Estados ausentes falham fechados e `capital_permission` permanece `FORBIDDEN` sem promoção humana explícita. A semântica executável está em [PREDICTOR_CONTRACT.md](PREDICTOR_CONTRACT.md) e nos tipos em `src/ecosystem/contracts/`.

## Integração mecânica atual

A fonte corrente é [ECOSYSTEM_MECHANICAL_STATE.md](ECOSYSTEM_MECHANICAL_STATE.md), gerada a partir de `audit/canonical-ecosystem-facts.json` e validada por `scripts/sync_canonical_ecosystem_facts.py`.

Após a reconciliação P1, os três predictors econômicos declaram Python `>=3.13,<3.15`, Core 2.3.x e Ops 3.1.x e publicam adapters pelo mesmo entry-point `predictor.plugins`:

```text
cripto      = GarimpoInvestimentos.plugin:PLUGIN
brasileirao = src.ecosystem_plugin:PLUGIN
stocks      = src.ecosystem_plugin:PLUGIN
```

O snapshot mecânico também coleta esses entry-points. Essa integração comprova apenas compatibilidade arquitetural/descoberta; não comprova edge científico, resultado econômico ou prontidão para capital.

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
