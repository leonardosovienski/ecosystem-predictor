# PENDÊNCIAS ABERTAS — lista canônica

Lista canônica de tudo que ainda não está encerrado no ecossistema, em
2026-07-20. Consolida `FINAL_FORENSIC_REVIEW.md`, `ECOSYSTEM_FINAL_CLOSURE.md`,
`AUDIT_DIRECTORY_RECONCILIATION.md` (leitura de `audit/`, 71 arquivos, auditoria
independente de 2026-07-15) e verificação direta desta rodada. Cada item usa
uma destas classificações, nunca misturadas:

`OPEN_SECURITY_INCIDENT` · `OPEN_BUG` · `BLOCKED_EXTERNAL_ACTION` ·
`OPEN_OPERATIONAL_GAP` · `OPEN_SCIENTIFIC_GAP` · `OPEN_DOCUMENTATION_GAP` ·
`SHARED_BUT_INCUBATING` · `DOMAIN_LOCAL` · `CORRECTLY_DEFERRED` ·
`NOT_CONFIRMED` · `REJECTED` · `RESOLVED_AND_VERIFIED`

**Bugs de código reais e não corrigidos: zero.** O único item que bloqueia
um veredito limpo é de segurança e requer ação humana fora do código
(seção 1).

---

## 1. Incidente de segurança

| ID | Item | Classificação | Evidência | Ação restante |
|---|---|---|---|---|
| SEC-1 | Chave da SerpAPI em texto plano em 5 logs históricos do previsao-cripto (`garimpo_fase1_20260713.log` a `_17.log`); mecanismo de prevenção já corrigido e verificado funcionando (log de 18/07 limpo; a única ocorrência estrutural nele é o próprio marcador `[REDACTED]` — o filtro interceptou um vazamento em produção). Reverificado em 2026-07-18 (rodada de evolução final do cripto) com varredura ampliada: todos os logs nunca catalogados (`garimpo.log`, `cron_*`, `v3_daily_*`, `watchdog.log`, `operations/*`) e os 3 JSONL de eventos = 0 segredos reais; contagem do log de 17/07 corrigida 114→**115** (total 231) | `BLOCKED_EXTERNAL_ACTION`, explicitamente **baixa prioridade** por decisão humana (2026-07-18) | `SECURITY_INCIDENT_SECRET_ROTATION.md` (documento completo, sanitizado) | Rotação da credencial no provedor + decisão sobre os 5 logs — **só ação humana, sem prazo definido**; logs deixados como estão (decisão explícita: manter, não sanitizar) |

## 2. Bugs de código abertos

Nenhum. Todo bug reproduzido em qualquer rodada (tools/, predictor_core,
brasileirao financeiro, trials, quality.py) foi corrigido e testado —
ver `FINAL_FORENSIC_REVIEW.md` e `ECOSYSTEM_FINAL_CLOSURE.md` para a
verificação independente de cada um.

**Atualização F1 2026-07-20:** quatro falhas reproduzidas foram encerradas
localmente: publicação de snapshot resistente a erro parcial/concorrência,
bloqueio e revalidação de maturação prematura, substituição integral de
resultado corrigido no replay e rejeição de NaN/Inf em ratings/parâmetros.
Cobertura de regressão em `f1-predictor/tests/`; suíte 152 verdes e CI local
3/3. Nenhum gate ou critério científico foi alterado. Bugs F1 abertos: zero.
Hardening final: replay só substitui resultado após validação integral do
lote; corrupção de identidade/posição/grid/DNF/pontos/pitstops e NaN/Inf
falha sem apagar a versão anterior. Resposta vazia permanece não destrutiva.

## 3. Gaps operacionais

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| OP-1 | Race de heartbeat concorrente no caminho "perdedor" do lock em `tools/operational_runner.py` | `RESOLVED_AND_VERIFIED` (2026-07-19, tools/ 1.3.1) | Perdedor não escreve mais no heartbeat compartilhado: SKIPPED vai para sidecar `<name>.skipped.json` (`skipped_heartbeat_path`) + event log serializado; heartbeat principal é exclusivo do dono do lock. Nenhum consumidor lia SKIPPED do heartbeat (grep nos 5 vivos). Teste de regressão `test_lock_loser_never_touches_winner_heartbeat`; suíte 138 verdes; commit `80eca1a` (branch `claude/tools-maintenance-evolution-927d8a`) |
| OP-2 | Lock do `TrialRegistry` não distingue PID reciclado do PID original | `CORRECTLY_DEFERRED` | Fallback de idade preserva a garantia original; PID-reuso cai no mesmo comportamento de antes da correção, não piora |
| OP-3 | Glossário formal de status científico/operacional (GO/NO-GO/REFUTADA/COMPROVADA/INCONCLUSIVA) recomendado por `audit/13_FINAL_VERDICT.md` (item B-02) nunca foi criado como documento único | `RESOLVED_AND_VERIFIED` | **Atualização 2026-07-19**: criado `GLOSSARIO_STATUS.md` na raiz (vereditos científicos, gates GO/NO-GO, classificações de pendência, processo de errata não destrutivo), consolidando o uso já consistente dos documentos existentes |
| OP-4 | Backup/retenção/restore testado para os bancos SQLite/FeatureStore de cada consumidor (`audit/` OQ-040) | `PARTIALLY_RESOLVED` | F1: rebuild offline determinístico verificado. CS: `src.backup_restore` cria snapshot consistente via API SQLite, inclui ratings/snapshots, manifesta SHA-256, verifica `integrity_check` e restaura somente em raiz nova; restore real confirmou 17.320 partidas. **Brasileirão (2026-07-20):** `src.backup_restore` cobre SQLite + ledgers H3/H5 + trials/atestado/times, usa backup online, SHA-256, rejeita adulteração e só restaura em raiz nova; roundtrip real confirmou `integrity_check=ok` e 1.165 partidas. **Cripto (2026-07-20):** `scripts/feature_store_backup.py` usa backup online SQLite, manifesto SHA-256, publicação/restore atômicos e recusa sobrescrita; roundtrip real confirmou `integrity_check=ok`, 6 tabelas e contagens idênticas. Segue aberto para os demais consumidores e para uma política humana comum de retenção/local externo. |
| OP-5 | Schemas operacionais (heartbeat/health/eventos JSONL) sem `schema_version` explícito | `CORRECTLY_DEFERRED` | Nenhum consumidor pediu migração incompatível ainda |
| OP-6 | CI multiplataforma (só Windows validado localmente) | `CORRECTLY_DEFERRED` | Ambiente real de produção hoje é Windows; sem publicação, sem CI remoto configurado em nenhum dos 10 repos |
| OP-8 | previsao-cripto: `cripto-watchdog-coleta` falhou 18-19/07 com `0x800710E0` (mesma causa da GarimpoFase1 em 12/07 — config de energia nunca alinhada); e o 2º gatilho 22:30 (triagem 16/07, item b) nunca tinha sido aplicado | `RESOLVED_AND_VERIFIED` | Ambos corrigidos em 2026-07-20 (`scripts/fix_task_power_watchdog.ps1` + `scripts/fix_task_watchdog_trigger.ps1`, executados elevados com aprovação do dono via UAC); confirmado `StartWhenAvailable=True`/`DisallowStartIfOnBatteries=False`/`StopIfGoingOnBatteries=False` e 2 gatilhos ativos (19:00 + 22:30) |
| OP-7 | previsao-cripto: SerpAPI (mesma credencial do SEC-1) esgotada desde 18/07 — **confirmado por e-mail do provedor (2026-07-20)**: plano free, 250/250 buscas do mês usadas, renova só em 2026-08-07 (depois da janela de decisão da H5, 28/07) | `RESOLVED_AND_VERIFIED` (mitigado; SerpAPI em si segue esgotada até 07/08, sem custo monetário) | Aplicado em 2026-07-20 por decisão explícita do dono: `NEWS_FALLBACK_PROVIDER=curated_rss` ligado dentro da H5 (não trial nova — justificativa no `HANDOFF.md`). No processo, achado e corrigido um bug real: `blockworks.co` (1 das 5 fontes) migrava com redirect 308 não seguido pelo cliente HTTP, derrubando toda chamada que hasheasse pra ela (`1f51618`, 2 testes novos). Verificado com chamada real: `ethereum` trouxe notícia via `curated_rss`. **Caveat**: cobertura por ativo é MENOR que a do SerpAPI (1 feed geral por hash, filtro por substring) — previsões seguirão aparecendo com `input_degradado=1` mesmo com o fallback ativo; isso é esperado, não é regressão. Rotacionar a chave (SEC-1) também restauraria 250 buscas novas na hora |

## 4. Gaps científicos

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| SCI-1 | `RatingBook` não normaliza identidade (case/whitespace) — `"Team A"` e `"team a "` viram entidades diferentes | `CORRECTLY_DEFERRED` | Normalizar mudaria trajetórias de rating futuras (mudança científica); só `f1-predictor` usa `RatingBook` diretamente hoje. Reabre com 2º consumidor real ou typo real observado em produção |
| SCI-2 | `PredictionPoint` não tem `observed_at`/`available_at` — sem checagem cruzada entre `predicted_at` e o `published_at` dos dados de entrada | `CORRECTLY_DEFERRED` | Gap de design, não bug reproduzido. Reabre com incidente real de lookahead reportado |
| SCI-3 | `is_mature()` é só informativo, sem enforcement técnico de acesso | `CORRECTLY_DEFERRED` | Nenhum dos 5 consumidores acessa `.value` sem checar `is_mature()` primeiro (confirmado por grep) |
| SCI-4 | Elo do F1 não usa `RatingBook` do core (K-factor combinado diferente) | `DOMAIN_LOCAL` | Migrar mudaria ratings históricos; sem 2º consumidor real da extensão Plackett-Luce |
| SCI-5 | Modo sombra do brasileirao-predictor (H3) ainda precisa de 100 picks liquidados (2/100 em 2026-07-20) antes de decidir viés OVER/UNDER, capturabilidade de odds e IC do ROI | `OPEN_SCIENTIFIC_GAP` | Infraestrutura fechada em 2026-07-20: novos registros têm predicted/kickoff exatos, turno, fonte, abertura/captura/fechamento bruto e custo da sombra explicitamente não aplicável; legados não são retropreenchidos. Governança científica normal — aguardar, não acelerar |
| SCI-6 | H8-F1 (choque estrutural de regulamento) segue com amostra insuficiente: `H8_REQUIRED_RACES=15`. **Correção 2026-07-20** (a formulação anterior confundia corridas disputadas com corridas válidas para H8 — exatamente o erro que o gate existe para prevenir): 10 corridas de 2026 já têm resultado no banco, mas são retropredição (R1-R10, o modelo roda depois do fato); **0 (zero)** têm o par PRE_EVENT→MATURED que a `snapshot-status` exige — o diretório `snapshots/` nunca foi criado, a coleta forward declarada em 2026-07-15 ainda não produziu nenhum snapshot real (falta um GP com quali real durante uma sessão de trabalho para criar o primeiro) | `OPEN_SCIENTIFIC_GAP` | Gate de decisão econômica corretamente fechado; reabre quando 2026 tiver ≥15 corridas com par PRE_EVENT→MATURED válido (`VALID_FOR_H8`), não 15 corridas disputadas |
| SCI-7 | Fase 1b via mercado: Polymarket público read-only operacional em CS/LoL. **LoL H4-R retrospectiva separada**: 177 partidas/28 competições, Brier Elo 0,4320 vs mercado 0,4023, diferença IC95% cruza zero; ROI shadow +10,57% em 116 sinais, IC95% [-11,82%; +33,70%] — `INCONCLUSIVA`, não substitui H4. H4 prospectiva segue em coleta automática com gate 50 partidas/30 dias/3 competições. CS também operacional prospectivamente. | `RESOLVED_SOURCE_AWAITING_SAMPLE` | LoL e CS: acumular amostra prospectiva sem analisar cedo nem fazer trading; retrospectiva serve para diagnóstico, não acelera passagem do tempo. |
| SCI-8 | Hipótese H5 (multi-juiz, previsao-cripto) em coleta, sem GO/NO-GO — janela de decisão original citada em `SINERGIAS_ECOSSISTEMA.md` como 28/07 | `OPEN_SCIENTIFIC_GAP` | Não deve ser refinada nem convertida em nova hipótese antes da janela por decisão de governança já registrada |

## 5. Capacidades incubadas / candidatas ao core (não promovidas)

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| INC-1 | Lifecycle `PRE_EVENT`/`MATURED` compartilhado — cs-predictor, f1-predictor, lol-predictor têm 3 implementações locais com garantias estruturalmente diferentes. **Reconciliado em 2026-07-20**: CS e F1 hasheiam o payload e vinculam `pre_event_payload_hash`; LoL vincula PRE_EVENT→MATURED por `prediction_id` e copia o registro, sem hash do payload PRE_EVENT. Portanto ainda não há equivalência semântica suficiente para promoção | `SHARED_BUT_INCUBATING` | Reabre quando um 4º domínio precisar do mesmo padrão E as 3 implementações convergirem em garantias |
| INC-2 | `shin_probabilities`, cliente `curl_cffi`+impersonate, `PlattCalibrator`, motor prequential, harness Brier+DM — listados como "candidatos ao core (roadmap de agosto)" em `SINERGIAS_ECOSSISTEMA.md`, cada um hoje duplicado em 2-3 domínios | `SHARED_BUT_INCUBATING` | Nenhuma promoção feita nesta rodada nem nas anteriores — decisão explícita de tratar como ciclo de trabalho próprio, separado de trabalho de domínio |

## 6. Dívidas técnicas / limpeza cosmética (sem risco, sem prazo)

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| DEBT-1 | Símbolos "acidentalmente públicos" em `tools/` (`content_hash`, `redact_mapping`, `build_manifest`, etc.) | `CORRECTLY_DEFERRED` | Classificados no README como internos-na-prática, não renomeados (decisão explícita: "apenas classificar") |
| DEBT-2 | 2 wrappers redundantes de `CircuitBreaker` (`dpl/` e `v3/`) em previsao-cripto | `CORRECTLY_DEFERRED` | Resíduo de migração, ambos funcionam, nenhum bug |
| DEBT-3 | 11 scripts de scratch em brasileirao-predictor reimplementam `brier` localmente em vez de importar do core | `DOMAIN_LOCAL` | Só scripts de experimentação, nunca pipeline de produção |
| DEBT-4 | `cs-predictor` tem rating Elo local (`ShrunkMapElo`) que não usa `RatingBook` | `DOMAIN_LOCAL` | Mecânica de shrinkage parece genuinamente específica do CS |
| DEBT-5 | Fixtures de teste compartilhadas em `tools/` não criadas | `CORRECTLY_DEFERRED` | Sem duplicação comprovada entre 2+ consumidores ainda |

## 7. Não objetivos (rejeitados deliberadamente)

| ID | Item | Classificação |
|---|---|---|
| REJ-1 | Instalação de `tools/` via `pip install` (build-system, entry points) | `REJECTED` — consumido via sys.path por todos os 5 vivos, declarar suporte não testado seria afirmação falsa |
| REJ-2 | Reconstrução estrutural / monorepo / fim do vendoring | `REJECTED` — `audit/13_FINAL_VERDICT.md`, custo comparativo nunca medido, risco de fazer supera prova de benefício |
| REJ-3 | Normalização automática de identidade dentro do `RatingBook` (`.strip().lower()` escondido no core) | `REJECTED` — mudaria ciência silenciosamente |

## 8. Fatos não confirmados (removidos de versões anteriores deste documento)

| ID | Alegação | Classificação | Motivo |
|---|---|---|---|
| NC-1 | "`predictor_core/incubating/`" como diretório real contendo `nullref`/`metrics`/`state_asof` | `NOT_CONFIRMED` | Diretório não existe; são módulos de produção normais em `measurement/` e `data/` |
| NC-2 | "S4U continuava pendente" no Cripto | `NOT_CONFIRMED` (na verdade `RESOLVED_AND_VERIFIED`) | `audit/39` já mostrava as 3 tarefas `Ready, S4U` em 2026-07-15; reconfirmado agora via `Get-ScheduledTask`: `LogonType=S4U` nas 3, `LastTaskResult=0` |
| NC-3 | "nba-predictor: renascimento com abordagem Four Factors" | `NOT_CONFIRMED` | Zero menção literal em qualquer lugar do workspace; `audit/54`/`45` mencionam apenas "fatores" genericamente no contexto do histórico negativo do NBA |

## 9. Itens resolvidos nesta rodada (verificados, não requerem mais atenção)

| ID | Item | Classificação | Evidência |
|---|---|---|---|
| RES-1 | Tarefa `GarimpoInvestimentos-ColetaDiaria` (legada) permanece desabilitada, sem risco de coleta duplicada | `RESOLVED_AND_VERIFIED` | `Get-ScheduledTask`: `State=Disabled`, reconfirmado agora |
| RES-2 | 3 tarefas agendadas do previsao-cripto (`GarimpoFase1`, `GarimpoV3Daily`, `cripto-watchdog-coleta`) rodando com sucesso, S4U correto | `RESOLVED_AND_VERIFIED` | `LastTaskResult=0` nas 3, execuções em 2026-07-17 22:00/21:30/19:00 |
| RES-3 | Mecanismo de redação de logs (SEC-1) funciona corretamente para o cenário do incidente | `RESOLVED_AND_VERIFIED` | Reproduzido com credencial sintética + confirmado por execução real de produção (log de 18/07 limpo) |
| RES-4 | `release_check.py` sem teste dedicado (achado original de `audit/13`, item B-atual) | `RESOLVED_AND_VERIFIED` | 10 testes adicionados na rodada tools/ desta sessão (`60b02a8`), reexecutados agora, passam |
| RES-6 | Rodada de identidade do cs-predictor (2026-07-19/20): `EloModel._elo` resolvia case-insensitive pelo primeiro hit do dict e devolvia silenciosamente a entidade errada quando organizações distintas diferem só pela caixa (reais na base: `LEO`/`Leo`, `CHAOS`/`Chaos`, `WINNERS`/`Winners`). Corrigido: caixa exata resolve, comparação flexível só quando única, ambíguo rejeita; `cs_snapshots._resolve` com a mesma preferência. Contrato estendido ao Top 30 e aliases com NFC + `casefold` e rejeição explícita de colisões. O replay que materializa ratings usa nomes exatos do banco e não estava exposto ao lookup. Base reverificada: 0 `match_id` duplicado; snapshots reais 2026 verificam | `RESOLVED_AND_VERIFIED` | Suíte cs-predictor 85→91→99 verdes, CI 3/3, testes de identidade/config/snapshots |
| RES-5 | Rodada hostil 2 do brasileirao-predictor (2026-07-18/19): 5 correções de robustez — Shin rejeita odds 0/negativa/NaN/Inf com erro claro; `_market_probs` ignora linhas-placeholder 1X2=1.0 do Sofascore (4 reais na base viravam p=⅓ fabricado); `sombra.settle` com dedupe intra-execução (pick duplicado não liquida 2×), CLV só com fechamento válido e recusa de linha O/U inteira; `record_result` rejeita placar negativo. B3b/B4 reconfirmados com seus testes. Nenhuma mudança científica | `RESOLVED_AND_VERIFIED` | Commit `ba0bd7d` (branch `claude/brasileirao-predictor-audit-11f575`), suíte 302→320 verdes, CI 5/5, vendor 44/44 byte-idêntico |
| RES-7 | Auditoria final do lol-predictor (2026-07-19/20): 12 correções/lacunas de robustez — as 6 do commit `d8e7fd2` mais NFC, persistência concorrente/atômica de ratings, colisão de nomes entre regiões, série incompleta com formato explícito, timestamps/horizontes inválidos e dedupe concorrente do lifecycle. Nenhum artefato de produção alterado; previsões congeladas intactas. Não restou pendência técnica local conhecida | `RESOLVED_AND_VERIFIED` | Branch `claude/lol-predictor-final-audit-db522d`; suíte 53→65→67→71 verdes, CI 3/3, smoke EWC 8/8, `tests/test_hostile_audit.py` |

| RES-8 | Evolução final do f1-predictor (2026-07-19): 4 correções de robustez — `update_ratings` rejeitava aliases duplicados que resolvem para a mesma identidade (antes colapsava silenciosamente com n inflado) e posição final < 1; `predict_race_with_grid` idem para o grid + `params_file` opcional; `create_pre_event_snapshot(root=...)` agora usa os MESMOS `fase2_params.json` que congela/hasheia (divergência latente de proveniência quando root != ROOT); `mature_snapshot` rejeita posição final duplicada; 3 strings de erro com mojibake corrigidas. Gate H8 confirmado fechado (`H8_REQUIRED_RACES=15`, 0 VALID_FOR_H8); gate de operação segue NO-GO. Nenhuma mudança científica | `RESOLVED_AND_VERIFIED` | Branch `claude/f1-predictor-final-audit-99f36c`, suíte 126→134 verdes, CI 3/3 |
| RES-9 | f1-predictor (2026-07-20): bug científico REAL corrigido — `is_dnf()` não reconhecia o status `"Lapped"` (convenção da Jolpica a partir de 2023 para "classificado, voltas atrás do líder", equivalente a `"+N Lap(s)"` só usado em 2022); 363 resultados reais (2023-2026, quase toda a janela de avaliação cega) estavam marcados DNF por engano, contaminando `finish_order` de TODO backtest e diretamente a feature de Reliability (H6-F1c = DNF rolling). Corrigido; banco reconstruído do cache local (offline, sem rede) e as 4 fases (`run_backtest.py`→`run_fase2.py`→`run_fase4.py`→`run_fase5.py`) reexecutadas do zero sem tocar em nenhum threshold/critério. **Os 9 vereditos permaneceram idênticos** — achado mais informativo: o peso ótimo de Reliability no dev caiu de `w_rel=1.0` para `w_rel=0.0` após a correção, sugerindo que parte do sinal aparente antes era artefato do próprio bug. DSQ/DNS revisados e mantidos como DNF (semântica correta, não é o mesmo caso). Gate H8 inalterado (0/15) | `RESOLVED_AND_VERIFIED` | Branch `claude/f1-predictor-final-audit-99f36c`, suíte 135→136 verdes, CI 3/3, tabela completa antes/depois em `f1-predictor/HANDOFF.md` |

| RES-10 | lol-predictor (2026-07-21): ingestão Oracle deixou de sobrescrever CSV raw diretamente. Cache condicional (ETag/Last-Modified/304), SHA, retry limitado, validação de conteúdo, snapshot imutável + ponteiro atômico e gate de frescor (192 h) agora bloqueiam serving sem dado confiável. | `RESOLVED_AND_VERIFIED` | Código e runbook locais em `lol-predictor/src/data/ingestion.py` e `docs/INGESTION_RESILIENCE.md`; testes hostis 200/304/429/5xx/timeout/HTML/schema/timestamp/interrupção/concorrência, suíte e CI locais verdes. Nenhuma mudança em tools/core. |

## 10. Estado historicamente preservado, sem ação necessária

- Branch `reintegracao-f1-ondas-2-3` em `f1-predictor`: commits redundantes preservados, não mesclados. **Verificado 2026-07-20**: `git diff main..reintegracao-f1-ondas-2-3` mostra só remoções (subconjunto estrito de `main` — vendor mais antigo, testes mais antigos); nenhum conteúdo exclusivo, confirma a nota original. **Achada também nesta verificação**: `claude/belgium-quali-gp-test-72bff2` (branch não catalogada antes), mesmo padrão — subconjunto estrito de `main`, ponta em `aae48a1` (antes da Fase 5/SELADO). Nenhuma ação tomada em nenhuma das duas (deletar branch é operação destrutiva fora do escopo desta auditoria); documentado para não serem confundidas com trabalho pendente real.
- 4 worktrees paralelos (`brasileirao-predictor`, `previsao-cripto`, `nba-predictor`, `wc-predictor-v2`) intocados.
- `predictor-stocks/AGENTS.md` untracked — pré-existente, também ausente da `main` remota; não commitado por não ser artefato desta linha de trabalho. **Atualização 2026-07-19**: o projeto foi REABERTO para pesquisa pelo operador (2026-07-18, H4/H5 pré-registradas e julgadas NÃO COMPROVADAS; vendor segue congelado em 1.3.0 e o nome permanece no set `PARKED` do sync como proteção de vendor) — ver `ECOSYSTEM_HANDOFF.md` seção "Projetos PARKED e o caso predictor-stocks".
- Bumps PATCH recomendados concluídos: `tools/` está em 1.3.1 (`2ed64e4`)
  e `predictor_core` em **1.3.2-ga-20260720** (`969cad5`). O core está
  publicado e sincronizado com `origin/main`; tools permanece com 2 commits
  locais ainda não publicados. Sem tags. **Atualização 2026-07-19**: push
  realizado a pedido do operador em `previsao-cripto` (`af39a89..d4706d4`)
  e `predictor-stocks` (até `5132a1c`).

## Resumo por severidade

- **Incidente de segurança aberto**: 1 (SEC-1) — bloqueado por ação humana externa
- **Bugs de código abertos**: 0
- **Gaps operacionais**: 1 aberto, parcialmente coberto (OP-4 backup — F1, CS e previsao-cripto verificados em 2026-07-20; demais consumidores e política comum de retenção seguem abertos) + 3 corretamente deferidos (OP-2, OP-5, OP-6); OP-1 resolvido em 2026-07-19 (tools/ 1.3.1, sidecar de SKIPPED); OP-3 resolvido em 2026-07-19 (`GLOSSARIO_STATUS.md`); OP-7/OP-8 resolvidos em 2026-07-20 (previsao-cripto)
- **Gaps científicos**: 4 abertos (SCI-5, SCI-6, SCI-7, SCI-8), governança normal de pesquisa em andamento — nenhum é bug, todos aguardam amostra/janela por design; SCI-6 corrigida em 2026-07-20 (contagem estava desatualizada e confundia corridas disputadas com maturação forward válida — 10 disputadas, 0 `VALID_FOR_H8`)
- **Capacidades incubadas**: 2
- **Dívidas técnicas**: 5, todas deferidas conscientemente
- **Não objetivos**: 3
- **Fatos não confirmados**: 3
- **Resolvidos nesta rodada**: 4 (+ RES-5/RES-6/RES-7 em rodadas de auditoria subsequentes de brasileirão, cs e lol; RES-8/RES-9 na evolução final do f1-predictor)
