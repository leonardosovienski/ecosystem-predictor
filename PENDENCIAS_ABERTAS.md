# PENDÊNCIAS ABERTAS — lista consolidada

Consolida em um único lugar tudo que ficou pendente, deferido ou é risco
residual em todo o ecossistema, extraído de `FINAL_FORENSIC_REVIEW.md`
(seção 25), `ECOSYSTEM_FINAL_CLOSURE.md` (seção 21) e achados soltos ao
longo das rodadas. Nada aqui é um bug ativo desconhecido — são decisões
conscientes de não agir, com a condição que faria reabrir cada uma.

**Bugs reais conhecidos e não corrigidos: zero.** Tudo que foi reproduzido
como bug real neste ciclo foi corrigido e testado. O que resta abaixo é
risco teórico, decisão de design deferida, ou limpeza cosmética opcional.

## 1. Decisões científicas deferidas (requerem 2ª evidência ou 2º consumidor para reabrir)

| # | Item | Onde | Por que está parado | O que reabriria |
|---|---|---|---|---|
| 1 | `RatingBook` não normaliza identidade (case/whitespace) — `"Team A"` e `"team a "` viram entidades diferentes, um typo cria fantasma sem histórico | `predictor_core/kernel/rating.py` | Normalizar mudaria trajetórias de rating futuras (mudança científica); só `f1-predictor` usa `RatingBook` diretamente hoje | 2º consumidor real de `RatingBook`, ou um typo real observado em produção |
| 2 | Lifecycle `PRE_EVENT`/`MATURED` não promovido a `predictor_core` | cs-predictor, f1-predictor, lol-predictor (3 implementações locais) | As 3 têm garantias estruturalmente diferentes — CS tem vínculo criptográfico (hash) entre snapshots, F1 e LoL não; semântica ainda não convergiu | Um 4º domínio precisar do mesmo padrão E as 3 implementações convergirem em garantias |
| 3 | `PredictionPoint` não tem `observed_at`/`available_at` — não há checagem cruzada entre `predicted_at` e o `published_at` dos dados que alimentaram a previsão | `predictor_core/data/contracts.py` | Decisão de design nova, não um bug reproduzido; exigiria desenhar um contrato novo | Um consumidor real reportar um incidente de lookahead causado por essa ambiguidade |
| 4 | `is_mature()` é só informativo — nada impede código de ler `.value` de uma previsão ainda imatura | `predictor_core/data/contracts.py` | Enforcement real exigiria um wrapper de tipo novo; hoje nenhum dos 5 consumidores acessa `.value` sem checar `is_mature()` primeiro (confirmado por grep) | Um consumidor real acessar `.value` prematuramente |
| 5 | Elo do F1 não usa `kernel/rating.py` (`RatingBook`) — família matemática igual, mas K-factor combinado diferente (média no F1 vs. máximo no core) | `f1-predictor` | Migrar mudaria ratings históricos; sem 2º consumidor real da extensão Plackett-Luce que o F1 usa | 2º consumidor real precisando da mesma extensão |

## 2. Riscos residuais técnicos (comportamento aceito, documentado)

| # | Item | Onde | Risco real | Mitigação atual |
|---|---|---|---|---|
| 6 | Race de heartbeat concorrente no caminho "perdedor" do lock — o processo que perde a corrida do lock ainda escreve heartbeat sem lock nenhum | `tools/operational_runner.py` | Baixo — só o sintoma (`PermissionError` no Windows) foi absorvido por retry; a escrita concorrente em si não foi eliminada | Retry com backoff absorve a colisão transitória; comportamento pré-existente, fora do escopo da correção |
| 7 | Lock do `TrialRegistry` não distingue PID reciclado do PID original | `predictor_core/measurement/trials.py` | Teórico — reuso de PID após reboot cairia no fallback de idade (10s), igual ao comportamento anterior à correção | Fallback de idade preserva a garantia original; falta só metadado extra (hostname/start-time) para desambiguar |
| 8 | Símbolos "acidentalmente públicos" em `tools/` (`content_hash`, `redact_mapping`, `build_manifest`, etc.) — importáveis mas sem consumidor externo real | `tools/*.py` | Nenhum — apenas classificados no README, não renomeados (decisão sua: "apenas classificar") | Um consumidor externo real começar a importar um desses diretamente |

## 3. Limpeza cosmética opcional (sem risco, sem prazo)

| # | Item | Onde |
|---|---|---|
| 9 | 2 wrappers redundantes de `CircuitBreaker` (`dpl/` e `v3/`), resíduo de migração — ambos funcionam, nenhum bug | `previsao-cripto` |
| 10 | 11 scripts de scratch reimplementam `brier` localmente em vez de importar do core | `brasileirao-predictor/scripts/*.py` | Só scripts de experimentação, nunca pipeline de produção |
| 11 | `cs-predictor` tem um rating Elo local (`ShrunkMapElo`) que não usa `RatingBook` — mecânica de shrinkage parece genuinamente específica do CS, nunca comparada a fundo | `cs-predictor/src/model_maps_shrunk.py` |

## 4. Infraestrutura/processo, sem urgência

| # | Item |
|---|---|
| 12 | Schemas operacionais (heartbeat/health/eventos JSONL) sem `schema_version` explícito — nenhum consumidor pediu migração incompatível ainda |
| 13 | CI multiplataforma (só Windows validado) — ambiente real de produção hoje é Windows |
| 14 | Fixtures de teste compartilhadas em `tools/` — sem duplicação comprovada entre 2+ consumidores ainda |
| 15 | Recomendação de versão pendente de aplicação: `tools/` 1.3.0→1.3.1 (PATCH), `predictor_core` 1.3.1→1.3.2 (PATCH) — não executado, sem autorização de bump |
| 16 | Nada foi publicado em nenhum repositório (sem push, sem tag) — pendente de decisão sua sobre quando/se publicar |

## 5. Estado historicamente preservado, não é pendência ativa

- Branch `reintegracao-f1-ondas-2-3` em `f1-predictor`: commits redundantes preservados (não mesclados), depois que se descobriu que `main` já tinha avançado com trabalho equivalente + melhor. Não precisa de ação.
- 4 worktrees paralelos existentes (`brasileirao-predictor`, `previsao-cripto`, `nba-predictor`, `wc-predictor-v2`) seguem intocados desde o início da sessão.
- `predictor-stocks/AGENTS.md` untracked — projeto protegido (PARKED), fora de escopo, não investigado nem tocado.

## Resumo por severidade

- **CRÍTICO aberto**: 0
- **HIGH aberto sem decisão explícita**: 0 (itens 1 e 2 são HIGH mas têm decisão sua registrada — `CORRECTLY_DEFERRED`/`INCUBATING`)
- **MEDIUM/LOW deferido conscientemente**: itens 3-11
- **Informativo/infraestrutura**: itens 12-16
- **Histórico, sem ação necessária**: seção 5
