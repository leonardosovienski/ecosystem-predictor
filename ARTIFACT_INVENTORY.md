# ARTIFACT_INVENTORY.md

Inventário de artefatos por projeto. Verificado em 2026-07-18 por
`git ls-files`/`git check-ignore`/`git status` diretos — não por alegação
de relatório anterior. **Git nunca é usado como prova de preservação para
arquivos gitignored** — para esses, a evidência é filesystem (tamanho,
timestamp, hash quando seguro fazer).

## O que o Git prova (e o que não prova)

Um arquivo **git-tracked** com `git status` limpo prova que o conteúdo é
byte-idêntico ao último commit — prova forte. Um arquivo **gitignored**
não tem essa prova nenhuma: só sabemos o que vemos agora no filesystem
(tamanho/timestamp/hash), sem histórico de versões anteriores. Ao longo
deste ecossistema, `.db`/`ratings.json`/`events.jsonl` são gitignored por
desenho (comentários explícitos nos `.gitignore` de cada projeto: dados de
runtime regeneráveis, ancorados para não engolir `vendor/predictor_core/data/`
por engano).

## brasileirao-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Mutável em produção | Evidência de integridade |
|---|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | Sim, por maturação registrada | `git status`/`git diff` |
| atestado do harness | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | Só em nova trial | `git status` |
| identidade de times | `data/teams_brasileirao.json` | `SCIENTIFIC_VERSIONED` | Sim | — | Raro | `git status` |
| banco de partidas | `data/matches.db`, `data/data/matches.db` | `DATABASE` | Não | Sim (`*.db`) | Sim, diário | Hash SHA-256 comparado antes/depois de cada rodada de engenharia (não prova histórico, só ausência de alteração pela sessão) |
| backup operacional | destino externo escolhido pelo operador (`C:\Claude-projetos\Claude\backups\brasileirao-*` na prova real) | `OPERATIONAL_BACKUP` | Não | — | Sob demanda | `src.backup_restore`: snapshot online SQLite, hashes SHA-256, `integrity_check`, rejeição de adulteração e restore somente em raiz nova; roundtrip real de 2026-07-20 confirmou 1.165 partidas |
| ledgers de sombra (H3/H5) | `data/sombra_picks.jsonl`, `data/sombra_results.jsonl`, `data/sombra_h5_picks.jsonl`, `data/sombra_h5_results.jsonl` | `SCIENTIFIC_UNVERSIONED` (append-only, populações das hipóteses H3/H5) | Não | Sim | Sim, diário pelo agendador (`sombra_diaria`) | Filesystem (tamanho/timestamp); dedupe por `(event_id, selection)` no código; leitura oficial via `scripts/report_shadow_mode.py` |
| log de predições | `data/predictions.jsonl` | `SCIENTIFIC_UNVERSIONED` (append-only) | Não | Sim | Sim, a cada serving | Filesystem |
| heartbeats operacionais | `logs/operations/*.heartbeat.json` | `OPERATIONAL` | Sim (rastreado, mas muda a cada execução real) | — | Sim, a cada ciclo agendado | `git status` mostra o diff; committed quando a sessão de engenharia termina |
| lock operacional | `logs/operations/*.lock` | `EPHEMERAL` | Não | Sim | Sim, só durante execução | Autolimpo pelo `operational_runner` |

## cs-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| atestado | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| identidade de times | `data/teams_cs.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| testes hostis de identidade/lifecycle | `tests/test_identity_hostile.py`, `tests/test_config.py`, `tests/test_cs_snapshots.py` | `CODE_VERSIONED` | Sim | — | suíte completa verde; colisões reais, Unicode NFC, alias ambíguo, truncamento, traversal e concorrência |
| banco | `data/cs.db*` | `DATABASE` | Não | Sim | Hash antes/depois |
| ratings vividos | `data/ratings.json` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | Hash antes/depois |
| snapshots PRE_EVENT/MATURED | `snapshots/` | `SCIENTIFIC_UNVERSIONED` (com vínculo hash interno próprio) | Depende do projeto | — | Verificação própria via `cs_snapshots.py`; reverificado 2026-07-20: 4 `VALID_FORWARD`, 0 pendentes |
| backups operacionais | `backups/` | `OPERATIONAL_BACKUP` | Não | Sim | `src.backup_restore`: manifesto SHA-256 + SQLite `integrity_check`; restore real verificado em 2026-07-20 |
| cotações shadow Polymarket CS | `data/market_shadow.jsonl` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | append-only e deduplicado; identidade/formato exatos; fonte pública read-only; PRE_EVENT obrigatório |
| Market DB | `data/market.db` | `ECONOMIC_UNVERSIONED` | Não | Sim (`*.db`) | Contrato de moneyline de série com timestamp, bookmaker, lote, proveniência e mapping canônico; não confundir com Sports DB |
| contratos Sports/Market e ledger de tentativas | `docs/SPORTS_MARKET_CONTRACTS.md`, `docs/PAST_ATTEMPT_LEDGER.md` | `CODE_VERSIONED` | Sim | — | Define exclusão de quotes legados sem mapping e proíbe promoção automática a trading |

## f1-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| atestado | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| banco de corridas | `data/f1.db` | `DATABASE` | Não | Sim | Hash antes/depois |
| ratings | `data/ratings.json` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | Hash antes/depois |
| snapshots de ingestão Oracle | `data/ingestion/` | `SOURCE_CACHE` + `PROVENANCE` | Não | Sim | payload imutável + metadata SHA-256; `current.json` atômico; não comitar |
| snapshots PRE_EVENT/MATURED | `snapshots/` (F1; ainda ausente) | `SCIENTIFIC_UNVERSIONED` (SHA-256 explícito entre estados; publicação atômica sem overwrite e limpeza de erro parcial) | Não | Sim | `snapshot-status` reverificado 2026-07-20: 0 `VALID_FOR_H8`, gate H8 fechado — faltam 15 |
| banco reconstruível | `data/f1.db` + `data/raw/` | `DATABASE` + `SOURCE_CACHE` | Não | Sim | `integrity_check=ok`; 114 corridas/2.058 resultados/3.750 pitstops; replay corrigido substitui conjunto oficial sem linhas obsoletas |
| testes hostis (auditorias 2026-07-19/20) | `tests/test_model.py`, `tests/test_snapshots.py`, `tests/test_db.py` | `CODE_VERSIONED` | Sim | — | 152 verdes; cobre identidade, DNF, posições, truncamento, duplicidade, tempo, erro parcial, concorrência, replay/correção, lote inválido não destrutivo, determinismo e NaN/Inf |

## lol-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| atestado (trials) | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| atestado (scheduler probe) | `data/scheduler_probe_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| identidade de times | `data/teams_lol.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| banco | `data/lol.db*` | `DATABASE` | Não | Sim | Hash antes/depois |
| ratings | `data/ratings.json` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | Hash antes/depois |
| snapshot EWC (pré-evento) | `data/snapshots/ewc_2026_pre_event_ratings.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| testes hostis (auditoria 2026-07-19/20) | `tests/test_hostile_audit.py` | `CODE_VERSIONED` | Sim | — | commit `d8e7fd2` + fechamento local de identidade, tempo e concorrência; 71 verdes |
| cotações shadow Polymarket | `data/shadow/market_quotes.jsonl` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | append-only PRE_EVENT; fonte pública read-only; criado apenas quando houver mercado coberto |
| testes da fonte de mercado | `tests/test_polymarket_provider.py` + `tests/test_collect_polymarket_shadow.py` | `CODE_VERSIONED` | Sim | — | 5 testes determinísticos; suíte total 76 verdes |
| pré-registro H4 LoL | entrada `h4-lol-market-shadow-prospectivo` em `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | registrado 2026-07-20T06:20:41Z; probes anteriores excluídos; gate 50/30 dias/3 competições |
| H4-R LoL retrospectiva | `data/reports/h4r_polymarket_retrospective_2026-07-20.json` | `SCIENTIFIC_VERSIONED` | Sim | — | 177 partidas/28 competições; resultado inconclusivo; hash do banco incorporado |
| alias Polymarket | `data/polymarket_aliases.json` | `SCIENTIFIC_VERSIONED` | Sim | — | mapping fonte-específico explícito; sem fuzzy matching |
| tarefa shadow LoL | Task Scheduler `lol-market-shadow` | `OPERATIONAL_EXTERNAL` | Não | — | 30 min; primeira execução `LastTaskResult=0`; sem trading |

## previsao-cripto

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `GarimpoInvestimentos/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` — teve 1 mudança real de produção nesta linha do tempo (commit `40f3ddc`, sharpe maturado) |
| atestado | `GarimpoInvestimentos/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| eventos telemetria | `events.jsonl` | `SCIENTIFIC_UNVERSIONED` (telemetria estruturada, não dado bruto) | Não | Sim | Hash antes/depois (mudou por atividade real de produção concorrente à sessão) |
| eventos v3 | `data/v3/events_v3.jsonl` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | idem |
| feature store | `previsao-cripto/output/feature_store.db` (relativo ao workspace; `output/feature_store.db` no repo) | `DATABASE` | Não | Sim | `PRAGMA integrity_check=ok` em modo read-only (2026-07-20); 4.714.496 bytes |
| backups do feature store | destino escolhido pelo operador, fora do repo | `OPERATIONAL_BACKUP` | Não | — | `scripts/feature_store_backup.py`: snapshot online SQLite, manifesto SHA-256, `integrity_check` e restore somente em raiz nova; roundtrip real verificado em 2026-07-20 |
| **logs operacionais afetados por incidente** | `logs/garimpo_fase1_20260713.log` a `_17.log` | `LOG` | Não | Sim | **Nunca entraram no Git** — ver `SECURITY_INCIDENT_SECRET_ROTATION.md`. Contagem de ocorrência verificada por scanner seguro (sem exibir valor) |

## tools/ e predictor_core

Não produzem dado — só código e manifests. `TOOLS_MANIFEST.json` e
`CORE_MANIFEST.json` (por vendor) são `MANIFEST`, git-tracked, hash por
arquivo + agregado — a prova de integridade É o próprio Git aqui, sem
ressalva.

## Projetos PARKED

Não investigados a fundo nesta rodada (fora de escopo — consulta apenas
histórica). `vendor/predictor_core/CORE_MANIFEST.json` de cada um continua
declarando a versão antiga (`3445e37f43c458cc` para wc-predictor-v2 e
predictor-stocks; `026f1f7b761440d9` para nba-predictor) — drift esperado
e correto contra o canônico atual.

## O que nunca deve ser commitado

`.env`, qualquer `*.db`, `logs/` de qualquer projeto, saída de scanner de
segredo contendo valor, arquivos de heartbeat/lock enquanto uma execução
real está em andamento (esperar o job terminar antes de considerar
commitá-los).

## Cobertura de backup e lacunas restantes

Bancos SQLite/FeatureStore ainda não cobertos em todos os consumidores —
`OPEN_OPERATIONAL_GAP` em `PENDENCIAS_ABERTAS.md` (OP-4). Brasileirão, CS,
F1 e cripto já possuem recuperação verificada; a lacuna restante é dos outros
consumidores e de uma política humana comum de retenção/local externo.

## O que exige hash externo

Qualquer artefato `*_UNVERSIONED` acima, quando uma sessão de engenharia
for tocar código que os lê/escreve — sempre calcular SHA-256 antes/depois
da sessão como prova de não-alteração (é o que esta e as rodadas
anteriores fizeram, documentado em `ECOSYSTEM_FINAL_CLOSURE.md` seção 15).
