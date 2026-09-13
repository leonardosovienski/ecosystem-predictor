# Stocks — integração concluída na instalação principal

Estado verificado em 12/09/2026 no horário local (13/09 UTC). Substitui a etapa anterior deste documento, que tratava PR85 e Bundle como candidatos e não validava a instalação principal. Os recibos anteriores permanecem no histórico Git e na entrega local.

## Combinação validada

| Componente | Revisão ou distribuição |
|---|---|
| Stocks main | `3066321e599ee15dd0ace4167d2791545ce6eb95`, pacote 0.2.0 |
| CAIN main instalado | `d604a0ed359528acfcf4272d8f2a8ecc11774e65`, pacote 0.4.7 |
| Ecosystem main do aceite | `dda782761c430af654b59208d3e41faf6ee7fe28` |
| Contratos instalados | `predictor-research-snapshot==1.0.1`, `predictor-research-bundle==1.0.0` |

Os contratos já estão na main do Ecosystem. Seus bytes são os mesmos da revisão canônica `6a998520825292895bcae71e589fa8ac0e02bb85`, origem dos wheels usados. Commits posteriores apenas documentais não reemitem a validação científica nem mudam o pacote instalado.

- Wheel CAIN SHA256: `0eb67a0f8229d10144c87c4b3c7d625a04fde4ba404a31c33a8eb8e6b68dd5e7`.
- Wheel Snapshot SHA256: `5e62cdf6ea7790a9e4beb0b3dd874a9a40c54cbd97e69e5a8408e88f8f22ec1a`.
- Wheel Bundle SHA256: `7c5792e6573d55af92fd9b50cd9a2c357052b7673a61eef8abdaeaeef401ebee`.
- Snapshot novo SHA256: `c15e6554f01a2fe0f5874af181fd7bea8935a2b3ad26633124ffbe0b7a590cfc`.
- Bundle novo SHA256: `480d3feae7623c923c6c91cfbac5d77c21b2f75eeac66e45ad91e93a8eca8681`.

## Percurso demonstrado

Stocks main → exportação nova → contratos canônicos instalados → CAIN principal → importação → consulta rastreável CLI/API/web → reimportação `duplicate` → backup/restauração offline.

A instalação não editável está em `C:/CAIN/.venv`; módulos instalados e carregados pelo serviço foram conferidos contra o wheel final. `pip check` passou. Usuário `leo`, projeto Geral, acervos `stocks-main-snapshot` e `stocks-main-bundle`, interface `http://127.0.0.1:8877` pelo launcher `C:/CAIN/ABRIR_CAIN.cmd`.

Snapshot contém um relato literal de `STOCKS_CURRENT_STATE.md`. Bundle contém duas entidades e três relações derivadas de `real-v020.json`, SHA256 `7699aa83c78f44bf0fef63d960e10334f125b01dcb264e88ef0efae2855a067d`. São metadados e referências; zero preços/objetos externos recebidos, licença UNKNOWN e geração negada. A aprovação foi recebida antes da admissão. PASS/UNKNOWN, clocks ausentes e cobertura parcial foram preservados.

CLI, API e web devolveram conteúdo coerente. Após restore, raízes dos produtores apontaram para caminho inexistente: records Snapshot e entidades/relações/evidências/artefatos/contagens Bundle permaneceram iguais; verify/rebuild passou. Todas as linhas anteriores do baseline research foram preservadas. Não se afirma identidade binária de bancos ou recuperação de objetos nunca materializados. Os casos negativos de autorização, adulteração, ausência e API foram exercitados em estado de teste com os mesmos pacotes instalados.

## CI e publicação

- [Stocks CI247](https://github.com/leonardosovienski/stocks-predictor/actions/runs/34725687619): 966 testes por Python 3.13/3.14, zero falhas/erros/skips, R8 e controles aprovados; wheel fora do checkout, ingestão sintética 250 mil, deduplicação e restore.
- [Exportadores Stocks](https://github.com/leonardosovienski/stocks-predictor/actions/runs/34725687720): Snapshot, Bundle e seleção em Python 3.12/3.13/3.14.
- [CAIN main](https://github.com/leonardosovienski/cain/actions/runs/34727241470): 605 testes por Python 3.11–3.14, zero falhas/erros, dois skips de plataforma; instalação Windows exercitada separadamente.
- Ecosystem do aceite: [CI](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34727305448) e [segurança](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34727305461) aprovadas. `check_ecosystem_drift.py` online retornou `ECOSYSTEM_NO_DRIFT (OFFLINE+ONLINE)` na conferência; não é garantia permanente de ausência de drift.
- [Stocks PR85](https://github.com/leonardosovienski/stocks-predictor/pull/85), [CAIN PR1](https://github.com/leonardosovienski/cain/pull/1) e [Ecosystem PR24](https://github.com/leonardosovienski/ecosystem-predictor/pull/24) integrados.

Stocks ficou somente em main no checkout canônico e origin; 13 branches locais e 13 remotas removidas com SHA esperado após preservação e CI. Nenhuma branch CAIN/Ecosystem foi excluída. Instalação local não equivale a nova tag/release.

## Pastas e continuidade

- Ecosystem canônico: `C:/CAIN/contrato`, branch `main`, remoto `leonardosovienski/ecosystem-predictor`.
- Relatório completo: `C:/STOCKS/outputs/AUDITORIA_INTEGRACAO_MAIN_20260912/RELATORIO.md`; manifesto e ZIP ao lado.
- Identidades e recibos finais Stocks: `C:/STOCKS/work/audit-main-20260912/primary-installed`.
- Backup privado, rollback de código, política e restore CAIN: `C:/CAIN/entregas/stocks-main-integration-20260912`. Não publicar esses bancos/políticas.
- Backups Git Stocks: `C:/STOCKS/work/audit-main-20260912/stocks-before.bundle` e `stocks-pre-consolidation.bundle`, com recuperação ensaiada em destino separado.

Não restaurar um banco antigo sobre consultas novas. Usar o mecanismo archive em destino novo e os recibos de instalação para decidir rollback de código. Não usar um worktree histórico como origem de cópia sobre main.

Os campos científicos históricos H1–H19 do registry não definem o estado científico atual; a autoridade permanece nos protocolos do Stocks. Esta integração não executou nova pesquisa, treino, trade, validação de rentabilidade ou aprovação semântica geral de modelos. O aceite é `VALIDADO_NO_ESCOPO` nos percursos descritos.
