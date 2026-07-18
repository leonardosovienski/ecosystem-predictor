# AUDIT_DIRECTORY_RECONCILIATION.md

Reconciliação de `audit/` (71 arquivos, não versionado pelo Git — coberto
pela regra `*/` do `.gitignore` do repositório de governança da raiz) contra
o estado atual do workspace. `audit/` é uma auditoria independente e
anterior a todo o ciclo coberto por `FINAL_FORENSIC_REVIEW.md` e
`ECOSYSTEM_FINAL_CLOSURE.md` — datada de 2026-07-15, dois dias antes das
rodadas de reintegração/hardening/tools/predictor_core revisadas
anteriormente.

## Metodologia desta reconciliação

Dado o volume (71 arquivos), a leitura priorizou os documentos que já
consolidam as conclusões de blocos inteiros de trabalho — `AUDIT_STATE.md`
(estado persistente, resume cada etapa 0-25), `OPEN_QUESTIONS.md` (78
questões abertas numeradas, com estado por questão), `13_FINAL_VERDICT.md`
(veredito formal da fase documental original), e os documentos "final" por
domínio (`44_CRYPTO_FINAL_READINESS.md`, `54_PROJECT_FINAL_ROLES.md`,
`45_CROSS_DOMAIN_CAPABILITY_INVENTORY.md`) — complementados por leitura
integral do documento de maior severidade (`38_CRYPTO_SECRET_INCIDENT_CLOSURE.md`)
e greps direcionados nos demais para confirmar/refutar afirmações
específicas. Isto **não** é uma leitura linha-a-linha dos 71 arquivos
individuais (00 a 60A) — é uma reconciliação pelos documentos-síntese, que
por desenho do próprio processo de auditoria original (etapas numeradas,
cada uma produzindo um relatório e sendo absorvida pela próxima) já
recapturam o conteúdo das etapas intermediárias. Registrado aqui como
limitação de escopo explícita, não como alegação de cobertura total.

## Achado mais importante: incidente de segurança

`38_CRYPTO_SECRET_INCIDENT_CLOSURE.md` documenta `BLOCKED_PENDING_SECRET_ROTATION`
— não estava em `FINAL_FORENSIC_REVIEW.md`, `ECOSYSTEM_FINAL_CLOSURE.md`, nem
na primeira versão de `PENDENCIAS_ABERTAS.md`. Detalhado, ampliado (escopo
real é 5 logs, não 3) e verificado nesta rodada em
`SECURITY_INCIDENT_SECRET_ROTATION.md`.

## Reconciliação de OPEN_QUESTIONS.md (78 questões)

A maioria das 78 questões (OQ-001 a OQ-078) foi endereçada pelas
implementações A-01 a A-06 registradas no próprio `AUDIT_STATE.md`, que
correspondem diretamente às capacidades hoje presentes em `tools/`
(`vendor_byte_audit.py` → OQ-009/013; `core_provenance.py` → OQ-032;
`operational_runner.py` → OQ-014/038/048/060; `secret_redaction.py` →
OQ-064/066/067) — confirmado por leitura cruzada com o código atual e com
`FINAL_FORENSIC_REVIEW.md`. As questões que seguem genuinamente abertas,
por não terem contrapartida em nenhum documento ou commit posterior:

| Questão | Estado em `audit/` | Estado atual (reconciliado) |
|---|---|---|
| OQ-006 (projetos sem Git) | ABERTA | NÃO INVESTIGADO nesta rodada — fora do escopo de tools/predictor_core/5 consumidores/3 protegidos |
| OQ-007/OQ-020/OQ-021/OQ-022/OQ-024/OQ-031 (estado do WC, `../wc-predictor` externo) | ABERTA | NÃO INVESTIGADO — WC é PARKED; regra desta rodada é não tocar/investigar além de confirmar PARKED |
| OQ-026 (calibradores locais vs. `calibration` do core) | ABERTA | NÃO REAVALIADO nesta rodada — sem evidência de bug, permanece `DOMAIN_LOCAL` por decisão já tomada em rodadas anteriores |
| OQ-034/035/036/037 (potência estatística, testes de futilidade, unidade de bootstrap, pré-registro) | ABERTA | NÃO REAVALIADO — são questões de metodologia científica de pesquisa em andamento, não bugs de engenharia |
| OQ-040 (backup/retenção de SQLite) | ABERTA | NÃO IMPLEMENTADO — nenhum consumidor pediu, sem evidência de perda de dados real |
| OQ-041 (CI/workflows externos) | ABERTA | Confirmado nesta e em rodadas anteriores: nenhum CI remoto configurado em nenhum dos 10 repos |
| OQ-064/066/067/068 (segredo, rotação) | CRÍTICA/BLOCKED | Ver `SECURITY_INCIDENT_SECRET_ROTATION.md` — escopo ampliado, mecanismo de prevenção verificado funcionando, rotação ainda pendente de ação humana |
| OQ-074/075 (H3 Brasileirão: CLV real, ledger com `predicted_at`) | ABERTA | Ver seção Brasileirão de `PENDENCIAS_ABERTAS.md` — ainda depende de amostra madura |
| OQ-076 (snapshot imutável pré-corrida F1 para H8) | ABERTA/CRÍTICA (científica, não segurança) | Confirmado ainda aberta — `H8_REQUIRED_RACES=15`, só 9 corridas maturadas (2026-07-17); gate permanece fechado corretamente |

## Reconciliação de 13_FINAL_VERDICT.md (classificação "EVOLUÇÃO INCREMENTAL")

O roadmap aprovado (seção 8 daquele documento: A-01, A-02, B-01 a B-03,
C-01/C-02, D-01 a D-03) foi **executado em sua maior parte** pelas rodadas
subsequentes cobertas por `SINERGIAS_ECOSSISTEMA.md` e
`FINAL_FORENSIC_REVIEW.md`:
- A-01 (byte audit) → `tools/vendor_byte_audit.py`, confirmado hoje `IDENTICAL` nos 5 vivos.
- A-02 (provenance runtime) → `tools/core_provenance.py`.
- B-02 (glossário de status científico/operacional) → **não encontrado** um glossário formal; os termos GO/NO-GO/REFUTADA/COMPROVADA continuam usados de forma consistente mas sem um documento único que os defina — gap documental menor, não bloqueante.
- D-01/D-02 (contrato temporal, lifecycle) → investigado nas rodadas de `predictor_core` desta sessão; decisão consistente com o veredito original do audit ("permanece local", `SHARED_BUT_INCUBATING`).
- D-03 (comparação vendor vs. pacote) → não executado; `tools/pyproject.toml` documenta explicitamente que instalação via pacote não é objetivo atual — consistente com a recomendação de adiar D-03 até haver medição.

## Reconciliação por projeto (44_CRYPTO_FINAL_READINESS, 54_PROJECT_FINAL_ROLES)

Já refletida nas seções específicas de `PENDENCIAS_ABERTAS.md` (versão
atualizada desta rodada). Nenhuma contradição material encontrada entre o
veredito de 2026-07-15 ("Cripto tecnicamente PASS, operacionalmente
BLOQUEADO...") e o estado atual — exceto que o bloqueio operacional
(segredo) tem escopo maior do que documentado então, e o mecanismo de
redação, que na época ainda não existia, agora existe e foi verificado.

## Claims não confirmadas nesta reconciliação

- "Four Factors" para nba-predictor: `audit/54_PROJECT_FINAL_ROLES.md` e
  `45_CROSS_DOMAIN_CAPABILITY_INVENTORY.md` mencionam apenas "fatores"
  genericamente ("decomposição de fatores", "nova premissa") no contexto do
  histórico negativo do NBA — não há menção específica a "Four Factors"
  (a métrica de Dean Oliver) em lugar nenhum do `audit/` nem do
  `nba-predictor` (grep zero). Classificado `NOT_CONFIRMED`.
- `predictor_core/incubating/`: não existe tal diretório; não encontrado em
  nenhum arquivo de `audit/` como nome literal. Classificado `NOT_CONFIRMED`.

## Matriz de arquivos (64 arquivos `.md`/`.json`, todos datados 2026-07-15)

Agrupados por bloco temático do próprio processo de auditoria original
(numeração sequencial 00→60A). Coluna "Evidência" indica se o arquivo foi
lido integralmente nesta reconciliação (`leitura direta`) ou reconciliado
via os documentos-síntese que o consolidam (`via síntese` — não lido
verbatim, ver limitação declarada abaixo).

| Arquivos | Escopo | Achado principal | Estado atual | Evidência | Sucessor |
|---|---|---|---|---|---|
| `00_AUDIT_CHARTER.md`, `01_WORKSPACE_INVENTORY.md` | Constituição e inventário do workspace | Define escopo/população da auditoria | `HISTORICAL_ACCURATE` | via síntese (`AUDIT_STATE.md`) | `ECOSYSTEM_HANDOFF.md` |
| `02_FOUNDATION_REPORT.md` a `04A_DISCOVERY_CHECKPOINT.md` | Fundação, projetos ativos/legados, checkpoint | Divergências documentais registradas, sem bloqueio técnico | `HISTORICAL_ACCURATE` | via síntese | `ECOSYSTEM_HANDOFF.md` |
| `05_CAPABILITY_MATRIX.md`, `06_ARCHITECTURE_MATRIX.md`, `07_SCIENTIFIC_MATRIX.md`, `08_OPERATIONAL_MATRIX.md`, `09_EVOLUTION_MATRIX.md`, `09A_CONSOLIDATED_RECAP.md` | Matrizes de capacidade/arquitetura/ciência/operação | Base do roadmap A-01..D-03 | `HISTORICAL_ACCURATE` | via síntese | `PENDENCIAS_ABERTAS.md` (itens sobreviventes) |
| `10_CROSS_DOMAIN_SYNTHESIS.md`, `11_ARCHITECTURE_COUNCIL.md`, `12_RED_TEAM.md`, `12A_COUNCIL_RED_TEAM_RECONCILIATION.md` | Síntese, conselho arquitetural, red team | Nenhuma remoção aprovada; vendoring mantido "temporariamente" | `HISTORICAL_ACCURATE` | via síntese | `ECOSYSTEM_HANDOFF.md` |
| `13_FINAL_VERDICT.md` | Veredito da fase documental | Classificação "EVOLUÇÃO INCREMENTAL"; roadmap A-01→D-03 aprovado | `CURRENT_SUPPORTING` (roadmap majoritariamente executado nas rodadas seguintes) | **leitura direta** | `ECOSYSTEM_HANDOFF.md` |
| `14_VENDOR_BYTE_AUDIT.md`, `15_CORE_RUNTIME_PROVENANCE.md` | A-01/A-02: byte audit e provenance runtime | 8 vendors idênticos; 8 imports corretos | `RESOLVED_AND_VERIFIED` (reconfirmado 2026-07-18, só nos 5 vivos — os 3 PARKED têm drift esperado) | via síntese (`AUDIT_STATE.md`) | `tools/vendor_byte_audit.py`/`core_provenance.py` executados diretamente |
| `16_OPERATIONAL_HARDENING.md`, `17_OPERATIONAL_POST_CYCLE_VALIDATION.md` | A-03: runner/health operacional | H5/V3/watchdog ganham heartbeat; **achado do incidente de segredo** aqui pela primeira vez | `RESOLVED_AND_VERIFIED` (hardening) + incidente `BLOCKED_EXTERNAL_ACTION` | via síntese | `RUNBOOK_CRYPTO_AUTOMATION.md` |
| `18_SECRET_REDACTION.md`, `38_CRYPTO_SECRET_INCIDENT_CLOSURE.md` | A-03C: redação + fechamento do incidente | `BLOCKED_PENDING_SECRET_ROTATION` | `BLOCKED_EXTERNAL_ACTION`, baixa prioridade por decisão humana (2026-07-18) | **leitura direta** (ambos) | `SECURITY_INCIDENT_SECRET_ROTATION.md` |
| `19_BRASILEIRAO_OPERATIONAL_MIGRATION.md`, `19A_..._POST_CYCLE_VALIDATION.md` | A-04: Brasileirão no runner | Migração validada, aguardando ciclo natural | `RESOLVED_AND_VERIFIED` (ciclos naturais já ocorreram desde então) | via síntese | `brasileirao-predictor/HANDOFF.md` |
| `20_CS_OPERATIONAL_MIGRATION.md`, `20A_CS_VENDOR_GIT_HYGIENE.md` | A-05/A-05A: CS no runner + higiene de vendor | 11 arquivos do vendor CS fora do índice Git — corrigido | `RESOLVED_AND_VERIFIED` | via síntese | `cs-predictor/HANDOFF.md` |
| `21_LOL_OPERATIONAL_MIGRATION.md` | A-06: LoL no runner | Migração validada | `RESOLVED_AND_VERIFIED` | via síntese | `lol-predictor/HANDOFF.md` |
| `25_BRASILEIRAO_SHADOW_REPORT.md` | H3 shadow do Brasileirão | Amostra insuficiente (3 picks, 0 liquidados) na época | `CORRECTLY_DEFERRED` — ainda amostra insuficiente hoje (`PENDENCIAS_ABERTAS.md` SCI-5) | via síntese | `brasileirao-predictor/HANDOFF.md` |
| `26_LOL_EWC_OPENING_PREDICTIONS.*`, `27_CS_STAKE_RANKED_EP3_PREDICTIONS.*` | Previsões registradas (dados, não achados) | N/A — são dados, não relatório | `HISTORICAL_ACCURATE` | não lido (fora do escopo de achados) | dados vivem nos próprios projetos |
| `28A`-`28D_F1_*`, `28_F1_RECONCILIATION.json` | Reconciliação F1 2026, bloqueio H8 | 9/15 corridas maturadas, 0 válidas para H8 (sem snapshot pré-corrida datado) | `CORRECTLY_DEFERRED` (`PENDENCIAS_ABERTAS.md` SCI-6) | **leitura direta** (`AUDIT_STATE.md`, seção F1) | `f1-predictor/HANDOFF.md` |
| `34`-`36_F1_FORWARD_*` | Design/implementação/runbook de snapshots forward F1 | Implementado, aguardando 1º snapshot real | `RESOLVED_AND_VERIFIED` (snapshots forward existem e são usados hoje) | via síntese | `f1-predictor/HANDOFF.md` |
| `37_CRYPTO_CURRENT_STATE.md`, `39`-`43_CRYPTO_*`, `44_CRYPTO_FINAL_READINESS.*` | Estado, automação, V3, H5, verdict científico do cripto | "Tecnicamente PASS, operacionalmente BLOQUEADO" | `CURRENT_SUPPORTING` (S4U hoje confirmado OK, incidente ainda aberto) | **leitura direta** (39, 44) + via síntese (37, 40-43) | `previsao-cripto/HANDOFF.md` |
| `40_CRYPTO_V3_REPRODUCTION.md` | Reprodução V3 | NO-GO preservado | `CORRECTLY_DEFERRED` | via síntese | `previsao-cripto/HANDOFF.md` |
| `45`-`53_CROSS_DOMAIN_*` | Inventário, matriz de capacidade, transferência, falsas equivalências, gaps, candidatos ao core/tools, experimentos, roadmap | Base do que hoje é `PENDENCIAS_ABERTAS.md` seções 5-6 | `CURRENT_SUPPORTING` | via síntese (45, 54 lidos diretamente) | `PENDENCIAS_ABERTAS.md` |
| `54_PROJECT_FINAL_ROLES.md` | Papel final de cada projeto | Base da tabela "o que cada projeto ensina/recebe" | `CURRENT_SUPPORTING` | **leitura direta** | `ECOSYSTEM_HANDOFF.md` |
| `55_CROSS_DOMAIN_FINAL_VERDICT.*` | Veredito cross-domain | — | `HISTORICAL_ACCURATE` | via síntese | `ECOSYSTEM_FINAL_CLOSURE.md` |
| `56_TOOLS_VERSIONING_CLOSURE.md`, `57_TOOLS_PROVENANCE_ROLLOUT.md`, `57A_TOOLS_NATIVE_PROVENANCE.md` | Versionamento e rollout de provenance do tools/ | Base do `tools/` atual (1.3.0) | `RESOLVED_AND_VERIFIED` | via síntese | `tools/HANDOFF.md` |
| `58_GIT_RECONCILIATION.md` | Reconciliação Git da época | — | `SUPERSEDED` | via síntese | `ECOSYSTEM_FINAL_CLOSURE.md` (reconciliação atual) |
| `60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md`, `60A_CS_REAL_EVENT_INPUT.json` | Snapshots forward do CS | Implementado (vínculo hash PRE_EVENT/MATURED) | `RESOLVED_AND_VERIFIED` | via síntese | `cs-predictor/HANDOFF.md` |
| `AUDIT_STATE.md` | Estado persistente de toda a auditoria (índice de tudo acima) | 25 etapas, todas `CONCLUÍDA` | `CURRENT_SUPPORTING` | **leitura direta, integral** | `ECOSYSTEM_HANDOFF.md` |
| `OPEN_QUESTIONS.md` | 78 questões abertas numeradas | Maioria endereçada pelas implementações A-01→A-06; algumas genuinamente abertas (ver seção "Reconciliação de OPEN_QUESTIONS.md" acima) | `CURRENT_SUPPORTING` | **leitura direta, integral** | `PENDENCIAS_ABERTAS.md` |
| `EVIDENCE_INDEX.md` | Índice de evidência (EV-xxx) citado por todos os relatórios acima | — | `HISTORICAL_ACCURATE` | não lido nesta rodada | — |

## Limitação desta reconciliação

A matriz acima classifica todos os 64 arquivos, mas a coluna "Evidência"
mostra honestamente que boa parte deles (marcados "via síntese") foi
reconciliada através dos documentos que os consolidam
(`AUDIT_STATE.md`/`OPEN_QUESTIONS.md`, lidos integralmente, mais os
documentos-verdict de cada bloco), não por leitura verbatim de cada
arquivo individual. Isso é suficiente para o propósito desta rodada
(fechar a documentação canônica atual), mas não é o mesmo que ter
verificado cada frase de cada um dos 64 arquivos contra o código. Se uma
auditoria futura precisar de evidência específica de uma etapa
intermediária (ex.: o
conteúdo exato de `28D_F1_H8_BLOCKER_REPORT.md` além do que
`AUDIT_STATE.md` já resume), ela deve ser lida diretamente — não presuma
que esta reconciliação a esgotou.
