# Estado mecânico dos seis projetos canônicos

Este documento é o inventário mecânico corrente dos **seis repositórios definidos por `ECOSYSTEM_CHARTER.md`**. Ele mede identidade, HEAD, runtime declarado, forma de consumo de Core/Ops, workflow e arquivos canônicos encontrados.

Ele **não decide escopo**, não promove hipótese, não prova edge e não autoriza capital. O snapshot F1 de nove repositórios em `ECOSYSTEM_CURRENT_STATE.md` permanece preservado como evidência histórica de 2026-08-17.

<!-- canonical-mechanical-facts:start -->
_Snapshot `canonical-ecosystem-facts/1` gerado em `2026-08-24T02:31:00+00:00`._
_Escopo humano vem de `ECOSYSTEM_CHARTER.md`; este bloco só mede fatos mecânicos._

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | Workflow | Canônicos |
|---|---|---|---|---|---|
| `brasileirao-predictor` | `main` / `3837f84cce4c` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `core-predictor` | `main` / `f6754957eaed` | `2.3.0` / `>=3.13` | Core `—` / Ops `—` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `cripto-predictor` | `main` / `742b91ccd8a9` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.3.0,<3 (v2.3.0)` / Ops `>=3.1.0,<4 (v3.1.0)` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `ecosystem-predictor` | `main` / `22dc663c2536` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `.github/workflows/ci.yml` | `ECOSYSTEM_CHARTER.md`, `ECOSYSTEM_HANDOFF_2026-08-23.md`, `ECOSYSTEM_MECHANICAL_STATE.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `predictor-ops` | `main` / `c48b0a31a7eb` | `3.1.0` / `>=3.13` | Core `—` / Ops `—` | `.github/workflows/ci.yml` | `README.md`, `pyproject.toml`, `uv.lock` |
| `stocks-predictor` | `main` / `111182edbf49` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | `.github/workflows/ci.yml` | `HANDOFF.md`, `README.md`, `STOCKS_CURRENT_STATE.md`, `pyproject.toml`, `requirements.txt` |
<!-- canonical-mechanical-facts:end -->

## Achados mecânicos imediatos

A reconciliação de 2026-08-24 confirma que o drift arquitetural principal do Stocks foi fechado:

- os seis projetos canônicos agora declaram runtime/package metadata compatível com sua função; 
- os três predictors econômicos — Cripto, Brasileirão e Stocks — declaram Core 2.3 e Ops 3.1 como dependências compartilhadas;
- Stocks deixou de aparecer mecanicamente como `requirements / Python não declarado / Core vendorizado / Ops ausente` e passou a `stocks-predictor 0.1.0 / Python >=3.13,<3.15 / Core 2.3 / Ops 3.1`;
- `vendor/predictor_core` ainda existe em Stocks como artefato histórico, mas sua existência não altera os fatos de dependência coletados do `pyproject.toml`;
- Stocks ainda não possui `uv.lock` no snapshot corrente. Isso permanece dívida técnica de reprodutibilidade de dependências, não falha científica do RJ.

A migração técnica do Stocks não constitui prova de edge, não altera estado científico e não autoriza capital.

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
