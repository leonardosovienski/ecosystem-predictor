# Ops — integração, implantação e localização conferidas

Estado conferido em 13/09/2026: **Ops 4.2.1 registrado no Ecosystem, publicado e instalado nos ambientes locais de Cripto e Brasileirão**. O Ecosystem organiza contratos, versões, referências e evidências. O código do runner continua no repositório independente [predictor-ops](https://github.com/leonardosovienski/predictor-ops), conforme a topologia polyrepo existente.

## Onde está registrado

| Registro | Conteúdo do Ops |
|---|---|
| [project_registry.json](registries/project_registry.json) | Identidade predictor-ops, versão 4.2.1 e referência da main observada |
| [architecture_registry.json](registries/architecture_registry.json) | Runner genérico independente, sem dependência obrigatória dos domínios |
| [released_architecture.json](registries/released_architecture.json) | Tag, fonte imutável, URL, hash do wheel e CI da release |
| [compatibility_candidate.json](registries/compatibility_candidate.json) | Dependência compartilhada 4.2.1 com URL/hash exatos; consumidores em revisões fixadas |
| [ECOSYSTEM_RUNBOOK.md](ECOSYSTEM_RUNBOOK.md) | Papel, entrada e ambientes independentes |

Os manifestos de release e compatibilidade preservam as revisões testadas. Commits posteriores apenas de documentação não substituem silenciosamente esses pins. Os campos científicos dos domínios permanecem sob a autoridade de seus próprios protocolos.

## Identidades e evidências

- Release [v4.2.1](https://github.com/leonardosovienski/predictor-ops/releases/tag/v4.2.1), fonte `ddd91444282569ae8282e7c96e0ec372ef4e5144`.
- Wheel `predictor_ops-4.2.1-py3-none-any.whl`, 26093 bytes, SHA256 `da4fa540703879669caba919521ec7d3c33734b5d57781122823df8817346f0e`.
- [Estabilização, regressões, integrações e limpeza Git](https://github.com/leonardosovienski/predictor-ops/blob/main/docs/stabilization-20260912/REPORT.md).
- [Implantação local, verificações e recuperação](https://github.com/leonardosovienski/predictor-ops/blob/main/docs/DEPLOYMENT_20260913.md).
- [CI da fonte publicada](https://github.com/leonardosovienski/predictor-ops/actions/runs/34733345409) e [verificação pós-publicação](https://github.com/leonardosovienski/predictor-ops/actions/runs/34733366187): aprovadas.
- [CI do recibo de implantação](https://github.com/leonardosovienski/predictor-ops/actions/runs/34738564304): aprovada para `f6042688511c82e52573c9965404584046f094e1`.
- Main Ops observada nesta conferência: `d1aa309a6f899b237ec725e03b4ab7e3f82913c5`, que corrige somente a descrição da implantação no README. [CI 34739900590](https://github.com/leonardosovienski/predictor-ops/actions/runs/34739900590) e CodeQL aprovados também nessa revisão.

## Arquivos conferidos neste PC

| Local | Finalidade / resultado |
|---|---|
| `C:/PREDICTORS/predictor-ops` | Código e Markdown canônicos do Ops; main local/remota conferida |
| `C:/PREDICTORS/predictor-ops/docs/stabilization-20260912` | Relatório e recibo das oito branches remotas e três locais removidas |
| `C:/PREDICTORS/predictor-ops/docs/DEPLOYMENT_20260913.md` | Recibo da implantação posterior |
| `C:/PREDICTORS/work/ops-final-20260912` | Dois bundles e evidências de estabilização preservados |
| `C:/CRIPTO/pesquisa-20260909/.venv` | Ops 4.2.1 novamente confirmado por metadata e caminho site-packages |
| `C:/BRASILEIRAO/brasileirao-predictor/.venv` | Ops 4.2.1 novamente confirmado por metadata e caminho site-packages |
| `C:/CRIPTO/operacao/relatorios/OPS_DEPLOYMENT_20260913.md` | Recibo local do Cripto |
| `C:/BRASILEIRAO/AUDITORIA/OPS_DEPLOYMENT_20260913.md` | Recibo local do Brasileirão |
| `C:/CRIPTO/work/ops-deploy-20260913` | Wheel conferido, inventários, logs, probes e backup Ops 4.2.0 |
| `C:/BRASILEIRAO/work/ops-deploy-20260913` | Instalação frozen, inventário, logs e probes |
| `C:/CAIN/contrato` | Checkout local deste Ecosystem |

Doze arquivos de entrega/recuperação foram encontrados, medidos e tiveram SHA256 recalculado. O wheel local coincide com o hash publicado; os bundles e backup da instalação coincidem com os hashes dos recibos. [Inventário de arquivos e hashes desta conferência](docs/ops_integration_20260913/files.json), também preservado em `C:/CAIN/work/ops-organization-20260913/files.json`. Essa é uma conferência dos caminhos acessíveis da entrega, não uma varredura de todos os discos ou ambientes do PC.

Nenhuma pasta foi movida ou apagada para organizar a documentação. Evidências e backups ficam nos respectivos projetos; o Ecosystem mantém seus links e identidades. Os Markdown atuais foram reconciliados; registros históricos datados continuam preservados e recebem ligação para este estado posterior.

## Limites operacionais

Os testes da implantação exercitaram o runner instalado e percursos dos consumidores com dados sintéticos. Cripto manteve a instalação editável do consumidor e atualizou somente Ops entre seus 81 pacotes. Brasileirão recebeu ambiente próprio com Python 3.13.15 e 40 pacotes do lockfile. Agendadores, serviços, coletas e operações financeiras não foram ativados. A instalação não revalida resultados científicos nem concede capital.

## Validação desta organização

O verificador existente "scripts/check_ecosystem_drift.py" passou OFFLINE e OFFLINE+ONLINE, com saída zero. A checagem online exibiu apenas avisos informativos de main mais recente em Crypto/Brasileirão; não houve divergência de versão, pin ou atestado. As revisões imutáveis de compatibilidade foram preservadas. Treze links locais introduzidos nos Markdown foram resolvidos e os quatro hashes imutáveis dos recibos foram comparados com os arquivos locais. Mudanças desta rodada são documentais e de metadata do registro Ops; não alteram código, dependências, protocolos ou instalações.
