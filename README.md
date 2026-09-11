# ecosystem-predictor

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

> **Fonte de verdade:** [`CURRENT_STATE.md`](CURRENT_STATE.md) e `registries/`.
> Documentos FINAL/CLOSURE/AUDIT antigos são históricos e não definem o estado atual.

> **Estado reconciliado em 2026-09-06:** Core **3.2.0**, Ops **4.1.0** e os três
> predictors econômicos descobertos sem colisão pelos entry points namespaced.
> Brasileirão e cripto consomem Core/Ops; Stocks consome Core e ainda não declara
> Ops. Os pins não são uniformes de propósito: Brasileirão em Core 3.2.0/Ops 4.1.0,
> Cripto em Core **3.0.0** (bump é trabalho, não troca de pin — ver
> `PENDENCIAS_ABERTAS.md` CR-01) e Ops 4.1.0, Stocks em Core 3.2.0.
> O inventário mecânico em `ECOSYSTEM_MECHANICAL_STATE.md` é snapshot de
> 2026-09-01 e está superado quanto a versões.

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
uv run python scripts/check_ecosystem_drift.py          # registries x seis repos reais
uv run python scripts/check_ecosystem_drift.py --offline-check   # só invariantes, sem rede
```

`check_ecosystem_drift.py` responde à pergunta que este repositório existe para
responder: **o que os registries afirmam ainda é verdade?** Falha quando versão, pin
ou atestado divergem do `main` real; SHA de `main` movido vira apenas aviso, porque
muda a cada merge legítimo. Roda no CI a cada push e **diariamente** — o drift não
precisa de commit aqui para acontecer, basta outro repositório se mover. Sem rede,
use `--from-clones /caminho` para conferir a partir de clones locais.

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

Os gates econômicos permanecem domain-owned: futebol e cripto estão integrados em
shadow (cripto opt-in), enquanto ações possui apenas a primitiva ainda não conectada
ao backtest congelado. O agregador não transforma nenhum desses estados em permissão
de capital.


## Implementação arquitetural local — 2026-09-11

As alterações candidatas, seus limites, verificações e rollback estão em [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md). Esta implementação local não publica releases, não atualiza automaticamente os consumidores e não altera os vereditos científicos históricos.
