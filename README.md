# Ecossistema Preditivo Local

Verificado em: 2026-07-18. Este é o ponto de entrada. Para retomar o
trabalho numa nova sessão, leia **[ECOSYSTEM_HANDOFF.md](ECOSYSTEM_HANDOFF.md)**
antes de qualquer outra coisa.

## Visão geral

Workspace com 10 repositórios Git independentes (não é monorepo), duas
camadas compartilhadas canônicas, 5 domínios de previsão vivos e 3
projetos históricos congelados.

## Arquitetura

```
                    ┌─────────────┐         ┌──────────────────┐
                    │   tools/    │         │  predictor_core/  │
                    │ operacional │         │    científico      │
                    └──────┬──────┘         └─────────┬─────────┘
                           │                           │
                           │      vendoring (cópia byte-idêntica,
                           │      sync_core.py --write)
                           ▼                           ▼
       ┌────────────────────────────────────────────────────────┐
       │  brasileirao-predictor · cs-predictor · f1-predictor ·  │
       │  lol-predictor · previsao-cripto   (5 vivos)             │
       └────────────────────────────────────────────────────────┘

       wc-predictor-v2 · predictor-stocks · nba-predictor (3 PARKED,
       congelados — vendor antigo intocado, nunca recebem --write)
```

- **`tools/`** — infraestrutura operacional pura: runner com lock/heartbeat/
  timeout, redação de segredos, provenance, manifests de release. Zero
  lógica científica ou de domínio. Ver [tools/README.md](tools/README.md),
  [tools/HANDOFF.md](tools/HANDOFF.md).
- **`predictor_core/`** — contratos científicos compartilhados
  (`PredictionPoint`, `TrialRegistry`, `RatingBook`, mensuração). Só o que
  já provou ser compartilhável entre 2+ domínios reais. Ver
  [predictor_core/README.md](predictor_core/README.md),
  [predictor_core/HANDOFF.md](predictor_core/HANDOFF.md).
- **5 consumidores vivos** — cada um com hipóteses científicas, dados e
  automações próprias. Cada um tem `README.md` e `HANDOFF.md` no seu
  diretório.
- **3 projetos PARKED** (`wc-predictor-v2`, `predictor-stocks`,
  `nba-predictor`) — congelados, preservados como conhecimento histórico.
  Nunca sincronizam, nunca recebem evolução funcional. Ver seção abaixo.

## Status atual (2026-07-18)

| Camada | Testes | Estado |
|---|---|---|
| tools/ | 137 passed, 1 skipped | Verde |
| predictor_core | 263 passed | Verde |
| brasileirao-predictor | 302 passed | Verde |
| cs-predictor | 100% verde | Verde |
| f1-predictor | 100% verde | Verde |
| lol-predictor | 100% verde | Verde |
| previsao-cripto | 302 passed, 2 skipped | Verde |

**Bugs de código conhecidos e não corrigidos: zero.** Um incidente de
segurança segue aberto (rotação de credencial pendente, ação humana
externa) — ver [SECURITY_INCIDENT_SECRET_ROTATION.md](SECURITY_INCIDENT_SECRET_ROTATION.md).
Lista completa de pendências reais: [PENDENCIAS_ABERTAS.md](PENDENCIAS_ABERTAS.md).

## Pré-requisitos

Python **3.13+** (confirmado testado; `tools/pyproject.toml` declara
`requires-python = ">=3.13"`). Windows é o ambiente real de produção hoje
— nenhum CI multiplataforma foi executado. `tools/` e `predictor_core` são
**stdlib-only**; os domínios têm suas próprias dependências (ver o
`requirements`/venv de cada um).

## Comandos reais (testados 2026-07-18)

```bash
# tools/ — da raiz do workspace
python -m pytest tools/ -q

# predictor_core — do próprio diretório
cd predictor_core && python -m pytest -q

# cada consumidor vivo — do próprio diretório
cd brasileirao-predictor && python -m pytest -q   # idem para cs/f1/lol/previsao-cripto

# release preflight de tools/
python tools/release_check.py

# manifest de tools/
cd tools && python release_manifest.py --check

# sincronização/drift do predictor_core
cd predictor_core && python sync_core.py --check

# auditoria byte a byte dos vendors
python tools/vendor_byte_audit.py --workspace . --consumer brasileirao-predictor --consumer cs-predictor --consumer f1-predictor --consumer lol-predictor --consumer previsao-cripto
```

Comandos completos e detalhados: ver os runbooks em `RUNBOOK_*.md`.

## Manifests e vendors

`predictor_core/CORE_MANIFEST.json` (por vendor) e
`tools/TOOLS_MANIFEST.json` — hash por arquivo + agregado. Sincronização é
sempre unidirecional (`predictor_core/`/`tools/` → vendor), nunca o
contrário. Ver [RUNBOOK_VENDOR_SYNC.md](RUNBOOK_VENDOR_SYNC.md).

## Política PARKED

`wc-predictor-v2`, `predictor-stocks`, `nba-predictor` estão congelados.
Regra absoluta: nunca sincronizar, nunca atualizar vendor, nunca evoluir
funcionalmente. `predictor_core/sync_core.py:51` declara a lista
`PARKED` — `_is_parked()` é checado antes de qualquer escrita,
independente de `--target`. Podem ser consultados como fonte histórica.
Condição para reabrir cada um: ver os respectivos `HANDOFF.md`.

## Artefatos científicos e operacionais

Nem todo artefato citado como "importante" está sob controle de versão —
`.db`, `ratings.json`, `events.jsonl` são **gitignored por desenho** em
todos os 5 consumidores (dados de runtime regeneráveis). Os artefatos
científicos realmente versionados são `trials.json`,
`trials.harness_attestation.json`, `teams_*.json` — confirmados por
`git ls-files` em cada projeto. Inventário completo:
[ARTIFACT_INVENTORY.md](ARTIFACT_INVENTORY.md).

## Política de segredos

Nenhum segredo em código ou documentação. Redação obrigatória via
`tools.secret_redaction` antes de qualquer persistência de log. Ver
[SECURITY.md](SECURITY.md).

## Incidente ativo

Chave da SerpAPI (previsao-cripto) registrada em 5 logs históricos, nunca
versionados pelo Git. Mecanismo de prevenção corrigido e verificado
funcionando. Rotação da credencial no provedor é ação humana pendente,
explicitamente despriorizada por decisão do responsável (sem prazo).
Detalhe completo: [SECURITY_INCIDENT_SECRET_ROTATION.md](SECURITY_INCIDENT_SECRET_ROTATION.md).

## Tarefas agendadas

Ver [RUNBOOK_CRYPTO_AUTOMATION.md](RUNBOOK_CRYPTO_AUTOMATION.md) (único
projeto com automação via Windows Task Scheduler hoje) e o `HANDOFF.md` de
`brasileirao-predictor` (`sombra-manha`/`sombra-noite`, agendadas via
`operational_runner`).

## Documentos canônicos

| Documento | Finalidade |
|---|---|
| `README.md` (este) | Entrada |
| [ECOSYSTEM_HANDOFF.md](ECOSYSTEM_HANDOFF.md) | Continuidade — leia primeiro numa sessão nova |
| [PENDENCIAS_ABERTAS.md](PENDENCIAS_ABERTAS.md) | Lista ativa de tudo que resta |
| [SECURITY.md](SECURITY.md) / [SECURITY_INCIDENT_SECRET_ROTATION.md](SECURITY_INCIDENT_SECRET_ROTATION.md) | Segurança e incidente |
| [ARTIFACT_INVENTORY.md](ARTIFACT_INVENTORY.md) | O que é dado, o que é log, o que é ciência |
| [ECOSYSTEM_FINAL_CLOSURE.md](ECOSYSTEM_FINAL_CLOSURE.md) | Encerramento técnico (histórico reconstruído) |
| [FINAL_FORENSIC_REVIEW.md](FINAL_FORENSIC_REVIEW.md) | Revisão independente das rodadas técnicas |
| [AUDIT_DIRECTORY_RECONCILIATION.md](AUDIT_DIRECTORY_RECONCILIATION.md) | Reconciliação da auditoria independente `audit/` |
| [FINAL_DOCUMENTATION_CLOSURE.md](FINAL_DOCUMENTATION_CLOSURE.md) | Encerramento documental (esta rodada) |
| `RUNBOOK_*.md` | Execução — testes, sync, release, automação, incidente, integridade |

## Limites da validação

Tudo testado localmente, com evidência real quando aplicável (ex.: ciclo de
produção real confirmando o fix de redação de log). Não validado:
publicação real, CI remoto (nenhum configurado), operação distribuída
multi-máquina. Nenhuma alegação de "production-ready" sem escopo — ver
`ECOSYSTEM_FINAL_CLOSURE.md` para a distinção exata entre o que foi
provado e o que depende de operação real.

## Política de publicação

Nada foi publicado (sem push, sem tag) em nenhum dos 10 repositórios nesta
linha do tempo. `predictor_core` e `tools/` não têm remoto configurado.
Publicação é decisão humana explícita, fora do escopo de qualquer rodada
automática.
