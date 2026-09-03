# Estado mecânico dos seis projetos canônicos

> **HISTORICAL — snapshot de 2026-09-01.** Não representa versões ou estados
> atuais. Use [`CURRENT_STATE.md`](CURRENT_STATE.md) e `registries/`.

Este documento é o inventário mecânico corrente dos **seis repositórios definidos por `ECOSYSTEM_CHARTER.md`**. Ele mede identidade, HEAD, runtime declarado, forma de consumo de Core/Ops, entry point do plugin, workflow e arquivos canônicos encontrados.

Ele **não decide escopo**, não promove hipótese, não prova edge e não autoriza capital. O snapshot F1 de nove repositórios em `ECOSYSTEM_CURRENT_STATE.md` permanece preservado como evidência histórica de 2026-08-17.

<!-- canonical-mechanical-facts:start -->
_Snapshot `canonical-ecosystem-facts/2` gerado em `2026-09-01T00:00:00-03:00`._
_Escopo humano vem de `ECOSYSTEM_CHARTER.md`; este bloco só mede fatos mecânicos._

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | Plugin | Workflow | Canônicos |
|---|---|---|---|---|---|---|
| `brasileirao-predictor` | `main` / `29ce04f68046` | `0.1.0` / `>=3.13,<3.15` | Core `>=3.0,<4 (v3.0.0)` / Ops `>=4.0,<5 (v4.0.0)` | `brasileirao=brasileirao_predictor.ecosystem_plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `core-predictor` | `main` / `628b509d55b6` | `3.0.0` / `>=3.13` | Core `—` / Ops `—` | `—` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `cripto-predictor` | `main` / `0f54e1cd7b20` | `1.0.0` / `>=3.13,<3.15` | Core `>=3.0.0,<4 (v3.0.0)` / Ops `>=4.0.0,<5 (v4.0.0)` | `cripto=GarimpoInvestimentos.plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `ecosystem-predictor` | `main` / `5201836ddb46` | `0.1.0` / `>=3.13,<3.15` | Core `—` / Ops `—` | `—` | `.github/workflows/ci.yml` | `ECOSYSTEM_CHARTER.md`, `ECOSYSTEM_HANDOFF.md`, `ECOSYSTEM_MECHANICAL_STATE.md`, `PREDICTOR_CONTRACT.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `predictor-ops` | `main` / `46cd8e2b43aa` | `4.0.0` / `>=3.13` | Core `—` / Ops `—` | `—` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `stocks-predictor` | `main` / `dc5e34441fc1` | `0.1.0` / `>=3.13,<3.15` | Core `>=3.0,<4 (v3.0.0)` / Ops `—` | `stocks=stocks_predictor.ecosystem_plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `STOCKS_CURRENT_STATE.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
<!-- canonical-mechanical-facts:end -->

## Achados mecânicos imediatos

A reconciliação local de 2026-09-01 confirma:

- os três predictors econômicos declaram Core 3.0; Cripto e Brasileirão declaram Ops 4.0, enquanto Stocks ainda não depende de Ops;
- os três agora expõem um adapter pelo mesmo entry-point group `predictor.plugins`, tornando a superfície de descoberta mecanicamente verificável;
- `PREDICTOR_CONTRACT.md` define o vocabulário comum de estados científico, preditivo, econômico, operacional e permissão de capital, além de `NO_OPPORTUNITY` como resultado válido;
- Stocks agora possui `uv.lock`; a ausência de Ops é uma diferença explícita, não uma integração presumida;
- os gates econômicos novos permanecem locais: futebol e cripto estão integrados em shadow (cripto opt-in), e ações tem somente a primitiva opt-in ainda não ligada ao backtest congelado;
- a existência de plugin/dependência não prova que um domínio tem edge nem que toda a operação já usa todas as funções de Ops.

A integração técnica não constitui prova de edge, não altera estado científico e não autoriza capital.

## Atualização

Para validar apenas snapshot/documento, sem rede:

```bash
uv run python scripts/sync_canonical_ecosystem_facts.py --offline-check
```

Para comparar o snapshot com os HEADs remotos:

```bash
uv run python scripts/sync_canonical_ecosystem_facts.py --check
```

Para uma atualização deliberada após revisar o drift:

```bash
uv run python scripts/sync_canonical_ecosystem_facts.py --write
```

`--write` atualiza somente o inventário mecânico. Ele não pode alterar `ECOSYSTEM_CHARTER.md` nem decidir que um repositório entra ou sai dos seis.
