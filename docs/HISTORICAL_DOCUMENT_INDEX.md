# Índice de autoridade documental

**Navegação revisada:** 13/09/2026. Este índice impede que snapshots e fechamentos antigos
sejam interpretados como estado presente.

| Fonte | Classe | Uso permitido |
|---|---|---|
| [CURRENT_STATE.md](../CURRENT_STATE.md), [runbook](../ECOSYSTEM_RUNBOOK.md) | CURRENT_ENGINEERING | navegação, combinação de engenharia e procedimentos; histórico separado em `docs/archive/` |
| [Integração Core](../CORE_INTEGRATION_20260913.md) | VERIFIED_COMBINATION | fonte 9bf43ef, wheel 3.2.1, integração Ecosystem 3cfb74b e recibos de CI |
| `registries/released_architecture.json`, `registries/compatibility_candidate.json` | RELEASE_OR_PINNED_COMBINATION | distinguir fonte da release de combinação candidata e main observada |
| `registries/harness_registry.json`, claims científicas e [pendências](../PENDENCIAS_ABERTAS.md) | DATED_EVIDENCE | versões, datas e critérios dos recibos originais; não recertificar ciência por atualização documental |
| `ECOSYSTEM_CHARTER.md` | CURRENT | sete repositórios e fronteiras, reconciliados com a arquitetura implementada em 2026-09-13 |
| `ECOSYSTEM_CURRENT_STATE.md` | SUPERSEDED | ponte para a fonte corrente; conteúdo antigo está no Git |
| `ECOSYSTEM_MECHANICAL_STATE.md`, `audit/*ecosystem-facts.json` | HISTORICAL | snapshots mecânicos datados; nunca estado corrente |
| `ECOSYSTEM_HANDOFF.md`, `HANDOFF.md` | HISTORICAL_WITH_CURRENT_POINTER | histórico de transição; entrada vigente aponta para `CURRENT_STATE.md` |
| `FINAL_*`, `ECOSYSTEM_FINAL_CLOSURE.md`, `CODEX_FINAL_HANDOFF.md` | ARCHIVE | auditorias/fechamentos datados; não reabrir nem usar como presente |
| `FECHAMENTO_*`, `P4_CONSOLIDATION.md`, `F1_*`, `TCC_EVIDENCE_CLOSURE.md` | HISTORICAL | evidência e decisões da época |
| `docs/audit-2026-08-31/*`, `audit/AUDIT_STATE.md` | ARCHIVE | pacote de auditoria anterior, não backlog atual |
| `SECURITY_INCIDENT_SECRET_ROTATION.md` | SUPERSEDED | incidente histórico; errata no topo registra rotação e Git limpo |

## Mapa vigente por responsabilidade

- **Projetos externos:** fichas [Core](projects/core.md), [Ops](projects/ops.md),
  [Cripto](projects/cripto.md), [Brasileirão](projects/brasileirao.md),
  [Stocks](projects/stocks.md) e [CAIN](projects/cain.md). Cada uma encaminha ao
  manual do proprietário e aos recibos existentes; não é novo relatório de auditoria.
- **Contratos do Ecosystem:** [PluginV1](../PREDICTOR_CONTRACT.md),
  [Snapshot](../packages/research-snapshot/README.md) e
  [Bundle](../packages/research-bundle/README.md); código e schemas prevalecem
  para fatos executáveis. Registries não são manuais internos dos projetos.
- **Registros vigentes por escopo:** `architecture_registry.json` define a
  topologia; `released_architecture.json` identifica releases registradas;
  `compatibility_candidate.json` fixa a combinação de teste. Todos em `registries/`.
  `project_registry.json` combina observações de engenharia com campos científicos
  históricos: estes não passam a atuais por atualizar uma versão de software.
  `decision_log.json` preserva decisões datadas; claims, harnesses, economia e
  backup têm autoridade limitada à própria evidência, data e objeto.
- **Evidência de integração:** relatórios Core/Ops/Cripto/Brasileirão/Stocks na raiz
  conservam caminhos, revisões e contexto. `docs/core_integration_20260913/`,
  `docs/ops_integration_20260913/`, `docs/engineering_controls/` e `evidence/`
  preservam bytes e hashes. O recibo Core é consumido diretamente pela CI.
- **Arquitetura:** o [Charter](../ECOSYSTEM_CHARTER.md) e o
  [runbook](../ECOSYSTEM_RUNBOOK.md) descrevem o presente. Os ADRs
  [0001](adr/0001-plugin-protocol-v1.md) e [0002](adr/0002-data-ownership.md)
  registram decisões e constatações de agosto: suas listas de domínios, gateway,
  Postgres/Redis/storage e compliance não descrevem a implementação atual.
  `ECOSYSTEM_BLUEPRINT.md`, `DEPLOY_RUNBOOK.md`, `FASE_5_REPORT.md` e
  `GO_CHECKLIST.md` nesta pasta são procedimentos/planos dessa arquitetura histórica.
- **Histórico separado:** [tabelas e ações de 06/09](archive/current-state-20260906.md).
  `SESSION_HANDOFF.md`, `PUBLICATION_STATUS_20260912.md`, `ARCHITECTURE_IMPLEMENTATION.md`
  e os runbooks antigos na raiz permanecem registros datados ou procedimentos
  especializados, não uma fila de execução atual. Parta do runbook vigente antes
  de aplicar um procedimento antigo. `SECURITY.md` mantém seu papel de política.
- **Manutenção:** [organização de 13/09](maintenance/organization-20260913.md),
  com classificação verificável de branches, baseline e recuperação.

Os arquivos históricos permanecem nos caminhos originais quando já referenciados
ou quando não há benefício suficiente em movê-los. A separação de autoridade é
feita por este índice; evidências datadas continuam válidas para sua combinação.

## Reconciliações históricas — registro de 03/09/2026

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
