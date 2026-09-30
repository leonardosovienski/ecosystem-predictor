# Estado canônico atual

> **Atualização 2026-09-30.** A combinação corrente do stack, o que foi validado em conjunto e o estado do ciclo de
> qualificação D-27 estão em [ETAPA_B_INTEGRATED_STACK_20260928.md](ETAPA_B_INTEGRATED_STACK_20260928.md) (seção
> "Atualização de 2026-09-30"). Wheels publicadas: core 3.2.1, ops 4.2.2rc1, ecosystem 0.2.1, protocolo 2.0.0rc2,
> transporte 0.1.0rc7, snapshot 1.0.2rc1, bundle 1.0.1rc1, cain 0.4.13rc15, cripto 1.2.0rc4, brasileirão 0.3.0rc5,
> stocks 0.3.0rc3 (`registries/released_architecture.json`; `registries/compatibility_candidate.json` aponta para os
> commits das tags). As três distribuições de domínio instaladas juntas com o resto do stack carregam no registry
> isoladas, com capital `FORBIDDEN` (`scripts/check_real_plugin_integration.py`, `RELEASED_WHEELS=1`, 2026-09-30).
> O texto abaixo (revisão de 13/09/2026) continua válido para contratos, registry e recibos históricos.

**Revisão:** 13/09/2026. A [reconciliação de fidelidade](docs/maintenance/fidelity-20260913.md)
corrige representação, expiração e mensagens de erro, com regressões automatizadas.
A combinação fixada e seus recibos permanecem preservados; fonte corrigida não
significa nova release ou atualização automática de instalações.

## Estado e autoridade por assunto

| Dimensão | Fonte e interpretação |
|---|---|
| Código em `main` | Contratos, registry opcional, ResearchSnapshotV1 e ResearchBundleV1 incorporados. `git ls-remote origin refs/heads/main` informa a ponta publicada; cada SHA tem sua própria CI. |
| Topologia | [architecture_registry.json](registries/architecture_registry.json): sete repositórios, três domínios predictors e dez pacotes independentes. [Charter](ECOSYSTEM_CHARTER.md) define os limites. |
| Releases e artefatos | [released_architecture.json](registries/released_architecture.json): fontes, URLs e hashes das distribuições registradas. Não é inventário da instalação operacional nem consulta permanente de últimas releases. |
| Combinação testada | [compatibility_candidate.json](registries/compatibility_candidate.json), [integração Core](CORE_INTEGRATION_20260913.md) e [recibo](docs/core_integration_20260913/receipt.json). Pins não acompanham `main` automaticamente. |
| Instalação operacional | Autoridade do respectivo projeto; para CAIN, [estado oficial](https://github.com/leonardosovienski/cain/blob/main/ESTADO_DO_PROJETO.md). Os recibos de instalação deste repositório descrevem as revisões e datas que testaram. |
| Ciência e economia | Protocolos e evidências dos domínios, acessíveis nas fichas abaixo. [harness_registry.json](registries/harness_registry.json) preserva atestados datados; não certifica versões posteriores. |
| Operação e capital | Permissões pertencem aos domínios e à decisão humana explícita. Nenhuma autorização resulta desta organização ou de CI verde. |

A integração Ecosystem `3cfb74bef126c421424c08cc774034b42cae5cd4` tem
[CI](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765563374)
e [segurança](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765563366)
aprovadas. Essa evidência continua vinculada àquela revisão. A baseline documental
acima também tem [CI própria](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765919043).

## Projetos e reprodução

[Core](docs/projects/core.md) · [Ops](docs/projects/ops.md) ·
[Cripto](docs/projects/cripto.md) · [Brasileirão](docs/projects/brasileirao.md) ·
[Stocks](docs/projects/stocks.md) · [CAIN](docs/projects/cain.md).

Cada ficha delimita responsabilidades, interfaces e evidência de integração sem
duplicar o manual do projeto. O [runbook](ECOSYSTEM_RUNBOOK.md) contém os comandos
do Ecosystem. Checkout canônico neste PC: `C:/CAIN/contrato`, branch `main`.

## Manutenção e histórico

Antes de atualizar um registro, confronte sua autoridade, revisão e contexto.
Observe drift real, corrija apenas o escopo afetado e preserve pins e evidências
até nova validação explícita. Não retome ações de auditorias antigas por inferência.

As tabelas e ações de 06/09 foram separadas em
[registro histórico](docs/archive/current-state-20260906.md). O
[índice documental](docs/HISTORICAL_DOCUMENT_INDEX.md) classifica registros,
procedimentos e auditorias. O [registro desta organização](docs/maintenance/organization-20260913.md)
contém baseline, classificação de branches, recuperação e validação.
