Pré-release do transporte V2. Muda uma coisa em relação à rc6: **um arquivo de task ilegível no spool não derruba a passada**.

- `Consumer.run_once()` rejeita o arquivo (`SCHEMA_INVALID`, com o nome do arquivo na linha de saída) e continua com as tasks válidas. Na rc6 um JSON malformado ou absurdamente aninhado matava o consumidor com traceback (`RecursionError`), exit 1, e as tasks válidas ficavam sem entrega até o arquivo ser removido à mão (reproduzido na validação de 2026-09-29, cenário E2E-C9).
- A trava exclusiva por domínio (rc6), a allowlist de adapters (rc5) e o `research-protocol` (2.0.0rc2) não mudam.

Código: `packages/research-transport` em `main` desde `8ce2a64` (PR ecosystem-predictor#38). Build reprodutível: `git archive` + `SOURCE_DATE_EPOCH=1758240000`, duas vezes, mesmos bytes (workflow `release.yml`).
