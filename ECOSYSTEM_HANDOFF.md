# ECOSYSTEM_HANDOFF.md

Documento mestre de continuidade. Verificado em: 2026-07-18. Leia este
documento **primeiro** em qualquer sessão nova.

## COMO RETOMAR EM UMA NOVA SESSÃO

Ordem obrigatória de leitura:

1. `ECOSYSTEM_HANDOFF.md` (este documento)
2. `PENDENCIAS_ABERTAS.md`
3. `SECURITY_INCIDENT_SECRET_ROTATION.md`
4. `ECOSYSTEM_FINAL_CLOSURE.md`
5. O `HANDOFF.md` do projeto específico que você vai tocar
6. O `README.md` desse projeto
7. Git (`git log`, `git status`, `git diff`) do projeto
8. Código atual

Uma sessão nova **não deve depender desta conversa**. Tudo que uma sessão
nova precisa saber está nos documentos acima e no código/Git — não em
memória de chat.

## Mapa dos repositórios

**Desde 2026-07-19, por ordem explícita do operador, TODOS os repositórios
estão publicados no GitHub (privados, conta `leonardosovienski`) e
sincronizados** — verificação local×remoto commit a commit feita na
publicação. Linhas antigas pré-existentes no GitHub (junho/2026) foram
preservadas em branches `arquivo/*` antes de a `main` canônica substituí-las
(`wc-predictor-v2`: `arquivo/shadow-junho-2026`; `predictor_core`:
`arquivo/core-junho-2026`).

| Repo | Papel | Branch | Remoto (github.com/leonardosovienski/) |
|---|---|---|---|
| `tools/` | Operacional canônico | `main` | `predictor-tools` ✓ |
| `predictor_core/` | Científico canônico | `main` | `predictor_core` ✓ (linha junho arquivada) |
| `brasileirao-predictor` | Vivo | `main` | `brasileirao-predictor` ✓ |
| `cs-predictor` | Vivo | `main` | `cs-predictor` ✓ |
| `f1-predictor` | Vivo | `main` | `f1-predictor` ✓ |
| `lol-predictor` | Vivo | `main` | `lol-predictor` ✓ |
| `previsao-cripto` | Vivo | `main` | `previsao-cripto` ✓ |
| `wc-predictor-v2` | PARKED — encerramento em andamento (falta só a final) | `main` | `wc-predictor-v2` ✓ (linha junho arquivada) |
| `predictor-stocks` | REABERTO (ciência ativa; vendor congelado) | `main` | `predictor-stocks` ✓ |
| `nba-predictor` | PARKED (push = preservação, não reabertura) | `main` | `nba-predictor` ✓ |
| raiz (governança) | Documentação canônica | `master` | `predictor-ecosystem` ✓ |

## Arquitetura

Ver `README.md` para o diagrama. Regra de ouro: escrita é sempre
unidirecional — `predictor_core/`/`tools/` → vendor do consumidor, nunca o
contrário. Nenhum domínio importa outro domínio diretamente.

## Camadas canônicas — versões e commits-base

| Camada | Versão | Commit-base (2026-07-18) | Testes |
|---|---|---|---|
| tools/ | 1.3.0 | `2732713` | 137 passed, 1 skipped |
| predictor_core | 1.3.1-ga-20260716 | `9868c01` | 263 passed |

Recomendação de versão pendente de autorização: ambos são candidatos a
bump PATCH (correções de robustez, sem quebra de API pública) — não
executado.

## Consumidores vivos — vendors e testes

| Consumidor | Vendor de predictor_core | Byte-idêntico | Testes |
|---|---|---|---|
| brasileirao-predictor | sync `5276f65` | Sim (`vendor_byte_audit.py`) | 320 passed (2026-07-19, rodada hostil 2) |
| cs-predictor | sync `7627c03` | Sim | 100% verde |
| f1-predictor | sync `c99a545` | Sim | 100% verde |
| lol-predictor | sync `593dbc0` | Sim | 100% verde |
| previsao-cripto | sync `f4d4d81` | Sim | 302 passed, 2 skipped |

## Projetos PARKED e o caso predictor-stocks

`wc-predictor-v2` e `nba-predictor` — PARKED plenos: vendor congelado em
agregado antigo (`3445e37f43c458cc` o WC, `026f1f7b761440d9` o NBA),
drift esperado e correto contra o canônico atual, nenhuma evolução
funcional permitida. Condição para reabrir cada um: ver `HANDOFF.md` de
cada projeto.

**Encerramento do WC em andamento (2026-07-19, decisão do operador):** o
POSTMORTEM pré-registrado (`wc-predictor-v2/docs/POSTMORTEM_COPA_2026.md`)
está quase todo executado — causa raiz do truncamento do
`predictions.jsonl` provada por forense (sobrescrita por cópia de
worktree em 12/07, sessão de assistente; código/git/operador inocentados),
decisões do §5 tomadas (promoção SEM OBJETO: a produção original
`Downloads\wc-predictor` foi deletada para a Lixeira em 26/06 — resolve a
contradição histórica do SHADOW.md; v3 arquivada), 3º lugar aferido,
livro fechado com 0 apostas abertas (banca R$ 708, −5,84u). Falta apenas:
resultado da final → ingest/settle → backup congelado → métricas §1 →
veredito. Decisão humana aberta: restaurar ou não a produção deletada da
Lixeira (o `matches.db` do cron de odds está lá).

`predictor-stocks` — **REABERTO para pesquisa em 2026-07-18** por decisão
explícita do operador, satisfazendo a condição formal de reabertura do
seu próprio HANDOFF ("decisão humana explícita + hipótese formalizada
antes de qualquer código"): H4 (volatility targeting) e H5 (reversão de
curto prazo 21d) foram pré-registradas antes de código e julgadas em
rodada única — ambas **NÃO COMPROVADAS** (H5 com IC inteiramente
negativo, anti-sinal). O trabalho ocorreu numa linha remota
(GitHub `leonardosovienski/predictor-stocks`), mergeada em `main`
(`2dc23be`) e verificada localmente em 2026-07-19: suíte 144 verdes,
integridade do vendor 4/4, provenance de runtime `MATCH`. **O vendor
permanece deliberadamente congelado em 1.3.0-ga-20260711** (agregado
`3445e37f43c458cc`) por regra do próprio HANDOFF do projeto — a pesquisa
usa somente APIs já vendorizadas.

`sync_core.py:56` declara `PARKED = {"wc-predictor-v2",
"predictor-stocks", "nba-predictor"}` — checado antes de qualquer
escrita, mesmo com `--target` explícito. `predictor-stocks` permanece na
lista **intencionalmente**: para ele, a semântica passa a ser "vendor
congelado por decisão do projeto", não "projeto inativo". Histórico: essa
lista ficou vazia por engano entre 2026-07-03 e 2026-07-17, causando um
sync indevido nos 3 (commits `vendor: predictor_core v1.3.1...` locais,
nunca publicados); corrigido em `15b6ada`, os 3 revertidos via
`git revert` (nunca reset).

## Manifests e vendors

`tools/TOOLS_MANIFEST.json`: `--check` via `tools/release_manifest.py`.
`predictor_core/CORE_MANIFEST.json` por vendor: `--check` via
`predictor_core/sync_core.py`. Auditoria byte-a-byte independente:
`tools/vendor_byte_audit.py`. Todos confirmados corretos em 2026-07-18.

## Testes — resumo

Ver tabela em `README.md`. Comandos completos: `RUNBOOK_TESTS.md`.

## Automações

Único projeto com Windows Task Scheduler ativo hoje: `previsao-cripto`
(`GarimpoFase1`, `GarimpoV3Daily`, `cripto-watchdog-coleta` — `Ready`,
`S4U`, últimas execuções com sucesso verificadas 2026-07-18; tarefa legada
`GarimpoInvestimentos-ColetaDiaria` confirmada `Disabled`). Detalhe
completo: `RUNBOOK_CRYPTO_AUTOMATION.md`. `brasileirao-predictor` também
tem `brasileirao-sombra-manha`/`-noite` agendadas via `operational_runner`
— ver seu `HANDOFF.md`.

## Artefatos

Ver `ARTIFACT_INVENTORY.md` para o inventário completo por projeto.
Resumo: `.db`/`ratings.json`/`events.jsonl` são gitignored (não provados
por Git); `trials.json`/`trials.harness_attestation.json`/`teams_*.json`
são os artefatos científicos realmente versionados.

## Segurança

Ver `SECURITY.md` (política) e `SECURITY_INCIDENT_SECRET_ROTATION.md`
(incidente ativo, documento sanitizado, sem nenhum valor de segredo).
Estado: `BLOCKED_PENDING_SECRET_ROTATION`, explicitamente baixa prioridade
por decisão humana (2026-07-18).

## Pendências

Lista canônica completa: `PENDENCIAS_ABERTAS.md`. Resumo: 1 incidente de
segurança (bloqueado por ação externa, baixa prioridade), 0 bugs de código
abertos, o resto são gaps científicos/operacionais conscientemente
deferidos ou capacidades incubadas, todos com condição de reabertura
registrada.

## Decisões científicas (não reabrir sem evidência nova)

- `RatingBook` não normaliza identidade — mudaria ciência.
- Lifecycle `PRE_EVENT`/`MATURED` não é contrato comum do core — 3
  implementações com garantias diferentes (CS tem hash-linkage).
- `PredictionPoint` não prova proveniência de inputs — gap de design, não
  bug.
- `is_mature()` não bloqueia acesso — decisão de design.

## Decisões operacionais (não reabrir sem evidência nova)

- `tools/` sem instalação via pacote — consumo é por `sys.path`.
- Split-brain de import flat/package em `tools/` — travado por tripwire,
  não eliminado (removeria a forma que os testes internos usam).
- Sync do core é sempre por vendoring, nunca pacote publicado.

## Regras de sync

Ver `RUNBOOK_VENDOR_SYNC.md`. Nunca `--write` sem confirmar `PARKED`
primeiro. `--target` é preferível a sync global quando só 1 consumidor
precisa da mudança.

## Regras de publicação

Todos os repos publicados no GitHub (privados) em 2026-07-19 por ordem
explícita do operador — ver mapa acima. Pushes subsequentes, tags e
releases continuam sendo decisão humana explícita — nunca automáticos.
Autenticação: `gh` CLI instalado e autenticado via device flow
(`leonardosovienski`, escopo `repo`).

## Condições de reabertura — índice

Ver a coluna "condição para reabrir" em `PENDENCIAS_ABERTAS.md` para cada
item individual — não duplicada aqui.

## Documentos canônicos

Ver tabela em `README.md`.

## Ações humanas obrigatórias

1. Rotação da credencial da SerpAPI no provedor — quando for prioridade
   (checklist completo em `SECURITY_INCIDENT_SECRET_ROTATION.md`).
2. Nenhuma outra ação humana obrigatória pendente.
