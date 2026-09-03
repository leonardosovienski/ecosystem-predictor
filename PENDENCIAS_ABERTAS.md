# Pendências abertas canônicas

Verificado em 2026-09-03. Itens encerrados e listas históricas foram removidos desta
visão; continuam no histórico Git e no índice de documentos históricos.

| ID | repo | blocker | why_it_matters | owner | required_evidence | state |
|---|---|---|---|---|---|---|
| BR-01 | brasileirao-predictor | Prediction store geral e prospective DB originais não localizados | Evidência prospectiva irreversível não pode ser recriada retroativamente | domínio BR | localizar originais e verificar hashes/offsite, ou declarar definitivamente ausentes | OPEN_WITH_EXACT_BLOCKER |
| BR-02 | brasileirao-predictor | Market PIT 2024–2025 | Fonte gratuita testada retorna ausência; disponibilidade comercial não foi testada | domínio BR | export comercial licenciado ou decisão `NOT_VIABLE` por período | UNKNOWN_PAID_SOURCE |
| BR-03 | brasileirao-predictor | Feature PIT 2024–2026 | resultados/xG/estatísticas não têm timestamp suficiente para provar disponibilidade nos cutoffs | domínio BR | timestamps de publicação/ingestão ou coorte bitemporal prospectiva | PARTIAL |
| BR-04 | brasileirao-predictor | EXP-001 histórico sem os dois lados PIT | Execução agora violaria o protocolo de mesmo cutoff | domínio BR | market PIT e feature PIT `READY` no mesmo período/horizonte | NOT_STARTED |
| CR-01 | cripto-predictor | Harnesses emitidos contra Core 3.0.0 | Release corrente é 3.1.0; compatibilidade não equivale a certificação atual | domínio Cripto | reemissão real contra 3.1.0, se necessária | COMPATIBLE_BUT_OLDER |
| CR-02 | cripto-predictor | Próximo trigger natural do Task Scheduler não observado | Confirmação operacional futura; não bloqueia engenharia ou pesquisa | operador | evento natural e evidência de execução | PENDING_OBSERVATION |
| BIZ-01 | ecosystem-predictor | Hipótese comercial sem conversas reais | Não há evidência de dor, interesse ou pagamento | humano/comercial | V1: 10 conversas reais em até dois ICPs | B0 |

Não são pendências: Core 3.1.0/CHANGELOG (consistentes); Ops 4.0.0/main e decisão
`INTENTIONALLY_REMOVED` do monitor; preservação offsite de Core, Ops, Cripto e
Stocks; rotação da SerpAPI; pesquisa congelada de Cripto e Stocks; RJ arquivado.
