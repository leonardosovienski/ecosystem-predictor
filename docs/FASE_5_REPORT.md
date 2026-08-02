# Fase 5 — relatório obrigatório (ecosystem-predictor)

Data: 2026-08-02. Branch: `agent/modernize-ecosystem-predictor`. Repositório: `ecosystem-predictor` (o agregador, único repositório tocado nesta sessão).

## Escopo executado

Scaffold completo (profundidade rasa, conforme decisão explícita do
operador) de todos os itens listados em `prompt_fase_5.md`: registry de
plugins e capabilities, contratos versionados (`contracts/v1.py`), API
Gateway (FastAPI), autenticação/autorização/CORS, settings e secrets
(fail-closed), health/readiness, Redis, PostgreSQL, Object Storage,
OpenTelemetry (traces), migrations (Alembic), scheduler via
`predictor_ops`, contract tests, testes E2E, Compose, SBOM, scans, e
runbook de deploy/rollback. Nenhum código de nenhum domínio foi copiado
ou importado — o único material lido dos 5 domínios foi
`pyproject.toml`/`plugin.py`, como evidência para `docs/adr/0001`.

## PR / branch / commit

Nenhum PR foi aberto. Branch local `agent/modernize-ecosystem-predictor`
criada a partir de `master` (`64a6ab1`). Ainda **não commitada nem
enviada** no momento em que este relatório foi escrito — commit e push
acontecem logo após este relatório, antes da pausa para homologação
(push é permitido pela seção Autoridade de `ECOSYSTEM_RULES.md`; PR não
foi aberto, ver "Ação humana necessária").

## Causa raiz comprovada (bugs reais encontrados e corrigidos nesta sessão)

1. **Registry aceitava um shape não-conforme como válido.**
   `hasattr(instance, "capabilities")` retorna `True` mesmo quando
   `capabilities` é um atributo não-chamável — exatamente o shape real de
   `lol-predictor` hoje (`capabilities` é uma tupla de classe, não um
   método). Isso teria permitido o registro aceitar o plugin como
   carregado e falhar só depois, no primeiro dispatch real
   (`TypeError: 'tuple' object is not callable`). Corrigido para
   `callable(getattr(instance, "health", None))` /
   `capabilities`. Teste de regressão:
   `tests/unit/test_registry.py::test_attribute_shaped_capabilities_is_rejected_at_load_not_call_time`.
2. **Settings duplicadas entre app e dependências.** `Depends(get_settings)`
   dentro de `auth.py` reinstanciava `Settings()` a partir do ambiente do
   processo em vez de reusar a instância passada para `create_app()`,
   quebrando toda a suíte E2E autenticada com
   `pydantic.ValidationError` mesmo com o app funcionando normalmente fora
   de teste. Corrigido com
   `app.dependency_overrides[get_settings] = lambda: settings`.
3. **`.gitignore` herdado bloqueava todo código novo.** A regra `*/`
   (ignorar todos os subdiretórios), documentada como decisão histórica de
   quando este repositório era só documentação, teria impedido `git add`
   de rastrear `src/`, `tests/`, `docs/adr/`, etc., silenciosamente.
   Diagnosticado via `git status --short` mostrando só 4 arquivos
   untracked quando ~30+ existiam, confirmado com `git check-ignore -v`.
   Reescrito para um `.gitignore` de projeto Python padrão, preservando o
   histórico como comentário.
4. **Quase-fabricação de digests Docker, autocorrigida.** `compose.yaml`
   inicialmente continha um digest de Postgres inventado e tags
   adivinhadas de MinIO/otel-collector — violação direta da regra desta
   sessão de nunca fabricar hash. Capturado antes do commit, corrigido
   consultando a API real do Docker Hub Registry v2 (`curl` com token
   bearer via `auth.docker.io`), inclusive descobrindo que a tag de MinIO
   adivinhada nem existia (404) e localizando a tag real mais recente.

## Mudanças (arquivos novos, nenhum arquivo de domínio tocado)

`pyproject.toml`, `.gitignore` (reescrito), `src/ecosystem/{contracts,registry,settings.py,db,cache,storage,telemetry,scheduler,gateway}`,
`alembic.ini` + `migrations/`, `tests/{unit,contract,e2e,fixtures,conftest.py}`,
`.env.example`, `docker/{Dockerfile.gateway,otel-collector.yaml}`,
`.dockerignore`, `compose.yaml`, `.github/workflows/ci.yml`,
`docs/adr/{0001-plugin-protocol-v1,0002-data-ownership}.md`,
`docs/{ECOSYSTEM_BLUEPRINT,DEPLOY_RUNBOOK,GO_CHECKLIST,FASE_5_REPORT}.md`.

## Testes / cobertura / lint / tipagem (evidência real, comandos rodados nesta sessão)

| Gate | Comando | Resultado |
|---|---|---|
| Lint | `uv run ruff check src tests` | All checks passed |
| Formato | `uv run ruff format --check src tests` | 39 files already formatted |
| Tipos | `uv run pyright` | 0 errors, 0 warnings, 0 informations |
| Testes | `uv run coverage run -m pytest -q` | 47 passed, 0 warnings |
| Cobertura | `uv run coverage report` | 81% em `src/ecosystem` |

47 testes (era 42 antes do módulo de cache adicionado agora: `CacheClient`
via `fakeredis` real, não mock manual — mesmo padrão do `moto` já usado
para `ObjectStorage`).

## Packaging / container / segurança

- `pyproject.toml` com `[tool.uv.sources]` apontando para as wheels
  publicadas reais de `predictor-core` 2.1.0 / `predictor-ops` 2.0.1 (as
  mesmas URLs já usadas pelos 5 consumidores).
- `docker/Dockerfile.gateway`: multi-stage, base por digest
  (`python:3.13.14-alpine3.24@sha256:...`), non-root, `pip uninstall -y
  pip` no build stage (mesmo padrão de eliminação de CVE do
  cripto-predictor), healthcheck via urllib.
- CI (`.github/workflows/ci.yml`): job `quality` (ruff/pyright/pytest/uv
  build/wheel-smoke fora do checkout), job `secrets` (gitleaks +
  sbom-action), job `container` (docker build + sbom-action + trivy
  pinado por SHA), job `compose` (build + up + `/healthz`/`/readyz` +
  shutdown graceful + down --volumes).
- **Build de imagem, scan Trivy e boot real do Compose NÃO foram
  executados nesta sessão** — o sandbox tem o CLI do Docker mas não tem
  daemon (`docker info` falha; `service docker start` falha em
  `ulimit: Operation not permitted`, uma restrição do sandbox). Validado
  localmente apenas `docker compose config --quiet` (sintaxe). A prova
  real virá do job `container`/`compose` do CI, na primeira execução real
  em GitHub Actions — ver `docs/GO_CHECKLIST.md`.

## Equivalência científica

Não aplicável. Nenhuma fórmula, peso, threshold, seed, calibração,
partição, trial, backtest, closure, hash ou semântica temporal de nenhum
domínio foi tocada — esta sessão trabalhou exclusivamente no agregador,
que hoje não executa nenhuma lógica científica própria (delega tudo a
plugins de domínio, nenhum ainda conectado — ver bloqueadores).

## Itens não executados (deliberadamente, por decisão de escopo)

- Métricas via OpenTelemetry (só traces foram implementados).
- Rate limiting usando `CacheClient` (módulo existe e é testado; gateway
  ainda não o chama).
- Qualquer mudança em repositório de domínio (renomear grupo de entry
  point do cripto, adicionar `capabilities()` ao lol, decisão do f1,
  adapter HTTP do brasileirão) — fora da autoridade desta sessão,
  documentado como follow-up em `docs/adr/0001-plugin-protocol-v1.md`.
- Build de container, scan Trivy, e boot real de Compose (ver seção
  acima — restrição de ambiente, não escolha).

## Readiness

**READY_WITH_INTERNAL_BLOCKERS.** Código do agregador é real, testado e
verde localmente; não está pronto para tráfego de produção porque nenhum
domínio é hoje alcançável através dele (por design — falha fechada), e
porque a prova de container/compose real ainda depende de CI em GitHub
Actions, não executada ainda por não ter havido push. Detalhe completo em
`docs/GO_CHECKLIST.md`.

## Bloqueadores

Internos (documentados, não urgentes): nenhum domínio implementa hoje o
contrato `PluginV1`/`predictor.plugins` de forma correta (ver
`docs/adr/0001-plugin-protocol-v1.md` para os 5 casos específicos).
Nenhum bloqueador externo novo.

## Commits / pushes

Realizados logo após este relatório (ver mensagem de commit no branch
`agent/modernize-ecosystem-predictor`). Nenhum PR aberto, nenhum merge,
nenhum publish, nenhum deploy — ver `docs/DEPLOY_RUNBOOK.md`, seção
"Explicit non-actions this session".

## Ação humana necessária

1. Confirmar se o push do branch (já permitido pela Autoridade) deve vir
   acompanhado de um PR (rascunho) para visibilidade, ou se deve
   permanecer só como branch até nova instrução — esta sessão, dado o
   texto mais restritivo de `prompt_fase_5.md`, fez push mas **não** abriu
   PR; avisar se a leitura foi conservadora demais ou correta.
2. Confirmar os 4 jobs de CI (quality/secrets/container/compose) ficam
   verdes assim que o branch chegar ao GitHub Actions — é a primeira
   verificação real de build de container/boot do Compose.
3. Priorizar qual domínio ganha o primeiro adapter real (ver ranking em
   `docs/GO_CHECKLIST.md`).
4. Decidir destino real de deploy (registro de imagem, plataforma-alvo) —
   nenhum está configurado ainda, mesma postura já adotada para
   predictor-core/predictor-ops na Fase 3.
5. Gerar e armazenar `ECOSYSTEM_JWT_SECRET` real fora deste repositório,
   quando um ambiente real existir.

Parando aqui para homologação humana, conforme `ECOSYSTEM_RULES.md`. Não
inicio a próxima fase automaticamente.
