# Estado mecânico dos seis projetos canônicos

Este documento é o inventário mecânico corrente dos **seis repositórios definidos por `ECOSYSTEM_CHARTER.md`**. Ele mede identidade, HEAD, runtime declarado, forma de consumo de Core/Ops, entry point do plugin, workflow e arquivos canônicos encontrados.

Ele **não decide escopo**, não promove hipótese, não prova edge e não autoriza capital. O snapshot F1 de nove repositórios em `ECOSYSTEM_CURRENT_STATE.md` permanece preservado como evidência histórica de 2026-08-17.

<!-- canonical-mechanical-facts:start -->
_Snapshot `canonical-ecosystem-facts/2` gerado em `2026-08-24T03:10:00+00:00`._
_Escopo humano vem de `ECOSYSTEM_CHARTER.md`; este bloco só mede fatos mecânicos._

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | Plugin | Workflow | Canônicos |
|---|---|---|---|---|---|---|
| `brasileirao-predictor` | `main` / `f1ced5d09a48` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `brasileirao=src.ecosystem_plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `core-predictor` | `main` / `8dab1d9d806b` | `2.3.0` / `>=3.13` | Core `—` / Ops `—` | `—` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `cripto-predictor` | `main` / `2fc87a19011c` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.3.0,<3 (v2.3.0)` / Ops `>=3.1.0,<4 (v3.1.0)` | `cripto=GarimpoInvestimentos.plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `ecosystem-predictor` | `main` / `b460073780c9` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `—` | `.github/workflows/ci.yml` | `ECOSYSTEM_CHARTER.md`, `ECOSYSTEM_HANDOFF_2026-08-23.md`, `ECOSYSTEM_MECHANICAL_STATE.md`, `PREDICTOR_CONTRACT.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `predictor-ops` | `main` / `c48b0a31a7eb` | `3.1.0` / `>=3.13` | Core `—` / Ops `—` | `—` | `.github/workflows/ci.yml` | `README.md`, `pyproject.toml`, `uv.lock` |
| `stocks-predictor` | `main` / `6138be093f81` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `stocks=src.ecosystem_plugin:PLUGIN` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `STOCKS_CURRENT_STATE.md`, `pyproject.toml`, `requirements.txt` |
<!-- canonical-mechanical-facts:end -->

## Achados mecânicos imediatos

A reconciliação de 2026-08-24 confirma o fechamento dos principais drifts arquiteturais de P1:

- os três predictors econômicos — Cripto, Brasileirão e Stocks — declaram Core 2.3 e Ops 3.1 como dependências compartilhadas;
- os três agora expõem um adapter pelo mesmo entry-point group `predictor.plugins`, tornando a superfície de descoberta mecanicamente verificável;
- `PREDICTOR_CONTRACT.md` define o vocabulário comum de estados científico, preditivo, econômico, operacional e permissão de capital, além de `NO_OPPORTUNITY` como resultado válido;
- Stocks permanece sem `uv.lock`; isso é dívida técnica de reprodutibilidade de dependências, não falha científica do RJ;
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
