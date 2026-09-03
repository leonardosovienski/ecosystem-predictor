# Índice de autoridade documental

**Atualizado:** 2026-09-03. Este índice impede que snapshots e fechamentos antigos
sejam interpretados como estado presente.

| Fonte | Classe | Uso permitido |
|---|---|---|
| `CURRENT_STATE.md`, `registries/*.json`, `PENDENCIAS_ABERTAS.md` | CURRENT | estado, evidência, decisões, backups e blockers vigentes |
| `ECOSYSTEM_CHARTER.md` | CURRENT | papel e fronteiras do ecossistema, reconciliados em 2026-09-03 |
| `ECOSYSTEM_CURRENT_STATE.md` | SUPERSEDED | ponte para a fonte corrente; conteúdo antigo está no Git |
| `ECOSYSTEM_MECHANICAL_STATE.md`, `audit/*ecosystem-facts.json` | HISTORICAL | snapshots mecânicos datados; nunca estado corrente |
| `ECOSYSTEM_HANDOFF.md`, `HANDOFF.md` | HISTORICAL_WITH_CURRENT_POINTER | histórico de transição; entrada vigente aponta para `CURRENT_STATE.md` |
| `FINAL_*`, `ECOSYSTEM_FINAL_CLOSURE.md`, `CODEX_FINAL_HANDOFF.md` | ARCHIVE | auditorias/fechamentos datados; não reabrir nem usar como presente |
| `FECHAMENTO_*`, `P4_CONSOLIDATION.md`, `F1_*`, `TCC_EVIDENCE_CLOSURE.md` | HISTORICAL | evidência e decisões da época |
| `docs/audit-2026-08-31/*`, `audit/AUDIT_STATE.md` | ARCHIVE | pacote de auditoria anterior, não backlog atual |
| `SECURITY_INCIDENT_SECRET_ROTATION.md` | SUPERSEDED | incidente histórico; errata no topo registra rotação e Git limpo |

## Mapa de inconsistências reconciliadas

| Conflito | Origem antiga | Evidência atual | Resultado |
|---|---|---|---|
| Core 3.0 vs 3.1 | snapshots de 01/09 | main, wheel e CHANGELOG 3.1.0 | RESOLVED |
| Ecosystem/gateway ativo vs registry mínimo | Charter antigo | código atual e remoção de gateway/scheduler/storage | SUPERSEDED |
| Predictors comerciais/ativos vs freeze | Charter antigo | freezes de Cripto e Stocks; BR ativo só em EXP-001 | RESOLVED |
| BR `BLOCKED` vs backups verificados | auditoria de preservação agregada | ativos conhecidos offsite; dois stores ainda ausentes | SUPERSEDED por `PARTIAL` granular |
| BR fechado vs EXP-001 aberto | fechamentos antigos | readiness report: execução não iniciada, decisão `UNKNOWN` | RESOLVED |
| Harnesses todos atuais | alegação genérica | BR 3.1.0; Cripto 3.0.0 | OPEN_WITH_EXACT_BLOCKER (`COMPATIBLE_BUT_OLDER`) |
| SerpAPI rotação pendente | documento de julho | rotação confirmada e varredura Git segura | RESOLVED |
| Negócio/produto validado | linguagem histórica de lucro/produto | nenhuma conversa real | SUPERSEDED; `CLAIM-BIZ-001=B0` |
| Pesquisa congelada com tarefas de busca | backlogs históricos | freezes e única observação passiva permitida | RESOLVED |

Documentos históricos não são apagados nem reescritos para parecer que sempre
estiveram corretos. O histórico Git preserva seu conteúdo integral.
