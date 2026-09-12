# HANDOFF — ecosystem-predictor

<!-- DOC-SYNC-20260912 -->
> **Estado de publicação em 12/09/2026:** leia [a continuidade atual](PUBLICATION_STATUS_20260912.md). Branch `feature/research-bundle-v1`. O código deste projeto foi publicado na branch indicada. O candidato CAIN Supply permanece sem aprovação de estabilização. Afirmações anteriores de “sem push” descrevem a etapa histórica anterior à autorização.
<!-- /DOC-SYNC-20260912 -->


## Candidato local de intercâmbio ampliado

[ResearchBundleV1](packages/research-bundle/README.md) é um pacote aditivo independente.
SnapshotV1 permanece intacto. 57 testes novos do contrato e 60 existentes passaram
localmente em Python 3.13; wheels foram instalados isoladamente. A nova matriz CI
foi configurada, não executada remotamente. Não há release/push deste candidato.

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

O handoff canônico deste repositório é [ECOSYSTEM_HANDOFF.md](ECOSYSTEM_HANDOFF.md).

Estado vigente: [CURRENT_STATE.md](CURRENT_STATE.md). Em 2026-09-03, Core 3.1.0 e
Ops 4.0.0 estão publicados; Cripto e Stocks estão congelados; somente o EXP-001 do
Brasileirão permanece cientificamente aberto. `ECOSYSTEM_MECHANICAL_STATE.md` é um
snapshot histórico, não uma fonte corrente.


## Implementação arquitetural local — 2026-09-11

As alterações candidatas, seus limites, verificações e rollback estão em [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md). Esta implementação local não publica releases, não atualiza automaticamente os consumidores e não altera os vereditos científicos históricos.
