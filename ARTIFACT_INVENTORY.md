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
| heartbeats operacionais | `logs/operations/*.heartbeat.json` | `OPERATIONAL` | Sim (rastreado, mas muda a cada execução real) | — | Sim, a cada ciclo agendado | `git status` mostra o diff; committed quando a sessão de engenharia termina |
| lock operacional | `logs/operations/*.lock` | `EPHEMERAL` | Não | Sim | Sim, só durante execução | Autolimpo pelo `operational_runner` |

## cs-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| atestado | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| identidade de times | `data/teams_cs.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| banco | `data/cs.db*` | `DATABASE` | Não | Sim | Hash antes/depois |
| ratings vividos | `data/ratings.json` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | Hash antes/depois |
| snapshots PRE_EVENT/MATURED | `snapshots/` | `SCIENTIFIC_UNVERSIONED` (com vínculo hash interno próprio) | Depende do projeto | — | Verificação própria via `cs_snapshots.py` (hash entre PRE_EVENT e MATURED) |

## f1-predictor

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `data/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` |
| atestado | `data/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| banco de corridas | `data/f1.db` | `DATABASE` | Não | Sim | Hash antes/depois |
| ratings | `data/ratings.json` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | Hash antes/depois |
| snapshots PRE_EVENT/MATURED | forward snapshots (F1) | `SCIENTIFIC_UNVERSIONED` (SHA-256 explícito entre estados, escrita exclusiva de SO) | Depende | — | Verificação própria em `src/snapshots.py` |

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

## previsao-cripto

| Artefato | Caminho | Tipo | Git-tracked | Ignorado | Evidência |
|---|---|---|---|---|---|
| trials | `GarimpoInvestimentos/trials.json` | `SCIENTIFIC_VERSIONED` | Sim | — | `git status` — teve 1 mudança real de produção nesta linha do tempo (commit `40f3ddc`, sharpe maturado) |
| atestado | `GarimpoInvestimentos/trials.harness_attestation.json` | `ATTESTATION` | Sim | — | `git status` |
| eventos telemetria | `events.jsonl` | `SCIENTIFIC_UNVERSIONED` (telemetria estruturada, não dado bruto) | Não | Sim | Hash antes/depois (mudou por atividade real de produção concorrente à sessão) |
| eventos v3 | `data/v3/events_v3.jsonl` | `SCIENTIFIC_UNVERSIONED` | Não | Sim | idem |
| feature store | `output/feature_store.db` | `DATABASE` | Não | Sim | idem |
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

## O que exige backup (não implementado nesta rodada)

Bancos SQLite/FeatureStore de cada consumidor — `OPEN_OPERATIONAL_GAP` em
`PENDENCIAS_ABERTAS.md` (OP-4), sem evidência de perda de dados real até
hoje, não implementado por falta de necessidade comprovada.

## O que exige hash externo

Qualquer artefato `*_UNVERSIONED` acima, quando uma sessão de engenharia
for tocar código que os lê/escreve — sempre calcular SHA-256 antes/depois
da sessão como prova de não-alteração (é o que esta e as rodadas
anteriores fizeram, documentado em `ECOSYSTEM_FINAL_CLOSURE.md` seção 15).
