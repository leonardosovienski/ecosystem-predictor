# Brasileirão — integração do domínio

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Domínio de pesquisa de futebol, proprietário de dados, previsões, evidências e
gates temporais. Mantém a autoridade sobre EXP-001 e suas limitações prospectivas;
o Ecosystem não executa nem reclassifica o experimento.

## Interfaces, dependências e consumidores

O plugin `brasileirao` expõe health/capabilities sem tradução implícita de estados.
Core fornece primitivas científicas; Ops executa workloads autorizados. As fontes
documentais admitidas podem ser exportadas em Snapshot/Bundle para CAIN, preservando
claims, revisão, hashes e relógios científicos. Configuração, Sports/Market DB e
runtime root permanecem sob o domínio; não há banco compartilhado do Ecosystem.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/brasileirao-predictor)
· [README oficial](https://github.com/leonardosovienski/brasileirao-predictor/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

A [integração Brasileirão](../../BRASILEIRAO_INTEGRATION_20260912.md) liga a revisão
testada aos [recibos](../../evidence/brasileirao-main-20260912/README.md) de exportação,
admissão, consulta e recuperação. A [integração Core](../../CORE_INTEGRATION_20260913.md)
e o [manifesto fixado](../../registries/compatibility_candidate.json) documentam a
combinação posterior. Reexportação de claims existentes não é novo cálculo
científico; treino sintético não entra como evidência real. Ciência pertence ao
[registro oficial](https://github.com/leonardosovienski/brasileirao-predictor/blob/main/docs/EVIDENCE_REGISTRY.md).
