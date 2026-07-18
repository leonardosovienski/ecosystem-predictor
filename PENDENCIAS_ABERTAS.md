# PENDÊNCIAS ABERTAS — lista canônica

Lista canônica de tudo que ainda não está encerrado no ecossistema, em
2026-07-18. Consolida `FINAL_FORENSIC_REVIEW.md`, `ECOSYSTEM_FINAL_CLOSURE.md`,
`AUDIT_DIRECTORY_RECONCILIATION.md` (leitura de `audit/`, 71 arquivos, auditoria
independente de 2026-07-15) e verificação direta desta rodada. Cada item usa
uma destas classificações, nunca misturadas:

`OPEN_SECURITY_INCIDENT` · `OPEN_BUG` · `BLOCKED_EXTERNAL_ACTION` ·
`OPEN_OPERATIONAL_GAP` · `OPEN_SCIENTIFIC_GAP` · `OPEN_DOCUMENTATION_GAP` ·
`SHARED_BUT_INCUBATING` · `DOMAIN_LOCAL` · `CORRECTLY_DEFERRED` ·
`NOT_CONFIRMED` · `REJECTED` · `RESOLVED_AND_VERIFIED`

**Bugs de código reais e não corrigidos: zero.** O único item que bloqueia
um veredito limpo é de segurança e requer ação humana fora do código
(seção 1).

---

## 1. Incidente de segurança

| ID | Item | Classificação | Evidência | Ação restante |
|---|---|---|---|---|
| SEC-1 | Chave da SerpAPI em texto plano em 5 logs históricos do previsao-cripto (`garimpo_fase1_20260713.log` a `_17.log`); mecanismo de prevenção já corrigido e verificado funcionando (log de 18/07 limpo, confirmado por execução real de produção) | `BLOCKED_EXTERNAL_ACTION`, explicitamente **baixa prioridade** por decisão humana (2026-07-18) | `SECURITY_INCIDENT_SECRET_ROTATION.md` (documento completo, sanitizado) | Rotação da credencial no provedor + decisão sobre os 5 logs — **só ação humana, sem prazo definido**; logs deixados como estão (decisão explícita: manter, não sanitizar) |

## 2. Bugs de código abertos

Nenhum. Todo bug reproduzido em qualquer rodada (tools/, predictor_core,
brasileirao financeiro, trials, quality.py) foi corrigido e testado —
ver `FINAL_FORENSIC_REVIEW.md` e `ECOSYSTEM_FINAL_CLOSURE.md` para a
verificação independente de cada um.

## 3. Gaps operacionais

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| OP-1 | Race de heartbeat concorrente no caminho "perdedor" do lock em `tools/operational_runner.py` — só o sintoma (`PermissionError` no Windows) foi absorvido por retry, a escrita concorrente em si não foi eliminada | `CORRECTLY_DEFERRED` | Baixo risco, comportamento pré-existente fora do escopo da correção de retry |
| OP-2 | Lock do `TrialRegistry` não distingue PID reciclado do PID original | `CORRECTLY_DEFERRED` | Fallback de idade preserva a garantia original; PID-reuso cai no mesmo comportamento de antes da correção, não piora |
| OP-3 | Glossário formal de status científico/operacional (GO/NO-GO/REFUTADA/COMPROVADA/INCONCLUSIVA) recomendado por `audit/13_FINAL_VERDICT.md` (item B-02) nunca foi criado como documento único | `OPEN_DOCUMENTATION_GAP` | Os termos são usados de forma consistente nos documentos existentes, mas sem definição formal centralizada — não bloqueante |
| OP-4 | Backup/retenção/restore testado para os bancos SQLite/FeatureStore de cada consumidor (`audit/` OQ-040) | `OPEN_OPERATIONAL_GAP` | Não investigado em nenhuma rodada; sem evidência de perda de dados real até hoje |
| OP-5 | Schemas operacionais (heartbeat/health/eventos JSONL) sem `schema_version` explícito | `CORRECTLY_DEFERRED` | Nenhum consumidor pediu migração incompatível ainda |
| OP-6 | CI multiplataforma (só Windows validado localmente) | `CORRECTLY_DEFERRED` | Ambiente real de produção hoje é Windows; sem publicação, sem CI remoto configurado em nenhum dos 10 repos |

## 4. Gaps científicos

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| SCI-1 | `RatingBook` não normaliza identidade (case/whitespace) — `"Team A"` e `"team a "` viram entidades diferentes | `CORRECTLY_DEFERRED` | Normalizar mudaria trajetórias de rating futuras (mudança científica); só `f1-predictor` usa `RatingBook` diretamente hoje. Reabre com 2º consumidor real ou typo real observado em produção |
| SCI-2 | `PredictionPoint` não tem `observed_at`/`available_at` — sem checagem cruzada entre `predicted_at` e o `published_at` dos dados de entrada | `CORRECTLY_DEFERRED` | Gap de design, não bug reproduzido. Reabre com incidente real de lookahead reportado |
| SCI-3 | `is_mature()` é só informativo, sem enforcement técnico de acesso | `CORRECTLY_DEFERRED` | Nenhum dos 5 consumidores acessa `.value` sem checar `is_mature()` primeiro (confirmado por grep) |
| SCI-4 | Elo do F1 não usa `RatingBook` do core (K-factor combinado diferente) | `DOMAIN_LOCAL` | Migrar mudaria ratings históricos; sem 2º consumidor real da extensão Plackett-Luce |
| SCI-5 | Modo sombra do brasileirao-predictor (H3) ainda precisa de amostra madura (~40 jogos citados no histórico de commits de validação forward) antes de decidir viés OVER/UNDER, capturabilidade de odds e IC do ROI | `OPEN_SCIENTIFIC_GAP` | Governança científica normal — aguardar, não acelerar |
| SCI-6 | H8-F1 (choque estrutural de regulamento) segue com amostra insuficiente: `H8_REQUIRED_RACES=15`, só 9 corridas maturadas confirmadas em 2026-07-17; sem snapshot pré-corrida imutável e datado ainda comprovado para nenhuma corrida | `OPEN_SCIENTIFIC_GAP` | Gate de decisão econômica corretamente fechado; reabre quando 2026 tiver ≥15 corridas maturadas |
| SCI-7 | Fase 1b (avaliação econômica via odds) de CS e LoL bloqueada por ausência de fonte gratuita e comprovada de odds históricas/ao vivo | `OPEN_SCIENTIFIC_GAP` | Dependência externa de dados, não bug de modelo |
| SCI-8 | Hipótese H5 (multi-juiz, previsao-cripto) em coleta, sem GO/NO-GO — janela de decisão original citada em `SINERGIAS_ECOSSISTEMA.md` como 28/07 | `OPEN_SCIENTIFIC_GAP` | Não deve ser refinada nem convertida em nova hipótese antes da janela por decisão de governança já registrada |

## 5. Capacidades incubadas / candidatas ao core (não promovidas)

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| INC-1 | Lifecycle `PRE_EVENT`/`MATURED` compartilhado — cs-predictor, f1-predictor, lol-predictor têm 3 implementações locais com garantias estruturalmente diferentes (CS tem vínculo criptográfico/hash entre snapshots, F1 e LoL não) | `SHARED_BUT_INCUBATING` | Reabre quando um 4º domínio precisar do mesmo padrão E as 3 implementações convergirem em garantias |
| INC-2 | `shin_probabilities`, cliente `curl_cffi`+impersonate, `PlattCalibrator`, motor prequential, harness Brier+DM — listados como "candidatos ao core (roadmap de agosto)" em `SINERGIAS_ECOSSISTEMA.md`, cada um hoje duplicado em 2-3 domínios | `SHARED_BUT_INCUBATING` | Nenhuma promoção feita nesta rodada nem nas anteriores — decisão explícita de tratar como ciclo de trabalho próprio, separado de trabalho de domínio |

## 6. Dívidas técnicas / limpeza cosmética (sem risco, sem prazo)

| ID | Item | Classificação | Detalhe |
|---|---|---|---|
| DEBT-1 | Símbolos "acidentalmente públicos" em `tools/` (`content_hash`, `redact_mapping`, `build_manifest`, etc.) | `CORRECTLY_DEFERRED` | Classificados no README como internos-na-prática, não renomeados (decisão explícita: "apenas classificar") |
| DEBT-2 | 2 wrappers redundantes de `CircuitBreaker` (`dpl/` e `v3/`) em previsao-cripto | `CORRECTLY_DEFERRED` | Resíduo de migração, ambos funcionam, nenhum bug |
| DEBT-3 | 11 scripts de scratch em brasileirao-predictor reimplementam `brier` localmente em vez de importar do core | `DOMAIN_LOCAL` | Só scripts de experimentação, nunca pipeline de produção |
| DEBT-4 | `cs-predictor` tem rating Elo local (`ShrunkMapElo`) que não usa `RatingBook` | `DOMAIN_LOCAL` | Mecânica de shrinkage parece genuinamente específica do CS |
| DEBT-5 | Fixtures de teste compartilhadas em `tools/` não criadas | `CORRECTLY_DEFERRED` | Sem duplicação comprovada entre 2+ consumidores ainda |

## 7. Não objetivos (rejeitados deliberadamente)

| ID | Item | Classificação |
|---|---|---|
| REJ-1 | Instalação de `tools/` via `pip install` (build-system, entry points) | `REJECTED` — consumido via sys.path por todos os 5 vivos, declarar suporte não testado seria afirmação falsa |
| REJ-2 | Reconstrução estrutural / monorepo / fim do vendoring | `REJECTED` — `audit/13_FINAL_VERDICT.md`, custo comparativo nunca medido, risco de fazer supera prova de benefício |
| REJ-3 | Normalização automática de identidade dentro do `RatingBook` (`.strip().lower()` escondido no core) | `REJECTED` — mudaria ciência silenciosamente |

## 8. Fatos não confirmados (removidos de versões anteriores deste documento)

| ID | Alegação | Classificação | Motivo |
|---|---|---|---|
| NC-1 | "`predictor_core/incubating/`" como diretório real contendo `nullref`/`metrics`/`state_asof` | `NOT_CONFIRMED` | Diretório não existe; são módulos de produção normais em `measurement/` e `data/` |
| NC-2 | "S4U continuava pendente" no Cripto | `NOT_CONFIRMED` (na verdade `RESOLVED_AND_VERIFIED`) | `audit/39` já mostrava as 3 tarefas `Ready, S4U` em 2026-07-15; reconfirmado agora via `Get-ScheduledTask`: `LogonType=S4U` nas 3, `LastTaskResult=0` |
| NC-3 | "nba-predictor: renascimento com abordagem Four Factors" | `NOT_CONFIRMED` | Zero menção literal em qualquer lugar do workspace; `audit/54`/`45` mencionam apenas "fatores" genericamente no contexto do histórico negativo do NBA |

## 9. Itens resolvidos nesta rodada (verificados, não requerem mais atenção)

| ID | Item | Classificação | Evidência |
|---|---|---|---|
| RES-1 | Tarefa `GarimpoInvestimentos-ColetaDiaria` (legada) permanece desabilitada, sem risco de coleta duplicada | `RESOLVED_AND_VERIFIED` | `Get-ScheduledTask`: `State=Disabled`, reconfirmado agora |
| RES-2 | 3 tarefas agendadas do previsao-cripto (`GarimpoFase1`, `GarimpoV3Daily`, `cripto-watchdog-coleta`) rodando com sucesso, S4U correto | `RESOLVED_AND_VERIFIED` | `LastTaskResult=0` nas 3, execuções em 2026-07-17 22:00/21:30/19:00 |
| RES-3 | Mecanismo de redação de logs (SEC-1) funciona corretamente para o cenário do incidente | `RESOLVED_AND_VERIFIED` | Reproduzido com credencial sintética + confirmado por execução real de produção (log de 18/07 limpo) |
| RES-4 | `release_check.py` sem teste dedicado (achado original de `audit/13`, item B-atual) | `RESOLVED_AND_VERIFIED` | 10 testes adicionados na rodada tools/ desta sessão (`60b02a8`), reexecutados agora, passam |

## 10. Estado historicamente preservado, sem ação necessária

- Branch `reintegracao-f1-ondas-2-3` em `f1-predictor`: commits redundantes preservados, não mesclados.
- 4 worktrees paralelos (`brasileirao-predictor`, `previsao-cripto`, `nba-predictor`, `wc-predictor-v2`) intocados.
- `predictor-stocks/AGENTS.md` untracked — projeto protegido, fora de escopo.
- Recomendações de versão pendentes de autorização: `tools/` 1.3.0→1.3.1, `predictor_core` 1.3.1→1.3.2 (ambos PATCH); nada publicado (sem push/tag) em nenhum repositório.

## Resumo por severidade

- **Incidente de segurança aberto**: 1 (SEC-1) — bloqueado por ação humana externa
- **Bugs de código abertos**: 0
- **Gaps operacionais**: 2 abertos (OP-3 documentação, OP-4 backup) + 4 corretamente deferidos (OP-1, OP-2, OP-5, OP-6)
- **Gaps científicos**: 4 abertos (SCI-5, SCI-6, SCI-7, SCI-8), governança normal de pesquisa em andamento
- **Capacidades incubadas**: 2
- **Dívidas técnicas**: 5, todas deferidas conscientemente
- **Não objetivos**: 3
- **Fatos não confirmados**: 3
- **Resolvidos nesta rodada**: 4
