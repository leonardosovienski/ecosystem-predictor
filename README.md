# ecosystem-predictor

Pacote mínimo de contratos e descoberta de plugins do ecossistema PREDICTORS.

## Escopo canônico

- `ecosystem.contracts`: modelos Pydantic compartilhados para saúde, capacidades,
  status científico/econômico e permissão de capital.
- `ecosystem.registry`: descoberta fail-closed de entry points do grupo
  `predictor.plugins`.

O antigo gateway HTTP, Postgres, Redis, S3/MinIO, scheduler, migrações e telemetria
foram removidos em 2026-08-31 porque não tinham consumidores reais confirmados. Sua
reintrodução exige uma hipótese de uso nomeada, consumidor identificado e teste de
integração correspondente.

## Verificação

```bash
uv sync --all-extras
uv run pytest -q
uv run python scripts/check_real_plugin_integration.py
```

O último comando deve rodar em ambiente com `cripto-predictor`,
`brasileirao-predictor` e `stocks-predictor` instalados simultaneamente. Ele verifica
que os três adapters são carregados, têm identidade distinta e não apresentam colisão
de namespace.

## Regra de packaging

Plugins devem usar pacotes top-level próprios. Nomes genéricos como `src`, `scripts`,
`app` ou `plugin` não podem ser publicados como packages Python compartilhados.

## Fronteira econômica

Este pacote não produz previsões, não executa operações e não autoriza capital. Ele
transporta contratos e evidencia o estado informado pelos domínios.
