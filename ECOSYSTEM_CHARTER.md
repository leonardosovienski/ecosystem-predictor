# PREDICTORS — Charter canônico do ecossistema

**Status:** decisão humana canônica  
**Vigência:** 2026-08-23  
**Autoridade:** este documento define a composição, os papéis e o objetivo atual do ecossistema. Inventários mecânicos, READMEs, HANDOFFs e documentos históricos não podem alterar esta decisão por inferência.

## 1. Composição canônica atual

O PREDICTORS é composto por **seis repositórios canônicos**:

| Repositório | Papel canônico | Deve gerar lucro diretamente? |
|---|---|---|
| `ecosystem-predictor` | governança, registry, gateway, scheduler, storage e visão agregada | não |
| `core-predictor` | primitivas científicas, temporais, métricas e testes prequential compartilhados | não |
| `predictor-ops` | execução operacional, idempotência, observabilidade, reconciliação, segurança operacional e controles de runtime | não |
| `cripto-predictor` | predictor econômico de cripto | sim, quando houver edge validado |
| `brasileirao-predictor` | predictor econômico de mercados do Brasileirão | sim, quando houver edge validado |
| `stocks-predictor` | predictor econômico de ações; domínio ativo atual: `predictor-rj` | sim, quando houver edge validado |

A composição acima é uma **decisão humana**, não um resultado do coletor mecânico.

### Repositórios históricos ou fora do escopo canônico atual

`cs-predictor`, `f1-predictor`, `lol-predictor`, `wc-predictor`, `nba-predictor` e outros repositórios preservados podem continuar existindo como histórico, evidência, referência técnica ou pesquisa encerrada. Eles **não fazem parte dos seis projetos canônicos atuais** e não devem reaparecer no escopo corrente apenas porque um documento antigo, script ou snapshot ainda os enumera.

Nada neste charter apaga o histórico científico desses projetos.

## 2. Objetivo global

Os três predictors econômicos — Cripto, Brasileirão e Stocks — existem para produzir recomendações baseadas em informação disponível no momento da decisão que, quando executadas segundo uma política definida e mensurável, apresentem **evidência prospectiva de expectativa de lucro líquido positivo**.

No estágio atual, o fluxo operacional esperado é:

```text
dados disponíveis no instante t
        ↓
previsão / sinal
        ↓
recomendação do predictor
        ↓
decisão e execução humana
        ↓
resultado / settlement
        ↓
lucro ou prejuízo líquido auditável
```

A execução pode ser otimizada ou automatizada no futuro, mas automação **não é requisito para validar a existência de edge**. A ausência de oportunidade é uma saída válida; o predictor não deve emitir sinal apenas para produzir atividade.

## 3. O que NÃO constitui sucesso econômico

Nenhum dos itens abaixo, isoladamente, prova que um predictor cumpre o objetivo econômico:

- accuracy maior;
- RPS, Brier ou log-loss melhor;
- correlação estatisticamente significativa;
- identificação retrospectiva de um rally;
- backtest bruto positivo sem custos e disponibilidade temporal;
- CI verde;
- grande número de testes automatizados;
- existência de uma arquitetura compartilhada;
- hipótese classificada como `COMPROVADA` quando o que foi comprovado não é edge econômico.

Para alegar capacidade econômica, a evidência deve preservar causalidade temporal e considerar os elementos relevantes do domínio, como preço/odd disponível, spread, comissão, slippage, liquidez, custos, regra de entrada/saída e settlement.

## 4. Separação obrigatória de estados

O ecossistema não deve condensar ciência, previsão, economia e operação em um único `GO/NO-GO`. Cada predictor deve poder ser descrito em quatro eixos independentes:

### 4.1 `scientific_state`
Responde: **a hipótese ou mecanismo estudado possui evidência válida?**

Exemplos de classes permitidas: `NOT_TESTED`, `ACTIVE`, `INCONCLUSIVE`, `SUPPORTED`, `REJECTED`, `FROZEN`.

### 4.2 `predictive_state`
Responde: **há capacidade preditiva fora da amostra e contra o benchmark apropriado?**

Exemplos: `NOT_MEASURED`, `BELOW_BASELINE`, `INCONCLUSIVE`, `BEATS_BASELINE`, `PROSPECTIVE_CONFIRMED`.

### 4.3 `economic_state`
Responde: **a informação consegue ser transformada em retorno líquido positivo?**

Exemplos: `NOT_DEFINED`, `NOT_MEASURED`, `NO_EDGE`, `INCONCLUSIVE`, `POSITIVE_EDGE_SHADOW`, `POSITIVE_EDGE_PROSPECTIVE`.

### 4.4 `operational_state`
Responde: **a cadeia necessária para produzir, registrar e liquidar a decisão funciona de forma reproduzível?**

Exemplos: `RESEARCH_ONLY`, `SHADOW_INCOMPLETE`, `SHADOW_OPERATIONAL`, `MANUAL_LIVE_READY`, `AUTOMATED_LIVE_READY`, `DEGRADED`.

`capital_permission` é uma decisão separada e deve ser fail-closed. Nenhum estado científico ou preditivo, sozinho, autoriza capital.

## 5. Cadeia econômica compartilhada

Na versão 3.0, o Core foi deliberadamente estreitado e não publica mais os antigos
records econômicos da linha 2.3. A referência semântica vigente é o contrato do
ecossistema; as representações executáveis permanecem locais aos domínios até existir
uma abstração comprovadamente compartilhada:

```text
ProbabilisticForecast
        ↓
MarketQuote
        ↓
EconomicDecision
        ↓
ExecutionRecord
        ↓
SettlementRecord
```

O Core fornece medição, causalidade temporal e avaliação prequential; não decide gate,
estratégia, sizing, bankroll, risco de domínio ou autorização de capital.

O Ops executa e audita workloads; não deve decidir se uma hipótese é cientificamente verdadeira ou lucrativa.

O Ecosystem governa e agrega; não deve inventar previsão nem reclassificar ciência local sem evidência.

## 6. Regra de autoridade e conflito

Quando fontes discordarem, a precedência é:

1. **decisão humana explícita vigente**, quando a questão for escopo, objetivo ou autorização;
2. código, dados, Git e execução observável, quando a questão for fato técnico/mecânico;
3. charter/trial/registro científico do domínio, quando a questão for definição pré-registrada ou veredito científico;
4. documento corrente explicitamente marcado como fonte da verdade;
5. documentos históricos, apenas para a data a que se referem.

Um README não transforma claim em fato. Um snapshot mecânico não altera o escopo humano. Um CI verde não altera veredito científico.

## 7. Política de inconsistências

Qualquer divergência entre os seis repositórios deve ser classificada antes de ser corrigida:

- `CONTRADICTION`: duas fontes correntes incompatíveis;
- `STALE`: fonte antiga ainda não incorporou uma decisão posterior;
- `INTENTIONAL_DIVERGENCE`: diferença deliberada e documentada;
- `UNVERIFIED_CLAIM`: afirmação sem evidência suficiente;
- `BROKEN`: comportamento reproduzivelmente incorreto;
- `INCOMPLETE`: parte necessária ainda inexistente.

Documentos históricos permanecem append-only sempre que editá-los apagaria contexto. O estado corrente deve ser corrigido em uma fonte nova/canônica ou por errata explícita.

## 8. Situação de capital

Este charter **não autoriza capital real em nenhum predictor**. A autorização depende de evidência econômica e operacional específica de cada domínio e de decisão humana explícita.

A meta do ecossistema é permitir que um predictor chegue de forma auditável à cadeia:

```text
hipótese → previsão válida → edge econômico → shadow prospectivo → execução manual controlada → otimização/automação futura
```

Pular etapas para obter um resultado positivo viola a governança do PREDICTORS.
