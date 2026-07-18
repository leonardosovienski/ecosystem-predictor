# RUNBOOK_ARTIFACT_INTEGRITY.md

Como verificar preservação de artefatos antes/depois de qualquer sessão de
engenharia. Verificado 2026-07-18.

## Artefatos versionados (prova = Git)

```bash
git -C <projeto> status --short <caminho>
git -C <projeto> diff <caminho>
```
Limpo/sem diff = preservado. Lista por projeto: `ARTIFACT_INVENTORY.md`.

## Artefatos ignorados (prova = hash externo, NÃO Git)

Antes de tocar qualquer código que leia/escreva um artefato
`*_UNVERSIONED`/`DATABASE` ignorado:

```bash
sha256sum <caminho-do-artefato>   # registrar o valor
```

Depois da sessão, recalcular e comparar. Diferença = investigar se é
mudança de produção concorrente legítima (job real rodando em paralelo) ou
efeito colateral indevido da sessão.

## Distinguir mudança concorrente de efeito colateral

- Verificar se o arquivo é gitignored (`git check-ignore -v`) e se algo
  como um Task Scheduler job real rodou na janela de tempo em questão
  (`Get-ScheduledTaskInfo` para `LastRunTime`).
- Se o timestamp do arquivo bate com uma execução agendada real (não com
  nenhum comando que a sessão de engenharia executou), é
  `CONCURRENT_PRODUCTION_ACTIVITY` — não commitar, só documentar.
- Se nenhum comando da sessão nem nenhum job agendado explica a mudança,
  investigar antes de prosseguir.

## Snapshots com vínculo próprio (CS, F1)

`cs-predictor/src/cs_snapshots.py` e `f1-predictor/src/snapshots.py` têm
verificação de integridade PRÓPRIA (hash SHA-256 entre PRE_EVENT e
MATURED, mais forte no F1 com escrita exclusiva de SO). Não duplicar essa
verificação manualmente — rodar os testes desses módulos já valida.

## Limites do Git

Git não prova nada sobre um arquivo gitignored além de "não está no
índice". Não alegue "preservação científica confirmada" citando `git
status` para um artefato que está na lista de ignorados —
`ARTIFACT_INVENTORY.md` documenta explicitamente qual categoria cada
artefato pertence.

## Backups

Não implementado nesta linha do tempo para nenhum banco SQLite/FeatureStore
(`PENDENCIAS_ABERTAS.md`, OP-4). Se for implementar: escopo mínimo por
projeto, sem wrapper comum forçado entre domínios (decisão de
`audit/13_FINAL_VERDICT.md`, item B-03 do roadmap, nunca executado).

## Checklist antes de declarar "nenhuma alteração científica"

1. `git status`/`git diff` limpo nos artefatos versionados de cada projeto
   tocado.
2. Hash externo comparado antes/depois para cada artefato ignorado
   relevante.
3. Qualquer diferença classificada explicitamente (mudança da sessão vs.
   produção concorrente vs. inesperada).
4. Nenhuma diferença "inesperada" sem investigação e explicação registrada.
