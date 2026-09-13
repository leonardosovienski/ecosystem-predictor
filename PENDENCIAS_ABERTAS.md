# Pendências — registro histórico e encaminhamento atual

Os bloqueios técnicos de Bundle fora da main e instalação principal CAIN não
validada foram encerrados no [aceite Stocks](STOCKS_INTEGRATION_20260912.md).
A lista datada abaixo conserva os itens e critérios daquela revisão; não foi
reavaliada como pesquisa científica nesta manutenção documental.

A arquitetura vigente está em [ECOSYSTEM_RUNBOOK.md](ECOSYSTEM_RUNBOOK.md). As tabelas científicas e pendências datadas de 06/09 abaixo são históricas; o estado científico vigente pertence ao respectivo domínio. A entrega de engenharia de 11/09 não reemite esses vereditos.

## Entrega arquitetural publicada — 11/09/2026

Versão **0.2.0** publicada: [release e artefatos](https://github.com/leonardosovienski/ecosystem-predictor/releases/tag/v0.2.0). [CI de engenharia aprovada](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34630167633) para a fonte `2e8be61d3d8b0cf10e1dfbcce8ff7acdef219327`. Consulte [ARCHITECTURE_IMPLEMENTATION.md](ARCHITECTURE_IMPLEMENTATION.md) para comportamento, migração e limites. Este registro atualiza a entrega de software; estados científicos e registros datados abaixo conservam sua autoridade e contexto histórico.

Verificado em 2026-09-06. Itens encerrados e listas históricas foram removidos desta
visão; continuam no histórico Git e no índice de documentos históricos.

| ID | repo | blocker | why_it_matters | owner | required_evidence | state |
|---|---|---|---|---|---|---|
| BR-05 | brasileirao-predictor | EXP-001 prospectivo precisa acumular coorte PIT nativa | O histórico foi declarado `NOT_VIABLE`; a pergunta científica só pode ser respondida honestamente com novas observações | domínio BR | ledger prospectivo com features e mercado timestamped no mesmo cutoff | ACTIVE_COLLECTION |
| CR-01 | cripto-predictor | Harnesses emitidos contra Core 3.0.0 | Release corrente é **3.2.0**; compatibilidade não equivale a certificação atual. Subir NÃO é troca de pin: o 3.2.0 exige atestado também ao ATUALIZAR veredito, e cinco pontos do repo quebram com `PowerAttestationMissingError` (`test_experiment_registry.py` ×4, `test_trials.py` ×1) | domínio Cripto | reemissão real contra 3.2.0 + atestado nos cinco pontos | COMPATIBLE_BUT_OLDER_BY_DECISION |
| ST-01 | stocks-predictor | Atestado invalidado pelo bump do Core para 3.2.0 | Foi emitido com Core 3.1.0; o 3.2.0 invalida todo atestado anterior. Sem reemissão, H17/H18/H19 não registram trial. **Único item do ecossistema com prazo** | operador | atestado reemitido contra 3.2.0, `git status` limpo, sem `;dirty` | BLOCKING_H18 |
| ST-02 | stocks-predictor | Relatórios de H14/H15/H16 nunca versionados | Os três vereditos citam `reports/h1{4,5,6}_verdict_adhoc.md` "para detalhes completos"; H1–H13 estão versionados, esses não. O veredito se sustenta no ledger, mas a evidência detalhada só existe na máquina do operador | operador | `git add -f` dos três, ou nota permanente de que a evidência é local | REGISTERED_NOT_CLOSED |
| ST-03 | stocks-predictor | Ordem das rodadas H17/H18/H19 não fixada | O N do DSR cresce a cada tentativa: quem roda por último enfrenta a barra mais alta. Escolher depois de ver resultado é p-hacking | domínio Stocks | ordem declarada por escrito antes da primeira medição | OPEN |
| CR-02 | cripto-predictor | Próximo trigger natural do Task Scheduler não observado | Confirmação operacional futura; não bloqueia engenharia ou pesquisa | operador | evento natural e evidência de execução | PENDING_OBSERVATION |
| BIZ-01 | ecosystem-predictor | Hipótese comercial sem conversas reais | A lista de 10 nomes existe, mas não há evidência de dor, interesse ou pagamento | humano/comercial | primeira conversa qualificada e registro BIZ-001A..F | B0_CONTACT_LIST_READY |

Não são pendências: Core 3.2.0/CHANGELOG (a abertura da entrada 3.2.0 se contradizia
— dizia "aditivo" e "mudança de contrato" ao mesmo tempo — e foi corrigida em
2026-09-06); Ops 4.1.0/main, cujo bump desfez a ambiguidade em que
`predictor-ops==4.0.0` designava dois conteúdos conforme a origem; decisão
`INTENTIONALLY_REMOVED` do monitor; BR-01 a BR-04 foram encerrados pela decisão
`EXP001_HISTORICAL=NOT_VIABLE` e stores `MISSING_CONFIRMED`; preservação offsite de Core, Ops, Cripto e
Stocks; rotação da SerpAPI; pesquisa congelada de Cripto e das H1–H16 de Stocks; RJ arquivado.
