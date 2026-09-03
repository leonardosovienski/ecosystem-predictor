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

- Brasileirão: odds gratuitas históricas de 2024–2025 não são viáveis na fonte
  testada; cobertura de fontes pagas é `UNKNOWN`.
- Brasileirão: disponibilidade PIT das features em H−24h, H−6h e H−1h não foi
  comprovada para 2024–2026. O EXP-001 permanece não iniciado e sua decisão é `UNKNOWN`.
- Cripto: o disparo natural do Task Scheduler ainda é `PENDING_OBSERVATION`; não é
  blocker técnico nem científico.
- Harnesses: Brasileirão certifica Core 3.1.0; Cripto certifica Core 3.0.0 e é
  `COMPATIBLE_BUT_OLDER`, não alinhado.

## Estado comercial

`CLAIM_BIZ_001 = B0`. Existe apenas a hipótese de que empresas com sistemas
preditivos em produção possam pagar por auditoria independente. Não há mercado,
ICP, disposição a pagar ou product-market fit validados. Próxima evidência: V1,
dez conversas reais, limitadas inicialmente a fintech/crédito e indústria/demanda.

## Próximas ações permitidas

1. No Brasileirão, obter evidência de market PIT pago e de feature PIT ou declarar
   cada período histórico não viável; executar EXP-001 somente no repositório de domínio.
2. Manter coleta prospectiva com o contrato em `canonical_contracts/exp001_prospective.json`.
3. Observar o próximo disparo natural do scheduler do Cripto sem reabrir pesquisa.
4. Reemitir harnesses do Cripto contra Core 3.1.0 somente se a certificação atual for exigida.
5. Executar V1: dez conversas reais de descoberta comercial.

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

`TECHNICAL_DISCOVERY_PHASE = CLOSED`. Este repositório só muda diante de mudança
real de estado, versão, evidência, incidente ou decisão.
