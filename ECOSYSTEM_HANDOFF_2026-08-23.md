# Handoff corrente do PREDICTORS — 2026-08-23

Este é o handoff corrente após a reconciliação P0 de escopo. O antigo
`ECOSYSTEM_HANDOFF.md` permanece preservado como histórico e não deve ser usado
para redefinir o escopo atual quando divergir deste documento ou do Charter.

## 1. Fonte de autoridade

1. `ECOSYSTEM_CHARTER.md` — composição, papéis, objetivo econômico, estados e regra de autoridade;
2. `ECOSYSTEM_CURRENT_STATE.md` — fatos mecânicos e snapshots, sempre interpretados pela data;
3. este handoff — continuidade operacional da governança;
4. código/Git/dados/CI do projeto analisado;
5. documentos históricos, válidos para suas datas.

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

A governança passa a separar obrigatoriamente:

- `scientific_state`;
- `predictive_state`;
- `economic_state`;
- `operational_state`;
- `capital_permission`.

Nenhum domínio deve usar um único `GO/NO-GO` para esconder diferenças entre esses eixos.

## 5. Reconciliação desta P0

Corrigido no `ecosystem-predictor`:

- criação do Charter canônico;
- README deixa de declarar Stocks fora do escopo;
- README separa os seis atuais dos projetos históricos;
- `ECOSYSTEM_CURRENT_STATE.md` passa a rotular explicitamente o inventário de 17/08 como snapshot histórico da F1;
- ausência de Stocks no snapshot de 17/08 deixa de ser interpretável como exclusão vigente;
- missão econômica dos três predictors passa a estar escrita de forma explícita;
- ciência, predição, economia e operação passam a ter estados globais separados por definição.

## 6. O que esta P0 NÃO afirma

Esta P0 não afirma que:

- Stocks já esteja integrado tecnicamente a Core 2.3/Ops 3.1;
- o registry atual consiga descobrir/despachar os três predictors;
- Brasileirão tenha edge econômico comprovado;
- Cripto tenha edge econômico comprovado;
- Stocks/RJ tenha dados reais ou edge comprovado;
- qualquer predictor esteja autorizado para capital real.

Esses pontos continuam sujeitos a auditoria e fases posteriores.

## 7. Próxima fronteira

Depois desta P0 de governança, a próxima reconciliação mecânica deve inspecionar os HEADs atuais dos seis projetos, incluir Stocks no inventário técnico e classificar divergências como `CONTRADICTION`, `STALE`, `INTENTIONAL_DIVERGENCE`, `UNVERIFIED_CLAIM`, `BROKEN` ou `INCOMPLETE`.

Não promover automaticamente dependências, modelos ou capital durante essa coleta.
