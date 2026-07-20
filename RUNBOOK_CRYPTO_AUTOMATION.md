# RUNBOOK_CRYPTO_AUTOMATION.md

Automação do previsao-cripto via Windows Task Scheduler. Verificado
2026-07-20 (read-only, `Get-ScheduledTask`/`Get-ScheduledTaskInfo`).

## Tarefas ativas

| Tarefa | Estado | LogonType | Script | Runner |
|---|---|---|---|---|
| `GarimpoFase1` | Ready | S4U | `run_garimpo_fase1.bat`: coleta Fase 1 + backtest como segundo passo | `tools/operational_runner.py` (`GarimpoFase1` e `GarimpoBacktest`) |
| `GarimpoV3Daily` | Ready | S4U | `scripts/run_daily_v3.ps1` | `tools/operational_runner.py` (`GarimpoV3Daily`) |
| `cripto-watchdog-coleta` | Ready | S4U | script de watchdog | — |

Última verificação (2026-07-20): as 3 com `LastTaskResult=0` (sucesso).
Horários: `GarimpoV3Daily` 21:30; `GarimpoFase1` 22:00, com backtest logo
depois no mesmo `.bat`; `cripto-watchdog-coleta` 19:00 e 22:30.

## Tarefa legada (confirmada desabilitada)

`GarimpoInvestimentos-ColetaDiaria` — `State=Disabled`, confirmado
2026-07-20. Não deve ser reabilitada sem decisão explícita (risco de
coleta duplicada / dupla cota de API consumida).

## S4U

Já configurado desde antes desta linha do tempo (confirmado em
`audit/39_CRYPTO_AUTOMATION_RECONCILIATION.md`, 2026-07-15, e reconfirmado
2026-07-18 via `Get-ScheduledTask ... | Select Principal.LogonType`).
**Não é uma pendência** — qualquer documento antigo que liste "configurar
S4U" como pendência aberta está desatualizado (marcar `STALE`).

## O runner

`run_garimpo_fase1.bat` invoca `tools/operational_runner.py run --task
... -- <script>` — o job inteiro (lock, heartbeat, timeout, redação de
stdout/stderr) é envelopado pelo runner canônico, não pelo script
diretamente. `scripts/garimpo_fase1.py` **não tem mais lock próprio** (
removido em `50379b1`, 2026-07-17 — o runner externo já garante
single-instance).

## Locks

Lock derivado do heartbeat: `<heartbeat>.lock`, contém `{pid, run_id,
created_at_utc}`. Reclamado automaticamente na próxima tentativa de
aquisição se o PID dono estiver comprovadamente morto (fast path) ou se a
idade exceder `stale_after` (fallback, default 86400s). **Não há
verificação proativa em background** — um lock órfão só é limpo quando
alguém tenta adquirir o MESMO lock de novo (o próximo ciclo agendado).

## Logs

`logs/garimpo_fase1_<YYYYMMDD>.log` — um por dia (UTC), rotativo por
execução. **5 destes têm um incidente de segurança conhecido** (ver
`RUNBOOK_SECRET_INCIDENT.md`) — nunca abrir `_20260713.log` a `_17.log`
em texto bruto sem necessidade.

## Health

```bash
cd <workspace-raiz>
python -m tools.ecosystem_health --json   # ou sem --json para saída humana
```
Lê `HEALTH_TASKS.json` (declarativo, na raiz) — read-only, nunca dispara
nem altera tarefas.

## Verificação read-only (PowerShell)

```powershell
Get-ScheduledTask | Where-Object { $_.TaskName -match "Garimpo|watchdog|ColetaDiaria" } | Select-Object TaskName, State
Get-ScheduledTaskInfo -TaskName "GarimpoFase1" | Select-Object LastRunTime, LastTaskResult, NextRunTime
```

## Recuperação de um ciclo que falhou

Se `Get-ScheduledTaskInfo` mostrar `LastTaskResult != 0` e o heartbeat
correspondente estiver travado em `"status": "STARTED"` sem
`finished_at_utc`: **não é necessariamente um bug** — pode ser a máquina
tendo desligado/hibernado durante a execução (código Windows
`3221225786` = `0xC000013A`, terminação forçada, típico de
shutdown/logoff). O lock órfão se autocura no próximo ciclo agendado —
não requer intervenção manual. Só investigar mais a fundo se o padrão se
repetir em ciclos consecutivos.

## Ações que exigem elevação/acesso externo

Rotacionar a credencial exposta no incidente de segurança — só no painel
do provedor, nunca localmente (ver `RUNBOOK_SECRET_INCIDENT.md`).
Reabilitar `ColetaDiaria` — decisão humana explícita. Alterar horário ou
usuário de qualquer tarefa agendada — decisão humana explícita, fora do
escopo de qualquer rodada de engenharia automática.
