# Classificação prévia das fontes documentais — F1

Classificação realizada antes das edições da F1, em 2026-08-11, contra o
commit-base `a9214d69f188ab63bdbf0764a1bc28d7b0661b60`. Esta tabela registra a
decisão editorial; ela não substitui a evidência primária indicada em
`ECOSYSTEM_CURRENT_STATE.md`.

| Arquivo | Seção | Estado encontrado | Evidência usada | Classificação | Ação proposta |
|---|---|---|---|---|---|
| `README.md` | Visão geral/arquitetura | nomes locais, 10 repositórios e vendoring como modelo corrente | árvores, `pyproject.toml` e locks dos nove repositórios | `UPDATE_FACTUAL` | substituir pelo mapa remoto atual e separar plataforma de domínios |
| `README.md` | Status atual/testes | snapshot local de 2026-07-26 | CI no HEAD de 2026-08-03 a 2026-08-11 | `MARK_HISTORICAL` | apontar o snapshot para os fechamentos históricos e publicar CI corrente |
| `README.md` | Comandos reais | comandos do antigo workspace agregado | `pyproject.toml`, `uv.lock` e workflows atuais | `UPDATE_FACTUAL` | manter somente comandos oficiais deste repositório |
| `README.md` | Manifests/vendors e PARKED | modelo de cópia local superado para consumidores ativos | URLs de wheels nos `pyproject.toml`/`uv.lock`; árvore do WC | `UPDATE_FACTUAL` | publicar matriz real de consumo; preservar WC como legado vendorizado |
| `README.md` | Incidente/tarefas agendadas | fatos host-local de julho | nenhuma evidência atual equivalente nos nove HEADs | `MOVE_TO_HISTORY` | não apresentá-los como estado corrente; manter os relatórios históricos |
| `README.md` | Documentos canônicos | mistura de fontes correntes e fechamentos | declarações do próprio README/HANDOFF | `UPDATE_FACTUAL` | reduzir a três fontes correntes e rotular fechamentos como históricos |
| `README.md` | Limites/publicação | afirma que CI/remotos não existem | remotos e execuções de CI identificadas | `UPDATE_FACTUAL` | corrigir sem inferir prontidão produtiva |
| `ECOSYSTEM_HANDOFF.md` | Abertura/como retomar | snapshot de julho apresentado como atual | nove HEADs e CI atuais | `UPDATE_FACTUAL` | inserir handoff corrente e ordem de leitura verificável |
| `ECOSYSTEM_HANDOFF.md` | Mapa dos repositórios | inclui Stocks/NBA no universo corrente | escopo humano da F1 | `UPDATE_FACTUAL` | limitar a nove; registrar Stocks/NBA apenas como excluídos |
| `ECOSYSTEM_HANDOFF.md` | Camadas/consumidores | Core 1.3.3, Ops 1.3.4 e vendors | manifests e locks atuais | `UPDATE_FACTUAL` | usar Core 2.2.x/Ops 3.0.0 e forma de consumo real |
| `ECOSYSTEM_HANDOFF.md` | decisões, testes e números de julho | registro temporalmente válido, mas não atual | commits e documentos históricos citados | `MARK_HISTORICAL` | preservar integralmente sob aviso explícito de snapshot histórico |
| `PENDENCIAS_ABERTAS.md` | lista canônica | itens e contagens de 2026-07 | HEADs atuais não confirmam continuidade de todos os itens | `UNKNOWN_REQUIRES_REVIEW` | deixar de declarar a lista antiga como corrente; criar lista F1 factual mínima |
| `PENDENCIAS_ABERTAS.md` | resolvidos/histórico | evidência histórica detalhada | commits/documentos citados no próprio arquivo | `KEEP_CURRENT` | preservar como registro histórico, sem reclassificação científica |
| `ARTIFACT_INVENTORY.md` | inventário por domínio | números científicos e paths de julho | não houve reprodução de datasets na F1 | `MARK_HISTORICAL` | preservar; retirar do índice de estado corrente |
| `RUNBOOK_*.md` | procedimentos | procedimentos de workspace antigo | não executados nesta F1 | `UNKNOWN_REQUIRES_REVIEW` | manter como históricos/legados; não recomendar como comando corrente |
| `ECOSYSTEM_FINAL_CLOSURE.md`, `FINAL_*`, `FECHAMENTO_*`, `VEREDITOS_*`, `BLOQUEIOS_*` | todas | registros de encerramento e resultados datados | conteúdo versionado nos commits históricos | `KEEP_CURRENT` | não reescrever nem recalcular |
| `docs/ECOSYSTEM_BLUEPRINT.md`, `docs/adr/*`, `docs/GO_CHECKLIST.md`, `docs/FASE_5_REPORT.md` | todas | arquitetura e decisões da plataforma criada em agosto | código, testes e CI do próprio repositório | `KEEP_CURRENT` | referenciar como arquitetura da plataforma; não promover a estado dos domínios |
| `PREDICTOR_CORE_BLUEPRINT.md`, `SINERGIAS_ECOSSISTEMA.md` | propostas/candidatos | propostas e decisões antigas | sem autorização F2 | `MARK_HISTORICAL` | manter fora das fontes correntes; nenhuma promoção nesta F1 |
| referências `tools/`, `predictor_core/`, `previsao-cripto`, `wc-predictor-v2` | múltiplas | caminhos locais antigos | remotos `tools-predictor`, `core-predictor`, `cripto-predictor`, `wc-predictor` | `BROKEN_REFERENCE` | substituir nas fontes correntes por URLs GitHub válidas |
| referências a `Claude` | múltiplas | snapshot mencionado como fóssil | decisão de escopo F1 | `KEEP_CURRENT` | manter apenas a nota de que não é fonte canônica |

Nenhuma classificação acima autoriza alteração de ciência, execução de coleta,
promoção para Core/Ops ou início da F2.
