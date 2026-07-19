# RUNBOOK_VENDOR_SYNC.md

Sincronização do `predictor_core` para os vendors. Verificado 2026-07-18.

## Precondições (checar antes de QUALQUER `--write`)

1. `git status` limpo em `predictor_core/` — nunca sincronizar com
   mudanças não commitadas na fonte.
2. Confirmar `PARKED` atual: `python -c "import sync_core; print(sync_core.PARKED)"`
   de dentro de `predictor_core/` — hoje deve imprimir exatamente
   `{'wc-predictor-v2', 'predictor-stocks', 'nba-predictor'}`. Se vier
   vazio ou diferente, **pare** — é uma regressão do incidente já corrigido
   em `15b6ada`.
3. Rodar `--check` (read-only) antes de qualquer `--write`, para ver o
   estado atual sem modificar nada.

## `--check` (sempre seguro, nunca escreve)

```bash
cd predictor_core
python sync_core.py --check
```
Relata `OK (em sincronia)` / `DRIFT` por consumidor. Os 3 nomes do set
PARKED sempre aparecem `DRIFT ... [PARKED]` — é o estado correto, não um
erro. Nota (2026-07-19): `predictor-stocks` foi reaberto para pesquisa,
mas **permanece no set PARKED intencionalmente** — o HANDOFF dele proíbe
sync de vendor (congelado em 1.3.0 por decisão do projeto). Não remover
do set por causa da reabertura.

## `--target` (escopo por consumidor — preferível a sync global)

```bash
python sync_core.py --write --target brasileirao-predictor
```
Só toca o consumidor nomeado. `_is_parked()` é checado mesmo com
`--target` explícito — tentar `--target wc-predictor-v2` (ou qualquer
PARKED) resulta em `PULADO`, nunca escreve.

## `--write` sem `--target` (todos os não-PARKED)

```bash
python sync_core.py --write
```
Escreve em todos os consumidores com `vendor/predictor_core/` que NÃO
estejam em `PARKED`. Confirmar a lista impressa no final ("N
consumidor(es) sincronizado(s). Congelados não tocados: ...") bate com o
esperado antes de prosseguir.

## Proteção contra sync global indevido

O único mecanismo de exclusão é `PARKED` em `sync_core.py:56`. Não existe
outro caminho de bypass (`_select_consumers` não filtra por nome de forma
que ignore `PARKED`; `cmd_write` chama `_is_parked(d.name)` para cada
consumidor selecionado, incondicionalmente). Se `PARKED` for
acidentalmente esvaziado de novo, qualquer `--write` sem `--target`
tocaria os 3 protegidos — por isso a precondição 2 acima é obrigatória.

## Manifests

`--write` grava `CORE_MANIFEST.json` em cada vendor tocado (hash por
arquivo + agregado + timestamp + versão de origem). Nunca editar esse
arquivo manualmente.

## Byte audit pós-sync

```bash
cd <workspace-raiz>
python tools/vendor_byte_audit.py --workspace . --consumer <nome>
```
Deve retornar `IDENTICAL, N/N, 0 changed`. Qualquer `changed` != 0 após um
`--write` recém-executado é uma regressão real — investigar antes de
prosseguir.

## Testes pós-sync

Rodar a suíte completa do(s) consumidor(es) tocado(s) — ver
`RUNBOOK_TESTS.md`. Nunca considerar um sync "concluído" sem reexecutar os
testes do consumidor.

## Rollback

Sync é sempre uma cópia de arquivo simples — `git checkout -- vendor/` no
consumidor afetado desfaz um sync indesejado (desde que ainda não
commitado). Se já commitado, usar `git revert` no commit de sync (nunca
`git reset --hard` em histórico já potencialmente compartilhado).

## Comandos proibidos

`--write` sem antes rodar `--check`. `--write` com `git status` sujo na
fonte. Editar `CORE_MANIFEST.json`/`TOOLS_MANIFEST.json` manualmente.
Remover ou esvaziar `PARKED` sem decisão humana explícita e registrada.
