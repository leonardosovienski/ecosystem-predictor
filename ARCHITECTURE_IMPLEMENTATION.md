# Implementação arquitetural — 2026-09-11

A topologia corrente está em `registries/architecture_registry.json`: sete repositórios e nove unidades de distribuição. O histórico dos seis projetos e seus estados científicos permanece nos arquivos datados; ele não deve ser usado como inventário arquitetural corrente.

Ecosystem 0.2.0 é um candidato. O registry continua opcional. Nomes duplicados são recusados antes de importar qualquer plugin. `diagnostic_snapshot()` produz `plugin-diagnostics/2`, preserva o payload literal e separa validade contratual do estado científico. A API v1 continua disponível para compatibilidade; respostas de fallback não são aceitas pelo checker de integração real. Um plugin nativo incompatível com v1 deve aparecer como INVALID, sem tradução automática para um veredito científico.

O subpacote independente `predictor-research-snapshot` 1.0.1 mantém ResearchSnapshotV1 e usa somente stdlib/Python >=3.11. `research_snapshot.publication.publish` valida, sincroniza staging e publica por hard link sem substituição. Repetição idêntica recupera o hash; conteúdo diferente no mesmo destino é conflito. Sistemas sem hard links falham explicitamente. Staging órfão após encerramento abrupto não é uma publicação válida.

`scripts/inventory_packages.py` exige sete checkouts explícitos e inventaria também `packages/*/pyproject.toml`, dependências, versão de Python, arquivos e wheels por hash. Não confunde HEAD/base suja, observação de main e compatibilidade testada. Não abre bancos ou importa código dos domínios.

Validação: 56 testes do pacote raiz; 12 testes do exportador consumidor, incluindo falha antes da publicação e recuperação. Wheels do registry e do contrato foram gerados separadamente. A matriz de plugins v1 deve permanecer vermelha quando encontrar estados incompatíveis; não é um gate de ciência nem obrigação de coinstalar os domínios.

Rollback: versões anteriores permanecem distribuíveis em ambientes separados; os bytes das publicações V1 continuam legíveis pelo contrato 1.0.0 usado no CAIN. Nenhum registry histórico foi recertificado por esta implementação.

As releases dos sete repositórios estão em `registries/released_architecture.json`, com hashes verificados por download público. O guia de instalação, intercâmbio e recuperação está em [ECOSYSTEM_RUNBOOK.md](ECOSYSTEM_RUNBOOK.md).

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.


A CI 34631343634 aprovou também a instalação conjunta dos seis wheels publicados, verificando SHA-256 de cada distribuição e o comportamento dos três plugins. O recibo de integração publicado e o intercâmbio CAIN sem origem estão em `evidence/architecture-20260911/`.
