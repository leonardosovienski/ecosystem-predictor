# Handoff canônico da sessão Codex

> **STATUS: HISTORICAL.** `SUPERSEDED_BY: ECOSYSTEM_HANDOFF.md`.
> `LAST_RECONCILED: 2026-07-18`. Documento de 2026-07-15, anterior à
> reintegração (Ondas 1-6), ao hardening geral, e às rodadas de evolução
> de `tools/`/`predictor_core` desta linha do tempo. Preservado como
> registro histórico válido do que foi feito até aquela data — não é mais
> a fonte de continuidade operacional. Use `ECOSYSTEM_HANDOFF.md` e
> `PENDENCIAS_ABERTAS.md` para o estado atual.

**Data de consolidação:** 2026-07-15  
**Escopo:** auditoria do ecossistema quantitativo, hardening operacional, provenance de `tools/`, reconciliação Git e segundo consumidor temporal CS.  
**Regra de leitura:** este documento separa fatos atuais, fatos históricos e limitações. Um commit, relatório ou teste verde não é tratado como prova científica ou de execução forward real quando essa prova não existe.

## 1. Objetivo original da sessão

A sessão começou como uma auditoria em camadas de todo o workspace: inventário, fundação (`predictor_core`, vendors e ferramentas), projetos ativos, projetos legados, matrizes de capacidade/arquitetura/ciência/operação/evolução, síntese horizontal, Conselho, Red Team e veredito executivo. O objetivo não era redesenhar a plataforma durante a descoberta, mas tornar explícitos os limites entre infraestrutura compartilhada, protocolos temporais e lógica de domínio.

Depois do veredito, a execução foi deliberadamente limitada a mudanças pequenas, reversíveis e testáveis:

1. hardening operacional e provenance;
2. versionamento mínimo de `tools/`;
3. rollout de provenance nos consumidores elegíveis;
4. reconciliação Git sem apagar trabalho prévio;
5. implementação local de PRE_EVENT/MATURED no CS como segundo consumidor real do protocolo temporal.

Não foram autorizados nem implementados: modelos novos, alteração de Elo/Platt, odds, OPEN/SETTLED, shadow econômico de CS/LoL, alteração de Scheduler fora das migrações anteriores, execução financeira, promoção de contrato ao `predictor_core` ou solução silenciosa do incidente de segredo do cripto.

## 2. Linha do tempo das fases

| Fase | Estado antes | Ação e estado depois | Evidência principal |
|---|---|---|---|
| Auditoria 00–13 | Workspace sem mapa consolidado | Inventário, fundação, matrizes, Conselho, Red Team e veredito produzidos | `audit/00`–`13` |
| Implementações operacionais iniciais | tarefas e proveniência fragmentadas | wrapper operacional, lock, timeout, heartbeat, JSONL, health e redação foram aplicados nos projetos então autorizados | `audit/16`–`21` |
| F1 forward snapshots | H8 dependia de dados retrospectivos sem prova temporal | PRE_EVENT/MATURED local F1 implementado e testado; sem snapshot real/H8 validado | `audit/34`–`36`, commit `5ab0433` |
| Fechamento cross-domain | candidatos compartilháveis confundidos com core | tooling operacional separado de protocolos temporais e domínio; sem promoção ao core | `audit/45`–`55` |
| Fase 1 — Git de `tools/` | ferramentas compartilhadas fora de Git | repositório mínimo criado em 1.0.0 | `b24e283`, `audit/56` |
| Fase 2 inicial | consumidores exigiam provenance, runner 1.0.0 não a emitia | corretamente classificada BLOCKED, sem integração parcial | versão histórica de `audit/57` |
| Fase 2A | bloqueio por ausência de provenance nativa | `tools/` 1.1.0 emite provenance strict em heartbeat/JSONL | `6367b40`, `2c3d501`, `audit/57A` |
| Fase 2B | Brasil/LoL/F1 limpos; CS/cripto impróprios | Brasil, LoL e F1 integrados; CS/cripto bloqueados factualmente; WC N/A | `audit/57` |
| Reconciliação Git | cripto/WC detached, F1 fora da main, CS com EP3 não rastreado | cripto/WC normalizados para `main`, F1 fast-forward, estados restantes classificados/preservados | `audit/58` |
| CS segundo consumidor temporal | CS sem PRE_EVENT/MATURED e EP3 não rastreado | EP3 preservado; PRE_EVENT/MATURED local, append-only e strict implementado | `71e01ab`, `562a74f`, `audit/60` |

## 3. Estado antes/depois das fases recentes

### Tools 1.0.0 → 1.1.0

Antes, `operational_runner` produzia heartbeat e JSONL, mas não podia provar de qual versão de `tools/` vinham. Alterar somente os wrappers dos consumidores teria deixado o JSONL do runner sem provenance. Isso justificou o bloqueio inicial da Fase 2.

Depois, `tools/` permanece um repositório Git simples — não pacote instalado e não monorepo — com provenance nativa, aditiva e strict:

- `VERSION`: `1.1.0`;
- commit atual: `2c3d501189cf031bb140203cc9ceb6b835b929d8`;
- content hash: `40b8a99d28138842090b951fac1158255d231e73260033cb8dd57142db7effa6`;
- `TOOLS_MANIFEST.json` e algoritmo `sha256-path-nul-content-nul-v1`;
- `tools_provenance` em cada novo heartbeat e evento JSONL;
- metadata opcional de consumidor via `--consumer-provenance-json`;
- strict falha se Git, VERSION, manifesto, hash ou limpeza da árvore não forem verificáveis.

O rollback de `tools/` para o estado anterior é `b24e283f273afa5e56ae0372b8c0335ce05ee2b1` (1.0.0). O hash 1.0.0 era `32af466ef87165addce453da48bbacdaca724330a5ee63cde44e5282fe5c85be`.

### Rollout de provenance

Brasil e LoL passaram metadata de consumidor aos wrappers; o runner continua sendo o único emissor de identidade de `tools/`. F1 passou a registrar provenance em novos snapshots PRE_EVENT/MATURED e a expô-la nos comandos de verify/status. Artefatos históricos não foram reescritos.

CS não entrou no rollout operacional daquela fase porque havia mudanças não rastreadas. Essa afirmação histórica não significa que CS continua sem protocolo temporal: após reconciliação, ele recebeu o módulo local de snapshots, com provenance nativa de `tools/`, mas o wrapper semanal de CS não foi alterado nesta fase temporal.

### Reconciliação Git

O objetivo foi preservar conteúdo, não “limpar” com descarte:

- cripto e WC estavam detached exatamente no commit de `main`; ambos foram trocados para `main` sem alterar seus diffs locais;
- F1 foi fast-forward de `19e3ec4` para `aae48a1`, sem merge de conteúdo concorrente;
- CS teve os dois artefatos EP3 classificados e depois preservados em commit próprio;
- Stocks e NBA foram apenas classificados: não houve push, reset, sync write ou commit de vendor.

### CS PRE_EVENT/MATURED

O CS agora possui `python -m src.cs_snapshots` com comandos claros:

```text
snapshot-pre-event --event-file EVENT.json --snapshots-dir DIR
verify-snapshot --snapshot PATH
mature-snapshot --event-id ID --year YYYY --result-file RESULT.json --snapshots-dir DIR
snapshot-status --year YYYY --snapshots-dir DIR
```

O módulo lê `cs.db` em `mode=ro`, lê ratings/config/calibração, exige Git/provenance estritos, escreve JSON atômico e append-only, usa `fsync`, recusa overwrite e não usa rede em verify. MATURED não reexecuta o modelo, não altera probabilidades, ratings ou banco. A cadeia sintética CLI passou em diretório temporário; ela não é evidência forward. Não há snapshot real em `cs-predictor/snapshots/`.

## 4. Branches, commits e estado atual por projeto

| Projeto | Branch | Commit | Git | Técnico | Operacional | Científico | Econômico | Próximo passo |
|---|---|---|---|---|---|---|---|---|
| `tools` | `main` | `2c3d501` | limpo | 1.1.0, runner/provenance/redaction/health funcionais | pronto para ser consumido em strict | N/A | N/A | não alterar; usar como referência congelada |
| `predictor_core` | `main` | `08eb659` | limpo | vendor canônico; versão vendorizada observada `1.3.0-ga-20260711` | sem alteração nesta etapa | não é hipótese científica | N/A | não promover PRE_EVENT/MATURED ainda |
| `brasileirao-predictor` | `main` | `13b3889` | limpo | wrapper operacional com metadata de consumidor | pronto para observação; ciclo natural ainda é evidência requerida | shadow/H3 sem amostra maturada suficiente | sem shadow econômico novo | observar ciclos naturais e maturar amostra |
| `lol-predictor` | `main` | `58d1691` | limpo | refresh semanal com provenance de consumidor | pronto para observação; ciclo natural pendente | previsões históricas não são prova forward nova | sem shadow econômico | observar ciclo; só então considerar protocolo temporal/odds separado |
| `f1-predictor` | `main` | `aae48a1` | limpo | snapshots PRE_EVENT/MATURED e provenance em main | sem Scheduler novo nesta sessão | H8 continua sem evidência forward real suficiente | N/A | capturar próximo grid/evento real antes da corrida |
| `cs-predictor` | `main` | `9e6e12f` | limpo | wrapper semanal já em main; snapshots locais PRE_EVENT/MATURED novos | PRE_EVENT real capturado/verificado; MATURED pendente | segundo consumidor temporal parcialmente comprovado | sem odds, OPEN/SETTLED ou shadow | maturar Stake Ranked 3DMAX × HEROIC após o resultado |
| `previsao-cripto` | `main` | `4fcfc31` | **sujo**: cinco mudanças de automação/watchdog preservadas | HEAD normalizado, mas mudanças não revisadas/commitadas | **BLOCKED** por credencial/logs e ausência de ciclo pós-hardening | V3 NO-GO; H5 coleta depende do bloqueio | não validado | ação humana de segredo/logs antes de qualquer execução |
| `wc-predictor-v2` | `main` | `a1f7701` | **sujo**: HANDOFF e vendor parcial | branch canônica confirmada | congelado/histórico; sem automação nova | histórico; não é fonte de evidência nova | dados de odds/settlement históricos não devem ser transferidos sem fase própria | reconciliar vendor/HANDOFF separadamente |
| `predictor-stocks` | `main` | `cc0f514` | `AGENTS.md` não rastreado; `main` 31 commits à frente de `origin/main` | laboratório histórico preservado | não há tarefa operacional desta sessão | pesquisa encerrada/NO-GO histórico, conforme relatórios | não aplicável para uso atual | revisar cadeia local e decidir push com autorização explícita |
| `nba-predictor` | `main` | `9e51c28` | **sujo**: vendor parcial | arquivado/legado | sem operação nova | Fase 1 histórica NO-GO | N/A | reconciliar vendor apenas em fase própria |

## 5. Arquivos criados ou alterados nesta sessão

### Auditoria e documentação

- Relatórios de auditoria em camadas: `audit/00_AUDIT_CHARTER.md` até `audit/13_FINAL_VERDICT.md`, mais checkpoint/reconciliação e matrizes `04A`, `09A`, `12A`.
- Relatórios operacionais/cross-domain posteriores: `audit/14` até `audit/55`.
- Fechamentos desta execução: `audit/56_TOOLS_VERSIONING_CLOSURE.md`, `audit/57_TOOLS_PROVENANCE_ROLLOUT.md`, `audit/57A_TOOLS_NATIVE_PROVENANCE.md`, `audit/58_GIT_RECONCILIATION.md`, `audit/60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md`.
- Índices históricos existentes: `audit/EVIDENCE_INDEX.md`, `audit/OPEN_QUESTIONS.md`, `audit/AUDIT_STATE.md`.

### Tools

- Criados/alterados: `VERSION`, `TOOLS_MANIFEST.json`, `tools_provenance.py`, `operational_runner.py`, `PROVENANCE.md`, `README.md`, `CHANGELOG.md`, e testes de provenance/runner/redaction.
- Commits: `6367b40` (implementação) e `2c3d501` (hash estável entre clones).

### Consumidores

- Brasil: `scripts/sombra_diaria.py`, `tests/test_operational_provenance.py`; commit `13b3889`.
- LoL: `scripts/atualiza_semanal.py`, `tests/test_operational_provenance.py`; commit `58d1691`.
- F1: snapshots forward e testes foram incorporados à `main` por fast-forward; provenance adicionada em `src/snapshots.py`; commits relevantes `5ab0433`, `aae48a1`.
- CS: `data/fixtures/stake_ranked_ep3.json` e `scripts/predict_matches.py` preservados em `71e01ab`; `src/cs_snapshots.py` e `tests/test_cs_snapshots.py` criados em `562a74f`.

## 6. Testes executados e resultados observados

| Área | Resultado registrado |
|---|---|
| `tools/` 1.0.0 | workspace `64 passed, 1 skipped`; clone isolado `45 passed, 20 skipped` |
| `tools/` 1.1.0 | workspace `70 passed, 1 skipped`; clone isolado `51 passed, 20 skipped` |
| tools — runner/redaction/health/hashing | `35 passed` em recorte específico da Fase 2A |
| Brasil | `275 passed`, com um warning pré-existente de parâmetro no bound |
| LoL | suíte retornou exit 0 durante Fase 2B |
| F1 | suíte retornou exit 0 após fast-forward; snapshots específicos reportados com 4 testes passando |
| CS snapshots | seis testes novos passaram; suíte completa do CS retornou exit 0 |
| vendor byte audit | Brasil, LoL, F1 e CS: `IDENTICAL`, 44 arquivos |
| runtime core provenance strict | Brasil, LoL, F1 e CS: `MATCH` |
| `sync_core --check` | exit 0; oito vendors declararam sincronia |
| smoke strict Brasil/LoL | heartbeat e JSONL continham `tools_provenance` 1.1.0 e `consumer_provenance` |
| smoke CLI CS | PRE_EVENT → verify → MATURED → `MATURED` em diretório temporário |

As verificações registradas não provaram ciclos naturais de Brasil/LoL/CS, nem uma cadeia CS forward real. Também não substituem avaliação científica por terem sucesso técnico.

## 7. Bancos, ratings e artefatos preservados

Durante o rollout, os hashes antes/depois foram iguais para:

- Brasil: `matches.db`, `walkforward_summary.json`, `predictions.jsonl`;
- LoL: `lol.db`, `ratings.json`, `walkforward_summary.json`, `predictions.jsonl`;
- F1: `f1.db`, `ratings.json`, `validacao_2026_ultima.json`, `predictions.jsonl`;
- CS: `cs.db` = `a7dbef610b176250e3b1d7fe91ac2d79acac13e2c258884c46e35ab0e2c6f2ee`; `ratings.json` = `40379586465d8958957b068f3e65ebb59fec575f6521673e7b9674bcb132e516`.

Os snapshots sintéticos CS ficaram exclusivamente em diretório temporário. Além deles, o PRE_EVENT real 3DMAX × HEROIC foi preservado no commit `9e6e12f`; ainda não há MATURED real. Nenhum EP3 foi reescrito e nenhum artefato histórico recebeu provenance retroativamente.

## 8. Decisões tomadas

### Arquiteturais

- `tools/` é infraestrutura compartilhada versionada em Git mínimo; não é pacote publicado nem monorepo.
- Provenance de `tools/` é emitida pelo próprio runner; consumidores não duplicam versão, commit ou hash de `tools/`.
- Contratos temporais PRE_EVENT/MATURED permanecem locais/incubados em F1 e CS. Há segundo consumidor funcional, mas não há promoção ao `predictor_core`.
- Lógica de domínio continua local: Elo/Platt, aliases, formatos BO, grids, fontes de resultado, odds, custos e settlement não foram universalizados.
- Vendoring continua o mecanismo atual de distribuição do core; `sync_core --check` declarado não é prova isolada de bytes, por isso byte audit/runtime provenance foram usados como controles complementares.

### Científicas

- Nenhuma previsão retrospectiva EP3 pode ser chamada de PRE_EVENT válido. EP3 é fixture/histórico e ferramenta reprodutível somente leitura.
- H8 de F1 continua sem amostra forward válida suficiente; a referência de nove corridas retrospectivas não satisfaz o requisito temporal. O limiar declarado continua 15 evidências completas.
- H3/Shadow do Brasil permanece com dados insuficientes enquanto picks não maturarem; não calcular GO, ROI, CLV, calibração ou comparação manhã/noite com a amostra aberta.
- CS PRE_EVENT/MATURED sintético prova o contrato de software, não sinal, calibração, edge, execução ou resultado econômico.
- Não houve odds, OPEN/SETTLED, shadow econômico, recomendação financeira ou mudança de hipótese/modelo nesta sessão.

### Operacionais

- Runner preserva lock, timeout, códigos de saída e redação; provenance strict falha fechada antes do filho quando a identidade de tools é inválida.
- Brasil/LoL/F1 têm integração de provenance em novos artefatos; sua validação operacional forward depende de ciclos naturais/artefatos reais.
- Cripto continua bloqueado: normalizar Git não equivale a autorizar execução ou resolver credencial/logs.

## 9. Fases por status

| Fase | Status | Evidência | Commit | Pendência |
|---|---|---|---|---|
| Auditoria 00–13 e reconciliação Conselho/Red Team | PASS | relatórios 00–13 e 12A | N/A | não repetir como implementação |
| Fase 1 — tools Git 1.0.0 | PASS | `audit/56`; testes workspace/clone | `b24e283` | superada por 1.1.0 |
| Fase 2A — provenance nativa tools 1.1.0 | PASS | `audit/57A`; strict, clone e testes | `6367b40`, `2c3d501` | manter congelada até decisão explícita |
| Fase 2B — rollout provenance | PASS | `audit/57`; testes, byte audit, hashes invariantes | Brasil `13b3889`, LoL `58d1691`, F1 `aae48a1` | ciclos reais ainda observáveis |
| Reconciliação Git | PASS | `audit/58`; HEADs normalizados e F1 fast-forward | F1 `aae48a1`; CS histórico `71e01ab` | vendor WC/NBA e Stocks requerem fases próprias |
| CS PRE_EVENT/MATURED | PARTIAL | `audit/60`; testes, cadeia sintética e PRE_EVENT real verificado | `562a74f`, `9e6e12f` | MATURED real do primeiro confronto CS |
| Segurança/execução cripto | BLOCKED | `audit/42`, `43`, `44` | nenhum nesta sessão | credencial, logs e ciclo controlado humano |
| Shadow econômico CS | PENDENTE | explicitamente fora do escopo | nenhum | só após cadeia forward real e autorização |
| Shadow econômico LoL | PENDENTE | explicitamente fora do escopo | nenhum | depende de fase própria |
| Comparação semântica F1 × CS | PARTIAL / PENDENTE | comparação factual em `audit/60` | nenhum | requer evidência forward CS real antes de qualquer promoção |
| Veredito final pós-implementação | PENDENTE | veredito de auditoria existe em `audit/13`/`55`, mas não o fechamento operacional-forward | nenhum | ciclos reais, bloqueios humanos e evidência temporal |

## 10. Ações humanas obrigatórias

1. **Cripto:** rotação/revogação da credencial exposta, decisão sobre os três logs históricos e confirmação de que nenhum dado sensível permanece onde não deve. Sem isso, não executar H5/V3, watchdog, Scheduler ou ciclo manual controlado.
2. **CS:** identificar um confronto futuro real, confirmar horário UTC, formato e aliases antes de gerar PRE_EVENT. Depois do evento, fornecer resultado local explícito e maturar; não usar EP3 para preencher essa lacuna.
3. **Brasil/LoL:** deixar os ciclos naturais ocorrerem e reconciliar Scheduler × heartbeat × JSONL × artefato × lock × health antes de declarar operação comprovada.
4. **Stocks:** revisar os 31 commits locais à frente de `origin/main` e autorizar explicitamente qualquer push.
5. **WC/NBA:** decidir, com revisão específica, se as alterações de vendor/HANDOFF devem ser mantidas, sincronizadas ou descartadas. Não executar `sync_core --write` por inferência.

## 11. Pendências reais e ordem correta

1. Após o confronto **Stake Ranked Episode 3 — 3DMAX × HEROIC**, gerar **MATURED real de CS** a partir de resultado local explícito e confirmar vínculo/hash/ausência de escrita. Só então reclassificar CS temporal como PASS/segundo consumidor comprovado forward.
2. Para confrontos futuros posteriores, repetir PRE_EVENT antes do início: aliases, formato e UTC confirmados; rodar verify; preservar artefato.
3. Observar e reconciliar ciclos naturais de Brasil, LoL e CS, sem inventar nova fase de modelo.
4. Cumprir a ação humana de segredo/logs do cripto antes de qualquer execução operacional desse projeto.
5. Tratar vendor pendente de WC/NBA e publicação de Stocks em tarefas separadas, com rollback próprio.
6. Somente depois de evidência forward real e revisão semântica: discutir OPEN, captura de odds, SETTLED e shadow econômico. Não implementá-los agora.

## 12. Contradições e afirmações antigas superadas

| Afirmação antiga / aparente contradição | Estado factual atual |
|---|---|
| “tools Git pendente” | superada: `tools/` é Git 1.1.0, limpo e verificável em `2c3d501` |
| “Fase 2 está BLOCKED” | historicamente correta para tools 1.0.0; superada por 2A/2B. O documento 57 preserva a evolução e não deve ser lido como bloqueio atual total |
| “CS bloqueado por Git” | era correto na Fase 2B; EP3 foi preservado, branch foi integrada em main e CS agora está limpo com contrato temporal local |
| “Cripto em detached HEAD” | superada: está em `main` no mesmo commit; o bloqueio humano de segredo/logs permanece |
| “WC em detached HEAD” | superada: está em `main`; vendor/HANDOFF continuam sujos e não reconciliados |
| “F1 branch pendente de merge” | superada: `main` está em `aae48a1` por fast-forward |
| “F1 tem nove corridas válidas para H8” | inválida: são retrospectivas e não provam disponibilidade pré-evento; H8 continua sem 15 evidências forward completas |
| “CS PRE_EVENT/MATURED é segundo consumidor comprovado” | parcialmente verdadeiro: a implementação/sintético e um PRE_EVENT real confirmam o início da cadeia; falta MATURED real para fechar a prova forward |
| “todos os consumidores têm rollout operacional de provenance” | não: Brasil/LoL/F1 foram integrados na Fase 2B; CS recebeu provenance nos novos snapshots, mas não recebeu rollout do wrapper semanal naquela fase; cripto continua bloqueado |
| “arquitetura pronta para produção completa” | não sustentado: ferramentas/implementações estão prontas para observação controlada, mas ciclos naturais, cripto e evidência científica forward continuam pendentes |

## 13. O que este handoff não autoriza

- Não transformar EP3, EWC, H8 retrospectivo, relatórios ou fixtures em evidência forward.
- Não criar odds, OPEN/SETTLED, settlement ou shadow econômico para CS/LoL antes da cadeia CS real e de uma fase autorizada.
- Não alterar `tools/` 1.1.0, `predictor_core`, modelos, parâmetros, ratings, bancos, dados ou Scheduler sem tarefa própria.
- Não executar cripto, tocar segredo, limpar logs, commitar os cinco arquivos locais do cripto ou usar credenciais antes da ação humana obrigatória.
- Não apagar, resetar, checkoutar ou “limpar” mudanças de WC/NBA/Stocks/cripto sem decisão específica e revisão.
- Não promover PRE_EVENT/MATURED ao core; o contrato segue incubado/local.

## 14. Fechamento exigido

### A. Estado factual atual

O ecossistema tem audit trail, `tools/` versionado com provenance strict, Brasil/LoL/F1 integrados ao rollout, F1 e CS com protocolo temporal local, F1/CS main atualizadas e as mudanças Git sensíveis preservadas em vez de descartadas. A evidência científica/operacional forward ainda é incompleta: há PRE_EVENT CS real verificado, mas ainda não MATURED; H8 F1 continua bloqueado por amostra temporal, Brasil/LoL aguardam observação natural e cripto permanece bloqueado por segurança humana.

### B. Próximo passo exato

Após Stake Ranked Episode 3 — **3DMAX × HEROIC**, gerar MATURED real e reconciliar o vínculo/hash/ausência de escrita contra o PRE_EVENT de payload hash `19b3cf369e54eb54b010a0336ca28ab6e37b0247861effc2a81ea174395e646e`. Não tratar a fase como PASS antes disso.

### C. O que não deve ser feito

Não implementar odds, OPEN/SETTLED, shadow econômico, mudança de Elo/Platt, ingestão/refresh para “forçar” evento, promoção ao core, execução do cripto ou reinterpretação de EP3 como forward. Não resolver estados Git pendentes com descarte implícito.

### D. Documentos que precisam ser atualizados quando houver novo fato

- `audit/60_CS_FORWARD_SNAPSHOT_IMPLEMENTATION.md`: após PRE_EVENT/MATURED real de CS; então registrar PASS ou falha factual.
- `audit/57_TOOLS_PROVENANCE_ROLLOUT.md`: se e somente se o wrapper operacional do CS ou cripto receber rollout posterior autorizado.
- `audit/58_GIT_RECONCILIATION.md`: após decisão de vendor WC/NBA, cadeia/push de Stocks ou commit/revisão de cripto.
- `audit/42_CRYPTO_OPERATIONAL_VALIDATION.md`, `43_CRYPTO_SCIENTIFIC_VERDICT.md`, `44_CRYPTO_FINAL_READINESS.md`: somente após ação humana de segredo/logs e ciclo controlado autorizado.
- `audit/AUDIT_STATE.md`, `audit/EVIDENCE_INDEX.md` e `audit/OPEN_QUESTIONS.md`: quando uma fase realmente mudar de estado ou uma lacuna for fechada.
- Este `CODEX_FINAL_HANDOFF.md`: ao fim de cada mudança de estado relevante, sem reescrever o histórico anterior.
