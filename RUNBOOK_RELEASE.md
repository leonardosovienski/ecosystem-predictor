# RUNBOOK_RELEASE.md

Verificado 2026-07-18. Cobre só `tools/` — `predictor_core` não tem release
check próprio, usa `sync_core.py --check` (ver `RUNBOOK_VENDOR_SYNC.md`)
como equivalente de integridade.

## Release check de tools/

```bash
cd <workspace-raiz>
python tools/release_check.py
```
Faz, em sequência: (1) pytest no workspace, (2) `git clone` para um
diretório temporário, (3) pytest no clone isolado, (4) sonda de provenance
estrita (`collect_tools_provenance(strict=True)`) no clone. Falha em
qualquer etapa aborta as seguintes e imprime a etapa que falhou. Sucesso
imprime um JSON de uma linha: `{"workspace_tests": "passed",
"isolated_clone_tests": "passed", "clone_provenance": {...}}`.

## Provenance

`collect_tools_provenance(strict=True)` rejeita checkout sujo ou manifest
divergente do conteúdo real (não confia no manifest declarado — re-hasheia
os bytes). Ver `tools/PROVENANCE.md` para o algoritmo completo.

## Manifests

```bash
cd tools && python release_manifest.py --check   # read-only
cd tools && python release_manifest.py --write    # regenera, só após git add dos arquivos novos/alterados
```
`--write` se recusa (exit 2) se houver mudança não-staged em arquivo de
payload — evita gerar um manifest que não reflete o que será commitado.

## Versão

`tools/VERSION` e `tools/pyproject.toml` = `1.3.1` hoje. Todo bump deve
atualizar ambos; a suíte contém um tripwire que exige igualdade entre as
duas declarações. **Não execute novo bump sem autorização explícita** —
não é uma etapa automática deste runbook.

## Limitações

Nenhum CI remoto configurado — todo o release check é local. Nenhuma
matriz multiplataforma (só Windows validado). `tools/` tem remoto privado
configurado, mas publicação continua exigindo decisão humana explícita.

## Ausência de push/tag automático

Este runbook nunca inclui `git push`, `git tag`, nem qualquer comando de
publicação. Isso é deliberado — publicação é sempre decisão humana
separada.

## Critérios de publicação (quando for decidido)

1. `release_check.py` passou (workspace + clone isolado).
2. `sync_core.py --check` e `vendor_byte_audit.py` confirmam os 5 vivos
   `OK`/`IDENTICAL`.
3. `PENDENCIAS_ABERTAS.md` revisado — nenhum item `OPEN_BUG` ou
   `OPEN_SECURITY_INCIDENT` sem decisão humana explícita.
4. Versão bumpada e commitada antes da tag (se decidido taguear).
5. Remoto configurado e confirmado correto antes de qualquer push.
