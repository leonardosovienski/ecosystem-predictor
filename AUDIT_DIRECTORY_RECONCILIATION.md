# AUDIT_DIRECTORY_RECONCILIATION.md

Reconciliação de `audit/` (71 arquivos, não versionado pelo Git — coberto
pela regra `*/` do `.gitignore` do repositório de governança da raiz) contra
o estado atual do workspace. `audit/` é uma auditoria independente e
anterior a todo o ciclo coberto por `FINAL_FORENSIC_REVIEW.md` e
`ECOSYSTEM_FINAL_CLOSURE.md` — datada de 2026-07-15, dois dias antes das
rodadas de reintegração/hardening/tools/predictor_core revisadas
anteriormente.

## Metodologia desta reconciliação

Dado o volume (71 arquivos), a leitura priorizou os documentos que já
consolidam as conclusões de blocos inteiros de trabalho — `AUDIT_STATE.md`
(estado persistente, resume cada etapa 0-25), `OPEN_QUESTIONS.md` (78
questões abertas numeradas, com estado por questão), `13_FINAL_VERDICT.md`
(veredito formal da fase documental original), e os documentos "final" por
domínio (`44_CRYPTO_FINAL_READINESS.md`, `54_PROJECT_FINAL_ROLES.md`,
`45_CROSS_DOMAIN_CAPABILITY_INVENTORY.md`) — complementados por leitura
integral do documento de maior severidade (`38_CRYPTO_SECRET_INCIDENT_CLOSURE.md`)
e greps direcionados nos demais para confirmar/refutar afirmações
específicas. Isto **não** é uma leitura linha-a-linha dos 71 arquivos
individuais (00 a 60A) — é uma reconciliação pelos documentos-síntese, que
por desenho do próprio processo de auditoria original (etapas numeradas,
cada uma produzindo um relatório e sendo absorvida pela próxima) já
recapturam o conteúdo das etapas intermediárias. Registrado aqui como
limitação de escopo explícita, não como alegação de cobertura total.

## Achado mais importante: incidente de segurança

`38_CRYPTO_SECRET_INCIDENT_CLOSURE.md` documenta `BLOCKED_PENDING_SECRET_ROTATION`
— não estava em `FINAL_FORENSIC_REVIEW.md`, `ECOSYSTEM_FINAL_CLOSURE.md`, nem
na primeira versão de `PENDENCIAS_ABERTAS.md`. Detalhado, ampliado (escopo
real é 5 logs, não 3) e verificado nesta rodada em
`SECURITY_INCIDENT_SECRET_ROTATION.md`.

## Reconciliação de OPEN_QUESTIONS.md (78 questões)

A maioria das 78 questões (OQ-001 a OQ-078) foi endereçada pelas
implementações A-01 a A-06 registradas no próprio `AUDIT_STATE.md`, que
correspondem diretamente às capacidades hoje presentes em `tools/`
(`vendor_byte_audit.py` → OQ-009/013; `core_provenance.py` → OQ-032;
`operational_runner.py` → OQ-014/038/048/060; `secret_redaction.py` →
OQ-064/066/067) — confirmado por leitura cruzada com o código atual e com
`FINAL_FORENSIC_REVIEW.md`. As questões que seguem genuinamente abertas,
por não terem contrapartida em nenhum documento ou commit posterior:

| Questão | Estado em `audit/` | Estado atual (reconciliado) |
|---|---|---|
| OQ-006 (projetos sem Git) | ABERTA | NÃO INVESTIGADO nesta rodada — fora do escopo de tools/predictor_core/5 consumidores/3 protegidos |
| OQ-007/OQ-020/OQ-021/OQ-022/OQ-024/OQ-031 (estado do WC, `../wc-predictor` externo) | ABERTA | NÃO INVESTIGADO — WC é PARKED; regra desta rodada é não tocar/investigar além de confirmar PARKED |
| OQ-026 (calibradores locais vs. `calibration` do core) | ABERTA | NÃO REAVALIADO nesta rodada — sem evidência de bug, permanece `DOMAIN_LOCAL` por decisão já tomada em rodadas anteriores |
| OQ-034/035/036/037 (potência estatística, testes de futilidade, unidade de bootstrap, pré-registro) | ABERTA | NÃO REAVALIADO — são questões de metodologia científica de pesquisa em andamento, não bugs de engenharia |
| OQ-040 (backup/retenção de SQLite) | ABERTA | NÃO IMPLEMENTADO — nenhum consumidor pediu, sem evidência de perda de dados real |
| OQ-041 (CI/workflows externos) | ABERTA | Confirmado nesta e em rodadas anteriores: nenhum CI remoto configurado em nenhum dos 10 repos |
| OQ-064/066/067/068 (segredo, rotação) | CRÍTICA/BLOCKED | Ver `SECURITY_INCIDENT_SECRET_ROTATION.md` — escopo ampliado, mecanismo de prevenção verificado funcionando, rotação ainda pendente de ação humana |
| OQ-074/075 (H3 Brasileirão: CLV real, ledger com `predicted_at`) | ABERTA | Ver seção Brasileirão de `PENDENCIAS_ABERTAS.md` — ainda depende de amostra madura |
| OQ-076 (snapshot imutável pré-corrida F1 para H8) | ABERTA/CRÍTICA (científica, não segurança) | Confirmado ainda aberta — `H8_REQUIRED_RACES=15`, só 9 corridas maturadas (2026-07-17); gate permanece fechado corretamente |

## Reconciliação de 13_FINAL_VERDICT.md (classificação "EVOLUÇÃO INCREMENTAL")

O roadmap aprovado (seção 8 daquele documento: A-01, A-02, B-01 a B-03,
C-01/C-02, D-01 a D-03) foi **executado em sua maior parte** pelas rodadas
subsequentes cobertas por `SINERGIAS_ECOSSISTEMA.md` e
`FINAL_FORENSIC_REVIEW.md`:
- A-01 (byte audit) → `tools/vendor_byte_audit.py`, confirmado hoje `IDENTICAL` nos 5 vivos.
- A-02 (provenance runtime) → `tools/core_provenance.py`.
- B-02 (glossário de status científico/operacional) → **não encontrado** um glossário formal; os termos GO/NO-GO/REFUTADA/COMPROVADA continuam usados de forma consistente mas sem um documento único que os defina — gap documental menor, não bloqueante.
- D-01/D-02 (contrato temporal, lifecycle) → investigado nas rodadas de `predictor_core` desta sessão; decisão consistente com o veredito original do audit ("permanece local", `SHARED_BUT_INCUBATING`).
- D-03 (comparação vendor vs. pacote) → não executado; `tools/pyproject.toml` documenta explicitamente que instalação via pacote não é objetivo atual — consistente com a recomendação de adiar D-03 até haver medição.

## Reconciliação por projeto (44_CRYPTO_FINAL_READINESS, 54_PROJECT_FINAL_ROLES)

Já refletida nas seções específicas de `PENDENCIAS_ABERTAS.md` (versão
atualizada desta rodada). Nenhuma contradição material encontrada entre o
veredito de 2026-07-15 ("Cripto tecnicamente PASS, operacionalmente
BLOQUEADO...") e o estado atual — exceto que o bloqueio operacional
(segredo) tem escopo maior do que documentado então, e o mecanismo de
redação, que na época ainda não existia, agora existe e foi verificado.

## Claims não confirmadas nesta reconciliação

- "Four Factors" para nba-predictor: `audit/54_PROJECT_FINAL_ROLES.md` e
  `45_CROSS_DOMAIN_CAPABILITY_INVENTORY.md` mencionam apenas "fatores"
  genericamente ("decomposição de fatores", "nova premissa") no contexto do
  histórico negativo do NBA — não há menção específica a "Four Factors"
  (a métrica de Dean Oliver) em lugar nenhum do `audit/` nem do
  `nba-predictor` (grep zero). Classificado `NOT_CONFIRMED`.
- `predictor_core/incubating/`: não existe tal diretório; não encontrado em
  nenhum arquivo de `audit/` como nome literal. Classificado `NOT_CONFIRMED`.

## Limitação desta reconciliação

Os ~50 arquivos numerados intermediários (01 a 12, 14 a 37, 45 a 53, 56 a
60A) não foram lidos individualmente nesta rodada — apenas indiretamente,
via os documentos-síntese que os consolidam. Se uma auditoria futura
precisar de evidência específica de uma etapa intermediária (ex.: o
conteúdo exato de `28D_F1_H8_BLOCKER_REPORT.md` além do que
`AUDIT_STATE.md` já resume), ela deve ser lida diretamente — não presuma
que esta reconciliação a esgotou.
