# Fechamento de 2026-07-26 — segunda rodada

Sessão pedida com o objetivo **"dar GO em todos"**. Este documento registra o
que foi entregue, o que não pôde ser, e por quê — verificado por execução, não
por leitura de documentação.

---

## 1. O objetivo, respondido de frente

**GO em todos não é entregável hoje, e não é por falta de trabalho.**

As cinco regras que acompanharam o pedido (travas terminais; registro só vale
se anterior ao evento; folga de DSR esgotada; não baixar meta de gate depois de
ver dificuldade; refutar exige tanta evidência quanto aprovar) descrevem
exatamente o conjunto de operações que produziriam "GO em todos". Elas não
estão em conflito por acidente: **as regras são o motivo de o GO não existir.**
Só há três formas de fabricá-lo, e as três estão nomeadas ali como proibidas:

| Caminho para "GO" | O que ele exige | Regra que o barra |
|---|---|---|
| Declarar GO com a amostra atual | fechar cs em 18/50 e brasileirão em 4/100 | 5 — refutar/aprovar sem amostra é falso nos dois sentidos |
| Afrouxar o critério | baixar n, alargar IC, abaixar corte de DSR | 4 — já medido: N=47 passa em 26% das amostras por sorte |
| Ligar o capital | editar `go_gate`/`record_bet` | 1 — travas terminais **por desenho**, decisão anterior a estas sessões |

O que existe de real, e continua valendo: **8 hipóteses COMPROVADAS**, todas de
qualidade de previsão. Os modelos batem suas linhas-base — isso está medido e
não é pouco. O que não existe é uma hipótese econômica aprovada. Nas três
comparações diretas contra o mercado, o mercado ganhou as três.

Portanto o que esta sessão fez foi a única coisa que aproxima um GO futuro:
**tirar do caminho os defeitos que impediam as coortes de sequer contar** — e
encontrou dois que ninguém sabia que existiam, ambos ativos, ambos silenciosos.

---

## 2. Os dois defeitos encontrados hoje

Os dois estavam em código que **nunca havia sido executado do jeito que a
produção o executa**. As suítes passavam por cima dos dois.

### 2.1 `tools` — manifesto defasado parava TODA tarefa agendada (era B-11)

O commit `d104d01` (26/07 **15:12**) adicionou `monitor_task_health.ps1` sem
regenerar `TOOLS_MANIFEST.json`. A partir dali `collect_tools_provenance`
levantava `manifest included_files differs from tracked content`, e o
`operational_runner` — que envelopa **todas** as tarefas agendadas do
ecossistema — devolvia **exit 3 fail-closed em qualquer invocação**, strict ou
permissive.

**Não foi quase-acidente: uma tarefa real falhou.** A primeira leitura desta
sessão disse "nenhuma tarefa chegou a falhar, a última rodou às 14:54, 18
minutos antes do commit". Errado — bastava olhar o Scheduler em vez de inferir
pelo horário. `cs-archival-collection` roda **de hora em hora** e disparou às
**15:22**. O heartbeat dela, escrito pela própria máquina, registra:

```
started_at_utc  2026-07-26T18:22:28Z
status          FAILED
exit_code       3
error_summary   manifest included_files differs from tracked content
```

Janela de indisponibilidade: **15:12 → ~15:46** (commit que quebrou → commit
que corrigiu). Uma execução caiu dentro dela e falhou. As três tarefas que
dispararam depois (`cs-market-shadow` 15:54, `lol-market-shadow` 15:57,
`brasileirao-closing-snapshot` 15:45) voltaram a **exit 0** — confirmação em
produção, não em teste.

O sintoma visível o tempo todo era "23 testes vermelhos".

O `BLOQUEIOS_GO` registrava a causa como `ModuleNotFoundError: 'src'` e
concluía: *"nenhum desses testes vermelhos indica falha em produção"*. Os dois
indicavam.

**Por que a suíte não pegou:** todos os 26 testes de `test_release_manifest.py`
usavam repositório sintético em `tmp_path`. Nenhum olhava o manifesto **real**
desta checkout. Corrigido com `test_checked_in_manifest_matches_this_repository`.

### 2.2 `lol-predictor` — o payload semanal não importava, exit 1 antes da rede

`from src.data.ingestion import ...` entrou em `ff56d44` (21/07 20:49). O
módulo insere o WORKSPACE na `sys.path` para achar `tools`, mas nunca inseriu o
próprio ROOT — então `src` jamais resolveu, **nem sob teste nem sob Scheduler**.

`lol-ratings-semanal` é semanal e a última execução foi **20/07 13:28**, um dia
antes do import entrar. A quebra nunca disparou.

Isto muda a leitura do B-10. "Esperar o reset da cota do Drive" era necessário e
**não suficiente**: com o reset e sem esta correção, a próxima execução
falharia com exit 1 sem sequer requisitar o arquivo — e o diagnóstico aparente
seria *"a fonte continua caída"*, que é a conclusão errada, pela segunda vez no
mesmo bloqueio.

### O que a suíte não media

Os dois defeitos compartilham a forma: **o teste exercitava uma reprodução do
ambiente, nunca o ambiente.** Manifesto sintético em vez do manifesto do repo;
módulo carregado por `importlib` em vez de executado como script. Em ambos os
casos a suíte ficou verde enquanto a produção estava quebrada — que é
literalmente o modo de falha que o próprio `BLOQUEIOS_GO` descreve para B-2 e
B-3 ("*o próximo defeito real entra sem ninguém notar*").

---

## 3. Erro de documentação corrigido — coleta não estava parada

`VEREDITOS_2026-07-26.md` afirmava que **todas** as tarefas foram desabilitadas
em 26/07 a pedido do operador, e concluía "com elas paradas, nenhuma avança".

Verificado contra o Scheduler: **16 das 18 tarefas estão `Ready`**. As duas
`Disabled` são `f1-forward-snapshot` (desde 23/07, projeto encerrado) e
`GarimpoInvestimentos-ColetaDiaria` (legada). As coortes **estão coletando** e
as datas previstas valem.

Escrito do jeito errado, esse parágrafo instruía a próxima sessão a tratar como
morto um funil vivo — e a conclusão natural seria religar tarefas que já estão
ligadas, ou dar as coortes por perdidas.

---

## 4. Status por projeto

Suítes reexecutadas hoje. Todas verdes.

| Projeto | Testes | Estado formal | O que falta |
|---|---:|---|---|
| **predictor_core** | 268 | **FECHADO** — 1.3.3, 4 consumidores vivos byte-idênticos (46/46), 3 PARKED com drift esperado | só B-6: sincronizar `previsao-cripto` **depois** de 28/07 |
| **tools** | **142** +1 skip | **FECHADO** — B-11 corrigido, zero vermelhos, suíte roda sem `PYTHONPATH` externo | nada |
| **f1-predictor** | **203** | **FECHADO** — `NO_GO_CONFIRMED` desde 23/07, 10/10 vereditos escritos | nada. **Não reabrir** |
| **predictor-stocks** | 144 | **FECHADO** — 4 hipóteses, 4 ruído, nenhuma pendente; vendor congelado em 1.3.0 por regra do próprio projeto | nada |
| **cs-predictor** | 159 | **COLETANDO** — 18/50 maturadas, 5/30 dias, `decision_ready: false` | tempo. Veredito possível ~25/08 |
| **brasileirao-predictor** | 377 | **COLETANDO** — 4 emitidas, 0 maturadas, `remaining_to_100: 100`; CLV 0/50 | tempo |
| **lol-predictor** | 131 | **COLETANDO, destravado hoje** — import corrigido; resta a cota do Drive | cota reseta sozinha |
| **previsao-cripto** | 325 +2 skip | **GATE EM 28/07** | executar o gate e registrar o veredito |

**Hipóteses econômicas aprovadas para capital: zero.** Nenhum item desta tabela
altera isso, e nenhum gate deste ecossistema é capaz de alterá-lo.

### Os quatro que fecham; os quatro que não

Fecham porque **acabou o trabalho**: `predictor_core`, `tools`,
`f1-predictor`, `predictor-stocks`.

Não fecham porque **falta calendário**, não esforço: `cs-predictor` (18 de 50),
`brasileirao-predictor` (4 de 100), `lol-predictor` (cota externa),
`previsao-cripto` (gate marcado para 28/07, daqui a dois dias).

Fechar qualquer um dos quatro de baixo hoje exigiria declarar veredito sem
amostra — que é a regra 5, e vale nas duas direções: um NO-GO em 18/50 seria
tão inventado quanto um GO.

---

## 5. A folga do DSR do brasileirão é menor do que estava escrito

Calculado hoje com `expected_max_sharpe` do core, sobre o `trials.json` real:

```
var([0,0722; 0,1043]) = 0,00051520
n= 8  SR0 = 0,033117     (numero que estava no BLOQUEIOS_GO)
n= 9  SR0 = 0,034519     <- estado de hoje; DSR 0,9518
n=10  SR0 = 0,035740     <- acima do SR0 critico 0,0353
```

O texto anterior avisava que "qualquer tentativa nova **com Sharpe finito**"
poderia derrubar o resultado. É brando demais. `SR0` cresce com o **número** de
tentativas registradas, não com o valor delas: **a décima trial derruba o GO
exploratório abaixo de 0,95 mesmo com `sharpe: None`** — inclusive uma
pré-registrada que nunca produza número.

A regra operacional correta não é "calcule o Sharpe antes de registrar". É
**não registrar mais nada neste projeto sem aceitar conscientemente esse
preço.**

**Limite desta conta, registrado por honestidade:** os `SR0` acima são exatos.
O `DSR` correspondente **não pôde ser recalculado** — a série de retornos das
567 apostas não foi persistida em lugar nenhum, o run foi feito em cópia
isolada e só o Sharpe agregado entrou no registro. Um resultado de nível GO
cujo DSR não é re-derivável do acervo é uma falha de arquivamento independente
do mérito científico: se alguém contestar o 0,9518, não há como refazer a conta.

---

## 6. Protocolo do gate de 28/07 (previsao-cripto / H5)

Não executado hoje **de propósito** — antecipar dois dias é mexer na data do
gate, que é parte do contrato da trial.

Estado verificado, read-only, sem tocar em `trials.json`:

- `v2-dpl-multi-h7` registrada com `sharpe: -0.326`.
- Coorte multi-juiz coletando desde 10/07; último lote **26/07 01:06**, os 4
  juízes presentes (gemini/mistral/groq/cerebras).
- Critério pré-registrado: Spearman IC95 sem cruzar zero **positivo**, n ≥ 30
  maduras, estratificado por fonte; depois Sharpe líquido + DSR ≥ 0,95.
- Parcial de 20/07: Spearman **−0,255** [−0,377; −0,120] — IC não cruza zero
  **na direção oposta à hipótese**; DSR 0,00 contra corte 0,95.

Passos em 28/07, nesta ordem:

1. Deixar a coleta de 27/07 e 28/07 acontecer normalmente. Não forçar rodada.
2. Rodar o backtest de produção (`analyzers/backtest.py`, já é a 2ª etapa da
   `GarimpoFase1`) e ler Spearman, IC95, n maduras, Sharpe por-trade e DSR.
3. Registrar o veredito com os números **como saíram**. O critério foi
   congelado em 10/07 e não se toca nele agora — vale para os dois lados.
4. Anexar as estratificações por `input_degradado`, `news_provider`, fonte e
   juiz. São auditabilidade, **não** critério alternativo de aprovação e não
   autorizam trocar o veredito pooled.
5. Só **depois** do veredito registrado, sincronizar o vendor do core
   1.3.2 → 1.3.3 (B-6). Antes, não: seria trocar código no meio da trial.

Armadilha específica deste projeto: `close_trial_sharpes()` amadurece trials
casando `params.fonte`. A `h6-sinal-invertido-d7` usa
`fonte: reserved:h6-inversao-sinal` exatamente para nunca ser amadurecida por
engano com a coleta atual, que é não-invertida. Não mexer nisso.

---

## 7. Commits desta rodada

Tudo em branch, nada mesclado, nada publicado — publicação segue sendo decisão
humana explícita.

| Repo | Branch | Commit |
|---|---|---|
| `tools` | `claude/monitor-task-health-2026-07-26` | `eb676ef` — manifesto + teste de regressão + `pythonpath` |
| `lol-predictor` | `claude/evidencia-prospectiva-2026-07-26` | `a7528c0` — ROOT na `sys.path` do payload semanal |
| raiz | `claude/bloqueios-go-2026-07-26` | este documento + erratas em `VEREDITOS` e `BLOQUEIOS_GO` |

---

## 8. O que uma próxima sessão deve fazer

1. **28/07** — executar o gate da H5 pelo protocolo do §6 e registrar o
   veredito. Depois dele, e só depois, sincronizar o vendor (B-6).
2. **Conferir o `lol-ratings-semanal`** depois do reset da cota do Drive: com
   o import corrigido, ele deve sair de exit 10 sozinho. Se não sair, o
   override `ORACLES_ELIXIR_2026_URL` existe.
3. **Não registrar trial nova no brasileirão** sem ler o §5.
4. **Deixar cs e brasileirão coletarem.** Não há trabalho a fazer neles; há
   calendário a esperar. Mexer é que dá errado.
5. **Não reabrir f1 nem stocks.** Os dois estão fechados com veredito escrito.
