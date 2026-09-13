> **Atualização posterior do Ops:** as versões e instalações abaixo registram a combinação daquela data. Ops 4.2.1 foi posteriormente publicado e instalado nos ambientes locais; consulte [a integração de 13/09/2026](OPS_INTEGRATION_20260913.md).

# Brasileirão — entrega técnica e integração documental

Estado registrado em 12/09/2026 (America/Sao_Paulo). Atualização de documentação e representação do domínio; não altera a classificação científica nem autoriza capital.

## Código e combinação comprovada

- Brasileirão: `abdd965c98c228d73ae416944eb7531bed9ab197`, pacote 0.2.0; Core 3.2.1 e Ops 4.2.0. Main local/remota consolidada; branches antigas integradas e excluídas com proteção por SHA.
- CAIN validado: `5ba4177a11b9312900e5035517aa5ef25d509859`, instalado isoladamente. Atualizações concorrentes posteriores do CAIN não recebem automaticamente este aceite.
- Ecossistema no aceite original: `a9f6594c840482419d6c310f373813e0e71f17d0`. Essa revisão de BundleV1 já é ancestral de main `73111a1d13adfa09dd4928cae3b75ae28e4ea7e6`; a dependência de uma branch não integrada deixou de existir. O pin do teste original continua preservado como proveniência.
- Contratos usados pelo consumidor: ResearchSnapshotV1 1.0.0 e ResearchBundleV1 1.0.0; perfis `local-evidence/1` e `local-research/2`.
- A versão publicada da release e o candidato da main são identidades distintas. `released_architecture.json` conserva hashes da release; `compatibility_candidate.json` aponta para o candidato Brasileirão auditado.

## Percurso real e evidências

As três claims `CLAIM-BR-MARKET-001/002/003` saíram do documento real versionado `docs/EVIDENCE_REGISTRY.md`. Exportação → validação canônica → transporte para inbox → aprovação explícita → ingestão em SQLite/objetos novos → recuperação CLI/API → contexto factual do Historian → materialização offline foram executados. Preservados estado `BLOCKED_PENDING_PIT_FEATURES`, horizontes H-24h/H-6h/H-1h, nove colunas, revisão, hashes e relógios científicos nulos.

- Fonte SHA256: `206898ed8b303455ce1e02e5dcf22c6edf873585fc6a43d438609cfd456c0b66`.
- Bundle: `def9f8a03e06c8e75a258f538a99a2c941b88374ceb7534911414bdae04fd4f0`.
- Snapshot: `32594577d32ecc79e6d64d8ee85a98ceb449078a27ae0829e49673237d610e36`.
- Reimportação idempotente; schema inválido, ausência de metadados, corrupção, conflito, fonte ausente e falta de autorização rejeitados; revogação oculta conteúdo.
- [Recibo do caso](evidence/brasileirao-main-20260912/result.json), [combinação e testes](evidence/brasileirao-main-20260912/validated-combination.json), [critérios definidos antes das correções](evidence/brasileirao-main-20260912/ACCEPTANCE.md).

CI aprovada do SHA `abdd965`: [principal](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/34726769988), [escopada](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/34726770019), [exportação e integração CAIN](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/34726770025). Os 12 jobs passaram. Recibos em [ci-final.json](evidence/brasileirao-main-20260912/ci-final.json).

Validação local: 2.090 testes Python e 30 subtests; 31 skips, dos quais 30 Redis passaram em execução separada e um dependia de symlink Windows. Subconjunto escopado: 415 aprovados. .NET: 160 aprovados, 86,91% linhas/81,90% branches. CAIN: 118 aprovados e um skip POSIX; Bundle: 62 aprovados. Ruff/Pyright/build/wheel instalado aprovados. CI também cobriu Linux, Python 3.13/3.14 e Compose. Treino → previsão → persistência foi executado separadamente com dados explicitamente sintéticos, sem ingestão desses dados como evidência real no CAIN.

## Limites e continuidade

O plugin mantém health `WAITING`, ciência e qualidade preditiva `UNKNOWN`, estado econômico `NOT_VALIDATED` e capital `FORBIDDEN`. Os testes comprovam engenharia e uso documental; não comprovam rentabilidade, operação de produção ou precisão de LLM. O gate RPS 3.2.1 foi renovado executando os controles sintéticos existentes; expira em 19/09/2026 23:50:42 UTC. O recibo anterior foi preservado. Não houve nova hipótese, alteração de trials históricos ou liberação operacional.

Checkout canônico do domínio neste notebook: `C:\BRASILEIRAO\brasileirao-predictor`, branch `main`. Checkout do ecossistema: `C:\CAIN\contrato`, branch `main`. Outros worktrees pertencem a trabalhos próprios e não devem receber cópia cega ou limpeza. Backups Brasileirão restaurados: `C:\BRASILEIRAO\BACKUPS\integration-main-20260912`; relatório A–F e pacote local: `C:\BRASILEIRAO\ENTREGAS\integration-main-20260912`. Esses backups cobrem Git/índice/59 arquivos locais; não substituem a preservação dos acervos externos históricos.

## Reprodução

No checkout limpo do Brasileirão, use a versão registrada e os [comandos versionados](https://github.com/leonardosovienski/brasileirao-predictor/blob/abdd965c98c228d73ae416944eb7531bed9ab197/docs/INTEGRATION_MAIN_20260912.md). Instale CAIN `5ba4177` com os contratos do seu diretório `vendor` em venv separada. Execute com essa Python:

```text
python tools/integration_validation/run.py PRODUCER_CHECKOUT NEW_SIBLING_OUTPUT
```

O caminho do script pertence ao checkout Brasileirão. O destino deve ser novo, externo ao checkout e sob o mesmo pai; o runner produz política, banco, objetos e recibos isolados sem credenciais de produção. Para os registros do ecossistema: `python scripts/check_ecosystem_drift.py --offline-check`. Isso verifica coerência interna; não equivale a revalidar todas as versões atuais dos outros projetos.
