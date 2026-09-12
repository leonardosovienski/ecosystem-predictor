# Estado canônico atual

<!-- DOC-SYNC-20260912 -->
> **Estado de publicação em 12/09/2026:** leia [a continuidade atual](PUBLICATION_STATUS_20260912.md). Branch `feature/research-bundle-v1`. O código deste projeto foi publicado na branch indicada. O candidato CAIN Supply permanece sem aprovação de estabilização. Afirmações anteriores de “sem push” descrevem a etapa histórica anterior à autorização.
<!-- /DOC-SYNC-20260912 -->


A arquitetura vigente está em [ECOSYSTEM_RUNBOOK.md](ECOSYSTEM_RUNBOOK.md). As tabelas científicas e pendências datadas de 06/09 abaixo são históricas; o estado científico vigente pertence ao respectivo domínio. A entrega de engenharia de 11/09 não reemite esses vereditos.

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

**Data:** 2026-09-06
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
| stocks-predictor | caso de falsificação; H1–H16 congeladas, H17–H19 pré-registradas | ACTIVE_MINIMAL | FROZEN_H1_H16 + PREREGISTERED_H17_H19 | CLOSED_FOR_H1_H16 | MEASUREMENT_PENDING | NOT_A_PRODUCT |

## Questões abertas

- Brasileirão: `EXP001_HISTORICAL = NOT_VIABLE`. A investigação limitada não
  comprovou cobertura comercial exata de 2024–2025 e o inventário de features
  não encontrou timestamps suficientes para H−24h, H−6h e H−1h. A linha válida é
  `EXP001_PROSPECTIVE = ACTIVE`; a decisão científica segue `UNKNOWN` até dados futuros.
- Brasileirão: prediction store geral e prospective DB dedicados são
  `MISSING_CONFIRMED` após a busca final; não serão reconstruídos retroativamente.
- Cripto: o disparo natural do Task Scheduler ainda é `PENDING_OBSERVATION`; não é
  blocker técnico nem científico.
- Harnesses: Brasileirão certifica Core **3.2.0** (reemitido em 2026-09-06, sem
  `;dirty`, expira 2026-09-13); Cripto certifica Core 3.0.0 e segue
  `COMPATIBLE_BUT_OLDER` por decisão, não por esquecimento — subir exige emitir
  atestado nos cinco pontos que atualizam veredito (CR-01).
- Stocks: o atestado vigente foi emitido com Core 3.1.0 e o bump para 3.2.0, em
  2026-09-06, **o invalidou**. Enquanto não for reemitido na máquina do operador,
  com árvore limpa, a H18 não registra trial. É o único item com prazo do
  ecossistema (ST-01).
- Stocks: a **ordem** das rodadas H17/H18/H19 não está fixada. O N do DSR cresce a
  cada tentativa, então escolher depois de ver resultado é p-hacking; a ordem precisa
  ser decidida antes da primeira medição (ST-03).

## Estado comercial

`CLAIM_BIZ_001 = B0` e `COMMERCIAL_DISCOVERY_PHASE = STARTING`. A lista P3.0 tem
dez contatos nominais públicos em ICP-1 e ICP-2, registrada em
`registries/commercial_discovery.json`; isso inicia apenas a preparação operacional
de V1, não valida dor, acesso, comprador ou disposição a pagar. `OUTREACH_001` foi
preparado para Daniel Djonatha e está `READY_FOR_HUMAN_EXECUTION`; roteiro, captura
de evidência e follow-up também estão registrados. Nenhuma abordagem foi enviada.
Próxima evidência: envio pelo operador e primeira conversa qualificada real.

`CLAIM_ECON_001 = E0`: preço, esforço de entrega, aquisição, margem, reutilização e
retenção permanecem `UNKNOWN`. Receita e engagements pagos são zero. A oferta e os
templates de medição estão em `registries/economics_registry.json`; não constituem
evidência de mercado.

## Próximas ações permitidas

1. Manter coleta prospectiva do Brasileirão com o contrato em `canonical_contracts/exp001_prospective.json`.
2. Não reabrir o EXP-001 histórico sem evidência nativa e timestamped dos dois lados PIT.
3. Observar o próximo disparo natural do scheduler do Cripto sem reabrir pesquisa.
4. Reemitir harnesses do Cripto contra Core 3.2.0 somente se a certificação atual for
   exigida — e tratando como trabalho de código, não troca de pin (CR-01).
6. Reemitir o atestado do Stocks contra Core 3.2.0 antes de qualquer rodada de
   H17/H18/H19, e fixar a ordem das três antes da primeira medição.
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
- `registries/economics_registry.json`
- `PENDENCIAS_ABERTAS.md`
- `docs/HISTORICAL_DOCUMENT_INDEX.md`
- `SESSION_HANDOFF.md`

`TECHNICAL_DISCOVERY_PHASE = CLOSED` e `COMMERCIAL_DISCOVERY_PHASE = STARTING`.
Este repositório só muda diante de mudança
real de estado, versão, evidência, incidente ou decisão.
