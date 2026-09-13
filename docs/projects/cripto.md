# Cripto — integração do domínio

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Domínio de pesquisa cripto, proprietário de dados, hipóteses, protocolos e
resultados. O Ecosystem mantém a interface e a proveniência da integração;
o estado científico e o escopo de pesquisa pertencem às fontes do Cripto.

## Interfaces, dependências e consumidores

O adapter é descoberto em `predictor.plugins`, com identidade pública `cripto`
e domínio `crypto`; fornece health/capabilities com estados nativos. Core fornece
capacidades científicas e Ops contratos de execução. O pacote independente
`crypto-research-export` admite fontes e hashes explícitos e publica Snapshot
para consumo autorizado pelo CAIN. Dados e origem científica ficam no domínio.

## Componentes e capacidades principais

Além do adapter, o domínio mantém ingestão/DPL, Feature Store, pipeline com LLM
e ferramentas de pesquisa offline. O exportador em `packages/research-export`
também publica Bundle pelo extra `bundle` (contrato 1.0.0). Consulte seu manifest
e documentação no projeto. Fontes, grants e autorização de execução continuam
explícitos; famílias históricas congeladas não resumem toda a pesquisa posterior.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/cripto-predictor)
· [README oficial](https://github.com/leonardosovienski/cripto-predictor/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

A [integração Cripto](../../CRYPTO_INTEGRATION_20260912.md) conserva os SHAs e a CI
da rodada de 12/09; a [integração Core](../../CORE_INTEGRATION_20260913.md) descreve
a combinação posterior e seu controle sintético até CAIN. O
[manifesto fixado](../../registries/compatibility_candidate.json) identifica o
candidato dos plugins. Consulte também [proveniência dos wheels](../CRYPTO_WHEEL_COMPATIBILITY.md)
e [fontes científicas do domínio](https://github.com/leonardosovienski/cripto-predictor/blob/main/docs/EVIDENCE_REGISTRY.md).
Transporte e controles sintéticos não reabrem hipóteses nem concedem capital.
