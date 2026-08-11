# Validação local da F1

Executada em 2026-08-11 no checkout limpo criado de
`master@a9214d69f188ab63bdbf0764a1bc28d7b0661b60`, branch
`docs/f1-reconcile-ecosystem`.

| Comando/verificação | Resultado | Duração | Classificação/limite |
|---|---|---:|---|
| `git diff --check` | passou | < 1 s | diff sem erros de whitespace |
| verificador local de links Markdown nos cinco arquivos F1 | passou (`LOCAL_LINKS_OK`) | < 1 s | links relativos existem; URLs remotas foram confirmadas pelo acesso GitHub |
| `python -m ruff check src tests` | passou | 2,168 s | nenhum arquivo de código alterado |
| `python -m ruff format --check src tests` | passou: `39 files already formatted` | 1,997 s | output literal; não houve formatação |
| `python -m pyright` | não reproduzido no ambiente oficial | 17,979 s | falhou por dependências ausentes no Python global (`fastapi`, `alembic`, `predictor_ops` etc.); `uv` não está disponível no host |
| `python -m pytest -q` | não coletou | 6,327 s | `ModuleNotFoundError: jwt`; nenhuma falha de teste atribuível ao diff docs-only |
| `python -m build --no-isolation` | não iniciou build | 3,941 s | backend `hatchling.build` ausente; nenhuma instalação foi feita |

O comando oficial `uv sync --locked --all-extras --python 3.13` não pôde ser
executado porque `uv` não existe no `PATH`. A F1 não instalou ferramentas nem
dependências e não alterou o lockfile. A execução remota do draft PR será a
verificação do ambiente oficial travado pelo workflow.

## Integridade do escopo

- somente arquivos Markdown de `ecosystem-predictor` foram alterados;
- `src/`, `tests/`, `pyproject.toml`, `uv.lock`, workflows, datasets e
  artefatos científicos não mudaram;
- os oito checkouts usados como evidência permaneceram limpos e somente leitura;
- números históricos nos documentos de fechamento não foram reescritos;
- nenhuma coleta, settlement, scheduler, container, e2e ou operação financeira
  foi executada localmente.
