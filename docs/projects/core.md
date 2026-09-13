# Core — capacidades compartilhadas

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Biblioteca científica independente para contratos científicos, causalidade temporal,
medição e avaliação prequential. As capacidades compartilhadas servem aos domínios;
Core não escolhe estratégia, sizing, gate econômico ou permissão de capital.

## Interfaces, dependências e consumidores

Os domínios importam explicitamente `predictor_core.contracts.scientific` e
`predictor_core.measurement`. Entram dados/contratos fornecidos pelo chamador;
saem medidas e resultados dos controles definidos pela biblioteca. Não requer
processos dos predictors, Ops ou CAIN. O Ecosystem verifica o wheel distribuído
fora da fonte; CAIN consome evidência transportada, sem dependência direta do Core.

## Componentes e capacidades principais

Famílias públicas: `contracts`, `data`, `kernel`, `measurement` e `testing`.
Incluem Trial Registry V2, ciclo de coleta, qualidade de fontes, replay e avaliação.
A fachada `src/predictor_core/__init__.py` e `docs/TRIAL_REGISTRY_V2.md` no
repositório oficial delimitam as APIs; disponibilidade não valida um experimento.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/core-predictor)
· [README oficial](https://github.com/leonardosovienski/core-predictor/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

A [integração Core](../../CORE_INTEGRATION_20260913.md) identifica a main validada,
a fonte distinta da release e os testes funcionais do wheel. A combinação é a do
[manifesto fixado](../../registries/compatibility_candidate.json), sustentada pelo
[recibo](../core_integration_20260913/receipt.json). A aprovação do controle sintético
não substitui atestado operacional nem valida resultados econômicos dos domínios.
