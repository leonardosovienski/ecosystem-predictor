# Contrato canônico dos predictors econômicos

Autoridade de escopo: `ECOSYSTEM_CHARTER.md`.

Este contrato vale para `cripto-predictor`, `brasileirao-predictor` e `stocks-predictor` e existe para impedir que estados científicos, preditivos, econômicos e operacionais sejam confundidos.

## Superfície mínima

Todo predictor canônico deve ser descobrível pelo entry-point group `predictor.plugins` e expor:

- `domain`;
- `health()` — somente saúde operacional;
- `capabilities()` — capacidades e estados de governança;
- ausência de `predict()` é válida para domínio ainda em pesquisa.

A falta de informação falha fechada: estado desconhecido não vira sucesso e `capital_permission` assume `FORBIDDEN`.

## Estados ortogonais

`scientific_status` responde se existe evidência científica sobre a hipótese.

`predictive_status` responde se existe capacidade preditiva contra o benchmark adequado e, separadamente, evidência prospectiva.

`economic_status` responde se a previsão foi transformada em oportunidade economicamente mensurável depois de preço/custos.

`operational_status` responde se os jobs e fontes necessários estão saudáveis.

`capital_permission` é uma decisão explícita; nenhum outro estado a promove implicitamente.

## Regra econômica comum

A unidade comparável entre domínios não é accuracy, Brier, RPS, correlação ou quantidade de rallies. A trilha econômica canônica é:

`informação disponível no momento -> forecast -> quote/preço disponível -> decisão -> execução -> settlement -> P&L líquido`.

Resultados podem ter métricas científicas específicas do domínio, mas qualquer claim de lucro precisa ser reconciliável com essa trilha.

## NO OPPORTUNITY

`NO_OPPORTUNITY` é um resultado válido. Um predictor não é obrigado a emitir decisão econômica quando seu gate não encontra edge. O contrato expõe `supports_no_opportunity=true` por padrão para evitar pressão arquitetural para fabricar picks.

## Execução humana

No modo atual, recomendação e execução humana são entidades diferentes. A auditoria deve separar:

1. resultado econômico da recomendação conforme a política registrada;
2. resultado efetivamente executado pelo operador, com preço/timing/tamanho reais.

Uma execução humana diferente da recomendação não deve reescrever retrospectivamente a qualidade do predictor.

## Gate mínimo para promoção econômica

Nenhum domínio pode ser classificado como `ECONOMICALLY_VALIDATED` apenas por melhoria preditiva retrospectiva. A promoção exige evidência prospectiva registrada antes do outcome e settlement líquido auditável em quantidade suficiente segundo o protocolo do próprio domínio.

Este arquivo não decide os estados atuais dos três predictors; os adapters e documentos científicos de cada domínio fornecem evidência. O Ecosystem valida o vocabulário e agrega sem inventar promoção.
