# Ops — contratos operacionais

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Runner genérico para jobs locais, idempotência, leases, auditoria e reconciliação.
Executa workloads definidos pelo proprietário; não decide a verdade científica
ou a rentabilidade de uma hipótese.

## Interfaces, dependências e consumidores

A CLI `predictor-ops` recebe configuração de jobs e comandos; produz estado de
execução, tentativas e proveniência sob o runtime root do proprietário. O schema
operacional genérico e os gates de política/risco delimitam jobs econômicos.
Cripto e Brasileirão são consumidores operacionais; os projetos permanecem
independentes, com bancos e agendamentos próprios. Não compartilhar runtime root
entre runners incompatíveis; tentativa de efeito incerto exige reconciliação.

## Componentes e capacidades principais

A configuração de jobs, proveniência instalada e limites do backend local estão
em `docs/OPERATIONS_CONTRACT.md` do projeto. Observabilidade OTLP é opcional
(`predictor-ops[otel]`); o runner genérico não cria agendamentos por si só.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/predictor-ops)
· [README oficial](https://github.com/leonardosovienski/predictor-ops/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

A [integração Ops](../../OPS_INTEGRATION_20260913.md) registra fonte, distribuição,
CI e implantação local datada. O [manifesto de compatibilidade](../../registries/compatibility_candidate.json)
fixa o artefato usado pelo Ecosystem. Os recibos não significam ativação de
agendamentos ou autorização econômica. Procedimentos e estado local vigente
pertencem ao [relatório oficial](https://github.com/leonardosovienski/predictor-ops/blob/main/docs/stabilization-20260912/REPORT.md)
e à [implantação](https://github.com/leonardosovienski/predictor-ops/blob/main/docs/DEPLOYMENT_20260913.md).
