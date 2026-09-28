# Etapa B — stack integrado e qualificado (2026-09-28)

Este documento registra o stack que as três integrações da Etapa B qualificaram juntas. É só registro: nenhuma wheel muda aqui. As identidades vêm das attestations no `main` do predictor-qualification (`3e33a0b` ou posterior).

## Attestations

| Missão | Resultado | sha256 da attestation | Achados abertos |
|---|---|---|---|
| integration-crypto | QUALIFIED, 30/30 | `a071fe2ca22e4f301f8ba426ff772a20c506942561276739ad519f61c36831f6` | P0=0, P1=0, P2=4 |
| integration-stocks | QUALIFIED, 30/30 | `9979d19be7fc22f4731878d77496b91489b60fdf0bf350ff3336e81986791eae` | P0=0, P1=0, P2=0 |
| integration-brasileirao | QUALIFIED, 30/30 | `8aef11046708d53504da06c3796af1d5f14b024524c64290e7792527b517e29e` | P0=0, P1=0, P2=1 |

## Wheels (as mesmas nas três attestations)

| Pacote | Versão | Fonte | sha256 da wheel |
|---|---|---|---|
| cain-research | 0.4.13rc12 | cain `302a5c8` | `988a0fb9b5e9b00be95cbf48dbe8fdda2eec53dff86e384192a619888ef49394` |
| predictor-research-transport | 0.1.0rc5 | ecosystem-predictor `b11494a` | `408d73c2b991eb009806702121ed187f273aa6521979ed89bbe9491e58cff79f` |
| predictor-research-protocol | 2.0.0rc2 | ecosystem-predictor `49ffb16` | `34a1e4121e4085b901e3bd96552e2f5b4067c5e6af5e99dc1c26d6276fc7c820` |
| predictor-core | 3.2.1 | core-predictor tag `7bb212c` | `10ef42f34ace8bb2df5f83ff7de2ceec79b035a25ea0a690e8942bd60d2fb4e3` |
| predictor-ops | 4.2.2rc1 | predictor-ops tag `9831b0d` | `0be70bfbb2437dfb080baceb9af41043a09d03b15a358903b8bd7007f5f169b3` |
| cripto-predictor | 1.2.0rc3 | `ee3d3d1` | `02b5e5dbbc60cfb5ed6bb6458331047d7d6de9d55914fb9b1644d78fd0d2b82d` |
| stocks-predictor | 0.3.0rc3 | `6f857b2` | `902f0d34efe7aef02c084e7886ef997c9b3f9bfe28e0e923c9c178361131ea00` |
| brasileirao-predictor | 0.3.0rc4 | `1fc2e88` | `1874e22f7a735d31109979d0cbdd35fd4afa0d893f48caa073e37e5b7ef46e19` |

**Core:** as attestations do cripto e do stocks registram como final_commit o `main` do Core (`5a08415`); a do Brasileirão registra a tag (`7bb212c`). A wheel é a mesma, construída de `7bb212c`. Desde a tag, o `main` só acrescentou `tools/` e documentação, sem código do pacote.

**Ops:** a 4.2.2rc1 saiu do commit da branch do PR #26, antes do merge. O `main` (`40c703a`) tem o mesmo código.

## Como a integração foi provada

Cada missão sobe, só a partir das wheels publicadas, o domínio, o Core e o Ops (cadeia admissão → Ops → Core), o protocolo V2, o transporte e o CAIN. Em cada uma rodam:
- cleanroom;
- contrato (C24.3);
- E2E com dados reais;
- N+1 determinístico;
- isolamento e IDs com domínio contra os outros dois domínios;
- matriz de falhas F01–F15;
- soak;
- Windows.

O workflow histórico `cross-repo-compatibility.yml` (D-13/D-15) continua só por `workflow_dispatch`, e `registries/compatibility_candidate.json` fica como está: é a entrada desse workflow e aponta para as revisões antigas de propósito.

## Teste conjunto dos três domínios

Os três domínios reais ficaram instalados ao mesmo tempo, cada um no seu venv de consumidor com o Core e o Ops, e o CAIN rc12 orquestrou os três num mesmo estado. O teste rodou no PC 2 (WSL), por conta da D-25, com o cenário `ecosystem_joint.py` da integration-brasileirao; a lista de conferências foi feita pelas três sessões.

**Resultado da tentativa 3, a publicada: 57/58.** O `no_data_rows_check` saiu limpo, e o sha256 do dado ficou igual antes e depois.

| Item | O que confere | Resultado |
|---|---|---|
| 1 | identidade do stack: wheels com o sha publicado, pacotes lidos do dist-info, venv do CAIN sem domínio, cada consumidor só com o seu | 9/9 |
| 2 | um ciclo ALLOW real por domínio, payload = releitura autoritativa do domínio | 9/9 |
| 3 | entrega cruzada nos dois sentidos, estado do domínio inalterado | 6/6 |
| 4 | o mesmo H9 nos três domínios: IDs distintos e qualificados; proposta de X em Y → R01; H9 fechada → R05 | 2/2 |
| 5 | memória por cubo, view isolado, memória íntegra | 2/2 |
| 6 | `metrics` só no cripto, iguais ao payload | 1/1 |
| 7 | mesmo `policy.code_sha256` nos três; config de cada domínio = digest empacotado, distinta | 1/1 |
| 8 | três consumidores em paralelo, sem perda nem duplicata | 7/7 |
| 9 | R16 do brasileirao (3 vetores → REQUIRE_HUMAN, sem task) e R15 do cripto | 4/4 |
| 10 | modo LLM (phi4-mini local): cripto ALLOW, stocks ALLOW, brasileirao NO_ELIGIBLE_HYPOTHESIS (waiver IB-F009) | 1/1 |
| 11 | nenhum `capital_permission` true | 1/1 |
| 12 | Core/Ops: `core_facts` e `ops_facts` em todo RESULT; um experimento por pedido admitido; RECORD instalado = wheel publicada, nos três | 12/12 |
| 13 | disputa da trava do Ops, 20 repetições por domínio | brasileirao 20/20, cripto 20/20, **stocks falhou** |

O item 13 falhou no stocks: 2 de 20 repetições com `RECONCILIATION_REQUIRED` falso. Nas 18 outras, e nos outros dois domínios, o perdedor publicou `OPS_FAILED_RETRYABLE`. Não houve queda de processo, e em todas as repetições dos três domínios houve 1 experimento e 1 RESULT. É o mesmo achado IS-F009 descrito abaixo.

A evidência fica em `qualification/integration-brasileirao/RAW_LOGS/runtime/run-20260928T153733Z-eco/ecosystem-joint/` (predictor-qualification#83, commit `2688394`; relatório `ECOSYSTEM_JOINT_REPORT.md`), com os sha256 conferidos no commit:

| Arquivo | sha256 |
|---|---|
| `SUMMARY.json` | `39adaafe13cfe6c5e163d5371a2529ba71149e5b7a0c48d57eeef4deae627002` |
| `commands.log` | `d30c0a86c3534ddcc3b82068a3b36ef978990f328b0cedf46eb5e10e205a04ec` |
| `lock-contention/commands.log` | `fba4944d4b43777528697af196a285b9ecb817d798a069b019e843e926ede32b` |
| `no_data_rows_check.json` | `f0a2ad5d1e3c8362a58b698392643e058723f5af45c93c5c601b5415376fb339` |

As tentativas anteriores ficaram privadas e não foram publicadas; estão registradas no PR:
- **Tentativa 1:** 47/57, com 10 falhas do próprio script de teste e um falso positivo conhecido (IB-F003) do `no_data_rows_check`.
- **Tentativa 2:** 56/58, com um limiar estrito demais no script e a mesma falha do stocks no item 13.

## Limitação do ecossistema: um consumidor por domínio por vez

A disputa da trava do Ops foi testada assim: dois `predictor-research-consumer` do mesmo domínio iniciados ao mesmo tempo sobre a mesma task, o mesmo spool, o mesmo ledger e o mesmo estado.

**A trava do próprio Ops (correção SHARED-005) nunca derrubou processo.** Os domínios, porém, materializam as referências antes do `run_job` do Ops, fora da trava:
- **cripto:** em 1 de 20 repetições no Windows, o perdedor morre com `PermissionError` (IC-F016). Em 39 de 40 repetições (Windows e Linux), o perdedor publica `OPS_FAILED_RETRYABLE` falso (IC-F017).
- **stocks:** em 4 de 20 repetições no WSL, o perdedor publica `RECONCILIATION_REQUIRED` falso, e o CAIN retém o domínio pela R09 até uma decisão humana. Essa parada é falsa. Nas outras 16, publica `OPS_FAILED_RETRYABLE` falso, com o motivo `OPS_SKIPPED lock_not_acquired`. Registrado como IS-F009 (P2), com a mesma regra por decisão do dono do stocks: predictor-qualification#82, `qualification/integration-stocks/RAW_LOGS/pos-attestation-c2/race/RACE.json`.

Em todos os casos houve um único experimento e um único resultado terminal certo.

Regra operacional, por decisão do dono no cripto e no stocks: **um consumidor por domínio por vez.** O agendador do Ops já garante isso.

A correção de fundo é tomar a trava antes da materialização. É código de domínio fora dos `adapter_paths`, então pela C24.4 reabre a Etapa A de cada domínio e fica para decisão de cada dono.

## Registros atualizados neste PR

- `registries/project_registry.json`, `predictor-ops`:
  - `current_version` 4.2.1 → 4.2.2rc1;
  - `remote_main_sha` → `40c703a`;
  - fonte e verificação em 2026-09-28.
- `registries/project_registry.json`, `core-predictor`: `remote_main_sha` → `5a08415`, fonte e verificação em 2026-09-28.
- `registries/released_architecture.json`, `predictor-ops`: release `v4.2.2rc1`, fonte `9831b0d`, CI `35905678198` e wheel `0be70bfb…`.

A checagem `scripts/check_ecosystem_drift.py`, antes e depois:
- **antes:** `ECOSYSTEM_DRIFT_DETECTED` ("predictor-ops: registry diz 4.2.1, main diz 4.2.2rc1");
- **depois:** `ECOSYSTEM_NO_DRIFT (OFFLINE+ONLINE)`. Só restam os avisos de SHA de `main` dos domínios, que andam a cada merge.

## Atualização de 2026-09-28 (tarde): cain 0.4.13rc13 e transporte 0.1.0rc6

Depois do registro acima, a sessão STOCKS publicou a cain `v0.4.13rc13` (`960fb25`, wheel `a1d94fd5…`) e o
transporte `predictor-research-transport-v0.1.0rc6` (`bac1f7b`, wheel `6c7e83c4…`, a trava exclusiva por
domínio que corrige IC-F016, IC-F017 e IS-F009). As integrações do cripto e do stocks refizeram as fases
pela C14 e reemitiram as attestations; a do Brasileirão ainda é a da rc12/rc5 (o dado real é privado e
as fases rodam só no PC 2, D-19). Estado no `main` do predictor-qualification em `d188810`:

| Missão | cain | transporte | Resultado | sha256 da attestation |
|---|---|---|---|---|
| integration-crypto | 0.4.13rc13 `960fb25` | 0.1.0rc6 `bac1f7b` | QUALIFIED, 30/30 | `69fa0393a24ca727da7dc0131aa5b25935810d64e72095febddd65541aff88e7` |
| integration-stocks | 0.4.13rc13 `960fb25` | 0.1.0rc6 `bac1f7b` | QUALIFIED, 30/30 | `60b75594a229b0bffb9078302e791fc1cf7b7a6f332a2b7f8c36e18fb521846c` |
| integration-brasileirao | 0.4.13rc12 `302a5c8` | 0.1.0rc5 `b11494a` | QUALIFIED, 30/30 (C14 da rc13/rc6 pendente no PC 2) | `8aef11046708d53504da06c3796af1d5f14b024524c64290e7792527b517e29e` |

Core (3.2.1, `10ef42f3…`), Ops (4.2.2rc1, `0be70bfb…`), protocolo (2.0.0rc2) e os três domínios não mudaram.
O `brasileirao.json` empacotado na rc13 é byte a byte o da rc12 (só `stocks.json`, `llm.py`, `claims/` e
`findings/` mudaram entre as duas). A auditoria adversarial da cain rc13 e deste transporte está em
`qualification/shared/CAIN_EXTREME_20260928/` do predictor-qualification; as correções que ela motivou
(cain: envelope ilegível e `as_of` impossível; transporte 0.1.0rc7: arquivo de task ilegível) entram por PR e,
se o dono as adotar numa release, disparam a C14 nas três integrações.
