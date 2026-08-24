# Handoff corrente do PREDICTORS — 2026-08-23

Este é o handoff corrente após a reconciliação P0 de escopo e a primeira reconciliação mecânica dos seis projetos canônicos. O antigo `ECOSYSTEM_HANDOFF.md` permanece preservado como histórico e não deve ser usado para redefinir o escopo atual quando divergir deste documento ou do Charter.

## 1. Fonte de autoridade

1. `ECOSYSTEM_CHARTER.md` — composição, papéis, objetivo econômico, estados e regra de autoridade;
2. `ECOSYSTEM_MECHANICAL_STATE.md` — inventário mecânico corrente dos seis canônicos;
3. este handoff — continuidade operacional da governança;
4. código/Git/dados/CI do projeto analisado;
5. `ECOSYSTEM_CURRENT_STATE.md` e demais documentos históricos, válidos para suas datas.

## 2. Escopo canônico

Os seis projetos atuais são:

- `ecosystem-predictor`;
- `core-predictor`;
- `predictor-ops`;
- `cripto-predictor`;
- `brasileirao-predictor`;
- `stocks-predictor`.

Os três primeiros regem/viabilizam o ecossistema. Os três últimos são predictors econômicos e têm como objetivo final produzir recomendações com evidência prospectiva de expectativa de lucro líquido positivo.

CS, F1, LoL, WC e NBA permanecem como histórico/referência fora do escopo canônico atual. Nenhuma conclusão histórica é apagada por essa mudança.

## 3. Regra econômica

O sucesso de um predictor não é definido por accuracy ou por uma métrica científica isolada. O alvo econômico exige, conforme o domínio, cadeia temporal válida, preço/odd executável, custos, liquidez, regra de decisão e settlement.

O fluxo atual pressupõe execução humana após recomendação do predictor. Otimização e automação podem vir depois; não são pré-condição para provar edge.

Capital real continua fail-closed e depende de decisão humana explícita.

## 4. Estados globais

A governança separa obrigatoriamente:

- `scientific_state`;
- `predictive_state`;
- `economic_state`;
- `operational_state`;
- `capital_permission`.

Nenhum domínio deve usar um único `GO/NO-GO` para esconder diferenças entre esses eixos.

## 5. Reconciliação P0 concluída

Foi corrigido no `ecosystem-predictor`:

- criação do Charter canônico;
- README deixa de declarar Stocks fora do escopo;
- separação dos seis atuais dos projetos históricos;
- snapshot F1 de 17/08 preservado como histórico, sem poder excluir Stocks;
- missão econômica dos três predictors escrita explicitamente;
- ciência, predição, economia e operação separados por definição;
- criação de `ECOSYSTEM_MECHANICAL_STATE.md` e `audit/canonical-ecosystem-facts.json`;
- novo coletor `scripts/sync_canonical_ecosystem_facts.py` limitado exatamente aos seis definidos pelo Charter;
- CI passa a validar a consistência interna do snapshot mecânico canônico.

## 6. Primeira fotografia mecânica dos seis

A coleta atual registra:

- Ecosystem, Core, Ops, Cripto e Brasileirão com `pyproject.toml` e runtime Python declarado;
- Cripto e Brasileirão consumindo Core 2.3 / Ops 3.1 por dependência moderna;
- Stocks como a exceção estrutural: sem `pyproject.toml`, sem runtime Python declarado no manifest, Core vendorizado legado e sem Ops compartilhado declarado;
- todos os seis possuem workflow `.github/workflows/ci.yml` no HEAD observado.

A assimetria de Stocks é classificada como **drift arquitetural observado**. Ela não é corrigida automaticamente nesta fase.

## 7. O que esta fase NÃO afirma

Esta fase não afirma que:

- Stocks já esteja integrado tecnicamente a Core 2.3/Ops 3.1;
- o registry atual consiga descobrir/despachar os três predictors;
- Brasileirão tenha edge econômico comprovado;
- Cripto tenha edge econômico comprovado;
- Stocks/RJ tenha dados reais ou edge comprovado;
- qualquer predictor esteja autorizado para capital real.

## 8. Próxima fronteira

Com o escopo e o inventário dos seis reconciliados, a próxima fase deve atacar **drift técnico real**, começando por Stocks e pela capacidade do Ecosystem de representar/descobrir os três predictors econômicos de forma coerente.

Qualquer mudança deve continuar classificada como `CONTRADICTION`, `STALE`, `INTENTIONAL_DIVERGENCE`, `UNVERIFIED_CLAIM`, `BROKEN` ou `INCOMPLETE` antes de ser corrigida.
