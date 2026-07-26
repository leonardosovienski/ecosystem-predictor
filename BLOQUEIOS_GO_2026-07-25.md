# Bloqueios para GO — auditoria de 2026-07-25

Levantamento dos defeitos que impedem qualquer projeto de chegar a um veredito
econômico, e conferência do volume real de dados. Tudo verificado por execução,
não por leitura de documentação. Read-only exceto onde marcado `CORRIGIDO HOJE`.

Este documento **não** substitui `PENDENCIAS_ABERTAS.md` (lista canônica). Ele é
o registro datado desta rodada e deve ser reconciliado com aquele arquivo.

---

## 1. Conferência dos dados

**695.694 registros auditados. Todos os bancos passam `integrity_check=ok`.**

| Fonte | Linhas | Observação |
|---|---:|---|
| cripto `signals.jsonl` (V3) | 236.365 | sinais brutos do HMM |
| brasileirão `matches.db` | 370.331 | 199.702 stats + 130.304 odds_snapshots + 29.516 ratings |
| cs `cs.db` (Sports) | 45.940 | 17.324 partidas + 17.324 contratos + 11.291 mapas |
| cripto `feature_store.db` | 34.147 | 26.294 features + 6.575 market data |
| f1 `f1.db` | 5.922 | 3.750 pitstops + 2.058 resultados + 114 corridas |
| cs `market_shadow.jsonl` | 1.923 | cotações Polymarket reais |
| cs `market.db` (Market) | 579 | **547 quotes, 32 eventos, 0 closings, 0 resultados** |
| lol `market_quotes.jsonl` | 467 | cotações Polymarket reais |
| brasileirão sombra (H3+H5) | 17 | todos `LEGACY_INCOMPLETE` |
| cripto paper V3 | 3 | |
| lol `h4_signals.jsonl` | **0** | arquivo ausente |

### Quanto disso é evidência elegível para um gate econômico

| Projeto | Coletado | Elegível | Maturado |
|---|---:|---:|---:|
| brasileirão | ~370.000 | 0 | 0 / 100 |
| cs | ~48.000 | 547 quotes | **0 / 50** |
| lol | 467 | 0 sinais | **0 / 50** |
| f1 | 5.922 | 0 pares forward | **0 / 15** |
| cripto (H5) | 410 previsões | 410 | ~198 (D+7) |

O volume não é o gargalo. O funil prospectivo é.

### Classificação por função — auditoria de referências (2026-07-25)

Para cada tabela SQLite e cada JSONL, varredura de referências no código
separando leitura de escrita, e classificando **onde** a leitura acontece.

Quatro categorias, não três. A quarta só apareceu ao auditar:

| Categoria | Consumida por código? | Para que serve |
|---|---|---|
| **referência** | sim, na cadeia agendada | alimenta modelo/serving |
| **resultado** | sim, em análise | produziu veredito |
| **evidência** | sim, no gate | conta para GO/NO-GO |
| **registro de auditoria** | **não, por desenho** | responde "por quê" depois |

| Bloco | Registros | Função real |
|---|---:|---|
| `match_statistics` | 199.702 | **referência** — `display.py:299-319` faz JOIN; serve `scripts/prever.py` |
| `odds_snapshots` | 130.304 | **resultado** — backtest histórico |
| cripto `signals.jsonl` | 236.365 | **evidência (negativa)** — é o NO-GO do V3 |
| `sofascore_player_ratings` | 29.516 | referência periférica — `status.py`, `src/research/` |
| cripto `feature_store` | 34.147 | evidência — H5, 410 previsões |
| cs `cs.db::matches` | 17.476 | referência + fonte das 9 liquidações |
| `cs.db::sports_series_contract` | 17.324 | **registro de auditoria** — migração 22/07; leitura só em teste |
| `odds_lines` | 8.450 | resultado — H1 (567 apostas) |
| f1 `f1.db` | 5.922 | referência — ratings |
| `matches`/`sofascore_matches` | 1.165 | referência — modelo e coorte |
| `market.db::prospective_closings` | 9 | **registro de auditoria** — write-only puro |
| sombra legado | 15 | `LEGACY_INCOMPLETE` |

**Órfãos deletáveis: zero.** Os dois candidatos que a varredura apontou
(`sports_series_contract` e `prospective_closings`) foram verificados à mão e são
trilha de auditoria: existem para que alguém possa perguntar depois *"por que este
evento liquidou neste preço?"* e obter resposta com hash. Write-only é a função
deles, não um defeito.

Vazios de fato (esquema sem uso, não desperdício): `player_comp_stats` (0 linhas),
`bets.jsonl`, `bankroll.jsonl`, `period_predictions.jsonl`, `results.jsonl`.

**Limite da varredura:** não resolve SQL dinâmico nem `SELECT *` montado em
runtime. "Órfão" aqui é candidato a investigação manual, nunca ordem de apagar.

### Errata — classificação anterior desta mesma sessão

Uma versão anterior desta tabela dizia que `match_statistics` (199.702) e
`sofascore_player_ratings` (29.516) eram "features do modelo" e depois que
estariam fora de qualquer uso. **As duas leituras estavam erradas.** O modelo
econômico (Poisson + Elo + ensemble xG) usa placar, times, data e xG — nenhuma das
duas tabelas. Mas `match_statistics` é lida por `display.py` via JOIN e sustenta
`scripts/prever.py`, o CLI de previsão. Não alimenta o funil do gate **e** não é
descartável: são coisas diferentes, e confundi-las duas vezes é o motivo desta
errata existir.

Consequência colateral registrada: `odds_snapshots` perdeu seu último consumidor
vivo em 2026-07-25, quando o settle da sombra migrou para os snapshots do
bookmaker (B-1). Hoje serve apenas backtest histórico.

### Registro de tentativas

| Projeto | Trials | Com Sharpe finito |
|---|---:|---|
| brasileirão | 5 | 1 → `[0,0722]` |
| lol | 6 | 0 |
| cripto | 7 | 5 → `[−0,5733, −0,3056, −0,0022, −0,0132, −0,3258]` |
| f1 | 10 | 0 |

**Cripto tem 5 vereditos finitos e todos são negativos.** É o registro honesto de
cinco tentativas que não deram edge.

---

## 2. Bloqueios abertos

### B-0 · cs + lol — Polymarket bloqueado no DNS desta rede · **RESOLVIDO, verificado em 26/07**

> **Sondado ao vivo em 2026-07-26 e o bloqueio NAO existe mais.** O texto
> abaixo termina em "não é corrigível por código; use outra rede, peça
> liberação do domínio ou troque a fonte". Está desatualizado: a própria
> correção multi-endpoint registrada em `polymarket_provider.DOH_ENDPOINTS`
> resolveu.
>
> ```
> cloudflare-dns.com/dns-query   HTTP 200  A=[104.18.34.205, 172.64.153.51]
> dns.google/resolve             HTTP 200  A=[172.64.153.51, 104.18.34.205]
> 1.1.1.1/dns-query              ConnectTimeout        <- o unico ainda morto
> curl --resolve gamma-api...    rc=0, JSON real de /sports
> ```
>
> O diagnóstico original acertou o mecanismo (o IP `1.1.1.1` é bloqueado) e
> errou o alcance: **o hostname não é.** Com `cloudflare-dns.com` e
> `dns.google` na lista, o fallback resolve e o `curl --resolve` traz dado
> real. Evidência independente: a coorte do cs saiu de 0 para **18 maturadas
> com 18 closings e 18 settlements**, e o coletor do lol enxerga **29 eventos**
> no horizonte de 72h.
>
> **Consequência para a ordem de prioridade:** o documento diz "B-0 primeiro,
> sem fonte não há coorte". Essa etapa está cumprida. O que trava o lol hoje é
> o B-12, abaixo — e não é rede.

Os dois coletores reabertos hoje rodaram às 19:54 e 19:57 e **falharam**
(`LastTaskResult = 1`). Zero cotações novas. Erro: `httpx.ConnectTimeout`.

Diagnóstico por sonda direta:

| Alvo | Resultado |
|---|---|
| `api.sofascore.com` | resolve OK · **HTTP 200 em 1,8 s** |
| `polymarket.com` | **NXDOMAIN** |
| `gamma-api.polymarket.com` | **NXDOMAIN** |
| `clob.polymarket.com` | **NXDOMAIN** |
| `1.1.1.1` (fallback DoH) | sem resposta |

O servidor DNS da rede (`192.168.100.1`, `dev.opt`) devolve NXDOMAIN **apenas** para
o domínio polymarket.com. A rede externa funciona: o Sofascore responde normalmente,
e a ingestão de 380 jogos de 2023 rodou nesta mesma sessão sem falha.

O `polymarket_provider.py:81-118` já tinha um fallback DoH por IP (Cloudflare +
`curl --resolve`), criado em 2026-07-20 exatamente para contornar este NXDOMAIN.
**Esse fallback também está bloqueado agora** — `1.1.1.1` não responde. O bloqueio
apertou entre 2026-07-20 (quando o handoff registra "coleta real confirmada") e hoje.

**Consequência:** CS e LoL não conseguem coletar nesta rede. A reabertura de hoje
está inerte e o relógio dos 30 dias não começou. B-2 e B-3 ficam secundários
enquanto isto não for resolvido.

**Não é corrigível por código.** Opções, todas fora do repositório: usar outra rede
(hotspot pessoal), pedir liberação do domínio, ou trocar a fonte de mercado.

### B-1 · brasileirão — proveniência falsa na coorte prospectiva · **CORRIGIDO HOJE**

> **Resolvido em 2026-07-25.** Criado `src/data/bookmaker_odds.py` e religado o
> `scripts/sombra.py`: a odd agora vem do book nomeado via `TheOddsApiProvider`,
> `odds_captured_at` é o `last_update` do próprio book, e o fechamento é
> reconstruído do histórico desse mesmo book — o campo
> `closing-v1:last-valid-pre-kickoff-by-bookmaker` passou a ser cumprido, não só
> afirmado.
>
> **Bookmaker designado: `pinnacle`.** Menor vig do conjunto (o edge mede o
> modelo, não a margem da casa), padrão-ouro de CLV, e rendeu 4 picks/rodada
> contra 2 dos books de alta cobertura. Viés aceito e registrado: cobertura de
> totals ~37%, concentrada em jogos de maior porte.
>
> Identidade entre fontes segue `resolve_entity`/`EloModel._elo`: exato → dobra
> determinística de acento → alias explícito, só quando ÚNICO. Validado ao vivo:
> **16/16 eventos resolvidos**. Dois achados: a The Odds API publica
> `commence_time` 00:00 UTC como placeholder (18h de diferença no Botafogo x
> Grêmio — tolerância ajustada para 36h) e faltava o alias
> `Atletico Paranaense` → `Athletico`.
>
> Coorte NOVA pré-registrada (`h3-ou25-sombra-pinnacle-2026` e
> `h5-ensemble-xg-sombra-pinnacle-2026`), com a fonte da odd explícita nos
> params. Trocar fonte de preço e definição de fechamento é mudança de
> configuração: contagem do zero, arquivos novos
> (`sombra_*_pinnacle.jsonl`). Os 8 picks H3 e 3 H5 anteriores ficam intactos
> como `LEGACY_INCOMPLETE` e **não** foram migrados.
>
> O atestado em disco certificava a régua **RPS**, métrica diferente do veredito
> que estas trials emitem; foi reemitido para o funil O/U (`COMPROVADA`) sem
> rodar `governanca.main()`, que re-registraria H1 com `sharpe=None` e apagaria o
> **0,0722** que é o denominador do DSR. Verificado intacto após o registro.
>
> **Estado: 4 picks `PROSPECTIVE_ELIGIBLE`, 0 rejeitados, 0 legados.** Primeira
> vez que a coorte tem contagem válida diferente de zero. `BRASILEIRAO_BOOKMAKER`
> definida em escopo User para os jobs `brasileirao-sombra-manhã/noite`.
> Suíte 377 verde (+20), CI verde.

O diagnóstico original, preservado:

`BRASILEIRAO_BOOKMAKER` só escreve um rótulo; não troca a fonte do preço.

- `scripts/sombra.py:119` — a odd vem de `sofascore_matches.odds_over/odds_under`
- `scripts/sombra.py:150` — grava `"bookmaker": <env var>, "source": "sofascore"`
- `scripts/sombra.py:152` — declara `closing-v1:last-valid-pre-kickoff-by-bookmaker`
- `scripts/sombra.py:250` — o settle lê o fechamento **também** de `sofascore_matches`

Definir a variável destrava a captura e produz picks com proveniência falsa: preço
agregado do Sofascore carimbado com o nome de um book que nunca o forneceu, sob um
campo que afirma fechamento por bookmaker. O guard é satisfazível sem satisfazer
seu propósito.

**Estado:** 0/100, captura bloqueada desde 2026-07-22. `monitor_shadow_cohort.py`
reporta `remaining_to_100: 100`, `legacy_incomplete: 8`.

**Correção:** ligar `TheOddsApiProvider` no caminho de captura e de settle, e só
então designar o book. Fonte saudável e disponível: 15 bookmakers, ≥6 janelas de
estabilidade, 0 quotes rejeitadas, cobertura O/U de 19% a 98%.

### B-2 · cs — cadeia de settlement sem driver de produção · **CORRIGIDO HOJE**

> **Resolvido em 2026-07-25.** Criado `scripts/settle_prospective_market.py`, o
> entrypoint que faltava. Sports DB atualizado via `src.ingest_hltv` (17.324 →
> 17.476 partidas, cobertura até 25/07) e a coorte liquidada:
> **9 de 9 mapeamentos aceitos agora estão `MATURED`.**
> `prospective_results`, `prospective_closings` e `prospective_settlements`
> saíram de 0 para 9. Suíte 155 verde (+12 testes), CI verde.
>
> Achado no meio do caminho: 2 dos 9 pareciam sem resultado por **divergência de
> caixa** (`ECHO`/`Echo`, `Heroic`/`HEROIC`). A resolução aplicada é a MESMA de
> `EloModel._elo` — caixa exata primeiro, casefold só quando único, ambíguo falha
> fechado —, porque o HLTV tem organizações distintas que diferem só pela caixa
> (LEO/Leo, CHAOS/Chaos, WINNERS/Winners, as 3 únicas colisões reais em 1.261
> nomes). Resolver por aproximação devolveria o resultado da equipe errada.
>
> Contadores atuais: **9/50 maturadas, 4/30 dias**. `decision_ready: false`.

O diagnóstico original, preservado:

A coorte não pode maturar. Nunca pôde.

- `src/prospective_market.py:192` — `record_result` existe e é testado
- Call sites em produção: **zero**. Só `tests/test_prospective_market.py`
- Nada escreve `prospective_closings` nem `prospective_results`
- `market.db` confirma: 547 quotes, 32 eventos, **0 closings, 0 resultados**

O job `cs-market-shadow` roda `collect_polymarket_upcoming.py` — só coleta. Os 9
mapeamentos aceitos ficam em `EVENT_TIME_PASSED` e param ali.

**Consequência:** o encerramento de 2026-07-23 com "0/50 após 2 dias" não foi
amostra insuficiente. Aos 30 dias o contador estaria em 0 do mesmo jeito.

**Correção:** escrever o entrypoint que alimenta resultado oficial e closing.

### B-3 · lol — settlement sem agendamento · **CONSTRUÍDO EM 26/07**

> **Revertida a decisão de 25/07 de não construir.** Criado
> `scripts/build_h4_results.py`, o produtor que faltava: lê os sinais H4,
> reconstrói a SÉRIE a partir dos jogos individuais do Oracle's Elixir
> (`data/lol.db::games`) e emite o JSON que `settle_h4_signals.py` consome.
>
> O ponto delicado é que **os lados trocam entre jogos de uma mesma série** —
> contar por coluna em vez de por nome de time inverteria o vencedor. Tem teste
> dedicado para isso. Identidade segue `config._identity_key` (NFC + casefold,
> **sem** remover acento: o lol-predictor é deliberadamente mais estrito que os
> outros domínios, e há teste garantindo que `Movistár` ≠ `Movistar`).
> Empate, série ausente ou par degenerado devolvem ausência — o sinal fica
> `PENDING`, que é o estado correto. Nunca inventa resultado.
>
> Validado contra os 3.877 jogos reais: reconstruiu Bo5 do MSI corretamente
> (3x1, 3x0, 1x3). Ligado ao ciclo semanal logo após o ingest:
> `ingest → h4_results → h4_settle → ratings`.
>
> **10 testes novos; suíte 131 verde; CI verde 3/3.** No caminho, os testes novos
> vazavam conexão sqlite e o `-W error` do `ci_check.py` transformava o
> `PytestUnraisableExceptionWarning` em falha atribuída a OUTRO teste
> (`test_arquivo_de_ratings_truncado_falha_alto`). Corrigido com fixture que
> fecha no teardown.
>
> Continua inerte até B-0 (rede) e B-10 (fonte-base) saírem — mas agora **sem
> lacuna interna**: quando o dado voltar, a cadeia fecha sozinha.

O diagnóstico original, preservado:

> Avaliado em 2026-07-25 e deixado como está. `settle_h4_signals.py` exige um
> arquivo de resultados de `oracle-elixir` ou `riot-esports`, casado por
> `canonical_event_id`. Construir esse produtor agora seria escrever um mapeador
> não trivial **sem nenhum sinal contra o qual testá-lo** (`h4_signals.jsonl` não
> existe; `raw_signals: 0`, estado `WAITING_FOR_TIME_WINDOW`) e para um pipeline
> que não roda: as tarefas `lol-market-shadow` e `cs-market-shadow` rodaram às
> 21:27 e 21:24 e falharam de novo (`LastTaskResult = 1`, B-0).
>
> Infraestrutura especulativa, sem dado de verificação, é como se escreve o
> próximo B-2. Fica registrado como próximo passo **depois** do B-0.

O diagnóstico original, preservado:

Melhor que o CS, ainda insuficiente.

- `scripts/collect_polymarket_upcoming.py:61` — constrói sinal e grava em
  `data/shadow/h4_signals.jsonl`. Automatizado pela task `lol-market-shadow`.
- `scripts/settle_h4_signals.py:43` — exige `--results` (arquivo externo obrigatório)
  e **não tem job agendado**
- `h4_signals.jsonl` está ausente hoje: 467 cotações, 0 sinais

**Correção:** definir a fonte de resultado oficial e agendar o settle.

### B-9 · brasileirão — "fechamento" defasado 6-9h do apito · **CORRIGIDO EM 26/07**

Achado ao instalar o gate de CLV, e ele atacava justamente esse gate.

```
captura de picks : 13:00 e 02:00 UTC  (cron manhã/noite)
apitos tipicos   : 19:00 · 21:30 · 22:30 UTC
ultimo snapshot antes do apito -> 13:00 = 6h a 9h30 de defasagem
```

O settle define fechamento como `last-valid-pre-kickoff-by-bookmaker`. Com
amostragem só duas vezes ao dia, esse "fechamento" era a linha do meio da tarde —
e a maior parte do movimento acontece nas horas finais. O `h7-clv-prospectivo-
pinnacle-2026`, registrado horas antes, mede exatamente contra o fechamento:
teria produzido 50 picks com CLV que não é o que a trial declara medir.

**Correção:** `scripts/record_closing_snapshots.py` — registrador que grava
cotação do book perto do apito e **nunca emite pick**. A separação é deliberada:
o INSTANTE DA DECISÃO é parte do contrato da trial e continua fixo em 13:00/02:00;
só o FECHAMENTO passa a ter amostragem densa.

Task `brasileirao-closing-snapshot`, 3 disparos diários (15:45 / 18:15 / 19:15
local = 18:45 / 21:15 / 22:15 UTC). O script se auto-protege: fora da janela de 4h
antes de um apito sai como `NO_KICKOFF_WINDOW` **sem gastar cota**.

Cota verificada antes de decidir a cadência: **386 restantes de 500/mês**, queima
atual ~4/dia. A adição custa ~45/mês (3 chamadas só em dia de jogo).

### B-11 · tools — 23 testes falhando na versão 1.3.4 · **CORRIGIDO EM 26/07**

> **Diagnóstico refeito por execução em 2026-07-26. A causa registrada abaixo
> estava errada, e o erro escondia um defeito de produção, não de teste.**
>
> As 23 falhas tinham **duas causas independentes**, e a que respondia por 18
> delas nem foi mencionada:
>
> **1. `TOOLS_MANIFEST.json` defasado (18 dos 23).** O commit `d104d01`
> (26/07 15:12) adicionou `monitor_task_health.ps1` sem regenerar o manifesto.
> A partir dali `collect_tools_provenance` levantava
> `manifest included_files differs from tracked content`, e o
> `operational_runner` — que envelopa **todas** as tarefas agendadas do
> ecossistema — devolvia **exit 3 fail-closed em qualquer invocação**, strict
> **ou** permissive. Isto **não era problema de teste**: era uma parada total
> do agendamento.
>
> **Uma tarefa real caiu.** A primeira leitura desta sessão concluiu "nenhuma
> chegou a falhar, a última rodou às 14:54" — inferência pelo horário, sem
> olhar o Scheduler. `cs-archival-collection` roda de hora em hora e disparou
> às 15:22; o heartbeat da própria máquina registra `FAILED`, `exit_code 3`,
> `error_summary: manifest included_files differs from tracked content`.
> Janela de indisponibilidade: **15:12 → ~15:46**. As tarefas que dispararam
> depois (`cs-market-shadow` 15:54, `lol-market-shadow` 15:57) voltaram a
> exit 0 — a correção está confirmada em produção, não só na suíte.
>
> Por que a suíte não pegou: **todos** os testes de `test_release_manifest.py`
> usavam repositório sintético em `tmp_path`. Nenhum verificava o manifesto
> **real** desta checkout. Corrigido com
> `test_checked_in_manifest_matches_this_repository`.
>
> **2. `ModuleNotFoundError: No module named 'src'` (os 5 restantes).** Esta
> parte do diagnóstico original estava certa quanto ao sintoma e errada quanto
> à natureza: **não é artefato do contexto de teste, é bug de produção.**
> `atualiza_semanal_payload.py` insere o WORKSPACE na `sys.path` para achar
> `tools`, mas nunca insere o próprio ROOT — então `from src.data.ingestion
> import ...` (introduzido em `ff56d44`, 21/07) **nunca resolveu**, nem sob
> teste nem sob Scheduler. Reproduzido rodando o payload exatamente como
> produção o roda: `ModuleNotFoundError`, exit 1, antes de qualquer rede.
> Como `lol-ratings-semanal` é semanal e a última execução foi 20/07 13:28 —
> um dia antes do import entrar —, a quebra nunca chegou a disparar. Ver B-10.
>
> **Estado: suíte 142 passed, 1 skipped, sem `PYTHONPATH` externo** (era 23
> failed / 118 passed com `PYTHONPATH`, e 4 erros de coleta sem ele). O
> `pythonpath = [".."]` foi declarado no `pyproject.toml`: não muda o contrato
> de consumo por `sys.path`, apenas o declara onde o pytest lê.
>
> Commits: `tools@eb676ef`, `lol-predictor@a7528c0`.

O diagnóstico original, preservado:

Descoberto em 2026-07-26 ao levantar o estado dos 8 projetos. O
`ECOSYSTEM_HANDOFF` registrava "139 passed, 1 skipped" para `tools/` 1.3.1;
a versão hoje é **1.3.4** e a suíte está assim:

```
sem PYTHONPATH            4 erros de coleta (ModuleNotFoundError: 'tools')
PYTHONPATH=<workspace>    23 failed, 118 passed, 1 skipped
```

**Não é regressão desta rodada** — verificado: as falhas são
`ModuleNotFoundError: No module named 'src'` ao importar payloads de domínio
(`lol-predictor/scripts/atualiza_semanal_payload.py:20`) a partir do contexto de
teste do `tools`. É o mesmo split-brain de import já registrado como decisão
operacional ("`tools/` sem instalação via pacote — consumo é por `sys.path`"),
mas agora com 23 testes vermelhos em vez de contornado.

Afeta `test_lol_operational_entrypoint`, `test_operational_runner`,
`test_secret_redaction` e `test_ecosystem_health` — ou seja, justamente a
camada que envelopa TODAS as tarefas agendadas do ecossistema.

Nenhum desses testes vermelhos indica falha em produção: os jobs reais rodam
com o layout correto e reportam exit 0. Mas uma suíte com 23 vermelhos
permanentes deixa de servir como barreira — o próximo defeito real entra sem
ninguém notar, que é exatamente como B-2 e B-3 sobreviveram tanto tempo.

**Ação:** decidir entre consertar o layout de import dos testes ou marcá-los
com `skipif` explícito e documentado. Deixar vermelho não é opção.

> A frase acima — "nenhum desses testes vermelhos indica falha em produção" —
> é o erro central deste bloqueio. Os dois indicavam.

### B-12 · lol — a fonte não traz `competition_id`, e o gate exige · **ABERTO, decisão científica**

Descoberto em 2026-07-26 ao sondar por que a coorte segue em 0 sinais depois
de o B-0 cair. **Não é rede e não é a cota do Drive.**

```
provider.list_upcoming_matches(72h)  ->  29 eventos reais
todos os 29                          ->  competition_id = None
h4_gate.py:79  if not competition_id or not competition_name: rejeita
```

O `raw_signals: 0` não é "esperando aparecer jogo". É **100% de rejeição na
criação do sinal**: a busca `/public-search` do Gamma devolve o confronto, o
horário e o preço, mas não devolve a competição, e o gate — corretamente —
recusa inventá-la (`"never infer competition"`, `h4_gate.py:78`).

O fail-closed está certo: foi exatamente por proveniência de competição
incompleta que a v1 (`h4-lol-market-shadow-prospectivo`) virou `SUPERSEDED` em
22/07. Repetir isso inferindo competição destruiria o motivo de a v2 existir.

**Mas o efeito prático é o mesmo do B-2 e do B-3:** infraestrutura que coleta
para sempre e nunca matura. A trial exige **3 competições distintas** e 30
sinais elegíveis; com a fonte atual o contador é estruturalmente zero, não
lentamente crescente. Nenhuma quantidade de espera resolve.

**O que a fonte realmente traz** — inspecionado no payload cru do
`/public-search` em 2026-07-26, para não decidir no escuro:

```
series      = [{"ticker": "league-of-legends", "title": "League of Legends"}]
seriesSlug  = "league-of-legends"
tags        = [{"label": "Esports"}, {"label": "league of legends"}, ...]
title       = "LoL: Gen.G Global Academy vs BNK FearX Youth (BO3)
               - LCK Challengers League Rounds 3-4 Trial Group"
```

Isto fecha a questão de um jeito desconfortável: **não existe campo estruturado
de competição.** O `series` é o jogo inteiro — é `league-of-legends` para
**todos** os eventos, então usá-lo daria **1** competição, nunca as 3 exigidas.
A competição real (`LCK Challengers League`) existe apenas como **texto livre**
no sufixo do `title`, depois de um " - ".

Ou seja, a opção 1 abaixo não é "ler um campo que estávamos ignorando": é
*parsing de string livre de terceiro*, que quebra quando o Polymarket mudar o
formato do título e não avisa quando quebra.

**Isto é decisão científica, não conserto.** As saídas visíveis, e nenhuma é
obviamente certa:

1. Enriquecer a competição por outro endpoint do Polymarket (`series`/`tags`
   aparecem no `/sports`) — precisa provar que o mapeamento é determinístico e
   auditável, senão é inferência com outro nome.
2. Casar o evento contra o `lol.db` (Oracle's Elixir), que tem liga por
   partida — mas isso depende do B-10 e amarra a coorte de mercado ao dado
   base congelado em 10/07.
3. Registrar uma v3 com critério que não exija competição — é trocar o
   critério depois de ver a dificuldade, ou seja, a regra 4.

Enquanto nenhuma for escolhida, o status honesto da `h4-lol-market-shadow-
prospectivo-v2` não é "coletando": é **bloqueada por contrato de fonte**.

### B-4 · f1 — sem fonte de mercado e impossibilidade aritmética

- `MARKET_H2H_NOT_FEASIBLE`: 0 fontes aceitas, 0 cotações
- H8 exige 15 pares forward `VALID_FOR_H8`; contador final 0/15
- `snapshots/` nunca foi criado; `f1-forward-snapshot` está `Disabled`
- Restam **12 corridas** em 2026 (rodadas 11–22, contado em 25/07). 12 < 15

Mesmo reabrindo com pipeline perfeito, o gate não fecha em 2026. Precisa de 2027.

> **Conferido no calendário real em 2026-07-26.** A temporada tem 22 rodadas e
> a 11ª (Hungaroring) é **hoje** — logo restam **11**, não 12. Os dois números
> estão certos nas suas datas e o `VEREDITOS_2026-07-26.md` usa o de hoje; não
> é contradição entre documentos. A conclusão não depende de qual: 11 < 12 <
> 15, e cada dia que passa só afasta mais. Este bloqueio **encolhe sozinho**,
> nunca melhora.

### B-5 · cripto — janela de 28/07 com critério já falhado

- Critério pré-registrado: Spearman IC95 sem cruzar zero (positivo), n≥30, DSR ≥ 0,95
- Parcial de 2026-07-20: Spearman **−0,255** [−0,377; −0,120] — IC não cruza zero,
  mas **na direção oposta à hipótese**. DSR 0,00.
- `trials.json` hoje: `v2-dpl-multi-h7` Sharpe **−0,3258**

Nada técnico falta. Falta executar o gate e registrar o veredito.

### B-10 · lol — fonte-base do Oracle's Elixir caiu · **RESOLVIDO em 26/07 19:10**

> **Encerrado. A cota resetou e a tarefa rodou inteira, verde.** Disparada à
> mão às 19:10 (não se esperou o gatilho de 27/07):
>
> ```
> [download] snapshot publicado: b32041d8f5f2 (fonte 1)
> [ingest]   games no banco: 3953 (2025-01-12 .. 2026-07-26 15:32:40)
> [h4_results] NO_SIGNALS, artefato publicado
> [h4_settle]  {"settled": 0}  OK
> [ratings]  serving materializado: 82 times, 11 ligas
> === atualiza_semanal: fim (exit 0) ===   SUCCEEDED
> ```
>
> O banco saiu de **3.877 jogos congelados em 2026-07-10** para **3.953 até
> hoje** — 16 dias de dado-base recuperados. `lol-ratings-semanal` saiu de
> `PARTIAL`/`FAILED` para `SUCCEEDED` pela primeira vez desde 20/07.
>
> A previsão registrada estava certa: o ID no código sempre esteve correto e a
> cota pública do Drive resetou sozinha. Nenhuma ação humana foi necessária —
> só as duas correções de código de hoje (o import, e a cadeia h4 abaixo), sem
> as quais o reset da cota teria sido inútil.
>
> **O espelho S3 continua morto e piorou:** agora dá NXDOMAIN, antes dava 403.
> O `_urls_para_ano()` está de fato reduzido a uma fonte única, e essa fonte
> falha por cota com regularidade. Uma segunda via real continua valendo.

> **Segunda causa, encontrada em 26/07 pelo B-11 e ausente de todo o
> diagnóstico abaixo: o job não chegava à cota.** O payload semanal quebrava
> no import, exit 1, antes de tocar o Drive — `from src.data.ingestion import
> ...` entrou em `ff56d44` (21/07 20:49) e o módulo nunca teve o próprio ROOT
> na `sys.path`. A última execução foi 20/07 13:28, **um dia antes**, então a
> tarefa semanal nunca disparou com o código quebrado e o exit 10 registrado
> é o `PARTIAL` legítimo da cota, de 20/07.
>
> Consequência para a ação humana: **"esperar o reset da cota" era necessário
> e não suficiente.** Com o reset e sem esta correção, a próxima execução
> falharia com exit 1 sem sequer requisitar o arquivo — e o diagnóstico
> aparente seria "a fonte continua caída", que é a conclusão errada.
>
> Corrigido em `lol-predictor@a7528c0`; suíte 131 verde. **O que resta de
> B-10 é só a cota do Drive**, que reseta sozinha.

Descoberto em 26/07 ao revisar exit codes: `lol-ratings-semanal` está `PARTIAL`
(exit 10) **desde 2026-07-20**.

> **Diagnóstico refeito em 2026-07-26 com navegador real.** A classificação
> inicial ("mais um redirect permanente não seguido") estava **errada**. São
> três problemas independentes, e nenhum é redirect:
>
> **1. ~~O file ID no código não existe mais.~~ ERRATA de 2026-07-26 — isto
> estava errado.** Eu testei `1IDDdzR3JhAOJPnHfSAJHfHtfXTOcaDdw`, que de fato dá
> 404, mas **esse não é o ID do código**: li errado. `DRIVE_IDS` em
> `scripts/atualiza_semanal_payload.py:14` usa
> **`1hnpbrUpBMS1TZI7IovfpKeZfWJH1Aptm`**, que **está presente na pasta atual do
> Drive** e responde `Quota exceeded` — ou seja, existe e está correto.
>
> **Consequência: não há ID a trocar.** O `ORACLES_ELIXIR_2026_URL` não é
> necessário. A cota pública do Google reseta sozinha (~24h) e a coleta volta
> sem intervenção. A ação humana caiu de "descobrir o ID certo" para **nenhuma**
> — só verificar, depois do reset, se o `lol-ratings-semanal` saiu de `PARTIAL`.
>
> **2. O espelho S3 foi desativado por completo.** Testados os anos 2024, 2025 e
> 2026, nos formatos virtual-host e path-style: **403 em todos os seis**. Não é
> o 2026 que sumiu — o bucket `oracles-elixir` deixou de ser publicamente
> legível. Listagem também negada (`AccessDenied`).
>
> **3. Os arquivos atuais existem, mas o Drive está com cota estourada.** A
> página de downloads (que bloqueia fetch automatizado com 403; foi preciso
> navegador) aponta para a pasta pública **`OE Public Match Data`**
> (`1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH`). Extraí ~13 file IDs do DOM. Baixar
> qualquer um devolve `<title>Google Drive - Quota exceeded</title>`.
>
> Consequência: **não é URL errada, é fonte indisponível.** Mesmo com o ID
> correto, o Drive recusa o download agora. A cota pública do Google costuma
> resetar em ~24h.
>
> **Por que não escolhi um dos 13 IDs:** o Drive não renderiza os nomes sem
> login, e o download que revelaria o nome no `Content-Disposition` bate na
> cota. Ingerir o CSV errado (ano ou liga errada) corromperia os 3.877 jogos
> íntegros que sustentam o Elo e as três hipóteses já COMPROVADAS do LoL. O
> custo de errar é muito maior que o de esperar.

Registro do diagnóstico original, preservado:

```
fonte 1 (Google Drive)  -> 404, devolve pagina de erro (2009 bytes)
fonte 2 (S3)            -> 301 PermanentRedirect
   corpo do erro aponta para s3.amazonaws.com, que devolve 403
```

Banco do LoL congelado em **2026-07-10** (3.877 jogos), rodando de cache há 16 dias.

**O fail-closed funcionou:** preservou o cache válido, recusou publicar arquivo
inválido, reportou `PARTIAL`. O que falhou foi ninguém olhar o exit code por 6 dias.

Terceira ocorrência da MESMA classe nesta base: `blockworks.co` (308, cripto,
corrigido 20/07), feed `coindesk` (308, cripto, corrigido 25/07), agora Oracle's
Elixir (301/404). **Redirect permanente de fonte externa é o modo de falha
recorrente deste ecossistema** — vale um monitor de exit code, não só de heartbeat.

**Ação: esperar o reset da cota.** Nenhuma intervenção é necessária — o ID está
correto. Depois do reset (~24h), confirmar que o `lol-ratings-semanal` voltou a
exit 0 e que `data/lol.db` passou de 2026-07-10.

Se a cota persistir (o arquivo é popular e a cota do Drive é por arquivo, não
por usuário), aí sim vale baixar manualmente e apontar
`ORACLES_ELIXIR_2026_URL` para um caminho local. O override existe em
`scripts/atualiza_semanal_payload.py:38` e tem prioridade sobre as duas fontes.

O **espelho S3 continua morto** e isso é permanente: 403 em 2024, 2025 e 2026,
nos dois formatos de endpoint, listagem `AccessDenied`. O fallback do
`_urls_para_ano()` está efetivamente reduzido a uma fonte única — vale
considerar uma segunda via real, já que a atual falha por cota com regularidade.

**Correção estrutural que vale considerar:** as duas fontes do
`_urls_para_ano()` caíram em silêncio e o job passou 6 dias em `PARTIAL` sem
ninguém ver. Um monitor de exit code (não só de heartbeat) teria pego no dia 1 —
vale para todo o ecossistema, não só para o LoL.

Independe do B-0: consertar isto devolve dado-base fresco ao LoL mesmo com a
trilha de mercado bloqueada.

### B-6 · previsao-cripto — vendor do core desatualizado

> **Decisão de 26/07: NÃO sincronizar antes do gate de 28/07.** Trocar o vendor de
> `1.3.2` para `1.3.3` dois dias antes do veredito seria mudança de código no meio
> da trial em curso — o mesmo tipo de contaminação que o resto deste documento
> existe para impedir. A coorte H5 rodou inteira sobre 1.3.2 e deve ser julgada
> sobre 1.3.2. Sincronizar **depois** do gate, junto com o registro do veredito.

Vendor em `1.3.2-ga-20260720`, 44/46 arquivos; faltam `contracts/collection.py` e
`data/collection.py`. Drift limpo (manifest coerente, `dc7676a61c86f908`), não
adulteração. `sync_core.py --check` retorna exit 1 por causa dele.

---

## 3. Corrigidos nesta rodada

### B-7 · lol — guard de encerramento falhava ABERTO · **CORRIGIDO HOJE**

`closure_status` devolvia `None` quando o arquivo não existia, e `assert_h4_open`
passava. **Apagar o registro assinado reabria a coorte**, destruindo contadores e
hashes preservados. O cs-predictor bloqueia exatamente isso; o lol não bloqueava.

Corrigido em `src/h4_gate.py`: o caminho canônico falha fechado na remoção, e foi
adicionado o status `REOPENED_BY_HUMAN_DECISION` exigindo `reopened_at_utc`,
`reopening_decision` e `supersedes_commit`. 4 testes de regressão. Suíte 121 verde.

### B-8 · cs — instalador da task apagado no encerramento · **CORRIGIDO HOJE**

`scripts/install_market_shadow_task.ps1` tinha sido esvaziado e substituído por um
`throw`. A task não estava desabilitada: não existia. Restaurado de `af7f5c8`
(versão pré-encerramento, `RunLevel Limited`, sem UAC) e reinstalado.

### Reaberturas registradas hoje

Ambas por decisão humana do operador, pelo caminho sancionado, com o encerramento
anterior preservado em `previous_closure` e backup `.bak`:

| Projeto | supersedes | Task |
|---|---|---|
| cs | `5e5e7b1` | `cs-market-shadow` Ready |
| lol | `fa0d1b9` | `lol-market-shadow` Ready |

**`operational_status` continua `NO_GO` nos dois.** Reabertura retoma coleta, não
libera capital.

---

## 4. O que NÃO é erro: capital é terminal por desenho

Nenhum dado, amostra ou veredito torna `operational_status` igual a `GO`.

- `lol-predictor/src/betting.py:18-29` — `go_gate` calcula `ready` com todos os
  critérios e usa o resultado **apenas para escolher o texto da justificativa**.
  O campo `decision` é a string literal `"NO-GO"` nos dois ramos. `record_bet`
  exige `decision == "GO"`, valor que a função nunca produz.
- `cs-predictor/src/betting.py:19` — `if real: raise PermissionError(...)`,
  incondicional, sem consultar o gate.
- `previsao-cripto` — `paper_trader`, "sem capital real" por construção.
- `brasileirao-predictor/src/bet_log.py` — ledger **manual**: "OPERADOR apostou".

Varredura por `place_order` / `submit_order` / `place_bet` em código de projeto:
**zero ocorrências** (os únicos hits estão na lib `ccxt` vendorizada).

Nenhum sistema do ecossistema consegue apostar. Levar capital ao ar exige editar
essas funções — decisão humana de remover salvaguarda, não critério a atingir.

---

## 5. H1 do brasileirão com 2023 — registrado como EXPLORATÓRIO

> **Atualização da mesma sessão.** O resultado abaixo foi registrado em
> `data/trials.json` como `h1-ou25-walkforward-2023-2026-exploratoria`
> (sharpe 0,1043), com a proveniência do peek escrita no campo `notes`: o
> baseline sem 2023 foi observado ANTES da decisão de rodar com 2023.
>
> **Efeito real da deflação após o registro:** o segundo Sharpe finito ativou a
> variância entre tentativas, que estava dormente.
>
> ```
> sharpes finitos: [0.0722, 0.1043]   n_trials: 8
> SR0: 0.0331  (era 0.0000)      DSR: 0.9550  — corte 0.95, PASSA por 0.005
> ```
>
> A estimativa anterior (0,9626) assumia 6 trials; com as duas coortes Pinnacle
> registradas são 8. **A folga do DSR deste projeto está esgotada:** qualquer
> tentativa nova com Sharpe finito pode derrubar este resultado abaixo do corte.
> Isso torna "registrar mais análise" uma operação que DESTRÓI evidência, não
> que a melhora.

> **Correção de 2026-07-26, calculada com `expected_max_sharpe` do core.** A
> ressalva acima ("com Sharpe finito") é branda demais e engana na direção
> perigosa. `trials.json` hoje tem **9** entradas — a `h7-clv-prospectivo-
> pinnacle-2026` entrou depois daquele texto —, e `SR0` cresce com o **número**
> de tentativas, não com o Sharpe delas:
>
> ```
> var([0,0722; 0,1043]) = 0,00051520
> n= 8  SR0 = 0,033117      (o texto acima)
> n= 9  SR0 = 0,034519      <- estado de hoje, DSR 0,9518
> n=10  SR0 = 0,035740      <- acima do SR0 critico 0,0353
> n=11  SR0 = 0,036821
> ```
>
> Ou seja: **a décima trial derruba o resultado abaixo de 0,95 mesmo com
> `sharpe: None`.** Registrar qualquer hipótese nova neste projeto — inclusive
> uma pré-registrada que nunca produza número — custa o GO exploratório. A
> regra operacional correta não é "calcule o Sharpe antes de registrar", é
> **não registrar mais nada aqui sem aceitar conscientemente esse preço**.
>
> **Limite desta conta, registrado:** o `SR0` acima é exato (função do core,
> valores do `trials.json` real). O `DSR` resultante **não pôde ser
> recalculado**: a série de retornos das 567 apostas não foi persistida em
> lugar nenhum — o run foi feito em cópia isolada e só o Sharpe agregado
> entrou no registro. O `SR0` crítico 0,0353 vem da rodada anterior e não é
> reproduzível a partir do acervo. **Um resultado de nível GO cujo DSR não pode
> ser re-derivado do registro** é uma falha de arquivamento independente do
> mérito científico: se alguém contestar o 0,9518, não há como refazer a conta.

Rodado em cópia isolada; produção intocada. Season 48982 ingerida: 380 jogos,
249 com O/U.

| | sem 2023 | com 2023 |
|---|---|---|
| blocos | 4 | 6 |
| n (OU2.5) | 461 | 567 |
| ROI | +8,77% | +11,48% |
| CLV open | +19,39% | +20,60% |
| PSR | 0,9578 | 0,9935 |
| IC95_lower | −0,0105 | **+0,0264** |
| veredito | NO-GO | **GO** |

DSR honesto, se registrado como 6ª tentativa (Sharpe 0,1043 ativa a variância
entre trials): `SR0 = 0,0295`, **DSR = 0,9626** — ainda ≥ 0,95.

**Não registrado, de propósito.** O run é diagnóstico: o baseline foi visto antes
da decisão de registrar, e a trial registrada declara `seasons: ["2024","2025"]`.
Atenuante verificável: a ingestão de 2023 foi pré-autorizada em 2026-07-10, no dia
do NO-GO, antes de qualquer dado de 2023 existir. É um movimento pré-especificado,
não garimpo — mas não é pré-registro verdadeiro.

Ressalva que vale mais que o número: isto é backtest contra odds agregadas do
Sofascore. Não prova capturabilidade. O WC tinha CLV +16,9% no funil validado e
P&L real de **−5,84u**.

---

## 6. Correção de leitura desta própria sessão

Registrado porque a conclusão errada era operacional, não cosmética.

Eu afirmei que reabrir CS e LoL era "o melhor negócio disponível, zero código,
pipeline provado". **Estava errado em dois níveis, e o segundo é pior.**

1. A metade de settlement não roda: o CS não tem entrypoint algum (B-2) e o LoL
   não tem agendamento (B-3). Sem isso os dois chegam aos 30 dias com 0 maturadas.
2. Pior: **a coleta em si não funciona nesta rede** (B-0). O DNS bloqueia o domínio
   polymarket.com e o fallback DoH criado para contornar isso também está bloqueado.
   Verificado ao vivo: as duas tarefas rodaram hoje e falharam.

Portanto o encerramento de 2026-07-23 pode ter coincidido com a perda de acesso à
fonte, não só com impaciência. Não afirmo causalidade — registro a coincidência de
datas para quem for reabrir a investigação.

Ordem correta de prioridade: **B-0 primeiro** (sem fonte não há coorte), depois
B-2 e B-3, e só então esperar qualquer coisa das coortes reabertas.

A conclusão mais útil desta rodada é desconfortável: **o único projeto com trilha
científica viva e fonte de dados funcionando é o brasileirão** — e ele está travado
por um defeito de proveniência que é corrigível por código (B-1).
