# Estado Persistente da Auditoria

**Última atualização:** 2026-07-15  
**Regime de escrita:** somente `audit/`  
**Próxima ação permitida:** A-02 de proveniência runtime concluída; aguardar validação humana e autorização para a próxima mudança (triagem operacional somente leitura).

## Nota de autorização futura

Após o encerramento desta auditoria, poderão ser avaliadas alterações no workspace (incluindo código, testes, configurações ou commits) mediante solicitação e escopo explícitos. Essa possibilidade não autoriza implementações durante a auditoria nem altera a regra de escrita exclusiva em `audit/`.

| Etapa | Status | Artefato esperado | Data de execução | Bloqueios | Aprovação humana necessária antes da próxima etapa |
|---|---|---|---|---|---|
| 0 — Constituição | CONCLUÍDA | `00_AUDIT_CHARTER.md`, `EVIDENCE_INDEX.md`, `OPEN_QUESTIONS.md`, `AUDIT_STATE.md` | 2026-07-15 | Nenhum | Sim — aprovar início da Etapa 1. |
| 1 — Inventário do workspace | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `01_WORKSPACE_INVENTORY.md` | 2026-07-15 | Nenhum bloqueio técnico; divergências e questões abertas registradas. | Sim — validar inventário e aprovar Etapa 2. |
| 2 — Fundação | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `02_FOUNDATION_REPORT.md` | 2026-07-15 | Nenhum bloqueio técnico; lacunas e contradições registradas. | Sim — validar fundação e aprovar Etapa 3. |
| 3 — Projetos ativos | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `03_ACTIVE_PROJECTS_REPORT.md` | 2026-07-15 | Lacunas experimentais e operacionais registradas. | Sim — aprovar Etapa 4. |
| 4 — Legado e arquivados | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `04_LEGACY_AND_ARCHIVED_REPORT.md` | 2026-07-15 | Estados contraditórios e dependências residuais registrados. | Sim — aprovar matrizes. |
| 5 — Capacidades | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `05_CAPABILITY_MATRIX.md` | 2026-07-15 | Equivalência dinâmica e lacunas de adoção permanecem abertas. | Sim — aprovar Etapa 6. |
| 6 — Arquitetura | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `06_ARCHITECTURE_MATRIX.md` | 2026-07-15 | Dependências dinâmicas e decisões de topologia permanecem abertas. | Sim — aprovar Etapa 7. |
| 7 — Científica | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `07_SCIENTIFIC_MATRIX.md` | 2026-07-15 | Reprodução, controles positivos e interpretação de inconclusão permanecem abertos. | Sim — aprovar Etapa 8. |
| 8 — Operacional | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `08_OPERATIONAL_MATRIX.md` | 2026-07-15 | Falhas de scheduler, backup/recovery e CI externo permanecem abertos. | Sim — aprovar Etapa 9. |
| 9 — Evolução | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `09_EVOLUTION_MATRIX.md` | 2026-07-15 | Conhecimento local e questões de preservação permanecem abertos. | Sim — aprovar síntese. |
| 10 — Síntese cross-domain | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `10_CROSS_DOMAIN_SYNTHESIS.md` | 2026-07-15 | Oportunidades registradas sem roadmap ou decisão de migração. | Sim — aprovar conselho. |
| 11 — Conselho arquitetural | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `11_ARCHITECTURE_COUNCIL.md` | 2026-07-15 | Decisões priorizadas com gates; sem veredito final. | Sim — aprovar red team. |
| 12 — Red team | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `12_RED_TEAM.md` | 2026-07-15 | Conselho preservado; recomendações testadas adversarialmente. | Sim — aprovar veredito. |
| 13 — Veredito final | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `13_FINAL_VERDICT.md` | 2026-07-15 | Reconciliação, Red Team e lacunas explícitas; sem implementação. | Não aplicável. |
| 14 — A-01 auditoria byte a byte | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `14_VENDOR_BYTE_AUDIT.md` | 2026-07-15 | Oito vendors verificados, todos idênticos; nenhuma sincronização/correção. | Sim — aprovar A-02. |
| 15 — A-02 proveniência runtime | CONCLUÍDA — AGUARDANDO VALIDAÇÃO | `15_CORE_RUNTIME_PROVENANCE.md` | 2026-07-15 | Oito imports controlados MATCH; nenhum entrypoint/vendor alterado. | Sim — aprovar triagem operacional. |

## Atualização da Etapa 3 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `03_ACTIVE_PROJECTS_REPORT.md`.
- **Próxima ação permitida:** aguardar validação humana deste relatório e aprovação explícita para a Etapa 4.
- Foram feitas somente leituras de auditoria, código, Git, configurações, Scheduled Tasks e logs/bancos pré-existentes.
- Nenhum teste, backtest, coletor, CLI, serving ou servidor foi executado; nenhum arquivo fora de `audit/` foi alterado.

## Atualização da Etapa 4 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `04_LEGACY_AND_ARCHIVED_REPORT.md`.
- **Próxima ação permitida:** aguardar validação humana deste relatório e aprovação explícita para as matrizes.
- Foram feitas somente leituras de auditoria, código, Git, configurações, Scheduled Tasks, referências cruzadas e artefatos pré-existentes.
- Nenhum teste, backtest, coletor, CLI, serving ou servidor foi executado; nenhum arquivo fora de `audit/` foi alterado.

## Checkpoint de descoberta — 2026-07-15

- Criado `04A_DISCOVERY_CHECKPOINT.md` como reconciliação das Etapas 1–4 antes das matrizes.
- A próxima etapa de conteúdo permanece dependente de validação humana do checkpoint e dos relatórios anteriores.
- O checkpoint corrige a leitura consolidada; não altera silenciosamente os registros históricos de coleta.

## Atualização da Etapa 5 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `05_CAPABILITY_MATRIX.md`.
- **Próxima ação permitida:** aguardar validação humana da matriz de capacidades e aprovação explícita para a Etapa 6.
- A matriz foi produzida por inspeção horizontal; nenhum teste, pipeline ou comando de domínio foi executado e nenhum arquivo fora de `audit/` foi alterado.

## Atualização da Etapa 6 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `06_ARCHITECTURE_MATRIX.md`.
- **Próxima ação permitida:** aguardar validação humana da matriz arquitetural e aprovação explícita para a Etapa 7.
- Foram feitas apenas leituras de artefatos, manifests, código de sync/health e buscas estáticas. Nenhum sync write, teste, pipeline ou arquivo fora de `audit/` foi alterado.

## Atualização da Etapa 7 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `07_SCIENTIFIC_MATRIX.md`.
- **Próxima ação permitida:** aguardar validação humana da matriz científica e aprovação explícita para a Etapa 8.
- A análise foi estática e baseada em artefatos; nenhum teste, backtest, coleta, harness ou arquivo fora de `audit/` foi alterado.

## Atualização da Etapa 8 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `08_OPERATIONAL_MATRIX.md`.
- **Próxima ação permitida:** aguardar validação humana da matriz operacional e aprovação explícita para a Etapa 9.
- Executada somente a verificação não mutante `sync_core --check` (exit 0, 261 ms); nenhum pytest, CLI, coleta, scheduler ou arquivo fora de `audit/` foi alterado.

## Atualização da Etapa 9 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `09_EVOLUTION_MATRIX.md`.
- **Próxima ação permitida:** aguardar validação humana da matriz de evolução e aprovação explícita para a Etapa 10.
- A análise foi histórica e sintética; não foram procurados novos bugs, executados experimentos ou alterados arquivos fora de `audit/`.

## Atualização da Etapa 10 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `10_CROSS_DOMAIN_SYNTHESIS.md`.
- **Próxima ação permitida:** aguardar validação humana da síntese cross-domain e aprovação explícita para a Etapa 11.
- A análise cruzou artefatos e fonte somente para verificação; não houve alteração de código/configuração fora de `audit/`, execução de pipeline ou roadmap.

## Atualização da Etapa 11 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `11_ARCHITECTURE_COUNCIL.md`.
- **Próxima ação permitida:** aguardar validação humana do parecer do conselho e aprovação explícita para a Etapa 12.
- Decisões sobre topologia, remoções e promoção ao core foram mantidas condicionadas à evidência; nenhum código/configuração fora de `audit/` foi alterado.

## Atualização da Etapa 12 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `12_RED_TEAM.md`.
- **Próxima ação permitida:** aguardar validação humana do red team e aprovação explícita para a Etapa 13.
- O Conselho não foi alterado silenciosamente; o red team registrou ataques, classificações, riscos residuais e testes decisivos sem alterar código/configuração fora de `audit/`.

## Reconciliação e Atualização da Etapa 13 — 2026-07-15

- **Reconciliação:** criado `12A_COUNCIL_RED_TEAM_RECONCILIATION.md`; Conselho e Red Team foram conciliados antes do veredito.
- **Status da Etapa 13:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `13_FINAL_VERDICT.md`.
- **Resultado:** classificação final `EVOLUÇÃO INCREMENTAL`; lacunas, riscos e recomendações rejeitadas permanecem explícitos.
- **Estado da auditoria:** CONCLUÍDA como parecer documental. Nenhum código, teste, configuração, dependência, automação ou dado fora de `audit/` foi alterado.

## Atualização da implementação A-01 — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `14_VENDOR_BYTE_AUDIT.md`; utilitário em `tools/vendor_byte_audit.py` e testes isolados em `tools/tests/test_vendor_byte_audit.py`.
- **Resultado:** oito vendors reais, 44 arquivos por vendor, byte a byte idênticos ao canônico; exit code observado `0`.
- **Segurança:** nenhum `--write`, sync, correção de drift, alteração de manifest ou modificação de vendor/`predictor_core` ocorreu.
- **Próxima ação permitida:** aguardar validação humana e autorização explícita para A-02, triagem operacional somente leitura.

## Atualização da implementação A-02 — proveniência runtime — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `15_CORE_RUNTIME_PROVENANCE.md`; ferramenta `tools/core_provenance.py` e testes isolados em `tools/tests/test_core_provenance.py`.
- **Resultado:** oito consumers importaram o vendor esperado, com versão e hash correspondentes; `--all --strict` retornou `0`.
- **Segurança:** nenhum vendor/core/manifest/entrypoint/banco/automação foi modificado; subprocessos bloqueiam bytecode em vendor.
- **Próxima ação permitida:** aguardar validação humana e autorização para triagem operacional somente leitura.

## Recapitulação consolidada — 2026-07-15

- Criado `09A_CONSOLIDATED_RECAP.md` como entrada organizada para a síntese cross-domain.
- A síntese final ainda não foi iniciada; a recapitulação preserva incertezas e não decide mudanças.

## Atualização da implementação A-03 — hardening operacional — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO VALIDAÇÃO.
- **Artefato:** `16_OPERATIONAL_HARDENING.md`; envelope em `tools/operational_runner.py` e health somente-leitura em `tools/ecosystem_health.py`.
- **Resultado:** H5, V3 e watchdog cripto agora possuem contrato observável/heartbeat; falhas silenciosas confirmadas em PowerShell foram eliminadas; nenhuma tarefa do Scheduler foi alterada.
- **Validação:** `tools/tests` retornou 33 passed, 1 skipped; health real retornou 1, expondo corretamente resultados não zero e heartbeats ainda inexistentes.
- **Próxima ação permitida:** observar o próximo ciclo agendado sem dispará-lo e, separadamente, diagnosticar `0x800710E0` com logs/owner antes de qualquer alteração de tarefa.

## Atualização da validação A-03B — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO CICLO NATURAL E VALIDAÇÃO.
- **Artefato:** `17_OPERATIONAL_POST_CYCLE_VALIDATION.md`.
- **Resultado:** a implantação ocorreu após os últimos ciclos H5/V3/watchdog; não há ainda heartbeats, JSONL ou locks A-03. O health retornou 1 coerente com os dados, sem falso verde.
- **Novo achado:** segredo em log histórico H5; a preservação de stdout/stderr pelo wrapper pode reproduzi-lo em log operacional futuro. Não foi feita correção nesta etapa.
- **Próxima ação permitida:** implementar uma correção isolada de redação do log operacional, com teste simulado, ou aguardar ciclos naturais após essa decisão. Diagnóstico de `0x800710E0` requer logs/Event Viewer de ocorrência atual ou owner.

## Atualização da implementação A-03C — redação de segredos — 2026-07-15

- **Status técnico:** CONCLUÍDA — BLOQUEADA PARA CICLO REAL POR ROTAÇÃO PENDENTE.
- **Artefato:** `18_SECRET_REDACTION.md`; redator em `tools/secret_redaction.py` integrado ao wrapper operacional.
- **Resultado:** stdout/stderr, comandos, JSONL, heartbeats e erros são redigidos antes da persistência; `tools/tests` retornou 43 passed, 1 skipped.
- **Histórico:** três logs H5 potencialmente contaminados foram inventariados sem conteúdo e não foram modificados.
- **Gate humano:** revogar/rotacionar a credencial exposta, não usar a substituta na CLI e decidir sanitização/remoção dos originais antes de liberar H5/V3.

## Atualização da implementação A-04 — Brasileirão operacional — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO CICLO NATURAL E VALIDAÇÃO.
- **Artefato:** `19_BRASILEIRAO_OPERATIONAL_MIGRATION.md`; rollback XML em `audit/task_backups/`.
- **Resultado:** manhã/noite agora têm entrypoint operacional identificável, cwd explícito, timeout, lock, logs redigidos, JSONL e heartbeat por tarefa. As duas ações do Scheduler foram alteradas após exportação; agenda e identidade foram preservadas.
- **Validação:** 268 testes Brasileirão passaram (1 warning existente); 48 testes operacionais passaram, 1 skipped; provenance e vendor audit passaram.
- **Próxima ação permitida:** observar os próximos ciclos naturais e reconciliar Scheduler/heartbeat. Não iniciar CS automaticamente.

## Atualização da validação A-04 — janela inicial — 2026-07-15

- **Status:** OBSERVADA — AGUARDANDO CICLOS NATURAIS.
- **Artefato:** `19A_BRASILEIRAO_POST_CYCLE_VALIDATION.md`.
- **Resultado:** manhã e noite classificadas `NOT_RUN` pós-A04; não há operações, JSONL, heartbeat, lock ou artefato novo. O health continua a refletir o baseline histórico.
- **Próxima ação permitida:** observar após 13:00 UTC e após o ciclo noturno, sem disparar tarefas. Não iniciar CS automaticamente.

## Atualização da implementação A-05 — CS operacional — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO CICLO NATURAL E VALIDAÇÃO.
- **Artefato:** `20_CS_OPERATIONAL_MIGRATION.md`.
- **Resultado:** a tarefa semanal mantém a mesma definição do Scheduler e agora entra no wrapper via seu script existente; logs, heartbeat, JSONL, lock, timeout, provenance e redação foram integrados.
- **Validação:** 56 testes operacionais passaram, 1 skipped; provenance/vendor byte audit passaram. Suíte CS: 48 passed, 1 failed por arquivos de vendor não rastreados no Git, fora do escopo.
- **Próxima ação permitida:** observar o ciclo semanal natural e abrir investigação isolada do índice Git do vendor. Não iniciar LoL automaticamente.

## Atualização A-05A — higiene Git do vendor CS — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO REVISÃO/COMMIT E CICLO NATURAL.
- **Artefato:** `20A_CS_VENDOR_GIT_HYGIENE.md`.
- **Resultado:** 11 módulos canônicos necessários e os metadados coerentes foram adicionados ao índice; clone temporário com patch indexado passou 49 testes e importou o vendor próprio.
- **Validação:** suíte CS 49 passed; testes operacionais 56 passed, 1 skipped; sync, byte audit e provenance passaram.
- **Próxima ação permitida:** revisar/commitar o patch do vendor e observar o ciclo CS natural. Não iniciar LoL automaticamente.

## Atualização da implementação A-06 — LoL operacional — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO CICLO NATURAL E VALIDAÇÃO.
- **Artefato:** `21_LOL_OPERATIONAL_MIGRATION.md`.
- **Resultado:** `lol-ratings-semanal` passa pelo runner via o entrypoint existente, sem alteração de Scheduler. Foram integrados heartbeat, JSONL, lock, timeout, proveniência, redação e validação de artefato fresco.
- **Validação:** 31 testes LoL e 64 testes das ferramentas passaram; sync, auditoria byte a byte e provenance estrita passaram. Nenhum refresh ou chamada externa ocorreu.
- **Próxima ação permitida:** observar o ciclo semanal natural e reconciliar Scheduler/heartbeat/JSONL. Não iniciar A-07 automaticamente.

## Atualização científica — relatório H3 do Brasileirão — 2026-07-15

- **Status:** CONCLUÍDA — AGUARDANDO MATURAÇÃO NATURAL.
- **Artefato:** `25_BRASILEIRAO_SHADOW_REPORT.md`; comando `scripts/report_shadow_mode.py` no repositório Brasileirão.
- **Resultado:** snapshot offline de 3 picks únicos e 0 liquidados foi classificado `DADOS INSUFICIENTES`; nenhuma métrica econômica foi preenchida por inferência e nenhum banco/dado foi modificado.
- **Validação:** 6 testes novos do relatório e 274 testes do Brasileirão passaram; ferramentas operacionais: 64 passed, 1 skipped. O warning existente de `rho` no limite permanece registrado.
- **Git:** commits separados foram criados para Brasil (`4b1488a`, `d94d44f`), CS (`e6114b3`, `23faba1`, em branch local) e LoL (`f907543`). `tools/` não é repositório Git e segue sem commit local.
- **Próxima ação permitida:** aguardar settlement natural e reexecutar o relatório; não alterar hipótese, parâmetros ou Scheduler.

## Controle de bloqueios

Nenhum bloqueio técnico foi investigado ou identificado nesta etapa. A aprovação humana é um gate deliberado, não um defeito do workspace.

## Registro de execução desta etapa

- Foi criado `01_WORKSPACE_INVENTORY.md` e atualizados `EVIDENCE_INDEX.md`, `OPEN_QUESTIONS.md` e este estado.
- Foram realizadas somente leituras, buscas e comandos Git não mutantes; nenhum teste, entrypoint, CLI, servidor ou coletor foi executado.
- Não foram feitas avaliações arquiteturais, científicas ou recomendações.
- Ambientes, caches e artefatos existentes foram apenas identificados; nenhum arquivo fora de `audit/` foi alterado.
- Foi criado `02_FOUNDATION_REPORT.md`; foram lidos o core, sync, manifests, testes estáticos de integridade, documentação da fundação, script de saúde e configuração das tarefas agendadas.
- `sync_core --check` foi executado em modo somente leitura; nenhum `--write`, teste, CLI de domínio, servidor ou coletor foi executado.
- Nenhum arquivo fora de `audit/` foi alterado.

## Reconciliação F1 2026 — 2026-07-15

## Gate F1 Market H2H — 2026-07-21

## Fechamento autorizado F1 — 2026-07-23

- **Registro único:** `f1-predictor/data/authorized_closure.json`, com commit, timestamp UTC, hashes preservados e contador H8 0/15.
- **Estados:** H1-F1 `HYPOTHESIS_REFUTED`; operação original `NO_GO_CONFIRMED`; H2H/H8 `CLOSED_BY_HUMAN_DECISION`. H2H e H8 não foram aprovadas nem refutadas pelo encerramento.
- **Operação:** `f1-forward-snapshot` desabilitado; `predictor-gate-monitor` preservado por ser transversal. H8/H2H falham fechados; dinheiro real permanece bloqueado.

- **Status:** `MARKET_H2H_NOT_FEASIBLE`; 0 fontes e 0 quotes aceitos. Não é falha de modelo nem amostra de performance.
- **Garantias:** Market DB separado/fail-closed; sem timestamp, odds bilaterais, proveniência e settlement compatível, a ingestão é bloqueada. FastF1 permanece somente contrato exploratório.
- **Próxima ação permitida:** decisão humana sobre fonte licenciada e export de teste; sem scraping, odds inventadas, Stage 1, ROI/Sharpe ou apostas reais.
- **Atualização 2026-07-22:** ledger de tentativas negativas criado; Gate de cobertura agora apresenta mínimo/intermediário/conservador sem fixar critério. Contrato econômico requer opening/closing/decision timestamps e `season/race_id`; fonte parcialmente aceita continua bloqueada para ingestão.

- **Status:** RECONCILIAÇÃO PARCIAL — fase científica permanece bloqueada.
- **Artefatos:** `28A_F1_SNAPSHOT_RECONCILIATION.md`, `28B_F1_2026_RACE_MATRIX.md`, `28C_F1_GIT_STATE_RECONCILIATION.md`, `28D_F1_H8_BLOCKER_REPORT.md`, `28_F1_RECONCILIATION.json`.
- **Resultado:** `main` e a branch atual estão no commit `19e3ec4`; R1–R9 reproduzem exatamente o JSON de validação a partir do banco local; R10–R22 são somente calendário.
- **Bloqueadores:** apenas 9 resultados maturados (marco histórico: 15) e não existe snapshot pré-corrida datado/imutável; portanto 0 corridas são `VALID_FOR_H8` sob o critério definido.
- **Segurança:** não houve H8, rede, ingestão, merge, checkout, alteração de modelo, parâmetro, gate, banco ou HANDOFF. Hashes de banco/JSON foram preservados.

## Coleta forward F1 — 2026-07-15

- **Status:** IMPLEMENTADA — aguardando primeiro snapshot PRE_EVENT real.
- **Commit F1:** `5ab0433` (`Add immutable forward F1 snapshots`) na branch `claude/belgium-quali-gp-test-72bff2`; `main` permanece em `19e3ec4` até revisão/merge.
- **Artefatos:** `34_F1_FORWARD_SNAPSHOT_DESIGN.md`, `35_F1_FORWARD_SNAPSHOT_IMPLEMENTATION.md`, `36_F1_FORWARD_OPERATIONAL_RUNBOOK.md`.
- **Garantias:** snapshot/maturação usam banco somente leitura, não atualizam ratings/modelo/gate, não fazem rede e proíbem timestamps naive/tardios, grid incompleto, resultado prévio e overwrite.
- **Validação:** testes novos e suíte completa F1 passaram; audit de bytes, provenance runtime, `sync_core --check`, testes operacionais e gate real `NO-GO` passaram.
