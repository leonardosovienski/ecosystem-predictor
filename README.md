# ecosystem-predictor

Contratos compartilhados, descoberta opcional de plugins e referências de integração
do ecossistema PREDICTORS. O Ecosystem explica quem faz o quê, como os projetos se
conectam, qual combinação foi validada e onde estão as fontes. Cada projeto mantém
autoridade sobre seu funcionamento e seus resultados.

## Mapa de leitura

| Necessidade | Fonte canônica |
|---|---|
| Estado de engenharia, combinação testada e limites | [CURRENT_STATE](CURRENT_STATE.md) |
| Composição, responsabilidades e autoridade | [Charter](ECOSYSTEM_CHARTER.md) |
| Instalação, diagnóstico e reprodução | [Runbook](ECOSYSTEM_RUNBOOK.md) |
| Capacidades e interfaces dos projetos | [Core](docs/projects/core.md), [Ops](docs/projects/ops.md), [Cripto](docs/projects/cripto.md), [Brasileirão](docs/projects/brasileirao.md), [Stocks](docs/projects/stocks.md), [CAIN](docs/projects/cain.md) |
| Registros, evidências, decisões e histórico | [Índice documental](docs/HISTORICAL_DOCUMENT_INDEX.md) |

## O que este repositório entrega

- `ecosystem.contracts`: contratos de saúde, capacidades, estados e permissão de capital.
- `ecosystem.registry`: descoberta fail-closed de entry points `predictor.plugins`,
  preservando estados nativos dos domínios e erros de diagnóstico.
- [research-snapshot](packages/research-snapshot/README.md) e
  [research-bundle](packages/research-bundle/README.md): contratos de transporte
  distribuídos separadamente, usados por produtores de evidências e pelo CAIN.

A topologia é polyrepo: sete repositórios, três domínios predictors e dez pacotes
independentes, conforme o [inventário arquitetural](registries/architecture_registry.json).
Não há banco central. O antigo gateway, storage e scheduler do agregador foram
removidos; seu histórico não é instrução de implantação vigente.

## Verificação mínima

Em ambiente de desenvolvimento separado, com Python 3.13:

```sh
uv sync --all-extras
uv run pytest -q
uv run python scripts/check_ecosystem_drift.py --offline-check
```

O modo offline verifica invariantes internas. A comparação com o remoto, o
inventário de pacotes e a instalação conjunta dos três plugins têm requisitos
próprios: veja [verificações no runbook](ECOSYSTEM_RUNBOOK.md#verificações-do-ecosystem).
Plugins devem publicar namespaces próprios; pacotes genéricos como `src`, `scripts`,
`app` ou `plugin` não podem colidir no ambiente compartilhado.

Este pacote não produz previsões, executa trades ou autoriza capital. Testes de
engenharia e transporte não substituem os protocolos científicos dos domínios.
