# Predictor ecosystem

Este repositório é a plataforma agregadora e a fonte de governança do PREDICTORS; não é um monorepo dos domínios.

## Fonte de autoridade

Para retomar o trabalho, leia nesta ordem:

1. [ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md) — **decisão humana canônica** sobre composição, papéis, objetivo econômico e regras de autoridade;
2. [ECOSYSTEM_CURRENT_STATE.md](ECOSYSTEM_CURRENT_STATE.md) — fatos mecânicos, refs, dependências, CI e estado observado;
3. [ECOSYSTEM_HANDOFF_2026-08-23.md](ECOSYSTEM_HANDOFF_2026-08-23.md) — handoff corrente após a reconciliação P0;
4. [PENDENCIAS_ABERTAS.md](PENDENCIAS_ABERTAS.md) — pendências e registros históricos que ainda exigem interpretação temporal;
5. o README/HANDOFF/charter do repositório que será analisado;
6. Git, código, dados e execução observável no ref correspondente.

O antigo `ECOSYSTEM_HANDOFF.md` permanece preservado como snapshot histórico.

**Regra:** inventário mecânico não define escopo humano; documentação não transforma claim em fato; CI verde não comprova validade científica nem lucro.

## Composição canônica atual

A composição vigente, definida por decisão humana em 2026-08-23, possui **seis projetos**:

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

O fluxo atual esperado é:

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

Os predictors devem ser descritos em eixos separados, nunca por um único `GO/NO-GO` global:

- `scientific_state`: validade da hipótese/mecanismo;
- `predictive_state`: capacidade preditiva contra benchmark apropriado;
- `economic_state`: evidência de edge líquido;
- `operational_state`: capacidade de produzir/registrar/liquidar decisões de forma reproduzível;
- `capital_permission`: autorização humana separada e fail-closed.

A semântica completa está em [ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md).

## Estado mecânico e histórico

[ECOSYSTEM_CURRENT_STATE.md](ECOSYSTEM_CURRENT_STATE.md) contém um snapshot mecânico criado por uma reconciliação anterior. Ele continua útil como evidência dos refs e versões daquela coleta, mas **não tem autoridade para redefinir a composição canônica dos seis projetos**.

Documentos `FINAL_*`, `FECHAMENTO_*`, `VEREDITOS_*`, `BLOQUEIOS_*`, P4, F1 e outros artefatos datados permanecem como registros históricos. Quando houver conflito temporal, deve-se comparar a data, o ref Git e a fonte corrente antes de concluir que existe contradição.

## Comandos oficiais deste repositório

O ambiente é gerenciado por `uv.lock` e a CI atual cobre Python 3.13 e 3.14.

```bash
uv sync --locked --all-extras --python 3.13
uv run ruff check src tests scripts
uv run ruff format --check src tests scripts
uv run pyright
uv run coverage run -m pytest -q
uv build
```

Compose, container, segurança e smokes são definidos em [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Limites

Este repositório governa a arquitetura e a interpretação do estado global, mas não substitui a evidência dos domínios. Nenhuma mudança documental autoriza capital real. Promoção econômica exige evidência específica do predictor e decisão humana explícita.
