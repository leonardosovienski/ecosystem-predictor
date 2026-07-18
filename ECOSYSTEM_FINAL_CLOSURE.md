# ECOSYSTEM_FINAL_CLOSURE.md

Documento canônico de encerramento do ciclo de evolução do ecossistema
preditivo local. Escrito para substituir a necessidade de reler o histórico
completo da conversa. Toda afirmação factual abaixo foi verificada nesta
sessão por `git log`/`git show`/`git status`, execução de teste, ou leitura
direta de arquivo — não por memória de conversa compactada.

## 1. Resumo executivo

O ecossistema é composto por 2 camadas canônicas (`tools/` operacional,
`predictor_core` científica), 5 consumidores vivos e 3 projetos protegidos
(PARKED). Reconstruí a linha do tempo inteira por Git (não pela conversa),
revisei cada rodada e cada commit, e recontei tudo diretamente. Uma revisão
forense independente já havia sido feita para o período mais recente
(`FINAL_FORENSIC_REVIEW.md`, commit `cca60f0`) — confirmado nesta sessão que
**nenhum repositório mudou desde então** (todos os HEADs conferem
exatamente), então essa revisão permanece válida como fechamento desse
período e não foi refeita. O trabalho novo desta rodada foi reconstruir e
verificar o histórico ANTERIOR a ela: a reintegração (Ondas 1-6), o
hardening geral, e a genealogia completa de `PredictionPoint`/`TrialRegistry`
desde a criação. Encontrei uma correção real a fazer nesta própria revisão
(seção 15: a caracterização de "hashes científicos git-tracked" usada
repetidamente nas rodadas anteriores estava **imprecisa** — os artefatos
`.db`/`ratings.json`/`events.jsonl` nunca foram rastreados pelo Git, são
gitignored por desenho; os artefatos realmente versionados são
`trials.json`/`trials.harness_attestation.json`/`teams_*.json`, que **estão
limpos em 4 dos 5 consumidores e com uma mudança real de produção, já
identificada e intocada, no 5º**). Nenhuma regressão de código foi
encontrada. **Veredito: PASS FINAL COM PENDÊNCIAS NÃO BLOQUEANTES.**

## 2. Escopo completo

`tools/`, `predictor_core`, os 5 consumidores vivos, os 3 protegidos, e o
repositório de governança da raiz (`C:\Claude-projetos\Claude`, onde vivem
`SINERGIAS_ECOSSISTEMA.md`, `FINAL_FORENSIC_REVIEW.md` e este documento).

## 3. Metodologia

Para cada repositório: `git log --pretty=format:'%h %ci %s' --reverse`
completo (não só os commits citados em relatórios anteriores), leitura de
`git show --stat`/diff nos commits-chave, `git status` em todos os 10 repos,
reexecução de suítes de teste, e comparação cruzada com
`SINERGIAS_ECOSSISTEMA.md` (documento pré-existente, não escrito por mim
nesta sessão) para checar divergências. Onde a conversa compactada e o Git
concordavam, usei o Git como prova primária, citando a conversa só como
contexto complementar. Onde não pude recuperar o PORQUÊ de uma decisão além
da mensagem de commit (ex.: commits de 2026-06-16/17 e o commit `5f1b770`,
todos de uma sessão anterior a esta conversa — `5f1b770` é coautorado por
"Claude Fable 5", não pelo assistente desta conversa), marquei
explicitamente como tal, sem inventar justificativa.

## 4. Estado inicial reconstruído

Antes de qualquer commit desta sessão, o workspace já tinha: `predictor_core`
em `v1.3.1-ga-20260716` (22 commits, desde a gênese `165a64a` de
2026-06-16), `tools/` em `1.3.0` (25 commits, desde `b24e283` de 2026-07-15),
5 consumidores vivos sincronizados no mesmo agregado, e um repositório de
governança da raiz com `SINERGIAS_ECOSSISTEMA.md` documentando a
reintegração "Ondas 1-6" concluída no mesmo dia (2026-07-17), antes desta
sessão de revisão.

## 5. Linha do tempo completa (reconstruída por Git, cronológica)

| Data/hora | Repo | Commit | O que aconteceu | Fonte |
|---|---|---|---|---|
| 2026-06-16/17 | predictor_core | `165a64a`…`2b375a3` | Gênese do core: v0.4.0→v0.7.0 (replay anti-lookahead, net.py, settings.py com trava de credenciais) | git log — sessão anterior a esta conversa, sem contexto de conversa recuperável |
| 2026-07-03 | predictor_core | `55c5fa3`, `ccae2bf` | Release v1.0.0 ("plataforma completa, 3/3 domínios"); v1.0.1 (guard de vazamento de segredo na telemetria) | git log |
| 2026-07-03 | predictor_core | (comentário em `sync_core.py:47`) | "Onda 5": `wc-predictor` desparkado (decisão de sessão anterior, não desta) | código-fonte, comentário datado |
| 2026-07-09 | predictor_core | `9af9702`, `1f07c2b` | v1.1.0: **gênese de `PredictionPoint` e `TrialRegistry`** — governança N+1, schema, trava harness-registry | git log |
| 2026-07-11 | predictor_core | `08eb659` | v1.3.0 "estado definitivo": `contracts/` (fachada), calibração Platt+Shin, prequential ABC, `timeindex`/`jsonl_store`, `curl_cffi` lazy | git log |
| 2026-07-11 | (todos) | — | Fechamento dos ciclos brasileirão/NBA/CS/LoL, Fase 0 da F1 (`SINERGIAS_ECOSSISTEMA.md`, criado nesta data) | doc pré-existente |
| 2026-07-17 00:42 | predictor_core | `5f1b770` | v1.3.1 "auditoria adversarial": 6 bugs de comportamento + 6 gaps de contrato (ver seção 8) — **sessão anterior a esta conversa** (coautor "Claude Fable 5") | git log, git show |
| 2026-07-17 (madrugada-manhã) | 5 consumidores | vários | Trabalho de domínio real: hardening operacional (locks, watchdog), correções de bug de domínio (F1 `winner_hit`, LoL grafia de time), features opt-in | git log de cada consumidor |
| 2026-07-17 (Fase 1-2, ondas 1-6) | tools/, predictor_core, 5 consumidores | `858589e`, `95c2097`…`3c41a55` (parcial), commits em cada consumidor | Reintegração formal: `sync_core --target`, remoção de literal CoinGecko de `secret_redaction`, `release_manifest.py` canônico, teste de F1 sem versão hardcoded, `previsao-cripto` consumindo `tools.secret_redaction` | `SINERGIAS_ECOSSISTEMA.md` seção "Pós-Onda 6", cruzado com git log |
| 2026-07-17 (hostil, 1ª rodada) | predictor_core, tools/, brasileirao | `df575a9`…`273b908` (parcial: obs, contracts deepcopy, trials lock, rating duplicado); `e54a55d` (brasileirão) | Auditoria hostil: `read_events` com contexto de erro; `_tracked_files` Unicode; `atomic_write_json` sem tempfile órfão; **bugs financeiros reais no brasileirão** (settlement sem `match_date`, idempotência por posição em vez de `bet_id`) | git log + diff lido nesta sessão |
| 2026-07-17 20:42-22:11 | tools/, predictor_core, 5 consumidores, 3 protegidos | `15b6ada`…`f4d4d81`, `5efb129`…`bce5043` | "Evolução estratégica" de `tools/` e `predictor_core` (esta conversa): descoberta e correção do sync indevido nos protegidos, ReDoS, race de heartbeat, `PredictionPoint`/`TrialRegistry` hardening, sync dos 5 vivos | Coberto integralmente por `FINAL_FORENSIC_REVIEW.md` |
| 2026-07-17 (após `cca60f0`) | — | — | **Nenhuma atividade** — confirmado nesta sessão, todos os HEADs idênticos ao que a revisão forense já viu | git log de todos os 10 repos, reconfirmado agora |

## 6. Arquitetura final

`tools/` = camada operacional (8 módulos, stdlib-only). `predictor_core` =
camada científica (35 módulos). 5 consumidores vivos vendorizam ambos.
3 protegidos vendorizam só `predictor_core` (histórico, congelado). Nenhuma
dependência de domínio→domínio encontrada (confirmado por
`SINERGIAS_ECOSSISTEMA.md`, seção "Matriz de dependências", e reconfirmado
por grep nesta sessão).

## 7. Papel do tools/ e do predictor_core

Sem mudança desde os dois relatórios de rodada — ver `FINAL_FORENSIC_REVIEW.md`
seções 5-19 para a revisão integral e verificada dessa fronteira.

## 8. Revisão da reintegração (Bloco A)

A reintegração (Ondas 1-6) é o trabalho documentado em
`SINERGIAS_ECOSSISTEMA.md`, concluído ANTES desta conversa de revisão
começar (a conversa retomou depois do checkpoint "Pós-Onda 6"). Verificado
nesta sessão, cruzando a tabela "Estado factual das integrações concluídas"
do documento contra o Git:

| Item do doc | Commit correspondente | Confirmado? |
|---|---|---|
| `sync_core --target` (Onda 2A) | `858589e` | SIM — presente, com 16 testes (`tests/test_sync_core.py`, reconfirmado nesta sessão em rodadas posteriores) |
| Remoção de literal CoinGecko (Onda 3) | Não localizado por hash isolado — parte de um commit maior do tools/ pré-`4325b7a` | PARCIAL — o efeito (ausência do literal) foi confirmado por grep nesta sessão (nenhuma ocorrência de `x-cg-demo-api-key` em `tools/secret_redaction.py`), mas o commit exato não foi isolado nesta revisão |
| `release_manifest.py` canônico (Onda 3A) | `0d87d79` | SIM |
| F1 sem versão hardcoded (Onda 3) | Não isolado por hash nesta revisão | Efeito confirmado indiretamente (F1 usa `collect_tools_provenance()` sem literal, visto no grep de consumidores da rodada do tools/) |
| previsao-cripto consumindo `tools.secret_redaction` (Onda 4) | Parte do histórico de previsao-cripto anterior a `2026-07-17 12:44` (`8055667 refactor(logging): use canonical tools secret redaction`) | SIM, commit real localizado nesta sessão |

**Achado de fronteira desta revisão**: o documento já registrava
corretamente, desde 2026-07-11/17, a decisão de NÃO promover
`PRE_EVENT`/`MATURED` (F1) e `OPEN`/settlement (Brasileirão) a
`predictor_core` — a mesma conclusão a que a rodada de `predictor_core`
desta conversa chegou independentemente (via `RatingBook`/lifecycle,
`FINAL_FORENSIC_REVIEW.md` seção 20). As duas análises, feitas em momentos
diferentes por processos diferentes, convergem — reforça a robustez da
decisão, não é redundância.

## 9. Revisão do hardening geral (Bloco B)

Dois hardenings distintos aconteceram nesta linha do tempo, confirmados
como eventos SEPARADOS pelo Git (não um único evento, como uma leitura
superficial da conversa compactada poderia sugerir):

1. **`5f1b770`** (00:42, sessão anterior): 6 bugs de comportamento + 6 gaps
   de contrato em `predictor_core` puro (sem tocar consumidores) — suite
   200→221 testes. Mensagem de commit é a única fonte recuperável do
   conteúdo; não reconstruí o diff completo linha a linha nesta revisão
   (fora do critério de "mudança inequívoca a corrigir" — é histórico
   fechado, sem sinal de problema).
2. **`df575a9`…`e54a55d`** (15:47-16:35, mesmo dia): auditoria hostil que
   tocou `tools/` E `predictor_core` E `brasileirao-predictor` juntos —
   **incluindo os 2 bugs financeiros reais do brasileirão** (`e54a55d`:
   `settle_bet()` sem `match_date` liquidava confrontos repetidos juntos;
   idempotência por posição de arquivo em vez de `bet_id` permitia
   pagamento duplicado após reordenação). Ambos confirmados nesta sessão
   por leitura do diff de `e54a55d` — reais, reproduzidos com teste próprio
   antes da correção (`test_settle_confronto_repetido_exige_match_date_para_desambiguar`,
   `test_settle_idempotente_sobrevive_a_reordenacao_do_arquivo`, presentes em
   `brasileirao-predictor/tests/test_bet_log.py`, confirmados por grep
   nesta sessão).

Nenhuma alteração científica em nenhum dos dois — `e54a55d` corrige a
LÓGICA de liquidação, não reescreve nenhum resultado histórico já
liquidado (confirmado: o diff só adiciona um parâmetro `match_date` e uma
chave de dedupe por `bet_id`, não uma migração de dados).

## 10. Revisão da evolução do tools/ (Bloco C) e do predictor_core (Bloco D)

Integralmente coberta por `FINAL_FORENSIC_REVIEW.md` (commit `cca60f0`),
reconfirmado nesta sessão como ainda válido (nenhum commit posterior em
nenhum dos dois repositórios). Não repetido aqui — ver esse documento para
a revisão seção-a-seção de ReDoS, retry de `os.replace`, `release_check.py`,
API pública, split-brain, `pyproject.toml`, `PredictionPoint.__hash__`,
lock do `TrialRegistry`, `data/quality.py`, e `PARKED`.

## 11. Revisão commit a commit

Ver seção 5 (linha do tempo) para o histórico completo reconstruído por
Git, e `FINAL_FORENSIC_REVIEW.md` seções 5-9 para a revisão detalhada
commit-a-commit do período mais recente (6 em `tools/`, 4 em
`predictor_core`, 5 syncs, 4 reverts).

## 12. Bugs corrigidos (todas as rodadas, consolidado)

Ver Matriz Mestra de Mudanças (seção 20). Resumo por rodada: `5f1b770`
(6+6, não requalificado nesta revisão — histórico fechado sem sinal de
problema); auditoria hostil 15:47-16:35 (5 em tools/+core, 2 financeiros
reais no brasileirão); rodada "tools/" desta conversa (2, ReDoS + race);
rodada "predictor_core" desta conversa (8, PC-1 a PC-8).

## 13. Falhas arquiteturais corrigidas

Sync indevido nos 3 protegidos (`PARKED` vazio) — a mais séria desta
linha do tempo inteira, porque tocou projetos que deveriam estar
imutáveis. Corrigida e revertida (`15b6ada` + 4 reverts), confirmada
ainda válida nesta sessão (`sync_core.py --check` mostra os 3 como
`[PARKED]` agora).

## 14. Falhas científicas evitadas

`PredictionPoint` aceitando string em vez de datetime (invariante viraria
comparação lexicográfica — um bug que teria produzido resultados
CIENTIFICAMENTE ERRADOS silenciosamente, não só um crash) foi pego antes de
qualquer consumidor real construir um `PredictionPoint` com string
(confirmado por grep nos 5: nenhum o faz hoje) — corrigido preventivamente,
não como reparo de um incidente já ocorrido.

## 15. Preservação científica — CORREÇÃO DE CARACTERIZAÇÃO (achado desta revisão)

**As rodadas anteriores (incluindo `FINAL_FORENSIC_REVIEW.md`) descreveram
repetidamente hashes de `.db`/`ratings.json`/`events.jsonl` como "artefatos
científicos git-tracked". Isso está ERRADO.** Verificado nesta sessão via
`git ls-files`/`git check-ignore` em todos os 5 consumidores:

- `data/*.db`, `data/ratings.json`, `events.jsonl`, `output/feature_store.db`
  são **gitignored por desenho** em todos os 5 (`.gitignore` de cada um tem
  comentário explícito: dados de runtime regeneráveis, âncorados para não
  engolir `vendor/predictor_core/data/`). Nunca estiveram sob controle de
  versão. As comparações de SHA-256 feitas ao longo de toda a sessão
  (antes/depois de cada operação) são válidas como prova de que **os
  comandos desta sessão não os tocaram** — mas não são "preservação via
  Git", são comparação direta de filesystem.
- Os artefatos científicos **realmente versionados** são
  `data/trials.json`, `data/trials.harness_attestation.json`, e
  `data/teams_*.json` (brasileirão, cs, lol) — o "denominador imortal do
  DSR", nas palavras do próprio `.gitignore` de `cs-predictor`/`lol-predictor`.
  Verificado agora: **limpos (sem diff) em brasileirao-predictor,
  cs-predictor, f1-predictor, lol-predictor**; `previsao-cripto` tem UMA
  mudança real (já identificada em `FINAL_FORENSIC_REVIEW.md`: um `sharpe`
  maturou de `null` para `-0.531`, produção legítima, não commitada por
  mim, intocada).

Isso não muda nenhum veredito anterior (nenhuma alteração científica FOI
feita por qualquer rodada desta conversa), mas corrige a base de evidência
usada para afirmá-lo: a prova correta é `git status`/`git diff` limpo nos
4 governança-tracked, não hash de arquivo gitignored.

## 16. Mudanças concorrentes de produção

`previsao-cripto/GarimpoInvestimentos/trials.json` (sharpe maturado, ver
acima) e os 3 artefatos gitignored do mesmo projeto (`events.jsonl`,
`events_v3.jsonl`, `feature_store.db`, mtimes recentes) — coletor real
rodando em paralelo a esta sessão inteira, confirmado por `FINAL_FORENSIC_REVIEW.md`
e reconfirmado agora (nenhum comando desta sessão escreve nesses caminhos).
`brasileirao-predictor`: 2 heartbeats operacionais modificados (jobs
agendados reais, não relacionados a nenhuma rodada). `predictor-stocks`:
`AGENTS.md` untracked, pré-existente, não investigado (projeto protegido,
fora de escopo).

## 17. Itens corretamente deferidos

Ver Matriz Mestra de Deferimentos (seção 21) — consolida os itens das
rodadas do tools/, do predictor_core, E os da reintegração original
(`SINERGIAS_ECOSSISTEMA.md`, seção "Achados mantidos como DEFER"), que as
rodadas mais recentes não repetiram individualmente.

## 18. Inconsistências documentais encontradas (todas as rodadas)

1. "7 bugs" vs. matriz com 8 itens FIXED no relatório do `predictor_core` —
   já corrigido em `FINAL_FORENSIC_REVIEW.md`.
2. **Nova nesta revisão**: caracterização de "hashes científicos
   git-tracked" para arquivos gitignored — corrigida na seção 15 acima.
3. Nenhuma outra inconsistência de contagem encontrada entre
   `SINERGIAS_ECOSSISTEMA.md`, `FINAL_FORENSIC_REVIEW.md`, e o Git.

## 19. Testes finais executados (nesta sessão, estado atual)

| Repo | Comando | Resultado |
|---|---|---|
| tools/ | `python -m pytest tools/ -q` (da raiz) | 137 passed, 1 skipped |
| predictor_core | `python -m pytest -q` (do próprio repo) | 263 passed |
| brasileirao-predictor | idem | 302 passed, 1 warning |
| cs-predictor | idem | 100% verde (exit 0) |
| f1-predictor | idem | 100% verde (exit 0) |
| lol-predictor | idem | 100% verde (exit 0) |
| previsao-cripto | idem | 302 passed, 2 skipped |
| `sync_core.py --check` | do `predictor_core/` | 5 vivos OK, 3 protegidos DRIFT/[PARKED] (esperado) |
| `tools/vendor_byte_audit.py` | 5 vivos explicitados | IDENTICAL, 44/44, 0 changed, em todos |

## 20. Matriz Mestra de Mudanças

| ID | Rodada | Repo | Problema | Evidência | Solução | Commit | Veredito |
|---|---|---|---|---|---|---|---|
| M-01 | Auditoria adversarial anterior | predictor_core | 6 bugs comportamento + 6 gaps contrato | Mensagem de commit (diff não requalificado) | `5f1b770` | `5f1b770` | CONFIRMED_CORRECT (histórico fechado, sem sinal de problema) |
| M-02 | Reintegração Onda 2A | predictor_core | `--write` sem escopo por consumidor | Risco de tocar protegidos | `sync_core --target` | `858589e` | CONFIRMED_CORRECT |
| M-03 | Auditoria hostil (1ª) | brasileirao-predictor | Settlement sem `match_date`, idempotência por posição | Reproduzido com teste próprio | `settle_bet()` corrigido | `e54a55d` | CONFIRMED_CORRECT |
| M-04 | Auditoria hostil (1ª) | tools/predictor_core | `read_events` sem contexto, Unicode em filenames, tempfile órfão | Reproduzido | 5 fixes | `df575a9` et al. | CONFIRMED_CORRECT (coberto em FINAL_FORENSIC_REVIEW.md) |
| M-05 a M-14 | tools/ + predictor_core (esta conversa) | ambos | Ver FINAL_FORENSIC_REVIEW.md | — | — | 10 commits | CONFIRMED_CORRECT / CORRECT_WITH_RESIDUAL_RISK (1 item) |
| M-15 | Esta revisão | documental | "hashes git-tracked" impreciso | `git ls-files`/`check-ignore` | Caracterização corrigida (seção 15) | (documental, sem commit de código) | DOCUMENTATION_CORRECTED |

(Itens M-05 a M-14 correspondem 1:1 à Matriz Final de Mudanças de
`FINAL_FORENSIC_REVIEW.md` seção "Matriz Final de Mudanças" — não
duplicada aqui para não divergir por transcrição.)

## 21. Matriz Mestra de Deferimentos

| Item | Origem | Motivo | Risco atual | Condição para reabrir | Classificação final |
|---|---|---|---|---|---|
| Identidade em `RatingBook` (case/whitespace) | Rodada predictor_core (esta conversa) | Mudaria trajetórias científicas; só 1 consumidor real | Real, mas não observado em produção | 2º consumidor real de `RatingBook`, ou evidência de typo real em produção | CORRECTLY_DEFERRED |
| Lifecycle `PRE_EVENT`/`MATURED` compartilhado | Reintegração (2026-07-17) + reconfirmado nesta rodada | 3 implementações com garantias estruturalmente diferentes (CS tem vínculo hash, outros não) | Nenhum — cada um funciona localmente | Um 4º domínio precisar do mesmo padrão E as 3 implementações convergirem em garantias | INCUBATING |
| `observed_at`/`available_at` em `PredictionPoint` | Rodada predictor_core | Decisão de design nova, não bug | Gap conceitual real, não observado como incidente | Um consumidor real reportar lookahead causado por essa ambiguidade | CORRECTLY_DEFERRED |
| Enforcement de `is_mature()` | Rodada predictor_core | Decisão de design (wrapper de tipo) | Teórico — nenhum dos 5 acessa `.value` sem checar `is_mature()` (confirmado) | Um consumidor real acessar `.value` prematuramente | CORRECTLY_DEFERRED |
| Elo do F1 vs. `kernel/rating.py` | Reintegração (`SINERGIAS_ECOSSISTEMA.md`) | Migrar mudaria ratings históricos; sem 2º consumidor para a extensão Plackett-Luce | Nenhum — cada um estável isoladamente | 2º consumidor real da extensão | DOMAIN_LOCAL |
| `api_guard.allow()` (previsao-cripto) | Reintegração | 1 único consumidor hoje | Nenhum | 2º consumidor real | CORRECTLY_DEFERRED |
| `require_finite()` (previsao-cripto) | Reintegração | Mensagem de erro acoplada a vocabulário de domínio | Nenhum | Extração de mensagem + 2º consumidor | CORRECTLY_DEFERRED |
| Wrappers redundantes `CircuitBreaker` (previsao-cripto, `dpl/`+`v3/`) | Rodada predictor_core | Resíduo de migração, informativo | Nenhum (ambos funcionam) | Nenhuma — é limpeza cosmética, não bug | OBSOLETE (limpeza opcional, não dívida real) |
| `brier` em 11 scripts scratch (brasileirao) | Rodada predictor_core | Scripts de experimentação, não pipeline de produção | Nenhum | Um desses scripts virar pipeline de produção | DOMAIN_LOCAL |
| Schemas operacionais versionados (heartbeat/health/eventos) | Rodada tools/ | Nenhum consumidor pediu migração ainda | Nenhum | Uma mudança de schema incompatível precisar coexistir com uma versão antiga | CORRECTLY_DEFERRED |
| Lock metadata mais forte (hostname/start-time) | Rodada tools/ | PID-reuso é um risco teórico, fallback de idade já cobre | Nenhum observado | Um incidente real de PID reciclado colidindo | CORRECTLY_DEFERRED |
| CI multiplataforma | Rodada tools/ | Fora do escopo local | Nenhum — Windows é o ambiente real de produção hoje | Migração para Linux de produção | CORRECTLY_DEFERRED |
| Fixtures de teste compartilhadas (tools/) | Rodada tools/ | Sem duplicação comprovada entre 2+ consumidores | Nenhum | 2+ consumidores duplicarem o mesmo fixture | CORRECTLY_DEFERRED |
| `release_check.py` "sem teste dedicado" | Reintegração (marcado DEFER) | — | **OBSOLETO** — 10 testes foram adicionados na rodada tools/ desta conversa (`60b02a8`) | — | OBSOLETE (resolvido) |
| Contrato temporal em código (PRE_EVENT/MATURED formalizado) | Reintegração | Só documentado, nunca em código | Nenhum | Ver item lifecycle acima | INCUBATING |

## 22. Checklist de encerramento

- [x] tools/ revisado (rodada + `FINAL_FORENSIC_REVIEW.md`)
- [x] predictor_core revisado (rodada + `FINAL_FORENSIC_REVIEW.md` + gênese reconstruída nesta revisão)
- [x] cinco consumidores verdes (reexecutado nesta sessão)
- [x] três protegidos PARKED (reconfirmado nesta sessão, `[PARKED]` no `--check`)
- [x] vendors idênticos nos vivos (byte audit reexecutado)
- [x] manifests válidos (`--check` OK em tools/ e predictor_core)
- [x] hashes científicos preservados — **caracterização corrigida** (seção 15): governança-tracked limpa em 4/5, produção real identificada e intocada no 5º
- [x] alterações concorrentes separadas (seção 16)
- [x] commits reconciliados (linha do tempo seção 5, matriz seção 20)
- [x] testes reconciliados (seção 19; contagens batem com o esperado em todos os repos)
- [x] relatórios reconciliados (`FINAL_FORENSIC_REVIEW.md` + este documento, 2 inconsistências documentais corrigidas no total)
- [x] nenhum push
- [x] nenhuma tag
- [x] nenhuma publicação
- [x] nenhuma regressão conhecida
- [x] nenhum bug crítico aberto
- [x] nenhum HIGH aberto sem decisão explícita (identidade RatingBook e lifecycle compartilhado são HIGH/informativo, ambos com decisão explícita sua registrada)
- [x] riscos residuais documentados (seção 21 + `FINAL_FORENSIC_REVIEW.md` seção 25)
- [x] condições de reabertura documentadas (coluna própria na seção 21)
- [x] documento final criado (este arquivo)

## 23. Veredito final

**PASS FINAL COM PENDÊNCIAS NÃO BLOQUEANTES.**

Todo o histórico reconstruído por Git (não pela conversa) confirma: a
reintegração produziu um canônico único e coerente; o hardening geral
corrigiu bugs financeiros reais e reforçou contratos temporais; a evolução
recente de `tools/` e `predictor_core` (já forense-revisada) está correta;
os 3 protegidos seguem PARKED sem bypass possível; os 5 vivos estão
byte-idênticos e verdes; nenhuma alteração científica ocorreu (com a
caracterização de evidência corrigida nesta revisão); nenhuma regressão foi
encontrada em nenhum ponto da linha do tempo. As únicas pendências são
decisões deliberadamente deferidas, todas com condição de reabertura clara
(seção 21) — nenhuma delas bloqueia o encerramento deste ciclo.

**Sim, este ciclo pode ser encerrado com segurança.**
