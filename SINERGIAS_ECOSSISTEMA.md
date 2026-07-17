# Sinergias do Ecossistema — o que cada projeto agrega aos outros

> Criado 2026-07-11, após o fechamento dos ciclos de brasileirão/NBA/CS/LoL
> e a Fase 0 da F1. Documento vivo: atualizar quando uma sinergia for
> executada ou uma nova for identificada.
>
> **Atualizado em 2026-07-17** com o resultado da Reintegração do Ecossistema
> (Fase 1 — descoberta read-only; Fase 2 — execução controlada em ondas,
> Ondas 1 a 5). A seção abaixo é o estado atual; as seções de 2026-07-11 mais
> adiante ficam como registro histórico e não foram reescritas.

---

## Reintegração do Ecossistema — 2026-07-17 (Ondas 1–5)

### Contrato temporal conceitual (formalização, sem código compartilhado)

Descoberto na Fase 1: o par PRE_EVENT/MATURED do f1-predictor e o par
OPEN/settlement do brasileirao-predictor implementam o **mesmo padrão
conceitual**, com rigor de implementação diferente. Este é o núcleo semântico
comum, **documentado aqui apenas como contrato conceitual — não promovido a
código compartilhado nem a predictor_core/tools/**:

1. a previsão é criada antes do evento;
2. existe identidade estável do evento;
3. existe scheduled time;
4. existe timestamp de criação;
5. existe provenance;
6. o payload original se torna imutável;
7. o resultado é anexado posteriormente, nunca sobrescrevendo o original;
8. maturação não edita a previsão original;
9. existe vínculo verificável entre previsão e resultado;
10. artefato retrospectivo não conta como evidência forward;
11. erros de maturação não podem reescrever a decisão anterior;
12. o ciclo deve ser auditável e reproduzível.

**Extensões locais preservadas, não generalizadas:**

- **F1** (`f1-predictor/src/snapshots.py`): hash SHA-256 explícito entre
  PRE_EVENT e MATURED (`pre_event_payload_hash`), escrita exclusiva de SO
  (`open(..., "x")` — overwrite estruturalmente impossível, não só checagem
  lógica), verificação temporal reforçada na escrita E na leitura, gate de
  amostra por contagem (`H8_REQUIRED_RACES = 15`).
- **Brasileirão** (`bet_log.py`/`settle.py`): TrialRegistry com governança
  N+1, PSR/DSR como gate estatístico (não contagem simples), JSONL
  append-only por convenção de código (não por exclusividade de SO),
  vínculo por `bet_line_no`/`bet_id` (não hash de conteúdo).

Nenhuma implementação foi declarada padrão universal. Nenhum código foi
promovido a `predictor_core` ou `tools/` como resultado desta formalização.

### Estado factual das integrações concluídas (Ondas 1–4)

| Item | Estado |
|---|---|
| `sync_core.py` com sincronização direcionada (`--target`) | Concluído (Onda 2A). Sem `--target`, comportamento idêntico ao anterior; com `--target`, escreve só no consumidor nomeado. 16 testes de isolamento. |
| f1-predictor vendorizando predictor_core 1.3.1-ga-20260716 | Concluído (Onda 2). Antes: `1.3.0-ga-20260711` (drift de 1 patch, 10 arquivos divergentes). Byte-idêntico ao canônico, confirmado por vendor byte audit e core provenance. |
| `tools/secret_redaction.py` sem literal `x-cg-demo-api-key` | Concluído (Onda 3). Cobertura genérica preservada (fragmento `api[_-]?key` já cobre o caso), 9 testes novos provando a ausência do literal e a cobertura mantida. |
| `tools/release_manifest.py` como gerador canônico de `TOOLS_MANIFEST.json` | Concluído (Onda 3A). Lacuna real descoberta: não existia mecanismo para regenerar o manifesto após mudança legítima de conteúdo, deixando `tools/` estruturalmente "não publicável" sob provenance estrita. 19 testes; reutiliza `tools_provenance.content_hash`/`_tracked_files` como única fonte do algoritmo (não duplica). |
| Provenance estrita de `tools/` funcional | Concluído (Onda 3A). `collect_tools_provenance(strict=True)` = MATCH, confirmado após cada onda subsequente. |
| Teste do F1 sem versão de `tools/` hardcoded | Concluído (Onda 3). `test_snapshots.py` lia `tools_provenance["version"] == "1.1.0"` fixo; agora deriva de `tools/VERSION` (fonte canônica), com verificação independente via `collect_tools_provenance()`. |
| previsao-cripto consumindo `tools.secret_redaction` | Concluído (Onda 4). `_RedactSecrets` (único consumidor, em `scripts/garimpo_fase1.py`) virou adaptador fino sobre `safe_redact_text` — zero regex própria, zero lista de nomes sensíveis própria. Cobertura ampliada (padrões genéricos, não só valores conhecidos). Marcador de log mudou de `***` para `[REDACTED]`, documentado e testado. |
| Working tree de predictor_core, tools, f1-predictor, previsao-cripto | Limpa, com commits locais (sem push) ao final de cada onda. |

**Achados mantidos como DEFER** (investigados, não implementados nesta fase — decisão explícita de não agir agora):

- **Elo do F1 vs. `predictor_core/kernel/rating.py`**: mesma família matemática (Bradley-Terry/logístico), mas divergência real na combinação de K (média no F1, máximo no core) e persistência acoplada ao update no F1 (o core é puro). Classificado `DUPLICATED_DRIFT` no núcleo de update; `DOMAIN_LOCAL` na camada de simulação Plackett-Luce/Gumbel (sem equivalente no core). Migrar mudaria ratings históricos — não investigado se há 2º consumidor real para a extensão necessária.
- **`tools/release_check.py` sem teste dedicado**: monolítico (roda `git clone` real + `pytest` real duas vezes), sem pontos de injeção; testar os caminhos negativos exigidos (worktree sujo, fingerprint inconsistente) exigiria refatoração fora de escopo.
- **`api_guard.allow()`** (previsao-cripto, `core/api_guard.py`): genérico na mecânica, hoje com 1 único consumidor — aguardando 2º consumidor real antes de cogitar `tools/`.
- **`require_finite()`** (previsao-cripto, `dpl/providers/_validation.py`): mecânica genérica, mensagem de erro parametrizada com vocabulário de mercado — precisaria de extração antes de mover.
- **Lock local do Cripto vs. `operational_runner.py`**: `operational_runner.py` já tem lock com stale-detection; o lock local do Cripto (`acquire_lock`/`_lock_is_stale` em `garimpo_fase1.py`) não foi comparado a fundo nem promovido nem descartado — registrado para comparação futura.
- **Contrato temporal em código**: formalizado só em documentação (acima), não em `predictor_core`/`tools`/pacote compartilhado.
- Qualquer promoção nova ao core ou a `tools/` além do que já foi feito nas Ondas 2A/3A.

### Matriz de capacidades (atualizada)

| Capacidade | Origem | Consumidores | Estado | Classificação | Destino | Observação |
|---|---|---|---|---|---|---|
| Contratos (`PredictionPoint`, `MarketDataPoint`) | predictor_core | 8 domínios (vendoring) | Estável | CORE_READY | predictor_core | Sem mudança nesta reintegração |
| TrialRegistry / governança N+1 | predictor_core | brasileirão, cs, lol, cripto, stocks (confirmado por import) | Estável | CORE_READY | predictor_core | — |
| Anti-lookahead estrutural (`replay`/`PastView`) | predictor_core | domínios que fazem backtest | Estável | CORE_READY | predictor_core | — |
| `RatingBook`/`EloEngine` genérico | predictor_core (`kernel/rating.py`) | não confirmado como consumido pelo F1 | DUPLICATED_DRIFT (núcleo) / DOMAIN_LOCAL (simulação) | — | DEFER | Ver achado acima; não migrar sem 2º consumidor e reconciliação de K |
| `operational_runner.py` (runner com heartbeat/lock/timeout) | tools/ | brasileirao-predictor (import comprovado, `sombra_diaria.py:14`); cs/lol/cripto (indício forte por grep, não relido linha a linha) | Estável | TOOLS_READY | tools/ | — |
| `tools_provenance.py` (proveniência de release) | tools/ | cs-predictor (`cs_snapshots.py`, 5 usos), f1-predictor (`snapshots.py`) — ambos import comprovado | Estável | TOOLS_READY | tools/ | — |
| `release_manifest.py` (gerador canônico do manifesto) | tools/ | uso manual/CI de `tools/` | Novo (Onda 3A) | TOOLS_READY | tools/ | Sem consumidor externo — é ferramenta de manutenção do próprio `tools/` |
| `secret_redaction.py` | tools/ | previsao-cripto (import comprovado, Onda 4); `operational_runner.py` (interno) | Estável, cobertura ampliada nesta onda | TOOLS_READY | tools/ | — |
| F1 PRE_EVENT/MATURED | f1-predictor (`src/snapshots.py`) | f1-predictor | Estável | DOMAIN_LOCAL | f1-predictor | Ver contrato temporal conceitual acima |
| Brasileirão OPEN/settlement | brasileirao-predictor (`bet_log.py`) | brasileirao-predictor | Estável | DOMAIN_LOCAL | brasileirao-predictor | Ver contrato temporal conceitual acima |
| Cripto logging redaction | previsao-cripto (`scripts/garimpo_fase1.py`) | previsao-cripto | Migrado para consumir tools/ (Onda 4) | DOMAIN_LOCAL (adaptador) | previsao-cripto | Delega 100% a tools/secret_redaction |
| CS/LoL aliases | cs-predictor, lol-predictor (`config.py`) | cada projeto, local | Parcialmente equivalente (LoL estende com 2ª fonte) | DOMAIN_LOCAL | local | Não compartilhar — divergência legítima |
| CS/LoL freshness | cs-predictor (módulo central), lol-predictor (lógica embutida em script) | cada projeto, local | Apenas inspirado, maturidade diferente | DOMAIN_LOCAL | local | Não compartilhar |
| WC odds/EV/CLV/settlement | wc-predictor-v2 | histórico | Encerramento | HISTORICAL_LESSON | documentação | Não migrar, não tocar código |
| Stocks (custos, benchmark, point-in-time) | predictor-stocks | histórico | Encerrado | HISTORICAL_LESSON | documentação | Não reabrir hipótese |
| NBA (todo o projeto) | nba-predictor | — | Arquivado | DO_NOT_TOUCH | — | Fora da integração ativa, não analisado nesta fase |

### Matriz de dependências (atualizada)

| Direção | Estado | Evidência |
|---|---|---|
| projetos de domínio → predictor_core | Confirmado, unidirecional | `sync_core.py` só escreve vendor; nenhum import reverso encontrado |
| projetos operacionais → tools/ | Confirmado, unidirecional | idem |
| projeto de domínio → outro projeto de domínio (ex. cs↔lol) | **Nenhum encontrado** | grep de import direto entre cs-predictor/lol-predictor: zero resultados |
| core/tools → projeto de domínio | **Nenhum encontrado** | `tools/` não importa lógica de domínio; único vazamento (literal CoinGecko) removido na Onda 3 |
| f1-predictor → vendor predictor_core | **Consumidor comprovado**, 1.3.1-ga-20260716, byte-idêntico | vendor byte audit + core provenance, Onda 2 |
| previsao-cripto → tools.secret_redaction | **Consumidor comprovado** | teste dedicado confirma mesmo objeto de função resolvido, Onda 4 |
| f1-predictor, cs-predictor → tools_provenance | **Consumidor comprovado** (import direto lido) | `cs_snapshots.py:75-76`, `snapshots.py` |
| brasileirao-predictor → operational_runner | **Consumidor comprovado** (import direto lido) | `sombra_diaria.py:14` |
| lol-predictor, previsao-cripto → operational_runner | **Indício forte, não verificado por execução** | grep positivo em `atualiza_semanal*.py`/`watchdog_coleta.py`; não relido linha a linha nem executado nesta reintegração |

### Sinergias CONFIRMADAS (2026-07-17)

- predictor_core → projetos vivos (já em produção antes desta reintegração, mantido).
- tools provenance → F1/CS (comprovado por import, Onda 3A validou o mecanismo).
- tools redaction → Cripto (executado na Onda 4).
- Sincronização direcionada por consumidor no `sync_core.py` (Onda 2A) — mecanismo novo, testado, sem efeito colateral em outros consumidores.
- CircuitBreaker já unificado em `predictor_core.data.circuit_breaker` (achado pré-existente à Fase 1, confirmado — previsao-cripto tinha 2 implementações duplicadas, já reconciliadas antes desta reintegração).
- `require_secrets`/`MissingCredentialsError` já unificado em `predictor_core.kernel.settings` (idem, achado pré-existente confirmado).
- Governança CS/LoL (`governanca.py`, `atualiza_semanal.py`) — comprovadamente do mesmo desenho (comentário cruzado no código confirma intenção deliberada de simetria).

### Sinergias REJEITADAS

- Unificação de calibração CS/LoL — bifurcação deliberada e documentada no próprio código (CS remove intercepto por invariância A/B; LoL mantém Platt de 2 parâmetros). Não é drift a corrigir.
- Modelos de mapas/BO de CS para LoL — diferença de domínio real (mapas fazem sentido em CS2, não do jeito modelado aqui em LoL).
- Serviço genérico de calendário — não existe em nenhum dos dois projetos hoje; não inventar sem lacuna comprovada.
- Promoção imediata do lifecycle temporal (PRE_EVENT/MATURED, OPEN/settlement) ao predictor_core — formalizado só como contrato conceitual em documentação, não em código.
- Migração do Elo do F1 para `kernel/rating.py` nesta fase — risco confirmado de alterar ratings históricos, sem 2º consumidor verificado para justificar.

### Sinergias DEFER

Ver seção "Achados mantidos como DEFER" acima — contrato temporal em código, `api_guard`, `require_finite`, lock local do Cripto, testabilidade do `release_check.py`, Elo F1 vs. core.

---

## Estado dos modelos (2026-07-11)

| Projeto | Modelo | Estado | Limitação conhecida |
|---|---|---|---|
| brasileirao | Poisson/NegBin (OU2.5) | NO-GO, CLV +19,6%, **H3 sombra AUTOMATIZADA** | IC do pnl cruza zero (N pequeno) |
| cs | Elo série + **Platt (N+1 comprovada)** | H1 comprovada; Brier 0,4573→0,4518 | resolvida a sobreconfiança |
| lol | Elo mapa (cru) + kills por liga | H1 comprovada; Platt N+1 REFUTADA (p=0,36) | subconfiança leve não-significativa |
| f1 | Plackett-Luce ordinal | Fase 0; prompt Fase 1 pronto | aguarda backtest ordinal |
| nba | Normal de totais | NO-GO claro (CLV −4,6%) | arquivado até hipótese nova |
| wc | Poisson (Copa) | encerrando (semis/final) | migra para brasileirão |
| cripto | HMM + LLM multi-juiz | V3 NO-GO; H5 em coleta até 28/07 | fora do escopo esportivo |
| stocks | — | operacional | sem TrialRegistry (avaliar adoção) |
| core | v1.1.0 | 8/8 em sincronia | roadmap agosto abaixo |

## Sinergias EXECUTADAS (2026-07-11)

1. **CS → LoL: calibração Platt** (`src/calibration.py`, stdlib Newton).
   Governança N+1 nos dois: CS **COMPROVADA** (a=0,68 achata; serving
   calibrado, `elo-platt-fase1`); LoL **REFUTADA** (DM p=0,36; serving segue
   cru, gancho pronto). Lição: a mesma correção decide DIFERENTE por domínio
   — por isso cada uma é trial própria.
2. **Brasileirão: sombra automática**. `scripts/sombra_diaria.py`
   (ingest→espelho→cron→settle→capture→report, idempotente, log próprio) +
   Task Scheduler diário 10h/23h (`brasileirao-sombra-manha/-noite`).
3. **Monitor de saúde**: `ecosystem_health.ps1` (raiz do workspace),
   agendado domingo 22h (`ecosystem-health-semanal`) — testes, trees,
   sync_core, tarefas agendadas, último log da sombra.
4. **F1: prompt da Fase 1** (`f1-predictor/docs/PROMPT_FASE1.md`) — estreia
   do RPS e do nullref do core; baseline decisivo = grid de largada.

## Sinergias PENDENTES (backlog priorizado)

5. **Padrão H3-sombra (brasileirão → CS/LoL Fase 1b)**: `sombra.py` é o
   template para validar odds ao vivo de e-sports quando houver fonte.
6. **Ciclo settle (wc/brasileirão → e-sports/F1)**: aferição pós-evento dos
   logs de predição (hoje só futebol tem).
7. **Estratificação do edge (brasileirão → qualquer apostador)**: o CLV
   cresce com o edge (2-5% é ruído; 10-15% é sinal) — filtro empírico por
   distribuição de CLV em vez de threshold fixo, a incorporar quando algum
   domínio chegar à operação.
8. **Plackett-Luce (F1 → e-sports)**: classificação final de
   playoffs/mundiais de CS/LoL com a implementação de referência da F1.
9. **nullref (F1 → brasileirão)**: piso de "apostador aleatório nos mesmos
   jogos" como sanity extra do funil.

## Candidatos ao CORE (roadmap de agosto, junto com o Ledger)

- `shin_probabilities` (hoje duplicado em wc/brasileirão; NBA usou de-vig
  proporcional por falta dele);
- cliente curl_cffi+impersonate (3 cópias: sofascore ×2, hltv);
- `PlattCalibrator` (2 cópias: cs, lol — genérico, testado, stdlib);
- motor prequential prever→atualizar (3 reimplementações: cs, lol, f1);
- harness "evaluate por Brier+DM" (2 cópias: cs, lol; f1 terá o ordinal).

Regra: mudança de core tem ciclo próprio (sync_core --write + suítes dos 8
consumidores) — não fazer junto com trabalho de domínio.

## Serviços agendados (Task Scheduler)

| Tarefa | Quando | O quê |
|---|---|---|
| brasileirao-sombra-manha | diária 10:00 | ingest→settle→capture (H3) |
| brasileirao-sombra-noite | diária 23:00 | idem (pega jogos da noite) |
| cs-ratings-semanal | segunda 08:00 | ingest HLTV 35d + ratings + Platt |
| lol-ratings-semanal | segunda 08:30 | CSV OE do ano + ingest + ratings |
| ecosystem-health-semanal | domingo 22:00 | saúde dos 9 projetos + frescor H5 |
| GarimpoInvestimentos-ColetaDiaria | diária 18:00 | ingest + **previsões 4 juízes (H5)** + backtest/maturação — já era automática (evidência 10/07: 28 previsões, 4 juízes, 0 fallback) |
| GarimpoV3Daily | diária 21:30 | paper trading V3 |
| cripto-watchdog-coleta | diária 19:00 | vigia a coleta H5 (lição OPS-1); falha → ALERTA_COLETA_CRIPTO.txt |

## Pendências FECHADAS em 2026-07-11 (2ª rodada)

- **W2 (bet_id)**: uuid4 em toda aposta nova + carimbo no settlement, schema
  aditivo (legado intacto) — no wc (237 verdes) E no brasileirão (244; a H3
  herda a rastreabilidade quando promover picks ao livro).
- **Coleta H5**: verificada como JÁ automática (o run_daily.ps1 das 18h roda
  `main --summary` que grava as previsões carimbadas por juiz, e o backtest
  do passo 3 matura as trials). O que faltava era VIGILÂNCIA → watchdog 19h.
