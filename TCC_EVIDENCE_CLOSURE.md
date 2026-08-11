# Fechamento das evidências para o TCC

**Data:** 2026-08-11  
**Base:** `ecosystem-predictor@eaff4c4afce16424891fe58cfa9d51a99802e5ef`  
**Estado:** `TCC_EVIDENCE_CLOSURE_READY_FOR_HUMAN_REVIEW`

Este documento delimita o que a trajetória do ecossistema permite afirmar na
monografia. Ele não substitui relatórios científicos, não reabre hipóteses
encerradas e não interpreta CI como prova de qualidade preditiva.

## 1. Trajetória consolidada

| Marco | Resultado | Evidência primária |
|---|---|---|
| Rodadas 1A/1B | fatos e análise transversal aceitos | relatórios 1A/1B; E01–E89 |
| F0 | integridade Core/Ops do Brasileirão corrigida | `brasileirao@5a42d6c88298`; CI `31462565846` |
| F1 | estado central reconciliado | ecosystem PR #5; merge `0cde8662714a` |
| P1 | Ecosystem em Ops 3, Core preservado | PR #6; merge `7918698c04d6`; CI `31467366845` |
| P4-A/A.1 | piloto F1 e matriz Python efetiva | `f1@d6e54cc9997b`; CI `31486487656` |
| P4-B | piloto LoL | `lol@17425a75101c`; CI `31488598943` |
| P4-CS | piloto CS | `cs@f7bb21411450`; CI `31490882633` |
| Consolidação P4 | contrato comum; nenhuma mudança Core | `P4_CONSOLIDATION.md`; `P4E001–P4E034` |
| Atualização P4 | decisão registrada centralmente | PR #7; merge `eaff4c4afce1`; CI `31495446445` |

## 2. Contribuições sustentadas

### Arquitetura

O ecossistema separa Core científico, Ops operacional e regras locais dos
consumidores. A P1 demonstra transporte separado de estado operacional e estado
científico. Isso é evidência arquitetural, não confirmação de hipótese.

### Contrato temporal multidomínio

F1, LoL e CS aplicaram adapters experimentais ao contrato existente do Core. A
parte comum exercitada compreende `PredictionPoint`, replay, identidade de
previsão/resultado, cutoff verificável, rejeição de informação tardia,
rejeição de maturação inválida e golden versionado com falha determinística.

Obtenção/publicação, identidade de domínio, vínculos, métricas e seleção de
hashes permaneceram locais. Isso sustenta `P4_COMPLETED_NO_CORE_CHANGE`.

### Engenharia, supply chain e governança

A F0 demonstrou coerência verificável entre workflow, lockfile, checksums e
assets oficiais. WC e os documentos de fechamento preservam resultados
negativos e inconclusivos. CI verde comprova apenas os gates executados.

## 3. Alegações permitidas e limites

| Alegação permitida | Alcance | Limite | Formulação proibida |
|---|---|---|---|
| Há separação entre ciência e operação | arquitetura | não valida modelos | “a tese inteira foi confirmada” |
| Um contrato temporal comum foi exercitado | fixtures F1/LoL/CS | não são datasets oficiais | “todos os domínios estão livres de leakage” |
| Testes detectam violações temporais cobertas | casos dos pilotos | cobertura não é universal | “qualquer leakage é impossível” |
| Goldens protegem os casos versionados | replay determinístico | podem mudar por revisão futura | “goldens são absolutamente imutáveis” |
| Replay reproduz os casos protegidos | inputs identificados | não mede qualidade preditiva | “replay comprova acurácia” |
| Resultados negativos foram preservados | WC e closures | taxonomias são locais | “todos usam o mesmo veredito” |
| CI verifica compatibilidade e supply chain | runs citadas | não reexecuta toda ciência | “CI verde confirma a tese” |
| Versões Core diferentes são deliberadas | P5 | não há ranking de versões | “2.2.1 é melhor para todos” |

## 4. Limitações preservadas

- Fixtures sintéticas não reproduzem datasets oficiais.
- Replay determinístico não demonstra qualidade científica.
- Métricas de domínios diferentes não são automaticamente comparáveis.
- Recuperação de um dado não prova necessariamente sua publicação externa.
- Resultado científico não reexecutado permanece `DOCUMENTED_NOT_EXECUTED`.
- Contrato seguro não demonstra valor econômico ou comportamento ao vivo.
- Imports demonstram arquitetura, não validade científica.
- WC é caso histórico negativo, não consumidor moderno.
- Stocks e NBA não são fontes desta iniciativa.

## 5. Evidência suficiente e experimentos opcionais

Já existe evidência suficiente para discutir separação de responsabilidades,
governança, contrato temporal transversal, replay, goldens, testes negativos,
resultados negativos, supply chain e a decisão de não alterar o Core.

Experimentos adicionais só são necessários para alegações de equivalência em
datasets oficiais, qualidade dos modelos, comparabilidade estatística,
publicação externa real, comportamento live ou valor econômico. Eles não são
pré-condição para encerrar a contribuição arquitetural e de engenharia.

## 6. Decisões finais de escopo

- P2 permanece padrão reutilizável local; não há API Ops madura.
- P3 não será criada como API pública.
- P6 permanece orientação, sem schema obrigatório.
- P5 continua `KEEP_AS_IS`.
- WC permanece histórico.
- Não haverá uniformização Core, novos pilotos, migração em lote ou reexecução
  científica automática.

## 7. Condição de encerramento

O fechamento técnico depende de decisões humanas separadas sobre:

1. matriz Python do CS — draft PR #12;
2. gate factual do Ecosystem — draft PR #8.

Após eventual merge e CI verde de ambos, o estado poderá ser promovido para
`ECOSYSTEM_MODERNIZATION_COMPLETE`. Até lá, este documento não atribui mudanças
não mescladas aos HEADs principais.

## 8. Formulação-síntese recomendada

> Um ecossistema preditivo multidomínio pode compartilhar contratos científicos
> e operacionais mínimos, preservando semânticas locais, rastreabilidade
> temporal, replay determinístico e governança explícita. A avaliação também
> mostra que maturidade inclui rejeitar abstrações cuja equivalência ainda não
> foi demonstrada.
