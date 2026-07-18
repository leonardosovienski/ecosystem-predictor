# AUDIT_DIRECTORY_RECONCILIATION.md

Reconciliação de `audit/` (64 arquivos `.md` + 6 arquivos `.json` sidecar,
70 arquivos no total; diretório não versionado pelo Git — coberto pela
regra `*/` do `.gitignore` do repositório de governança da raiz, mais o
subdiretório `task_backups/` com os XML pré-A04 do Scheduler). `audit/` é
uma auditoria independente e anterior a todo o ciclo coberto por
`FINAL_FORENSIC_REVIEW.md` e `ECOSYSTEM_FINAL_CLOSURE.md` — datada de
2026-07-15, dois dias antes das rodadas de reintegração, hardening,
`tools/` e `predictor_core` revisadas em rodadas anteriores desta sessão.

## Status desta rodada

`AUDIT_INDIVIDUAL_REVIEW_COMPLETE = true`
`NEW_FINDINGS = 0`

## Metodologia desta reconciliação (revisada)

Ao contrário da reconciliação anterior (que se apoiava majoritariamente em
`AUDIT_STATE.md`/`OPEN_QUESTIONS.md`/documentos-síntese e classificava a
maior parte dos 64 arquivos como "via síntese"), esta rodada leu **os 64
arquivos `.md` individualmente e por completo**, verbatim, um a um — não
apenas os documentos-síntese. Os 6 arquivos `.json` (`26`, `27`,
`28_F1_RECONCILIATION`, `44`, `55`, `60A`) são artefatos de dados
estruturados, sidecar de relatórios `.md` já lidos integralmente; foram
inspecionados quanto à estrutura/conteúdo (não recontam achados novos além
do que seus `.md` correspondentes já narram em prosa) e por isso não
recebem linha própria na matriz — estão referenciados junto do `.md`
irmão.

**Constraint de segurança respeitado**: os três (na verdade cinco, escopo
ampliado por `SECURITY_INCIDENT_SECRET_ROTATION.md`) logs históricos
potencialmente contaminados (`garimpo_fase1_2026-07-13.log` a
`_17.log`) **não foram abertos** nesta leitura. Eles não fazem parte do
diretório `audit/` (vivem em `previsao-cripto/logs/`) e continuam sujeitos
às regras de segurança já definidas — nenhuma exceção foi feita.

### Resultado da leitura individual

Nenhum dos 64 arquivos contém um fato, número, hash, veredito ou decisão
que contradiga o que já está consolidado em `PENDENCIAS_ABERTAS.md`,
`ECOSYSTEM_HANDOFF.md`, `ECOSYSTEM_FINAL_CLOSURE.md` ou
`SECURITY_INCIDENT_SECRET_ROTATION.md`. A leitura verbatim **confirmou e
enriqueceu** o quadro já reconciliado (mais detalhe operacional, mais
hashes, mais rastreabilidade de decisões intermediárias — por exemplo, os
códigos de saída exatos do wrapper, os hashes de cada vendor por etapa, e
o histórico completo de como o incidente de segredo foi descoberto,
mitigado e ainda aguarda rotação humana) — não revelou nenhum item que
precise ser adicionado a qualquer documento canônico. Por isso nenhuma
atualização foi feita em `PENDENCIAS_ABERTAS.md`, `ECOSYSTEM_HANDOFF.md`,
`ECOSYSTEM_FINAL_CLOSURE.md` ou `SECURITY_INCIDENT_SECRET_ROTATION.md`
nesta rodada — o gatilho condicional da tarefa ("se houver achados novos,
atualizar X") não foi acionado.

Dois itens do `audit/` merecem nota — não são achados novos, são
**auto-resoluções internas ao próprio processo de auditoria original**,
já registradas nos arquivos subsequentes da mesma numeração:
- `20A_CS_VENDOR_GIT_HYGIENE.md` (A-05A) encontrou 11 módulos do vendor CS
  fora do índice Git e corrigiu com `git add` — resolvido dentro do
  próprio `audit/`, antes do fechamento da etapa A-05.
- `58_GIT_RECONCILIATION.md` encontrou dois arquivos não rastreados no CS
  (`data/fixtures/stake_ranked_ep3.json`, `scripts/predict_matches.py`) e
  os classificou `PRESERVAR / REVISAR`; `60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md`
  (etapa posterior, também dentro de `audit/`) resolveu isso commitando-os
  em `71e01ab`. Não é uma pendência para esta rodada — já fechada dentro
  da linha do tempo do próprio `audit/`, em 2026-07-15.

## Achado mais importante do `audit/` (herdado, não novo): incidente de segurança

`38_CRYPTO_SECRET_INCIDENT_CLOSURE.md` documenta
`BLOCKED_PENDING_SECRET_ROTATION`. Detalhado, com escopo ampliado (5 logs,
não 3) e mecanismo de prevenção verificado em `SECURITY_INCIDENT_SECRET_ROTATION.md`
em rodada anterior desta sessão. Rotação continua pendente de ação humana
por decisão explícita do usuário (prioridade baixa, ver
`ECOSYSTEM_HANDOFF.md`). Nenhuma mudança nesta rodada.

## Reconciliação de OPEN_QUESTIONS.md (78 questões) — mantida da rodada anterior, reconfirmada

A leitura individual dos 64 arquivos não alterou nenhuma das conclusões já
registradas na rodada anterior sobre as 78 questões (OQ-001 a OQ-078).
Ver detalhamento completo no histórico desta sessão / `PENDENCIAS_ABERTAS.md`.
As questões genuinamente ainda abertas continuam sendo: OQ-006, OQ-007/020/021/022/024/031
(WC), OQ-026, OQ-034-037, OQ-040, OQ-076 (F1 H8) e OQ-064/066/067/068
(segredo cripto, ver acima). Nenhuma questão nova foi identificada pela
leitura verbatim desta rodada.

## Matriz de arquivos — uma linha por arquivo (64 arquivos `.md`)

Todos datados 2026-07-15, exceto onde indicado. Coluna "Evidência" agora é
`leitura direta` para todos os 64 — sem exceção — nesta rodada.

### Bloco 00–04A — Constituição, inventário, fundação, projetos ativos/legados

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `00_AUDIT_CHARTER.md` | Carta/constituição da auditoria | 2026-07-15 | Hierarquia de evidência, taxonomia (FATO VERIFICADO/INFERÊNCIA FORTE/HIPÓTESE/RECOMENDAÇÃO/NÃO VERIFICADO/CONTRADIÇÃO DOCUMENTAL), severidade, "regra dos dois consumidores", condições de parada | Define o método usado em todos os 63 arquivos seguintes | Documento fundacional | `HISTORICAL_ACCURATE` — método ainda válido como referência | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |
| `01_WORKSPACE_INVENTORY.md` | Inventário do workspace | 2026-07-15 | 15 diretórios, 10 repos Git, fichas por projeto, 2 worktrees do `predictor_core` | Confirma 8 consumidores quantitativos; nota estado sujo pré-existente em cs/nba/wc e `AGENTS.md` não rastreado em stocks | Inventário inicial | `HISTORICAL_ACCURATE` — todos os 8 consumidores confirmados; estados sujos pré-existentes ainda existem em wc/nba/stocks (esperado, PARKED) | Nenhuma nova | Nenhuma | `ECOSYSTEM_HANDOFF.md` |
| `02_FOUNDATION_REPORT.md` | Relatório de fundação do `predictor_core` | 2026-07-15 | Catálogo de módulos, `PARKED = set()` já vazio em 2026-07-15, gap `sync_core --check` só compara agregado | Confirma que "wc desparkado" já era comentário no código em 03/07; contradições doc (blueprint vs. código, contagem 200 vs 196 testes) | Fundação | `HISTORICAL_ACCURATE` — o gap de checagem por agregado (não byte a byte) foi resolvido por `vendor_byte_audit.py`, criado dentro deste mesmo `audit/` (A-01) | Nenhuma | Contagem de testes 200 (doc) vs 196 (estático) — já era conhecida, não afeta hoje | `tools/vendor_byte_audit.py` |
| `03_ACTIVE_PROJECTS_REPORT.md` | Relatório dos projetos ativos | 2026-07-15 | Arquitetura/fluxo de dados de cripto, Brasil, F1, CS, LoL como eram em 2026-07-15 | Flags F1 "selado" (doc 07-12) vs. mudanças Git em 07-14 como contradição documental | Snapshot arquitetural | `HISTORICAL_ACCURATE` — a contradição F1 foi resolvida em `28C_F1_GIT_STATE_RECONCILIATION.md`, dentro do próprio `audit/` | Nenhuma | Já resolvida (ver `28C`) | `ECOSYSTEM_HANDOFF.md` |
| `04_LEGACY_AND_ARCHIVED_REPORT.md` | Relatório de legado e arquivados | 2026-07-15 | Stocks (H1 não comprovada), NBA (NO-GO), WC (estado contraditório — SHADOW.md diz PARKED, HANDOFF diz desparkado/dinheiro real) | WC classificado "não arquivável" — estado genuinamente não resolvido mesmo pelo audit original | Snapshot dos 3 protegidos | `CURRENT_SUPPORTING` — WC/Stocks/NBA hoje são tratados como PARKED/protegidos por decisão desta sessão, independentemente de terem sido "arquiváveis" tecnicamente; consistente com a decisão de não tocar | WC permanece com estado histórico ambíguo, mas isso é tratado por proteção (não investigação), não por resolução | WC: SHADOW.md vs HANDOFF.md — contradição documental pré-existente, nunca resolvida, fora do escopo (PARKED) | `ECOSYSTEM_HANDOFF.md` |
| `04A_DISCOVERY_CHECKPOINT.md` | Checkpoint de descoberta | 2026-07-15 | Reconciliação do erro de contagem "6→8 consumidores" do `01` | Confirma 8 consumidores; WC "estado não resolvido; não arquivável" | Checkpoint interno | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma nova | `ECOSYSTEM_HANDOFF.md` |

### Bloco 05–09A — Matrizes horizontais e recapitulação

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `05_CAPABILITY_MATRIX.md` | Matriz de capacidades | 2026-07-15 | Capacidades por consumidor, horizontal | Base para candidatos ao core | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `06_ARCHITECTURE_MATRIX.md` | Matriz de arquitetura | 2026-07-15 | Distribuição, resolução de vendor, paths absolutos | Base para decisões de topologia | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `07_SCIENTIFIC_MATRIX.md` | Matriz científica | 2026-07-15 | Protocolo/artefatos científicos por projeto | Nenhum resultado reexecutado | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `08_OPERATIONAL_MATRIX.md` | Matriz operacional | 2026-07-15 | Testes, configs, 9 tarefas do Scheduler; 4 falhas não zero, 3 sucessos, 1 desabilitada | Base para o hardening A-03 a A-06 | Matriz | `RESOLVED_AND_VERIFIED` — hardening implementado no próprio `audit/` (16-21) | Nenhuma | Nenhuma | `tools/operational_runner.py` |
| `09_EVOLUTION_MATRIX.md` | Matriz de evolução | 2026-07-15 | Trajetória/aprendizado por projeto | WC = "maior conflito de estado"; hipóteses refutadas ≠ descartáveis | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |
| `09A_CONSOLIDATED_RECAP.md` | Recapitulação consolidada | 2026-07-15 | 10 achados mais fortes das etapas 01-08 | Síntese, sem execução nova | Recap | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |

### Bloco 10–15 — Síntese cross-domain, conselho, red team, auditoria de integridade

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `10_CROSS_DOMAIN_SYNTHESIS.md` | Síntese cross-domain | 2026-07-15 | 14 oportunidades O-01 a O-14 classificadas | Nenhuma "remover" ou promoção incondicional | Síntese | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `11_ARCHITECTURE_COUNCIL.md` | Conselho de arquitetura | 2026-07-15 | 11 decisões D-01 a D-11 (FAZER AGORA/30/60-90/BACKLOG/NÃO FAZER/PRECISA EVIDÊNCIA) | Base do roadmap aprovado | Parecer do conselho | `CURRENT_SUPPORTING` — maioria executada nas rodadas seguintes | Nenhuma nova | Nenhuma | `13_FINAL_VERDICT.md` |
| `12_RED_TEAM.md` | Red team independente | 2026-07-15 | Ataque adversarial a cada decisão do Conselho | Nenhuma base para reconstrução/monorepo/remoção; "rigor aparente" não é benefício provado | Crítica adversarial | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `12A_COUNCIL_RED_TEAM_RECONCILIATION.md` |
| `12A_COUNCIL_RED_TEAM_RECONCILIATION.md` | Reconciliação Conselho × Red Team | 2026-07-15 | Ação reconciliada por D-01..D-11 | Maioria "aprovada como medição/gate", "não iniciar" ou "investigar" | Reconciliação | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `13_FINAL_VERDICT.md` |
| `14_VENDOR_BYTE_AUDIT.md` | Implementação A-01: auditoria byte a byte | 2026-07-15 | 8 vendors (escopo original, antes da reclassificação PARKED), todos idênticos, agregado `3445e37f43c458cc`, 44 arquivos | Ferramenta nova `tools/vendor_byte_audit.py` | Implementação | `RESOLVED_AND_VERIFIED` — reconfirmado nesta sessão (2026-07-18) nos 5 vivos; 3 PARKED têm drift esperado e correto | Nenhuma | Nenhuma | `tools/vendor_byte_audit.py` |
| `15_CORE_RUNTIME_PROVENANCE.md` | Implementação A-02: provenance runtime | 2026-07-15 | 8 consumidores, `core_provenance.py`, todos `MATCH` | Nota candidato residual: segundo `predictor_core` sempre em `sys.path` (ambiental, não é mismatch) | Implementação | `RESOLVED_AND_VERIFIED` | Risco residual de diagnóstico (path duplicado) — informativo, não bloqueante, nunca materializou em bug | Nenhuma | `tools/core_provenance.py` |
| `13_FINAL_VERDICT.md` | Veredito da fase documental original | 2026-07-15 | Classificação "EVOLUÇÃO INCREMENTAL"; roadmap A-01→D-03 | Condição de encerramento: "CONCLUÍDA como parecer documental" | Veredito formal | `CURRENT_SUPPORTING` — roadmap majoritariamente executado | B-02 (glossário formal GO/NO-GO) nunca criado — gap documental menor, não bloqueante | Nenhuma | `ECOSYSTEM_HANDOFF.md` |

### Bloco 16–21 — Hardening operacional (A-03 a A-06)

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `16_OPERATIONAL_HARDENING.md` | A-03 — hardening de Scheduler/watchdog | 2026-07-15 | `operational_runner.py`, `ecosystem_health.py` criados; 9 tarefas inventariadas | Health anterior mascarava falhas (aceitava log como sucesso); 4 falhas reais (`0x800710E0` etc.) preservadas, não mascaradas | Implementação | `RESOLVED_AND_VERIFIED` — runner/health em produção hoje | `0x800710E0` segue sem causa raiz diagnosticada (seria preciso Event Viewer/owner) | Nenhuma | `tools/operational_runner.py`, `tools/ecosystem_health.py` |
| `17_OPERATIONAL_POST_CYCLE_VALIDATION.md` | A-03B — validação pós-ciclo | 2026-07-15 | Janela de observação 07:49-07:51 UTC, somente leitura | **Achado do incidente de segredo pela primeira vez** (log H5 histórico com credencial em texto claro) | Validação | `BLOCKED_EXTERNAL_ACTION` (herdado) | Rotação humana pendente | Nenhuma | `SECURITY_INCIDENT_SECRET_ROTATION.md` |
| `18_SECRET_REDACTION.md` | A-03C — redação de segredos | 2026-07-15 | `tools/secret_redaction.py` criado; scan (não sanitize) de logs históricos: 3 logs com 29 ocorrências cada | Estado `BLOCKED_PENDING_SECRET_ROTATION` formalmente declarado | Implementação + bloqueio | `BLOCKED_EXTERNAL_ACTION`, baixa prioridade por decisão humana explícita (2026-07-18) | Rotação e decisão sobre os 5 logs (escopo ampliado depois) continuam pendentes | Nenhuma | `SECURITY_INCIDENT_SECRET_ROTATION.md` |
| `19_BRASILEIRAO_OPERATIONAL_MIGRATION.md` | A-04 — migração operacional do Brasileirão | 2026-07-15 | Duas tarefas (manhã/noite) migradas para `--task-name`; XML pré-A04 salvo em `audit/task_backups/` | 268+48 testes verdes; vendor idêntico; provenance MATCH | Implementação | `RESOLVED_AND_VERIFIED` — ciclos naturais já ocorreram desde então (confirmado em rodadas anteriores desta sessão, incluindo o crash não-bug de `sombra-noite` investigado e explicado por design self-healing) | Nenhuma | Nenhuma | `brasileirao-predictor/HANDOFF.md` |
| `19A_BRASILEIRAO_POST_CYCLE_VALIDATION.md` | A-04 — validação pós-migração (janela inicial) | 2026-07-15 | Observação 08:15 UTC, antes dos próximos ciclos naturais | `NOT_RUN` para ambos os turnos nesta janela — coerente, não é falha | Validação | `RESOLVED_AND_VERIFIED` (superada por ciclos reais posteriores) | Nenhuma | Nenhuma | `brasileirao-predictor/HANDOFF.md` |
| `20_CS_OPERATIONAL_MIGRATION.md` | A-05 — migração operacional do CS | 2026-07-15 | `atualiza_semanal.py` migrado, Scheduler não alterado | 56 testes operacionais verdes; suíte do projeto teve 1 falha (`test_vendor_manifest_files_are_tracked`) | Implementação + falha conhecida | `RESOLVED_AND_VERIFIED` — a falha de tracking foi corrigida na mesma etapa seguinte (`20A`) | Nenhuma | Nenhuma | `cs-predictor/HANDOFF.md` |
| `20A_CS_VENDOR_GIT_HYGIENE.md` | A-05A — higiene Git do vendor CS | 2026-07-15 | 11 módulos do vendor 1.3.0 fora do índice Git — corrigido com `git add`, validado em clone limpo (49 testes) | Causa raiz identificada e corrigida dentro do próprio `audit/` | Correção | `RESOLVED_AND_VERIFIED` | Alteração ficou staged, não commitada, ao final desta etapa — commitada em etapa posterior do mesmo `audit/` | Nenhuma | `cs-predictor/HANDOFF.md` |
| `21_LOL_OPERATIONAL_MIGRATION.md` | A-06 — migração operacional do LoL | 2026-07-15 | `atualiza_semanal.py` do LoL migrado; suporte a `PARTIAL` (exit 10) adicionado ao runner | 29+31+64 testes verdes; vendor idêntico | Implementação | `RESOLVED_AND_VERIFIED` | Nenhuma | Nenhuma | `lol-predictor/HANDOFF.md` |

### Bloco 25–28D — Relatórios reproduzíveis e F1

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `25_BRASILEIRAO_SHADOW_REPORT.md` | Relatório reproduzível do modo sombra do Brasileirão | 2026-07-15 | Leitor offline de `sombra_picks.jsonl`/`sombra_results.jsonl`; 3 picks, 0 maturados | Classificação `DADOS INSUFICIENTES` — não é NO-GO nem GO | Relatório H3 | `CORRECTLY_DEFERRED` — ainda amostra insuficiente hoje, marco é 100 picks liquidados | Amostra insuficiente (ainda) | Nenhuma | `brasileirao-predictor/HANDOFF.md` |
| `26_LOL_EWC_OPENING_PREDICTIONS.md` (+ `.json` sidecar) | EWC 2026 LoL: previsões de abertura | 2026-07-15 | 8 previsões BO1, Elo H1 puro, aliases verificados (AG.AL, MIBR.LOS) | Dado extraordinário, não achado de auditoria; hashes de ratings/DB preservados antes/depois | Dado/previsão | `HISTORICAL_ACCURATE` — dado histórico, não uma alegação operacional a reconciliar | Nenhuma | Nenhuma | dado vive no projeto LoL |
| `27_CS_STAKE_RANKED_EP3_PREDICTIONS.md` (+ `.json` sidecar) | Stake Ranked Episode 3: previsões CS | 2026-07-15 | 4 previsões BO3, Elo H1 + Platt H2 canônico | Dado extraordinário; branch ainda não mergeada na época (`23faba1`) | Dado/previsão | `HISTORICAL_ACCURATE` — branch já foi integrada por fast-forward em etapa posterior do mesmo `audit/` (`58`) | Nenhuma | Nenhuma | dado vive no projeto CS |
| `28A_F1_SNAPSHOT_RECONCILIATION.md` | F1 — reconciliação de snapshots e dados locais | 2026-07-15 | `retrodicao_2026()` reproduzida 2×, idêntica; R1-R9 `REPRODUCIBLE` mas `PARTIALLY_REPRODUCIBLE` quanto a proveniência temporal | Nenhum item local satisfaz papel de snapshot pré-corrida imutável | Reconciliação | `CORRECTLY_DEFERRED` — mesma limitação hoje (gate H8 fechado corretamente) | Snapshot pré-corrida datado continua ausente para R1-R9 (aceito — retropredição, não forward) | Nenhuma | `f1-predictor/HANDOFF.md` |
| `28B_F1_2026_RACE_MATRIX.md` | F1 — matriz canônica de corridas 2026 | 2026-07-15 | 22 corridas; 0 linhas `VALID_FOR_H8` sob critério estrito | R1-R9 `RETROPREDICTION_AVAILABLE`; R10-R22 `FUTURE_EVENT` | Matriz | `CURRENT_SUPPORTING` — hoje (2026-07-18) mais corridas maturaram naturalmente (ver `f1-predictor/HANDOFF.md` para contagem atual), mas o critério `VALID_FOR_H8` continua exigindo snapshot forward, não retropredição | Lacuna de 15 corridas `VALID_FOR_H8` continua | Nenhuma | `f1-predictor/HANDOFF.md` |
| `28C_F1_GIT_STATE_RECONCILIATION.md` | F1 — reconciliação do estado Git | 2026-07-15 | `main` e branch experimental no mesmo HEAD `19e3ec4`; 0 commits exclusivos | Resolve contradição doc "selado em 9415c7b" vs. realidade `19e3ec4` (patch sugerido, não aplicado nesta etapa) | Reconciliação Git | `RESOLVED_AND_VERIFIED` — `HANDOFF.md` do F1 foi corrigido em etapa posterior do mesmo `audit/` (`35`) | Nenhuma | Contradição doc já resolvida | `f1-predictor/HANDOFF.md` |
| `28D_F1_H8_BLOCKER_REPORT.md` | F1 — bloqueadores objetivos de H8 | 2026-07-15 | 4 bloqueadores objetivos listados; gate `NO-GO` mantido (não é novo veredito) | 0 de 9 retropredições válidas para H8; lacuna de 15 evidências temporais completas | Relatório de bloqueio | `CORRECTLY_DEFERRED` — gate continua fechado corretamente | Amostra forward completa (15 corridas) ainda pendente | Nenhuma | `f1-predictor/HANDOFF.md` |

### Bloco 34–36 — Coleta forward F1

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `34_F1_FORWARD_SNAPSHOT_DESIGN.md` | F1 — design de coleta forward imutável | 2026-07-15 | Contrato PRE_EVENT/MATURED, invariantes, elegibilidade `VALID_FOR_H8` (meta 15 artefatos) | Nenhuma mudança de modelo/parâmetros/banco | Design | `RESOLVED_AND_VERIFIED` — implementado na etapa seguinte | Nenhuma | Nenhuma | `f1-predictor/src/snapshots.py` |
| `35_F1_FORWARD_SNAPSHOT_IMPLEMENTATION.md` | F1 — implementação da cadeia forward de snapshots | 2026-07-15 | `src/snapshots.py` criado; testes cobrindo hash/overwrite/adulteração | `HANDOFF.md` corrigido quanto ao estado Git (de `28C`) | Implementação | `RESOLVED_AND_VERIFIED` | Nenhuma | Nenhuma | `f1-predictor/HANDOFF.md` |
| `36_F1_FORWARD_OPERATIONAL_RUNBOOK.md` | F1 — runbook operacional forward | 2026-07-15 | Procedimento manual pré/pós-corrida; envelope de exemplo não aplicado ao Scheduler | Próximo evento elegível: R10 Belgian GP, 2026-07-19 | Runbook | `CURRENT_SUPPORTING` — R10 já ocorreu ou está prestes a ocorrer (2026-07-19) na data desta reconciliação (2026-07-18); status exato de snapshot R10 deve ser consultado em `f1-predictor/HANDOFF.md` | Verificar se R10 recebeu snapshot PRE_EVENT antes da largada — fora do escopo de leitura desta rodada (não é papel do `audit/` reconciliar o presente) | Nenhuma | `f1-predictor/HANDOFF.md` |

### Bloco 37–44 — Cripto: estado, V3, H5, validação, veredito

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `37_CRYPTO_CURRENT_STATE.md` | Cripto — estado atual | 2026-07-15 | HEAD destacado `4fcfc31` = `main` = `origin/main`; 5 mudanças operacionais não commitadas; 272 testes verdes | Vendor idêntico; incidente de segredo permanece bloqueador | Estado | `RESOLVED_AND_VERIFIED` (Git) — HEAD normalizado para `main` em etapa posterior (`58`) | Incidente de segredo (herdado) | Nenhuma | `previsao-cripto/HANDOFF.md` |
| `38_CRYPTO_SECRET_INCIDENT_CLOSURE.md` | Fechamento do incidente de segredo cripto | 2026-07-15 | Origem, escopo e mitigação do incidente | `BLOCKED_PENDING_SECRET_ROTATION` | Fechamento formal | `BLOCKED_EXTERNAL_ACTION`, baixa prioridade | Rotação humana | Nenhuma | `SECURITY_INCIDENT_SECRET_ROTATION.md` |
| `39_CRYPTO_AUTOMATION_RECONCILIATION.md` | Reconciliação de automação cripto | 2026-07-15 | S4U já `Ready` em 2026-07-15 | Confirma que a automação Scheduler já estava correta antes do hardening | Reconciliação | `RESOLVED_AND_VERIFIED` — reconfirmado nesta sessão (2026-07-18) via `Get-ScheduledTask` | Nenhuma | Nenhuma | `previsao-cripto/HANDOFF.md` |
| `40_CRYPTO_V3_REPRODUCTION.md` | Cripto — V3 | 2026-07-15 | `v3-hmm-funding-oi-fr90` NO-GO preservado (BTC PSR 0,445, ETH líquido -1,11 bps) | CLI direto falhou por falta de `PYTHONPATH` (não é reprodução formal) | Reprodução parcial | `CORRECTLY_DEFERRED` — NO-GO não reaberto | Reprodução CLI formal não completada (limitação, não bug) | Nenhuma | `previsao-cripto/HANDOFF.md` |
| `41_CRYPTO_H5_RECONCILIATION.md` | Cripto — H5 multi-juiz | 2026-07-15 | Schema de `predictions` não cobre maturação/custo/retry completos | Classificação `CONTINUAR COLETA` | Reconciliação | `CORRECTLY_DEFERRED` — ainda coletando | Amostra/protocolo forward completo ainda pendente | Nenhuma | `previsao-cripto/HANDOFF.md` |
| `42_CRYPTO_OPERATIONAL_VALIDATION.md` | Cripto — validação operacional | 2026-07-15 | Não executada — credencial deve ser resolvida antes de qualquer ciclo | Status operacional `BLOCKED` | Bloqueio declarado | `BLOCKED_EXTERNAL_ACTION` (herdado) | Rotação humana | Nenhuma | `SECURITY_INCIDENT_SECRET_ROTATION.md` |
| `43_CRYPTO_SCIENTIFIC_VERDICT.md` | Cripto — veredito científico | 2026-07-15 | V3 NO-GO, H5 CONTINUAR COLETA, econômico NÃO VALIDADO, operacional BLOQUEADO | Nenhum GO científico ou recomendação financeira | Veredito | `CORRECTLY_DEFERRED` | Nenhuma nova | Nenhuma | `previsao-cripto/HANDOFF.md` |
| `44_CRYPTO_FINAL_READINESS.md` (+ `.json` sidecar) | Prontidão final do cripto | 2026-07-15 | "Tecnicamente PASS, operacionalmente BLOQUEADO" | Consolidação dos itens 37-43 | Veredito de prontidão | `CURRENT_SUPPORTING` — S4U hoje confirmado OK; incidente ainda aberto | Rotação humana | Nenhuma | `previsao-cripto/HANDOFF.md` |

### Bloco 45–55 — Inventário cross-domain final e vereditos

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `45_CROSS_DOMAIN_CAPABILITY_INVENTORY.md` | Inventário cross-domain definitivo | 2026-07-15 | Capacidades comprovadas por área (core/tools/WC/Brasil/F1/CS-LoL/cripto/Stocks/NBA) | Contratos temporais, fingerprints, readiness e verificação de artefatos são os únicos candidatos transversais reais, condicionados a segundo consumidor | Inventário | `HISTORICAL_ACCURATE` — nenhuma menção literal a "Four Factors" (confirmado por grep nesta e em rodada anterior); apenas "fatores"/"decomposição de fatores" genéricos | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `46_PROJECT_CAPABILITY_MATRIX.md` | Matriz projeto × capacidade | 2026-07-15 | 10 linhas (core, tools, WC, Brasil, F1, CS, LoL, Cripto, Stocks, NBA) × 5 colunas | Estado por projeto: MATURE/PROVEN, PARTIAL, FORWARD L4, BLOCKED, L2, REFUTED | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `47_SOURCE_TARGET_TRANSFER_MATRIX.md` | Matriz origem → destino | 2026-07-15 | 7 transferências candidatas (T01-T07) | Nenhuma "TRANSFERIR AGORA" incondicional; a maioria é "TESTAR EM SHADOW" ou "INCUBAR" | Matriz | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `48_FALSE_EQUIVALENCES.md` | Falsas equivalências rejeitadas | 2026-07-15 | 15 equivalências rejeitadas (Platt CS→LoL, Dixon-Coles fora de futebol, BO1=BO3, etc.) | Nenhuma reutilização por nome aceita sem prova semântica | Lista de rejeições | `HISTORICAL_ACCURATE` — confirmado consistente com a nota de sinergias (Platt CS✓/LoL✗) desta sessão | Nenhuma | Nenhuma | `SINERGIAS_ECOSSISTEMA.md` |
| `49_SHARED_GAPS.md` | Gaps compartilhados | 2026-07-15 | 7 gaps (PRE_EVENT/MATURED, freshness, alias, odds/CLV, readiness, tools Git, secret closure) | Prioridades P0-P2 atribuídas | Matriz de gaps | `CURRENT_SUPPORTING` — tools Git (P0) resolvido em `56`; secret closure (P0) ainda `BLOCKED_EXTERNAL_ACTION` | Secret closure (herdada) | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `50_CORE_CANDIDATES.md` | Candidatos ao core | 2026-07-15 | 7 itens classificados CORE READY/INCUBATING/CORE CANDIDATE/LOCAL BY DESIGN/TOOLS CANDIDATE | PredictionPoint/TrialRegistry/harness/bootstrap já são CORE READY | Classificação | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `51_TOOLS_CANDIDATES.md` | Candidatos a tools | 2026-07-15 | runner/redaction/heartbeat/JSONL/locks/timeout/health/byte-audit/provenance = TOOLS READY | `tools/` ainda sem Git próprio nesta etapa — P0 | Classificação | `RESOLVED_AND_VERIFIED` — `tools/` versionado em `56` | Nenhuma | Nenhuma | `tools/HANDOFF.md` |
| `52_CROSS_DOMAIN_EXPERIMENTS.md` | Experimentos mínimos | 2026-07-15 | 5 experimentos (E01-E05) com critério GO/NO-GO explícito | Todos exigem baseline local e rollback por remoção de adaptador | Desenho de experimentos | `HISTORICAL_ACCURATE` — nenhum executado ainda (correto, nenhum é obrigatório) | Nenhum destes experimentos foi executado — aceito, são candidatos futuros, não bloqueadores | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `53_CROSS_DOMAIN_PRIORITY_ROADMAP.md` | Roadmap cross-domain (máximo 12) | 2026-07-15 | 12 itens priorizados P0-P4 | Nada de modelo novo/monorepo/pacote publicado no roadmap | Roadmap | `CURRENT_SUPPORTING` — itens P0 (tools Git, rotação segredo) parcialmente concluídos (tools sim, segredo não) | Rotação de segredo (P0, item 2) ainda pendente | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `54_PROJECT_FINAL_ROLES.md` | Papel final de cada projeto | 2026-07-15 | Tabela "papel/força/lacuna/origem/próxima ação" por projeto | Base da tabela usada em `ECOSYSTEM_HANDOFF.md` | Síntese de papéis | `CURRENT_SUPPORTING` | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |
| `55_CROSS_DOMAIN_FINAL_VERDICT.md` (+ `.json` sidecar) | Veredito final cross-domain | 2026-07-15 | 3 tabelas (papéis, transferências priorizadas, candidatos ao core) | Conclusão: **PRONTO COM BLOQUEIOS** — nenhum componente promovido nesta fase | Veredito | `CURRENT_SUPPORTING` — bloqueios (tools sem Git, segredo cripto) parcialmente resolvidos (tools sim) | Segredo cripto (herdado) | Nenhuma | `ECOSYSTEM_FINAL_CLOSURE.md` |

### Bloco 56–60A — Versionamento de tools, reconciliação Git, snapshots forward CS

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `56_TOOLS_VERSIONING_CLOSURE.md` | Fechamento — versionamento de tools | 2026-07-15 | `tools/` convertido em repo Git mínimo; versão `1.0.0`, commit `b24e283f` | 64 testes workspace, 45 em clone isolado; nenhum segredo real encontrado no scan | Fechamento | `RESOLVED_AND_VERIFIED` — `tools/` hoje está em versão mais recente (evoluções 1.1.0 registradas em `57`/`57A`, e posteriores nesta sessão) | Nenhuma | Nenhuma | `tools/HANDOFF.md` |
| `57_TOOLS_PROVENANCE_ROLLOUT.md` | Rollout de provenance de tools (Fase 2B) | 2026-07-15 | Brasil/LoL/F1 integrados a `tools_provenance`+`consumer_provenance`; CS e cripto `BLOCKED` (Git sujo) | Hashes de banco/rating/output invariantes antes/depois confirmados | Rollout parcial | `RESOLVED_AND_VERIFIED` — CS foi integrado em etapa posterior (`60`); cripto segue bloqueado pelo incidente de segredo, não pela provenance | CS Git hygiene (resolvido em `60`); cripto (herdado) | Nenhuma | `tools/HANDOFF.md` |
| `57A_TOOLS_NATIVE_PROVENANCE.md` | Provenance nativa de tools 1.1.0 | 2026-07-15 | `tools/` evolui de `1.0.0` para `1.1.0`; algoritmo de hash baseado em blobs Git do índice (invariável entre clones) | Corrige falha de cálculo de hash dependente de normalização de fim de linha | Release | `RESOLVED_AND_VERIFIED` | Nenhuma | Nenhuma | `tools/HANDOFF.md` |
| `58_GIT_RECONCILIATION.md` | Reconciliação Git pós-Fase 2B | 2026-07-15 | HEAD normalizado para `main` em cripto/WC; F1 fast-forward; CS/Stocks/NBA classificados e preservados | 4 bloqueios explícitos listados (CS EP3, cripto segredo, WC/NBA vendor, Stocks 31 commits à frente) | Reconciliação estrutural | `SUPERSEDED` pela reconciliação de Git atual desta sessão — CS EP3 resolvido em `60`; WC/NBA/Stocks permanecem PARKED/protegidos (não investigados por decisão desta sessão, não por omissão) | Segredo cripto (herdado); WC/NBA/Stocks Git — fora do escopo por serem PARKED | Nenhuma | `ECOSYSTEM_FINAL_CLOSURE.md` |
| `60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md` | CS PRE_EVENT/MATURED: segundo consumidor temporal | 2026-07-15 | `src.cs_snapshots` criado; primeiro PRE_EVENT real capturado (Stake Ranked EP3: 3DMAX×HEROIC) | Estado `PARTIAL` — MATURED real ainda não existe; EP3 histórico resolvido via commit `71e01ab` | Implementação | `CURRENT_SUPPORTING` — segundo consumidor do contrato PRE_EVENT/MATURED confirmado; status de maturação deve ser consultado em `cs-predictor/HANDOFF.md` para o estado mais recente | MATURED real do primeiro evento — fora do escopo de leitura desta rodada | Nenhuma | `cs-predictor/HANDOFF.md` |
| `60A_CS_REAL_EVENT_INPUT.json` | Input do evento real (sidecar de `60`) | 2026-07-15 | JSON de entrada do evento Stake Ranked EP3 3DMAX×HEROIC | Dado estruturado, não achado | Dado | `HISTORICAL_ACCURATE` | Nenhuma | Nenhuma | `cs-predictor/HANDOFF.md` |

### Documentos de índice/estado (não numerados sequencialmente)

| Caminho | Título | Data | Escopo | Achados | Estado original | Estado atual | Pendências | Contradições | Sucessor |
|---|---|---|---|---|---|---|---|---|---|
| `AUDIT_STATE.md` | Estado persistente da auditoria | 2026-07-15 (atualizado incrementalmente) | Índice de todas as 25+ etapas de implementação (A-01 a A-06+ e além) | Todas as etapas registradas `CONCLUÍDA` | Estado vivo do processo | `CURRENT_SUPPORTING` — leitura integral confirmada em rodada anterior desta sessão | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |
| `OPEN_QUESTIONS.md` | 78 questões abertas numeradas | 2026-07-15 | OQ-001 a OQ-078, com estado por questão | Maioria endereçada por A-01→A-06; questões genuinamente abertas listadas acima | Registro de questões | `CURRENT_SUPPORTING` — reconciliado nesta e em rodada anterior; nenhuma questão nova | Ver lista de OQs ainda abertas (seção acima) | Nenhuma | `PENDENCIAS_ABERTAS.md` |
| `EVIDENCE_INDEX.md` | Índice de evidências | 2026-07-15 (ativo, EV-001 a EV-060) | Registro formal de toda evidência citada pelos 63 relatórios | Convenção de IDs `EV-###`, sequencial e imutável | Índice de evidência | `HISTORICAL_ACCURATE` — lido integralmente nesta rodada (primeira leitura verbatim completa) | Nenhuma | Nenhuma | `ECOSYSTEM_HANDOFF.md` |

## Artefatos sidecar `.json` (6 arquivos, não numerados como linhas próprias)

| Arquivo | Par `.md` | Natureza |
|---|---|---|
| `26_LOL_EWC_OPENING_PREDICTIONS.json` | `26_LOL_EWC_OPENING_PREDICTIONS.md` | Saída estruturada das 8 previsões BO1 — dado, não achado |
| `27_CS_STAKE_RANKED_EP3_PREDICTIONS.json` | `27_CS_STAKE_RANKED_EP3_PREDICTIONS.md` | Saída estruturada das 4 previsões BO3 — dado, não achado |
| `28_F1_RECONCILIATION.json` | `28A`-`28D_F1_*.md` | Resumo estruturado do estado de reconciliação Git/dados do F1 |
| `44_CRYPTO_FINAL_READINESS.json` | `44_CRYPTO_FINAL_READINESS.md` | Resumo estruturado de branch/hashes/estado de tarefas do cripto |
| `55_CROSS_DOMAIN_FINAL_VERDICT.json` | `55_CROSS_DOMAIN_FINAL_VERDICT.md` | Resumo estruturado do veredito final (papéis/prioridades/candidatos) |
| `60A_CS_REAL_EVENT_INPUT.json` | `60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md` | Input real do primeiro evento PRE_EVENT do CS |

Nenhum destes 6 arquivos contém conteúdo além do que seu `.md` correspondente
já narra em prosa — foram inspecionados (estrutura e trechos) para confirmar
essa equivalência, não para extrair achados adicionais.

## `task_backups/` (não é parte dos 64 arquivos de auditoria)

Subdiretório com os XML exportados pré-A04 do Scheduler
(`brasileirao-sombra-manha.pre-a04.xml`, `brasileirao-sombra-noite.pre-a04.xml`)
e `HEALTH_TASKS.1.2.3.json`, mencionados em `19_BRASILEIRAO_OPERATIONAL_MIGRATION.md`
como material de rollback. Não são documentos de auditoria e não recebem
linha própria na matriz.

## Logs excluídos desta leitura por regra de segurança

Os logs históricos potencialmente contaminados
(`previsao-cripto/logs/garimpo_fase1_2026-07-13.log` a `_17.log`) **não
foram abertos** nesta rodada nem em nenhuma rodada anterior desta sessão.
Eles não pertencem a `audit/` e continuam sujeitos às regras de segurança
já definidas em `SECURITY_INCIDENT_SECRET_ROTATION.md`.

## Limitação desta reconciliação (atualizada)

Diferente da rodada anterior — que classificava a maioria dos arquivos como
"via síntese" — esta rodada leu **todos os 64 arquivos `.md` verbatim, um a
um**. A limitação remanescente é apenas metodológica, não de cobertura: a
leitura individual confirma o *conteúdo textual* de cada arquivo contra os
documentos canônicos atuais, mas não reexecuta os testes/pipelines/hashes
que cada etapa do `audit/` original já documentou como tendo passado
naquele momento (2026-07-15) — isso já foi feito, de forma independente,
pelas rodadas de hardening/hostile-audit desta sessão em datas posteriores,
e está refletido em `PENDENCIAS_ABERTAS.md`/`ECOSYSTEM_HANDOFF.md`.
