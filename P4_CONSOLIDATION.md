# P4 — consolidação temporal F1 × LoL × CS

Registro factual aprovado em **2026-08-11**. A consolidação usou somente os
pilotos mesclados, os arquivos presentes em seus HEADs e execuções identificadas.
O estado humano aprovado é:

> `P4_COMPLETED_NO_CORE_CHANGE`

## Proveniência

| Domínio | Piloto | Merge / HEAD validado | CI pós-merge | Python efetivo |
|---|---|---|---|---|
| F1 | PR [#9](https://github.com/leonardosovienski/f1-predictor/pull/9), commit `52b0fd845f93`; correção de matriz PR [#10](https://github.com/leonardosovienski/f1-predictor/pull/10), commit `426472f27c30` | `d6e54cc9997b8e00648556bb3216ddd58cab7e9f` | [31486487656](https://github.com/leonardosovienski/f1-predictor/actions/runs/31486487656), verde | pytest em CPython 3.13.14 e 3.14.6; 238 testes em cada |
| LoL | PR [#9](https://github.com/leonardosovienski/lol-predictor/pull/9), commit `e88ff1a5debd` | `17425a75101cb1b9e412a30baa850865e5822ffc` | [31488598943](https://github.com/leonardosovienski/lol-predictor/actions/runs/31488598943), verde | pytest em CPython 3.13.14 e 3.14.6; 174 testes em cada |
| CS | PR [#11](https://github.com/leonardosovienski/cs-predictor/pull/11), commit `c27b5ce25719` | `f7bb214114503a7c29fdd8b56535b2155f1a87d6` | [31490882633](https://github.com/leonardosovienski/cs-predictor/actions/runs/31490882633), verde | pytest em 3.13.13 nos dois jobs; smoke do wheel em 3.13.13/3.14.5 |

## Resultado factual

- P4-A/F1, P4-A.1, P4-B/LoL e P4-CS foram concluídas e validadas.
- Os três pilotos usam fixtures sintéticas, goldens versionados e testes
  positivos e negativos. Divergência do golden causa falha determinística;
  isso não torna o arquivo absolutamente imutável.
- Os testes rejeitam casos construídos de relógio naive, previsão ou resultado
  temporalmente inválido, maturação precoce, vínculo/identidade incompatível,
  vazamento pós-evento ou replay ligado ao input errado, conforme a cobertura
  específica de cada consumidor.
- `PredictionPoint` e `replay` já atendem ao contrato comum pertencente ao Core:
  timestamps timezone-aware, ordem emissão/maturação, consulta de maturidade e
  replay por prefixo temporal.
- Cutoff, publicação ou recuperação do resultado, identidade, vínculo entre
  artefatos, métricas e seleção dos campos hasheados permanecem locais.
- JSON canônico e hashing são um padrão reutilizável, mas a P4 não encontrou
  semântica uniforme suficiente para uma nova API pública no Core.
- Brasileirão e Cripto não são necessários para encerrar a P4. Nenhum piloto
  adicional foi iniciado.

## Retificação da matriz CS

O workflow pós-merge do CS instalou Python 3.14.5 no job `quality (3.14)`, mas
os logs mostram `uv sync` e pytest em Python 3.13.13. Apenas o smoke do wheel
usou efetivamente Python 3.14.5. Assim, a alegação de pytest remoto em 3.14 foi
classificada como `CONTRADICTED` (`P4E008`).

Uma execução local separada no commit do piloto passou 419 testes em Python
3.14.7 e é `VERIFIED_BY_EXECUTION` (`P4E009`), não `VERIFIED_FROM_CI`. A
limitação não reabre a P4, mas permanece como dívida técnica e limite de
evidência. O CS não deve ser descrito como integralmente testado remotamente
em Python 3.14.

## Limites

A P4 demonstra propriedades de engenharia das fixtures e implementações
testadas. Ela não demonstra:

- instante real de publicação externa — `result_available_at` é fornecido nos
  pilotos F1/LoL e `result_retrieved_at_utc` do CS mede recuperação;
- reprodução de datasets ou resultados científicos oficiais;
- qualidade preditiva, equivalência estatística das métricas ou tese integral;
- valor econômico, operação ao vivo ou ausência universal de leakage.

## Rastreabilidade P4

| Evidências | Conteúdo | Classificação predominante |
|---|---|---|
| `P4E001–P4E009` | PRs, commits, merges, CI e Python efetivo | `VERIFIED_FROM_GIT`, `VERIFIED_FROM_CI`, `CONTRADICTED`, `VERIFIED_BY_EXECUTION` |
| `P4E010–P4E012` | primitivas Core 2.2.x anteriores à P4 | `VERIFIED_FROM_CODE` |
| `P4E013–P4E021` | adapters, testes negativos, goldens e replay | `VERIFIED_FROM_CODE`, `VERIFIED_FROM_CI` |
| `P4E022–P4E026` | diferenças de cutoff, publicação, identidade, métricas e hashes | `VERIFIED_FROM_CODE` |
| `P4E027–P4E032` | limitações de reprodução, ciência e operação | `DOCUMENTED_NOT_EXECUTED`, `VERIFIED_FROM_CODE` |
| `P4E033–P4E034` | dispensa de piloto adicional e atualização documental | `DOCUMENTED_NOT_EXECUTED`, `NOT_APPLICABLE` |

A tabela completa `P4E001–P4E034` pertence ao relatório de consolidação que
fundamentou esta atualização. Este documento registra seu resultado factual;
não substitui os arquivos e logs dos commits acima.

## Decisão

| Item | Classificação corrente |
|---|---|
| `PredictionPoint`, `is_mature`, `replay`/`PastView` | `CORE_CONTRACT_ALREADY_SUFFICIENT` |
| cutoff, disponibilidade, identidade e vínculo | `CONSUMER_LOCAL` / `DOMAIN_SPECIFIC` |
| métricas nativas | `DOMAIN_SPECIFIC` |
| publicação versus recuperação | `SEMANTIC_CONFLICT` enquanto não explicitada localmente |
| canonicalização/hash | `REUSABLE_PATTERN_NOT_CORE_READY` |

Nenhuma mudança em Core, Ops, consumidores, ciência, dados, dependências ou
workflows foi realizada por esta atualização documental.
