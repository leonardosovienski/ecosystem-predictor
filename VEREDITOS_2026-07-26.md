# Vereditos — todas as hipóteses registradas do ecossistema

Fechamento formal em 2026-07-26. Cobre as **38 hipóteses** dos cinco registros
(`trials.json` de brasileirao, cs, lol, f1 e previsao-cripto).

Cada linha traz o veredito, o número que o sustenta e a data. Onde não há
amostra para decidir, o status é `INCONCLUSIVA_AMOSTRA_INSUFICIENTE` — que é
status formal, não pendência: diz exatamente o que falta e sob qual critério.

Nada aqui autoriza capital. Nenhum gate deste ecossistema o faz — ver
`BLOQUEIOS_GO_2026-07-25.md` §4.

---

## Resumo

| Status | Nº |
|---|---:|
| **COMPROVADA** (previsão) | 8 |
| **REFUTADA / NO-GO** | 12 |
| **INCONCLUSIVA** (amostra insuficiente) | 5 |
| **PRÉ-REGISTRADA, não executada** | 3 |
| **SUPERSEDED** (substituída por coorte nova) | 3 |
| **VALIDADA informativa** | 1 |
| **GO exploratório** (não confirmatório) | 1 |
| **Inviável por ausência de fonte** | 1 |
| **Encerrada por decisão humana** | 4 |
| **TOTAL** | **38** |

**Hipóteses econômicas aprovadas para capital: zero.** Das que chegaram a
veredito econômico, 12 foram refutadas. As 8 COMPROVADAS são todas de
**qualidade de previsão** (Brier/RPS), não de lucro.

---

## brasileirão — 9

| Hipótese | Status | Evidência |
|---|---|---|
| `h1-ou25-edge-2-15-walkforward` | **NO-GO** (2026-07-10) | n=455, ROI +7,9%, CLV +19,55%, PSR 0,94, IC95 [−0,0218; +0,1719], DSR 0,94 — IC cruza zero |
| `h1-...-2023-2026-exploratoria` | **GO EXPLORATÓRIO** (2026-07-25) | n=567, PSR 0,9935, IC95 [+0,0264; +0,2032], DSR 0,9518. **Não confirmatório**: o baseline sem 2023 foi visto antes da decisão de rodar com 2023 |
| `h2-periodo-1t-conf60` | **VALIDADA** (informativa) | n=1.493, acerto 79,0% vs confiança 79,8%. Sem odds de período → sem ROI/CLV |
| `H4_DIXON_COLES_CALIBRATED` | **REFUTADA** (2026-07-11) | ΔRPS 0,00235, IC95 [−0,00216; +0,00684], n=737 — cruza zero |
| `h3-ou25-sombra-2026` | **SUPERSEDED** (2026-07-25) | 8 picks `LEGACY_INCOMPLETE` (odd do agregado Sofascore, sem bookmaker) |
| `h5-ensemble-xg-sombra-2026` | **SUPERSEDED** (2026-07-25) | 3 picks `LEGACY_INCOMPLETE`, mesma causa |
| `h3-ou25-sombra-pinnacle-2026` | **INCONCLUSIVA** | 4/100 picks. Critério: PSR≥0,80 ∧ IC_lower>0 ∧ DSR≥0,95 |
| `h5-ensemble-xg-sombra-pinnacle-2026` | **INCONCLUSIVA** | 2/100 picks, população paralela à H3 |
| `h7-clv-prospectivo-pinnacle-2026` | **INCONCLUSIVA** | 0/50 picks. Critério: IC95_lower(CLV) > 0 |

## cs — 6

| Hipótese | Status | Evidência |
|---|---|---|
| `h1-cs-elo-serie-prequential` | **COMPROVADA** (2026-07-11) | n=10.671, Brier 0,4573 vs semente 0,4956, acerto 62,6%, DM p<0,05 |
| `h2-cs-elo-platt-prequential` | **COMPROVADA** (2026-07-11) | Brier 0,4573 → 0,4518, DM p=0,00000, n=10.671 |
| `h2-cs-elo-platt-symmetric-prequential` | **COMPROVADA** (2026-07-16) | Brier 0,4570 → 0,4523, DM p=0,00000, n=10.699 |
| `h5-cs-beyond-market-retrospective` | **SEM EDGE** (retrospectiva) · **INCONCLUSIVA** (prospectiva) | 661 pares: Brier modelo 0,2283 vs mercado **0,2196** — o mercado ganhou. Coorte prospectiva em 18/50, 5/30 dias |
| `h3-cs-asymmetric-calibration-forward` | **PRÉ-REGISTRADA, não executada** | — |
| `h4-cs-inactivity-decay-forward` | **PRÉ-REGISTRADA, não executada** | Nenhum decay entra no rating canônico antes do veredito forward |

## lol — 6

| Hipótese | Status | Evidência |
|---|---|---|
| `h1-lol-elo-mapa-prequential` | **COMPROVADA** (2026-07-11) | n=3.053, Brier 0,4434 vs banda 0,4657, acerto 64,5%, DM p<1e-4 |
| `h2-lol-kills-normal-por-liga` | **REFUTADA** (2026-07-11) | 0/3 linhas; média por time é **pior** que a da liga nas 3, DM p<0,001 na direção errada |
| `h3-lol-elo-platt-prequential` | **REFUTADA** (2026-07-11) | Brier 0,4434 → 0,4416, DM p=0,35528 — indistinguível de sorte |
| `h4r-lol-polymarket-retrospectivo` | **INCONCLUSIVA** (2026-07-20) | 177 partidas: Brier Elo 0,4320 vs mercado **0,4023**; ROI shadow +10,57%, IC95 [−11,82%; +33,70%] — cruza zero |
| `h4-lol-market-shadow-prospectivo` | **SUPERSEDED** (2026-07-22) | Cotações sem competição/evento/provenance completos |
| `h4-lol-market-shadow-prospectivo-v2` | **INCONCLUSIVA** | Encerrada 23/07 em 0/50 · reaberta 26/07 · 0 sinais elegíveis |

## f1 — 10 · **projeto completo**

| Hipótese | Status | Evidência |
|---|---|---|
| `H0-F1-formal-grid-vs-elo` | **COMPROVADA** | RPS grid 0,1304 vs elo 0,1399; IC95 [−0,0145; −0,0047]; DM p=0,00026 (80 corridas) |
| `H1-F1-elo-pl-vs-grid-rps` | **REFUTADA** | RPS modelo 0,1399 vs grid 0,1303; DM 3,853, p=0,0002 |
| `H2-F1-h2h-companheiros` | **COMPROVADA** | acerto 0,6501 (392/603), Wilson95 [0,6112; 0,6871] |
| `H3-F1b-elo-grid-blend-vs-elo-puro` | **COMPROVADA** | w=0,5; RPS 0,1274 vs 0,1407; DM −9,219, p=0,0000 |
| `H4-F1b-platt-podium` | **COMPROVADA** | Brier cru 0,0930 vs calibrado 0,0794 |
| `H5-F1c-contexto-circuito` | **REFUTADA** | RPS 0,1309 vs 0,1275 (p=0,0375) |
| `H6-F1c-reliability-dnf` | **REFUTADA** | w_rel=0,0; RPS 0,1309 vs 0,1309 |
| `H7-F1c-pit-efficiency` | **REFUTADA** | w_pit=0,0; RPS 0,1309 vs 0,1309 |
| `H8-F1-choque-transicao-regulamento` | **REFUTADA** | RPS 0,1576 vs 0,1631; DM −0,697, p=0,5035 |
| `G0-F1-market-h2h-feasibility` | **MARKET_H2H_NOT_FEASIBLE** | zero fontes aceitas, zero quotes |

Operação real: `NO_GO_CONFIRMED` desde 2026-07-23. H8/H2H
`CLOSED_BY_HUMAN_DECISION`. Restam 11 corridas em 2026 contra 15 exigidas —
o gate H8 é **aritmeticamente impossível** neste ano.

## cripto — 7

| Hipótese | Status | Evidência |
|---|---|---|
| `v3-hmm-funding-oi-fr90` | **NO-GO** (2026-07-02) | n=3.958 OOS; bruto +0,44 bps → **líquido −0,09 bps**; PSR 0,445 |
| `v3-hmm-funding-oi-fr21` | **REFUTADA** (2026-07-02) | PSR 0,215; líquido −0,37 bps; MaxDD 25,8% |
| `v3-hmm-funding-oi-fr90-h48` | **REFUTADA** (2026-07-02) | edge bruto **vira negativo**; líquido −0,75 bps; MaxDD 50,3% |
| `v1-direct-gemini-h7` | **NO-GO** | Sharpe −0,5733 |
| `v2-dpl-gemini-h7` | **ENCERRADA IMATURA** | Sharpe −0,3057; coleta fechada com n=5 |
| `v2-dpl-multi-h7` (H5) | **GATE EM 28/07** | Sharpe −0,3260; Spearman −0,255, IC95 [−0,377; −0,120] — **não cruza zero, direção oposta**; DSR 0,00 vs corte 0,95 |
| `h6-sinal-invertido-d7` | **PRÉ-REGISTRADA, não ativada** | Sem coleta dedicada |

Reexecução de 2026-07-09 sobre a base estendida: PSR 0,465, IC_lower −0,0794 —
o edge de 2021-24 **não sobreviveu ao forward 2025-26**.

---

## As 5 que não podem ser fechadas hoje, e por quê

Refutar exige evidência, assim como aprovar. Declarar NO-GO numa coorte de
18/50 seria tão falso quanto declarar GO.

| Hipótese | Tem | Precisa | Previsão |
|---|---|---|---|
| `h5-cs-beyond-market` (prospectiva) | 18/50 · 5/30 dias | 50 maturadas | ~25/08 |
| `h3-ou25-sombra-pinnacle-2026` | 4/100 | 100 picks | ~jan/2027 |
| `h7-clv-prospectivo-pinnacle-2026` | 0/50 | 50 picks | ~dez/2026 |
| `h5-ensemble-xg-sombra-pinnacle-2026` | 2/100 | 100 picks | ~jan/2027 |
| `h4-lol-market-shadow-v2` | 0 sinais | 50 maturadas + 3 competições | indefinido |

As previsões assumem as tarefas agendadas religadas — **todas foram
desabilitadas em 2026-07-26 a pedido do operador**. Com elas paradas, nenhuma
avança.

## As 3 pré-registradas nunca executadas

`h3-cs-asymmetric-calibration-forward`, `h4-cs-inactivity-decay-forward`,
`h6-sinal-invertido-d7` (cripto). Existem como compromisso escrito e nunca
consumiram dado. Podem ser executadas ou encerradas como `NAO_ATIVADA` — em
ambos os casos, sem custo de DSR enquanto não produzirem Sharpe finito.

---

## Leitura final

**8 COMPROVADAS, todas de qualidade de previsão.** Os modelos preveem melhor
que suas linhas-base: o Elo do CS bate a semente, o do LoL bate a banda
regional, o grid do F1 bate o Elo, o Platt calibra melhor que o cru. Isso é
real e está medido.

**12 REFUTADAS, todas que tentaram virar dinheiro.** E nas três comparações
diretas contra o mercado, o mercado venceu as três:

```
CS   Brier 0,2283 vs mercado 0,2196
LoL  Brier 0,4320 vs mercado 0,4023
WC   CLV +16,9% no papel, P&L real −5,84u
```

Prever melhor que uma linha-base não é o mesmo que prever melhor que o
mercado. Este ecossistema demonstrou a primeira coisa e, até aqui, falhou em
demonstrar a segunda.

**Uma única pergunta econômica segue genuinamente aberta:** CLV contra o
fechamento do Pinnacle (`h7`), com 4 picks capturados e 0 maturados. É a
primeira medição do ecossistema feita contra um book real com fechamento a
minutos do apito. Pode responder sim. As três anteriores responderam não.
