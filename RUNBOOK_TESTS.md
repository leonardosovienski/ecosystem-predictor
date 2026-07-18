# RUNBOOK_TESTS.md

Comandos reais, testados em 2026-07-18. Ambiente: Windows, Python 3.13+.

## tools/

```bash
cd <workspace-raiz>
python -m pytest tools/ -q
```
Esperado: `137 passed, 1 skipped`. **CWD importa**: rodar de dentro de
`tools/` quebra (`ModuleNotFoundError: No module named 'tools'`) — o
workspace-raiz precisa estar no `sys.path`, o que só acontece rodando da
raiz.

## predictor_core

```bash
cd predictor_core
python -m pytest -q
```
Esperado: `263 passed`, mais 4 `DeprecationWarning` esperados (funções
depreciadas testadas de propósito, não regressão).

## brasileirao-predictor

```bash
cd brasileirao-predictor
python -m pytest -q
```
Esperado: `302 passed, 1 warning` (warning de `rho` no bound — conhecido,
documentado, não regressão).

## cs-predictor / f1-predictor / lol-predictor

```bash
cd cs-predictor && python -m pytest -q   # idem f1-predictor, lol-predictor
```
Esperado: 100% verde, exit 0.

## previsao-cripto

```bash
cd previsao-cripto
python -m pytest -q
```
Esperado: `302 passed, 2 skipped`. Suíte específica de redação de
segredos: `python -m pytest tests/test_ops_hardening.py -q` → `22 passed`.

## Smoke tests de integração

```bash
cd <workspace-raiz>
python tools/release_check.py                          # release preflight de tools/
cd tools && python release_manifest.py --check          # manifest de tools/
cd ../predictor_core && python sync_core.py --check     # drift/sync do core
cd ..
python tools/vendor_byte_audit.py --workspace . --consumer brasileirao-predictor --consumer cs-predictor --consumer f1-predictor --consumer lol-predictor --consumer previsao-cripto
```

## Limpeza de cache antes de "fresh run"

```bash
find . -maxdepth 3 -iname "__pycache__" -not -path "*/.git/*" -not -path "*/audit/*" | xargs rm -rf
```

## Falhas comuns (não são bugs)

- Rodar `pytest tools/` de dentro de `tools/` → `ModuleNotFoundError`. Rode
  da raiz.
- `grep -c` retornando exit 1 quando não há match — comportamento normal
  do grep, não falha de comando.
- Um teste de `predictor-stocks`/`nba-predictor`/`wc-predictor-v2` não deve
  ser rodado como parte de validação de rotina — são PARKED, fora do
  escopo de qualquer CI local deste ecossistema.

## Evidência a registrar após rodar

Comando exato, cwd, contagem passed/failed/skipped, duração, exit code —
não reaproveitar números de uma rodada anterior sem reexecutar.
