# ECOSYSTEM_HANDOFF.md

> **ESTADO CORRENTE — F1, verificado em 2026-08-11.** A fonte mecânica atual é
> [`ECOSYSTEM_CURRENT_STATE.md`](ECOSYSTEM_CURRENT_STATE.md), com branch, HEAD,
> versões, origem Core/Ops e CI concreta por repositório. O conteúdo datado de
> 2026-07 abaixo foi preservado integralmente como snapshot histórico e não
> deve ser usado sozinho para afirmar o estado corrente.
>
> Para retomar: (1) leia o inventário corrente; (2) confirme os HEADs remotos;
> (3) leia README/HANDOFF no ref do projeto-alvo; (4) separe fatos mecânicos de
> decisões humanas. No escopo corrente há nove repositórios. Stocks e NBA estão
> excluídos; `Claude` não é fonte canônica.
>
> As releases compartilhadas observadas são Core `2.2.1` e Ops `3.0.0. CS usa
> Core `2.2.1`; Brasileirão, Cripto, F1 e LoL usam Core `2.2.0`; todos esses
> domínios usam Ops `3.0.0`. A plataforma preserva Core `2.1.0` e usa Ops `3.0.0`.
> WC permanece histórico e vendorizado. Nenhuma dessas diferenças autoriza
> migração automática.
>
> A F0 do Brasileirão foi incorporada em `main@5a42d6c88298` e a CI pós-merge
> `31462565846` ficou verde. A F1 é exclusivamente documental. F2, mudanças de
> dependência, promoções, ciência e capital exigem nova decisão humana.
>
> **ADENDO P4 — 2026-08-11.** P4-A/F1, P4-A.1, P4-B/LoL e P4-CS foram
> mescladas e consolidadas como `P4_COMPLETED_NO_CORE_CHANGE`. A fonte corrente
> é [`P4_CONSOLIDATION.md`](P4_CONSOLIDATION.md), evidências `P4E001–P4E034`.
> `PredictionPoint`/`replay` já são suficientes no Core; regras de cutoff,
> resultado, identidade, vínculo, métrica e hash continuam locais. A CI CS não
> comprovou pytest em 3.14: o job correspondente rodou pytest em 3.13.13 e só
> o smoke usou 3.14.5. O snapshot histórico abaixo permanece inalterado.

## Snapshot histórico preservado — verificado originalmente em 2026-07-26

Documento mestre de continuidade. Verificado em: **2026-07-26**. Leia este
documento **primeiro** em qualquer sessão nova.

> **Rodada de 2026-07-25/26 — leia antes de agir.** Nove defeitos que
> impediam qualquer coorte de maturar foram corrigidos, e as **42** hipóteses
> do ecossistema receberam veredito formal. Dois documentos novos na raiz são
> agora leitura obrigatória:
>
> - **`VEREDITOS_2026-07-26.md`** — as 42 hipóteses fechadas. 8 comprovadas
>   (todas de qualidade de previsão), **12 refutadas** (todas as que tentaram
>   virar dinheiro), 4 ruído (stocks), 5 inconclusivas por amostra com data
>   prevista. **Hipóteses econômicas aprovadas para capital: zero.**
> - **`BLOQUEIOS_GO_2026-07-25.md`** — auditoria dos bloqueios (B-0 a B-11),
>   classificação dos 695.694 registros por função e as erratas da rodada.
>
> Defeitos corrigidos: proveniência falsa na coorte do brasileirão (B-1),
> settlement sem driver no cs (B-2) e no lol (B-3), guard do lol que falhava
> ABERTO na remoção do registro (B-7), instalador de task esvaziado no cs
> (B-8), "fechamento" 6-9h defasado do apito (B-9), DoH fixo num IP bloqueado
> que derrubava a coleta de cs e lol (B-0), manifesto defasado do `tools` que
> derrubava **toda** tarefa agendada (B-11) e o import quebrado do payload
> semanal do lol (2ª causa do B-10).
>
> Efeito medido: cs saiu de **0 para 18/50** maturadas; brasileirão de 0 para
> **4 picks com proveniência auditável**. Nenhum projeto tem mais lacuna
> interna de código.
>
> **Fechamento de 2026-07-26 (2ª rodada):** ver
> `FECHAMENTO_2026-07-26.md` — status GO/NO-GO por projeto, o que foi fechado
> e o que permanece aberto **por tempo de calendário**, não por trabalho.

## COMO RETOMAR EM UMA NOVA SESSÃO

Ordem obrigatória de leitura:

0. `VEREDITOS_2026-07-26.md` e `BLOQUEIOS_GO_2026-07-25.md` (estado atual real)
1. `ECOSYSTEM_HANDOFF.md` (este documento)
2. `PENDENCIAS_ABERTAS.md`
3. `SECURITY_INCIDENT_SECRET_ROTATION.md`
4. `ECOSYSTEM_FINAL_CLOSURE.md`
5. O `HANDOFF.md` do projeto específico que você vai tocar
6. O `README.md` desse projeto
7. Git (`git log`, `git status`, `git diff`) do projeto
8. Código atual

Uma sessão nova **não deve depender desta conversa**. Tudo que uma sessão
nova precisa saber está nos documentos acima e no código/Git — não em
memória de chat.

## Mapa dos repositórios

**Desde 2026-07-19, por ordem explícita do operador, TODOS os repositórios
estão publicados no GitHub (privados, conta `leonardosovienski`) e
sincronizados** — verificação local×remoto commit a commit feita na
publicação. Linhas antigas pré-existentes no GitHub (junho/2026) foram
preservadas em branches `arquivo/*` antes de a `main` canônica substituí-las
(`wc-predictor-v2`: `arquivo/shadow-junho-2026`; `predictor_core`:
`arquivo/core-junho-2026`).

Reverificação em 2026-07-20 encontrou três avanços locais ainda não
publicados, todos de um commit e sem divergência de histórico: raiz de
governança `907ea00` (remoto `128ed04`), `cs-predictor` `28a7d33` (remoto
`feeac2a`) e `f1-predictor` `030a5b7` (remoto `2bf2dad`). Os outros oito
repositórios estão idênticos ao remoto. Nenhum push foi feito nesta rodada.

Nomes no GitHub **padronizados em 2026-07-19** (`<domínio>-predictor` para
domínios; família `predictor-*` para infraestrutura). Pastas LOCAIS mantêm
os nomes originais — são estruturais (set `PARKED`, descoberta de
consumidores do `sync_core`, tarefas do Scheduler) e NÃO devem ser
renomeadas. O GitHub redireciona as URLs antigas; os remotos locais já
apontam para os nomes novos.

| Pasta local | Papel | Branch | Remoto (github.com/leonardosovienski/) |
|---|---|---|---|
| `predictor-ops/` | Operacional canônico | `main` | `predictor-ops` ✓ |
| `predictor_core/` | Científico canônico | `main` | `core-predictor` ✓ (linha junho em `arquivo/core-junho-2026`) |
| `brasileirao-predictor` | Vivo | `main` | `brasileirao-predictor` ✓ |
| `cs-predictor` | Vivo | `main` | `cs-predictor` ✓ |
| `f1-predictor` | Vivo | `main` | `f1-predictor` ✓ |
| `lol-predictor` | Vivo | `main` | `lol-predictor` ✓ |
| `previsao-cripto` | Vivo | `main` | `cripto-predictor` ✓ |
| `wc-predictor-v2` | **ENCERRADO 2026-07-19** (veredito emitido; PARKED como registro histórico) | `main` | `wc-predictor` ✓ (linha junho em `arquivo/shadow-junho-2026`) |
| `predictor-stocks` | REABERTO (ciência ativa; vendor congelado) | `main` | `stocks-predictor` ✓ |
| `nba-predictor` | PARKED (push = preservação, não reabertura) | `main` | `nba-predictor` ✓ |
| raiz (governança) | Documentação canônica | `master` | `ecosystem-predictor` ✓ |

Nota: existe também `github.com/leonardosovienski/Claude` — snapshot
histórico do workspace inteiro de 2026-06-21 (cópias da época de stocks/
core/cripto/wc como subpastas + docs de governança extintos). É um fóssil
de backup pré-ecossistema, superado pelos 11 repos acima. NÃO é canônico;
não confundir com `ecosystem-predictor`. Mantido como arquivo histórico.

## Arquitetura

Ver `README.md` para o diagrama. Regra de ouro: escrita é sempre
unidirecional — `predictor_core/`/`tools/` → vendor do consumidor, nunca o
contrário. Nenhum domínio importa outro domínio diretamente.

## Camadas canônicas — versões e commits-base

| Camada | Versão | Commit-base | Testes |
|---|---|---|---|
| tools/ | **1.3.4** | `eb676ef` | **142 passed, 1 skipped** |
| predictor_core | **1.3.3-ga-20260723** | `11c4792` | **268 passed** |

A suíte do `tools/` roda com `python -m pytest` puro desde `eb676ef`
(`pythonpath = [".."]` no `pyproject.toml`). Antes exigia
`PYTHONPATH=<workspace>` passado à mão, e sem ele 4 módulos nem coletavam.

`predictor_core` 1.3.3 entregou o contrato `COLLECTION_ONLY`
(`contracts/collection.py`, `data/collection.py`). Nenhuma recomendação de
versão permanece pendente de autorização.

## Consumidores vivos — vendors e testes

Reverificado em **2026-07-26**.

Suítes reexecutadas em **2026-07-26** (2ª rodada), todas verdes:

| Consumidor | Vendor de predictor_core | Byte-idêntico | Testes |
|---|---|---|---|
| brasileirao-predictor | 1.3.3 | Sim (46/46) | **377 passed** |
| cs-predictor | 1.3.3 | Sim (46/46) | **159 passed** |
| f1-predictor | 1.3.3 | Sim (46/46) | **203 passed** |
| lol-predictor | 1.3.3 | Sim (46/46) | **131 passed** |
| previsao-cripto | **1.3.2 — DRIFT** | **Não** (44/46) | **325 passed, 2 skipped** |
| predictor-stocks | 1.3.0 — congelado (PARKED) | Não, por decisão | **144 passed** |

Nota de proveniência, aprendida em 26/07: a suíte do `f1-predictor` exige
`tools/` com worktree **limpo** — `snapshots.py` chama
`collect_tools_provenance(strict=True)` e 8 testes falham com
`SnapshotError: tools working tree is dirty` enquanto houver alteração não
commitada em `tools/`. É o fail-closed funcionando, não regressão do f1.

`previsao-cripto` não recebeu a 1.3.3: faltam `contracts/collection.py` e
`data/collection.py`. É drift limpo (manifest interno coerente,
`dc7676a61c86f908`), não adulteração — mas faz `sync_core.py --check` retornar
exit 1. **Sincronizar só DEPOIS do gate de 28/07**: trocar o core no meio da
trial H5 em curso contaminaria o veredito. Ver `BLOQUEIOS_GO_2026-07-25.md` B-6.

## Projetos PARKED e o caso predictor-stocks

`wc-predictor-v2` e `nba-predictor` — PARKED plenos: vendor congelado em
agregado antigo (`3445e37f43c458cc` o WC, `026f1f7b761440d9` o NBA),
drift esperado e correto contra o canônico atual, nenhuma evolução
funcional permitida. Condição para reabrir cada um: ver `HANDOFF.md` de
cada projeto.

**WC ENCERRADO (2026-07-19):** POSTMORTEM completo com veredito final —
ver `wc-predictor-v2/docs/POSTMORTEM_COPA_2026.md` (documento definitivo).
Copa aferida em 15 jogos; banco congelado
(`matches_copa2026_frozen_20260719.db`; placar da final inserido
manualmente por ordem do operador — desvio documentado, fonte martj42
ainda não publicara). Veredito: mercado vence no agregado (CLV −8,4%
sig.); exceção comprovada OU2,5 (CLV +16,9% sig., n=78) — herdada como
base da H1 do brasileirão; P&L real −5,84u, prejuízo 100% fora do funil
validado. Causa raiz do truncamento do `predictions.jsonl` provada por
forense e ledger perdido recuperado de backup em E:\ (ver §4 do
POSTMORTEM); produção original de junho restaurada da Lixeira e arquivada
versionada em `archive/`. Legado inventariado (§7). Nenhuma pendência
aberta.

`predictor-stocks` — **REABERTO para pesquisa em 2026-07-18** por decisão
explícita do operador, satisfazendo a condição formal de reabertura do
seu próprio HANDOFF ("decisão humana explícita + hipótese formalizada
antes de qualquer código"): H4 (volatility targeting) e H5 (reversão de
curto prazo 21d) foram pré-registradas antes de código e julgadas em
rodada única — ambas **NÃO COMPROVADAS** (H5 com IC inteiramente
negativo, anti-sinal). O trabalho ocorreu numa linha remota
(GitHub `leonardosovienski/predictor-stocks`), mergeada em `main`
(`2dc23be`) e verificada localmente em 2026-07-19: suíte 144 verdes,
integridade do vendor 4/4, provenance de runtime `MATCH`. **O vendor
permanece deliberadamente congelado em 1.3.0-ga-20260711** (agregado
`3445e37f43c458cc`) por regra do próprio HANDOFF do projeto — a pesquisa
usa somente APIs já vendorizadas.

`sync_core.py:56` declara `PARKED = {"wc-predictor-v2",
"predictor-stocks", "nba-predictor"}` — checado antes de qualquer
escrita, mesmo com `--target` explícito. `predictor-stocks` permanece na
lista **intencionalmente**: para ele, a semântica passa a ser "vendor
congelado por decisão do projeto", não "projeto inativo". Histórico: essa
lista ficou vazia por engano entre 2026-07-03 e 2026-07-17, causando um
sync indevido nos 3 (commits `vendor: predictor_core v1.3.1...` locais,
nunca publicados); corrigido em `15b6ada`, os 3 revertidos via
`git revert` (nunca reset).

## Manifests e vendors

`tools/TOOLS_MANIFEST.json`: `--check` via `tools/release_manifest.py`.
`predictor_core/CORE_MANIFEST.json` por vendor: `--check` via
`predictor_core/sync_core.py`. Auditoria byte-a-byte independente:
`tools/vendor_byte_audit.py`. Todos confirmados corretos em 2026-07-18.

## Testes — resumo

Ver tabela em `README.md`. Comandos completos: `RUNBOOK_TESTS.md`.

## Automações

Único projeto com Windows Task Scheduler ativo hoje: `previsao-cripto`
(`GarimpoFase1`, `GarimpoV3Daily`, `cripto-watchdog-coleta` — `Ready`,
`S4U`, últimas execuções com sucesso verificadas 2026-07-18; tarefa legada
`GarimpoInvestimentos-ColetaDiaria` confirmada `Disabled`). Detalhe
completo: `RUNBOOK_CRYPTO_AUTOMATION.md`. `brasileirao-predictor` também
tem `brasileirao-sombra-manha`/`-noite` agendadas via `operational_runner`
— ver seu `HANDOFF.md`.

## Artefatos

Ver `ARTIFACT_INVENTORY.md` para o inventário completo por projeto.
Resumo: `.db`/`ratings.json`/`events.jsonl` são gitignored (não provados
por Git); `trials.json`/`trials.harness_attestation.json`/`teams_*.json`
são os artefatos científicos realmente versionados.

## Segurança

Ver `SECURITY.md` (política) e `SECURITY_INCIDENT_SECRET_ROTATION.md`
(incidente ativo, documento sanitizado, sem nenhum valor de segredo).
Estado: `BLOCKED_PENDING_SECRET_ROTATION`, explicitamente baixa prioridade
por decisão humana (2026-07-18).

## Pendências

Lista canônica completa: `PENDENCIAS_ABERTAS.md`. Bloqueios operacionais e o
que falta para cada gate: `BLOQUEIOS_GO_2026-07-25.md`.

**Aberto após a 2ª rodada de 2026-07-26:**

| | O que é | Quem resolve |
|---|---|---|
| **B-10** | Resta só a **cota pública do Google Drive**. O ID no código está correto e a 2ª causa (import quebrado do payload) foi corrigida em `a7528c0` | ninguém — a cota reseta sozinha (~24h). Depois, conferir se `lol-ratings-semanal` saiu de exit 10 |
| **B-6** | Vendor do `previsao-cripto` em 1.3.2 | sincronizar **depois** do gate de 28/07 |
| **SEC-1** | Chave SerpAPI em 5 logs históricos | rotação no provedor, baixa prioridade |
| gate cripto | H5 com critério já falhando na direção oposta | executar em **28/07** |
| amostra | 5 hipóteses inconclusivas | tempo de calendário |

Bugs de código abertos: **zero** — mas essa mesma linha estava escrita em
2026-07-26 de manhã, e naquele momento havia dois (B-11 e a 2ª causa do
B-10), ambos em código que **nunca havia sido executado do jeito que a
produção o executa**. Ver `FECHAMENTO_2026-07-26.md` §"o que a suíte não
media".

**Monitores instalados** (`tools/`): `predictor-task-health` (exit code e
atraso de todas as tarefas, a cada 6h, escreve/apaga `ALERTA_TAREFAS.txt` na
raiz) e `predictor-gate-monitor`. Este último **sai com exit 1 por desenho**
quando qualquer tarefa está degradada — hoje sai 1 por causa do exit 10 do
`lol-ratings-semanal` (B-10). Exit 1 aqui é o monitor funcionando, não o
monitor quebrado.

## Decisões científicas (não reabrir sem evidência nova)

- `RatingBook` não normaliza identidade — mudaria ciência.
- Lifecycle `PRE_EVENT`/`MATURED` não é contrato comum do core — 3
  implementações com garantias diferentes (CS e F1 têm hash-linkage;
  LoL vincula por `prediction_id`, sem hash do payload PRE_EVENT).
- `PredictionPoint` não prova proveniência de inputs — gap de design, não
  bug.
- `is_mature()` não bloqueia acesso — decisão de design.

## Decisões operacionais (não reabrir sem evidência nova)

- `tools/` sem instalação via pacote — consumo é por `sys.path`.
- Split-brain de import flat/package em `tools/` — travado por tripwire,
  não eliminado (removeria a forma que os testes internos usam).
- Sync do core é sempre por vendoring, nunca pacote publicado.

## Regras de sync

Ver `RUNBOOK_VENDOR_SYNC.md`. Nunca `--write` sem confirmar `PARKED`
primeiro. `--target` é preferível a sync global quando só 1 consumidor
precisa da mudança.

## Regras de publicação

Todos os repos publicados no GitHub (privados) em 2026-07-19 por ordem
explícita do operador — ver mapa acima. Pushes subsequentes, tags e
releases continuam sendo decisão humana explícita — nunca automáticos.
Autenticação: `gh` CLI instalado e autenticado via device flow
(`leonardosovienski`, escopo `repo`).

## Condições de reabertura — índice

Ver a coluna "condição para reabrir" em `PENDENCIAS_ABERTAS.md` para cada
item individual — não duplicada aqui.

## Documentos canônicos

Ver tabela em `README.md`.

## Ações humanas obrigatórias

1. Rotação da credencial da SerpAPI no provedor — quando for prioridade
   (checklist completo em `SECURITY_INCIDENT_SECRET_ROTATION.md`).
2. Nenhuma outra ação humana obrigatória pendente.
