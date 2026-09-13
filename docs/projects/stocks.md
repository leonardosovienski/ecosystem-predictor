# Stocks — integração do domínio

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Domínio de pesquisa quantitativa de ações, proprietário de hipóteses, dados,
protocolos e resultados. Seus estados científicos/econômicos são definidos pelo
projeto, sem promoção automática por engenharia ou transporte documental.

## Interfaces, dependências e consumidores

O plugin `stocks` fornece health/capabilities no grupo `predictor.plugins`,
consome Core e conserva estados nativos. Exportadores explícitos produzem Snapshot
de estado e Bundle de metadados/referências para admissão no CAIN. O teste de
plugins é executado em Linux; não instalar o runtime Stocks no Windows desta
estação. Dados, preços e backtests não são centralizados no Ecosystem.

## Componentes e capacidades principais

CLI, banco gerido, ingestão COTAHIST por hash, inspeção/replay e backup/restauração
são descritos em `STOCKS_CURRENT_STATE.md`. H21/H22 e protótipos de pesquisa
permanecem separados do runtime. H21 é pesquisa histórica condicional, não
lucro pessoal/futuro certificado. As entradas e limites pertencem ao domínio.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/stocks-predictor)
· [README oficial](https://github.com/leonardosovienski/stocks-predictor/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

A [integração Stocks](../../STOCKS_INTEGRATION_20260912.md) preserva a combinação
da instalação principal, hashes e recuperação offline. A combinação posterior
com Core e CAIN isolado está na [integração Core](../../CORE_INTEGRATION_20260913.md)
e no [manifesto fixado](../../registries/compatibility_candidate.json); não substitui
o aceite anterior. O percurso Bundle recebeu metadados, sem preços/objetos externos,
com licença UNKNOWN e geração negada. O
[estado científico oficial](https://github.com/leonardosovienski/stocks-predictor/blob/main/STOCKS_CURRENT_STATE.md)
prevalece sobre resumos históricos do registry.
