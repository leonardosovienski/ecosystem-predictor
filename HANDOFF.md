> **Ops 4.2.1 publicado:** registries reconciliados com a release validada e pins atuais de Crypto/Brasileirão. SHA256 do wheel: `da4fa540703879669caba919521ec7d3c33734b5d57781122823df8817346f0e`. [Evidências](https://github.com/leonardosovienski/predictor-ops/blob/main/docs/stabilization-20260912/REPORT.md). Instalações operacionais e estados científicos não foram promovidos.

> **Brasileirão — entrega consolidada em main:** [versões, integração CAIN, CI, backups e reprodução](BRASILEIRAO_INTEGRATION_20260912.md). A aprovação é técnica/documental; ciência, produção e capital conservam seus gates próprios.

# HANDOFF — ecosystem-predictor

<!-- DOC-SYNC-20260912 -->
> **Continuidade de publicação:** [estado e evidências atuais](PUBLICATION_STATUS_20260912.md). A combinação Crypto/Ecosystem/CAIN foi integrada e validada em main. As referências anteriores à branch candidata e à falha Linux são históricas; não definem o resultado desta combinação. Estados científicos e releases mantêm suas fontes próprias.
<!-- /DOC-SYNC-20260912 -->


## Intercâmbio ampliado em main

ResearchBundleV1 1.0.0 e ResearchSnapshotV1 (distribuição 1.0.1) estão na main.
A cadeia Stocks foi validada também na instalação principal do CAIN; consulte
[STOCKS_INTEGRATION_20260912.md](STOCKS_INTEGRATION_20260912.md) para os SHAs, hashes,
CI e acervos de consulta. Checkout principal local: `C:/CAIN/contrato`, branch `main`.

### Histórico da primeira implementação do candidato

[ResearchBundleV1](packages/research-bundle/README.md) é um pacote aditivo independente.
SnapshotV1 permanece intacto. 57 testes novos do contrato e 60 existentes passaram
localmente em Python 3.13; wheels foram instalados isoladamente. A nova matriz CI
foi configurada, não executada remotamente. Não há release/push deste candidato.

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

O handoff canônico deste repositório é [ECOSYSTEM_HANDOFF.md](ECOSYSTEM_HANDOFF.md).

Estado vigente: [CURRENT_STATE.md](CURRENT_STATE.md). Registro histórico: em 2026-09-03, Core 3.1.0 e
Ops 4.0.0 estão publicados; Cripto e Stocks estão congelados; somente o EXP-001 do
Brasileirão permanece cientificamente aberto. `ECOSYSTEM_MECHANICAL_STATE.md` é um
snapshot histórico, não uma fonte corrente.


## Implementação arquitetural local — 2026-09-11

As alterações candidatas, seus limites, verificações e rollback estão em [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md). Esta implementação local não publica releases, não atualiza automaticamente os consumidores e não altera os vereditos científicos históricos.
