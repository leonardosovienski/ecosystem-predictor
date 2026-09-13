# HANDOFF — ecosystem-predictor

**Continuidade de engenharia:** [estado e navegação atuais](CURRENT_STATE.md),
[integração do Core](CORE_INTEGRATION_20260913.md) e
[índice documental](docs/HISTORICAL_DOCUMENT_INDEX.md). Core 3.2.1 em main
`9bf43ef`; a integração Ecosystem `3cfb74b` tem CI e segurança aprovadas.
As seções datadas abaixo conservam a identidade da execução original.

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

## Reconciliação de inventário e documentação — 13/09/2026

O inventário corrente inclui dez pacotes em sete repositórios, incluindo ResearchBundle. O gate compara os caminhos declarados com metadados reais da fonte local e dos candidatos remotos imutáveis. O runbook distingue Ops 4.2.1 publicado, CAIN 0.4.9 observado localmente e combinações históricas de integração.

As integrações documentais de Brasileirão e Stocks com CAIN já existem, conforme os recibos próprios ligados acima. A rodada final do core integrou o PR29 e repetiu os três percursos em uma combinação fixada: Crypto com atestado sintético novo, BR e Stocks com documentos/metadados admitidos. Veja CORE_INTEGRATION_20260913.md; os recibos anteriores continuam históricos. Qualquer gate adicional precisa de requisito contratual e análise de impacto explícitos; evidência histórica não certifica outro SHA automaticamente.
