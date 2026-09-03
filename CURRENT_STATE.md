# Estado canônico atual

**Data:** 2026-09-03
**Autoridade:** este arquivo e os registros em `registries/` substituem qualquer
descrição de estado anterior. Evidência executada prevalece sobre documentação antiga.

## Projetos

| Projeto | Papel | Manutenção | Pesquisa | Ciência | Operação | Comercial |
|---|---|---|---|---|---|---|
| ecosystem-predictor | governança e registros | ACTIVE_ON_STATE_CHANGE | FROZEN | NOT_APPLICABLE | CANONICAL_REGISTRY | NOT_A_PRODUCT |
| core-predictor | motor científico interno | ACTIVE | CLOSED_P0 | READY | FOUNDATION_READY | NOT_A_PRODUCT |
| predictor-ops | infraestrutura interna | ACTIVE | FROZEN | NOT_APPLICABLE | READY | NOT_A_PRODUCT |
| brasileirao-predictor | laboratório científico e portfólio público | ACTIVE_MINIMAL | ACTIVE_EXP001_ONLY | OPEN | READY_WITH_DATA_GATES | NOT_A_PRODUCT |
| cripto-predictor | ativo de pesquisa congelado e casos científicos | PASSIVE | FROZEN | CLOSED | PASSIVE_COLLECTION | NOT_A_PRODUCT |
| stocks-predictor | ativo de pesquisa congelado e caso de falsificação | FROZEN | FROZEN | CLOSED | ARCHIVED | NOT_A_PRODUCT |

## Questões abertas

- Brasileirão: `EXP001_HISTORICAL = NOT_VIABLE`. A investigação limitada não
  comprovou cobertura comercial exata de 2024–2025 e o inventário de features
  não encontrou timestamps suficientes para H−24h, H−6h e H−1h. A linha válida é
  `EXP001_PROSPECTIVE = ACTIVE`; a decisão científica segue `UNKNOWN` até dados futuros.
- Brasileirão: prediction store geral e prospective DB dedicados são
  `MISSING_CONFIRMED` após a busca final; não serão reconstruídos retroativamente.
- Cripto: o disparo natural do Task Scheduler ainda é `PENDING_OBSERVATION`; não é
  blocker técnico nem científico.
- Harnesses: Brasileirão certifica Core 3.1.0; Cripto certifica Core 3.0.0 e é
  `COMPATIBLE_BUT_OLDER`, não alinhado.

## Estado comercial

`CLAIM_BIZ_001 = B0` e `COMMERCIAL_DISCOVERY_PHASE = STARTING`. A lista P3.0 tem
dez contatos nominais públicos em ICP-1 e ICP-2, registrada em
`registries/commercial_discovery.json`; isso inicia apenas a preparação operacional
de V1, não valida dor, acesso, comprador ou disposição a pagar. `OUTREACH_001` foi
preparado para Daniel Djonatha e está `READY_FOR_HUMAN_EXECUTION`; roteiro, captura
de evidência e follow-up também estão registrados. Nenhuma abordagem foi enviada.
Próxima evidência: envio pelo operador e primeira conversa qualificada real.

## Próximas ações permitidas

1. Manter coleta prospectiva do Brasileirão com o contrato em `canonical_contracts/exp001_prospective.json`.
2. Não reabrir o EXP-001 histórico sem evidência nativa e timestamped dos dois lados PIT.
3. Observar o próximo disparo natural do scheduler do Cripto sem reabrir pesquisa.
4. Reemitir harnesses do Cripto contra Core 3.1.0 somente se a certificação atual for exigida.
5. O operador revisar e enviar `OUTREACH_001`; depois registrar somente a interação humana real.

## Ações proibidas

Novo predictor; nova busca de alpha; reabrir fatores de Stocks, HMM/LLM/trend do
Cripto, RJ ou hipóteses fechadas do Brasileirão; SaaS antes de demanda; dashboard;
rebuild genérico de MLOps; abstração no Core sem segundo consumidor; nova auditoria
ampla; execução do EXP-001 neste repositório.

## Registros

- `registries/project_registry.json`
- `registries/evidence_registry.json`
- `registries/decision_log.json`
- `registries/backup_registry.json`
- `registries/harness_registry.json`
- `PENDENCIAS_ABERTAS.md`
- `docs/HISTORICAL_DOCUMENT_INDEX.md`

`TECHNICAL_DISCOVERY_PHASE = CLOSED` e `COMMERCIAL_DISCOVERY_PHASE = STARTING`.
Este repositório só muda diante de mudança
real de estado, versão, evidência, incidente ou decisão.
