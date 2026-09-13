> **Brasileirão — entrega consolidada em main:** [versões, integração CAIN, CI, backups e reprodução](BRASILEIRAO_INTEGRATION_20260912.md). A aprovação é técnica/documental; ciência, produção e capital conservam seus gates próprios.

> **Crypto — integração atual:** [combinação, CI e limites](CRYPTO_INTEGRATION_20260912.md). Os controles sintéticos de engenharia não reemitem os vereditos científicos das tabelas históricas abaixo.

> **Stocks — atualização de software:** [integração observada em 12/09](STOCKS_INTEGRATION_20260912.md). A linha histórica H1–H19 abaixo não define a prontidão atual do runtime. Estados científicos não foram recertificados.

# ecosystem-predictor

<!-- DOC-SYNC-20260912 -->
> **Continuidade de publicação:** [estado e evidências atuais](PUBLICATION_STATUS_20260912.md). A combinação Crypto/Ecosystem/CAIN foi integrada e validada em main. As referências anteriores à branch candidata e à falha Linux são históricas; não definem o resultado desta combinação. Estados científicos e releases mantêm suas fontes próprias.
<!-- /DOC-SYNC-20260912 -->


## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

> **Fonte de verdade:** [`CURRENT_STATE.md`](CURRENT_STATE.md) e `registries/`.
> Documentos FINAL/CLOSURE/AUDIT antigos são históricos e não definem o estado atual.

A arquitetura atual, os pacotes publicados e as instruções de uso estão em
[ECOSYSTEM_RUNBOOK.md](ECOSYSTEM_RUNBOOK.md) e
[released_architecture.json](registries/released_architecture.json).
Os snapshots mecânicos/científicos de seis projetos de 01–06/09 são históricos;
a topologia atual contém sete repositórios e nove distribuições independentes.

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
