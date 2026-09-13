# Core — integração da main validada no Ecosystem

Estado de engenharia conferido em 13/09/2026. O Core integra o ecossistema como biblioteca científica compartilhada pelos domínios, com identidade, distribuição e compatibilidade registradas aqui.

## Fonte e artefato aplicáveis

- Main do [core-predictor](https://github.com/leonardosovienski/core-predictor): `9bf43efe92459a0b484cac00f51170b2c70d420f`, após [PR29](https://github.com/leonardosovienski/core-predictor/pull/29).
- [CI da main](https://github.com/leonardosovienski/core-predictor/actions/runs/34740848667) e [compatibilidade dos três plugins](https://github.com/leonardosovienski/core-predictor/actions/runs/34740848668): aprovadas no SHA acima.
- Wheel oficial `predictor_core-3.2.1-py3-none-any.whl`: SHA256 `10ef42f34ace8bb2df5f83ff7de2ceec79b035a25ea0a690e8942bd60d2fb4e3`.
- A fonte da release continua `7bb212cfa06333886e11e849b209c5aab801c04b`. A main posterior acrescentou gates de CI e documentação; os 41 arquivos de runtime coincidem byte a byte com a wheel publicada. Não houve nova release ou substituição de asset.

O [registry de projetos](registries/project_registry.json) registra a main validada. O [manifesto de releases](registries/released_architecture.json) preserva a fonte real do artefato publicado. O [manifesto de compatibilidade](registries/compatibility_candidate.json) usa a combinação testada abaixo. [Recibo durável desta integração](docs/core_integration_20260913/receipt.json) e [recibo original dos plugins](docs/core_integration_20260913/compatibility-receipt.json).

## Combinação fixada e resultados

| Projeto | SHA testado |
|---|---|
| Crypto 1.1.0 | `59f6cf80d4a95153efa159c8b6e0d7d5e7f540ff` |
| Brasileirão 0.2.0 | `0f69ba8a1da744eb4239b680fc0389f9dc631987` |
| Stocks 0.2.0 | `3066321e599ee15dd0ace4167d2791545ce6eb95` |
| CAIN 0.4.10 | `203048c752973cd730a18345a739c29413eede12` |

Ops publicado 4.2.1, Snapshot 1.0.1 e Bundle 1.0.0 completam a combinação. Commits concorrentes posteriores não recebem aprovação automática. Esses pins identificam fontes de teste; não afirmam novas releases dos consumidores nem atualização da instalação operacional do CAIN.

No clone novo da main do Core: 278 testes e 86% de cobertura, Ruff, Pyright, fronteiras de imports e build aprovados. Python 3.13 obrigatório; 3.14 experimental aprovado na CI. Oito testes funcionais por wheel instalada fora dos checkouts, com verificação de origem e bytes. Crypto: 40 testes funcionais; Brasileirão: 20; Stocks: CI Linux do mesmo SHA e teste conjunto de plugins. CAIN: 56 testes de Bundle/recuperação. Zero skips nas rodadas finais; dois warnings de depreciação no CAIN.

O Ecosystem agora possui o job `Core official wheel functional integration`: obtém o verificador do SHA fixado no recibo, baixa a wheel oficial com conferência de hash e executa as oito verificações em ambiente mínimo externo. O job de três plugins usa o manifesto atualizado. O resultado da CI deste commit Ecosystem é uma execução separada da CI anterior do Core; não se transfere aprovação entre SHAs.

## Publicação da integração no Ecosystem

A integração foi publicada no commit
`3cfb74bef126c421424c08cc774034b42cae5cd4` da main do Ecosystem.
A [CI 34765563374](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765563374)
aprovou o teste funcional da wheel oficial, os três plugins, as distribuições
publicadas, o inventário e os contratos. A
[segurança 34765563366](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765563366)
também passou. Foram 79 testes locais e oito casos funcionais da wheel no novo job.

Esse recibo identifica o commit de integração. Atualizações posteriores somente
em Markdown preservam sua proveniência; o resultado de cada novo SHA deve ser
consultado na própria CI. Nenhum recibo antigo recebe um SHA novo por substituição.

## Evidências até o CAIN

- Crypto executou um controle do domínio com Core instalado, produziu um atestado sintético novo e o exportou pelo contrato admitido.
- Brasileirão reexportou três claims reais de `docs/EVIDENCE_REGISTRY.md`, preservando estados e relógios científicos.
- Stocks reexportou duas entidades de metadados e três relações admitidas do recibo versionado.

Nos três percursos passaram aprovação/admissão, segunda importação idempotente, rejeição de adulteração e consulta/verify offline, em bases novas isoladas. Identidades dos bundles e hashes dos recibos constam do recibo desta página. Somente Crypto demonstra cálculo Core → evidência nova; BR e Stocks demonstram seus transportes documentais existentes. Não são três novas validações científicas. O CAIN permanece consumidor dos contratos de evidência, sem dependência direta de Core.

## Arquivos neste PC e continuidade

| Local | Conteúdo |
|---|---|
| `C:/PREDICTORS/core-predictor` | Core canônico, main `9bf43ef`, checkout limpo e remoto somente main na conferência |
| `C:/CAIN/contrato` | Ecosystem canônico, esta documentação e seus registries |
| `C:/PREDICTORS/work/core-completion-20260913` | Manifesto, clone novo, testes, CI, comparação de wheels e recibos de consolidação |
| `C:/PREDICTORS/work/core-completion-20260913/pre-cleanup` | Backup final restaurado; acesso restrito; não publicado |
| `C:/CRIPTO/operacao/relatorios/core-completion-20260913/pinned` | Controle sintético, 40 testes e identidade da wheel |
| `C:/BRASILEIRAO/work/core-completion-20260913` | Fonte fixada, 20 testes e integração final |
| `C:/STOCKS/work/core-completion-final-20260913` | Recibo de transporte final; nenhuma instalação de Core/Stocks no Windows |
| `C:/CAIN/work/core-completion-20260913` | CAIN isolado, wheel, 56 testes e transporte Crypto |
| `C:/CAIN/work/core-ecosystem-integration-20260913` | Backup e verificação desta organização no Ecosystem |

Os 11 arquivos locais selecionados foram encontrados e tiveram seus hashes recalculados: [inventário conferido](docs/core_integration_20260913/files.json). Os arquivos foram alinhados no checkout canônico do Ecosystem. Evidências privadas permanecem nas raízes de seus projetos; os dois recibos públicos desta página contêm a combinação e resultados de engenharia. A consolidação já concluída do Core removeu nove branches remotas e duas locais com proteção atômica por SHA, após recuperação comprovada dos backups e clone novo. Tags preservadas. Esta organização não limpa branches do Ecosystem ou dos outros projetos.

Para reproduzir plugins e distribuição, use o [runbook](ECOSYSTEM_RUNBOOK.md) e os jobs versionados de CI. Para reexecutar integração, os runners exigem destinos novos; não reutilize bancos ou recibos anteriores. Os atestados científicos em `harness_registry.json` e as claims históricas continuam com suas versões e SHAs de origem.

A revisão auxiliar de IA no PR do Core falhou por modelo não suportado antes da análise. Os gates obrigatórios e CodeQL passaram; nenhum controle foi desativado. Essa limitação permanece no recibo. Engenharia não comprova lucro, hipóteses ou qualidade científica; não houve ativação operacional ou autorização de capital.
