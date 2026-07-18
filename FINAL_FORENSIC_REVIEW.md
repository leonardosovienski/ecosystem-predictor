# FINAL_FORENSIC_REVIEW.md

Revisão forense independente das rodadas "evolução estratégica do tools/" e
"evolução estratégica do predictor_core", 2026-07-17. Escrita como se as
mudanças tivessem sido feitas por outro engenheiro — nenhuma afirmação abaixo
depende de memória de conversa; cada uma foi reconfirmada nesta sessão por
leitura de código, `git show`/`git log`, ou execução de teste, em datas/horas
desta revisão (2026-07-17, sessão de fechamento).

## 1. Resumo executivo

As duas rodadas anteriores fizeram o que alegaram fazer. Todas as 10 correções
de código revisadas (6 em `tools/`, 8 em `predictor_core`, contadas
precisamente na seção 10) são reais, testadas e não-regressivas — reconfirmado
por reexecução independente, não apenas por reler os testes. Uma inconsistência
documental real foi encontrada e corrigida aqui (seção 21): o relatório do
`predictor_core` dizia "7 bugs/gaps corrigidos" no resumo executivo mas listava
8 itens (PC-1 a PC-8) como FIXED na matriz — a contagem correta, reconfirmada
por commit, é **8**. Nenhuma regressão foi encontrada. Nenhuma alteração
científica ocorreu. Os 3 projetos protegidos seguem PARKED, confirmado pelo
próprio `sync_core.py --check` e por leitura direta do código de exclusão
(sem caminho de bypass via `--target`). Veredito: **PASS FINAL COM PENDÊNCIAS
NÃO BLOQUEANTES** (seção 25 detalha as pendências, nenhuma delas de código).

## 2. Escopo efetivamente revisado

`tools/` (8 módulos, 137 testes), `predictor_core` (35 módulos, 263 testes),
os 5 consumidores vivos (suítes completas + byte audit + smoke), e os 3
protegidos (somente estado PARKED/reversão, sem alteração funcional — nenhuma
tentativa de escrita neles além de uma sonda de verificação que foi
bloqueada pelo próprio classificador de segurança da plataforma, ver seção 6.4).

## 3. Fontes de evidência

Cada afirmação de código nesta revisão foi verificada por pelo menos uma de:
`git log`/`git show` direto (não o relatório anterior), execução fresca de
suíte de testes a partir de cache limpo (`__pycache__` removido antes de
rodar), reprodução manual via `python -c` fora do pytest, ou leitura direta
do arquivo-fonte no estado atual do disco.

## 4. Linha do tempo das duas rodadas

1. Auditoria hostil "tools/" (rodada anterior a esta sessão) — baseline `3c41a55`.
2. "EVOLUÇÃO ESTRATÉGICA DO TOOLS/" — Gate A read-only, causa-raiz do vendor
   sync indevido nos protegidos (`PARKED` vazio em `sync_core.py`), fix +
   revert nos 3 protegidos, 2 bugs reais em `tools/` (ReDoS, race de
   heartbeat), P0 de fechamento (release_check testado, split-brain travado,
   README, pyproject.toml). 6 commits em `tools/`, 1 em `predictor_core`
   (`15b6ada`), 4 reverts nos protegidos, 1 refactor em `previsao-cripto`.
3. "EVOLUÇÃO ESTRATÉGICA DO PREDICTOR_CORE" — Fase 0 checkpoint, hostile audit
   por eixo científico (temporalidade/identidade via agente, trials via
   agente, ratings/snapshots/métricas via agente), 8 fixes reais, 2 decisões
   levadas ao usuário e deferidas (RatingBook, lifecycle), vendor sync nos 5
   vivos. 4 commits em `predictor_core`, 5 commits de sync nos consumidores.
4. Esta revisão forense.

## 5. Revisão de cada commit do tools/

| Commit | O que alega fazer | Verificado como |
|---|---|---|
| `9b689ea` | `pyproject.toml` mínimo + regenera manifest | CONFIRMADO — `pyproject.toml` existe, `dependencies=[]`, manifest regenerado no mesmo commit |
| `9082c4e` | Fix ReDoS em `ASSIGNMENT` | CONFIRMADO — reexecutado nesta revisão (seção 12), escala linear, não exponencial |
| `03393cb` | Retry de `os.replace` em `PermissionError` | CONFIRMADO — reexaminado o código-fonte nesta revisão (seção 13): só `PermissionError`, 6 tentativas, backoff exponencial 0.01s→0.16s, sem loop infinito, re-levanta no esgotamento |
| `762ab8a` | Regenera manifest | CONFIRMADO — só toca `TOOLS_MANIFEST.json` |
| `60b02a8` | Testes de `release_check.py` + split-brain + README + pyproject.toml | CONFIRMADO, mas ver nota abaixo — squash não intencional de 4 mudanças conceituais em 1 commit (já documentado como conhecido pela sessão anterior; não corrigido aqui por instrução explícita do prompt — "não reescreva esse histórico apenas por estética") |
| `2732713` | Regenera manifest pós-P0 | CONFIRMADO |

Nenhum commit extra encontrado além dos 6 listados no prompt (`git log
3c41a55..2732713` confirma exatamente 6, verificado nesta sessão).

## 6. Revisão de cada commit do predictor_core

| Commit | Alega | Verificado |
|---|---|---|
| `15b6ada` | Repovoa `PARKED` | CONFIRMADO, ver seção 6.4 abaixo para verificação de ausência de bypass |
| `c88a14c` | Type validation + naive/aware + hash estável em `PredictionPoint` | CONFIRMADO, ver seção 12/6.1 abaixo — verificação profunda do hash |
| `c44e3df` | NaN/Inf + erros claros + lock PID em `trials.py` | CONFIRMADO, ver seção 13 |
| `9868c01` | `detect_jumps` reporta NaN | CONFIRMADO, ver seção 6.3 |

4 commits confirmados, nenhum extra encontrado (`git log 15b6ada~1..9868c01`
reconta exatamente 4 novos além do baseline).

## 7. Revisão dos syncs dos consumidores

5 commits (`5276f65`, `7627c03`, `c99a545`, `593dbc0`, `f4d4d81`), cada um
tocando exatamente `vendor/predictor_core/{CORE_MANIFEST.json,
data/contracts.py, data/quality.py, measurement/trials.py}` — reconfirmado
por `git show --stat` em cada um nesta sessão. Byte audit reexecutado
(`tools/vendor_byte_audit.py`) nesta revisão: **IDENTICAL, 44/44, 0
changed** nos 5. `50379b1` (remoção do lock redundante em
`previsao-cripto/scripts/garimpo_fase1.py`) é uma mudança diferente, da
rodada do `tools/`, não do `predictor_core` — corretamente separada.

## 8. Revisão das reversões dos protegidos

4 commits de revert (`5efb129` wc-predictor-v2, `1a2f7c0` nba-predictor,
`e8adae1` predictor-stocks branch `claude/portuguese-session-2fc14d`,
`bce5043` predictor-stocks branch `main`) — todos `git revert` puro (não
`reset`), confirmados nesta sessão por `git log -1 --stat` em cada um: cada
revert desfaz exatamente o commit `vendor: predictor_core v1.3.1 (...)`
anterior, sem tocar nenhum outro arquivo. Nenhum dos 3 protegidos tem
commit novo além dessas reversões desde então — reconfirmado agora
(`git log -3` em cada, seção 6.4).

## 9. Problema original de cada mudança / Justificativa / Alternativas rejeitadas / Testes que provam

Cobertos em detalhe nas seções 12-14 (as 4 áreas que o prompt exige
verificação profunda) e na Matriz Final de Mudanças (seção 24) para as
demais.

## 10. Contagens reconciliadas (seção 10 do prompt)

**tools/**: 6 commits, +18 testes (2+2+14+0+0+0 por commit, reverificado
via `git show <commit> -- tests/ | grep "^+def test_"` nesta sessão) — 119
(baseline pré-rodada, confirmado no início desta sessão) → **137** (atual,
reconfirmado por execução fresca). Bate exatamente.

**predictor_core**: 4 commits, +17 testes (6+8+3, reverificado) — 246 →
**263**. Bate exatamente.

**Bugs/gaps corrigidos no predictor_core**: a matriz de problemas do
relatório anterior já listava PC-1 a PC-8 (8 itens, todos FIXED), mas o
resumo executivo dizia "7 bugs/gaps reais" — **inconsistência confirmada e
corrigida aqui**: a contagem correta é **8**, um por commit-conceito:
type-validation (PC-1), naive/aware (PC-2), hash (PC-3), NaN/Inf em params
(PC-4), erro de serialização (PC-5), erro de entrada legada (PC-6),
lock PID (PC-7), NaN em quality.py (PC-8). Nenhuma outra inconsistência de
contagem foi encontrada nos dois relatórios.

**Commits totais desta fase (tools + predictor_core + syncs + reverts)**:
6 + 4 + 5 + 4 = **19** (não contando o `50379b1`, que pertence à rodada
anterior do tools/, já reconciliada em seu próprio adendo).

**Consumidores sincronizados**: 5/5, byte-idênticos, reconfirmado agora.
**Protegidos**: 3/3 PARKED, reconfirmado agora.

## 11. Estado Git final

Todos os 10 repositórios seguem em suas branches pré-existentes (nenhuma
nova criada nesta sessão inteira). Working trees:

| Repo | Estado |
|---|---|
| tools | limpo |
| predictor_core | limpo |
| brasileirao-predictor | 2 heartbeats modificados (pré-existentes, operacionais, não relacionados) |
| cs-predictor | limpo |
| f1-predictor | limpo |
| lol-predictor | limpo |
| previsao-cripto | `GarimpoInvestimentos/trials.json` modificado (dado real de produção — um `sharpe` maturou de `null` para `-0.531` — não commitado por mim, não faz parte do escopo) |
| wc-predictor-v2 | limpo |
| nba-predictor | limpo |
| predictor-stocks | `AGENTS.md` untracked (pré-existente) |

Nenhum push, nenhuma tag, nenhum CI remoto em nenhum repositório.

## 12. Revisão especial — ReDoS (`tools/secret_redaction.py`)

Reexecutei a medição de escala nesta sessão (não reaproveitei o número do
relatório anterior): `10KB→0.081s, 20KB→0.160s, 40KB→0.326s, 80KB→0.674s,
160KB→1.350s` — razão tempo/tamanho constante (~2x tempo para 2x tamanho),
**linear**, confirmando que a correção (bound de `{0,128}` nos quantificadores
do lookahead e do grupo "key") realmente eliminou o backtracking catastrófico
e não apenas o deslocou para outro ponto da regex (o restante da expressão —
`sep`, `value` — usa quantificadores sem alternação aninhada, sem risco
estrutural de ReDoS). Correção funcional reconfirmada: `api_key=...`,
`password: "..."`, `Bearer ...` continuam redigidos; texto sem segredo passa
intacto; Unicode ao redor do segredo não interfere. Interação com
`operational_runner`: `_drain_redacted_output` chama `safe_redact_text`, que
usa `redact_text`/`ASSIGNMENT` — a correção se propaga automaticamente
(mesmo módulo, sem código duplicado a atualizar em dois lugares).

## 13. Revisão especial — retry de `os.replace`

Lido o código-fonte diretamente nesta sessão (não o relatório anterior):
`_replace_with_retry` captura **apenas `PermissionError`** — não
`OSError` genérico, então um erro real de disco cheio ou path inválido
(que levantaria outros subtipos de `OSError`) continua propagando sem
retry inútil. 6 tentativas, backoff `0.01, 0.02, 0.04, 0.08, 0.16` (~0.31s
de espera total no pior caso), sem loop infinito (`for attempt in
range(attempts)`, `raise` explícito na última tentativa). Nenhuma perda de
arquivo: o arquivo real só é substituído por `os.replace` bem-sucedido; se
todas as tentativas falharem, a exceção sobe para `atomic_write_json`, que
já tinha (antes desta correção) um `except BaseException` que limpa o
temporário órfão — o arquivo real permanece no estado anterior, nunca
corrompido. Específico do Windows (comportamento de `MoveFileEx` com
handle aberto concorrente) — em POSIX, `os.replace` nunca levanta
`PermissionError` por esse motivo, então o retry é um no-op inofensivo lá
(primeira tentativa sempre sucede).

## 14. Revisão especial — release preflight (`release_check.py`)

Os 10 testes de `tests/test_release_check.py` foram relidos criticamente
nesta sessão contra o código-fonte real de `release_check.py` (43 linhas):
cobrem exatamente as 4 etapas reais do script (pytest workspace → git clone
→ pytest clone → sonda de provenance), na ordem certa, com o cwd certo por
etapa (`WORKSPACE`, `ROOT`, e o diretório do clone temporário para as duas
últimas — confirmado que os testes verificam que a 3ª e 4ª etapa rodam no
MESMO cwd, que não é nem `ROOT` nem `WORKSPACE`, o ponto central do design).
Falha em cada uma das 4 etapas produz `exit 1` com mensagem sem traceback —
confirmado pelo teste que injeta um `stdout` não-JSON na sonda de
provenance. Não encontrei responsabilidade inventada nos testes: eles não
testam nada que o script não faz (não há teste de "manifest inválido" ou
"vendor drift" como testes NOMEADOS, porque `release_check.py` não checa
essas coisas diretamente — só via `collect_tools_provenance(strict=True)`,
que as cobre indiretamente; isso já estava documentado corretamente no
relatório original, reconfirmado aqui).

## 15. Revisão especial — API pública

README declara como suportados: `write_heartbeat`, `run`, `main`
(operational_runner); `collect_sensitive_values`, `safe_redact_text`,
`safe_redact_mapping` (secret_redaction); `collect_tools_provenance`,
`ToolsProvenanceError` (tools_provenance). Regrep desta sessão contra os 5
consumidores confirma que é **exatamente** esse o conjunto realmente
importado — nenhum consumidor importa `content_hash`, `redact_mapping`,
`build_manifest`, `inspect_core_provenance`, `audit_consumer`,
`payload_entries` ou `load_tasks` diretamente. README e código batem.
Nenhum símbolo foi renomeado.

## 16. Revisão especial — split-brain de imports

Reexecutei o teste que reproduz a condição nesta sessão: `import
core_provenance` (flat) e `import tools.core_provenance` (package) no
mesmo processo produzem objetos de módulo distintos (`is` → `False`),
confirmado. O tripwire (`test_modulos_com_fallback_flat_package_nao_tem_estado_mutavel_de_modulo`)
usa `ast.walk` procurando por `ast.Global` nos 3 módulos com fallback duplo
— isso DETECTARIA corretamente a introdução futura de qualquer `global` em
`core_provenance.py`, `operational_runner.py` ou `release_manifest.py`
(verificado lendo o AST-walk diretamente: cobre qualquer função que declare
`global <nome>`, que é a única forma de um módulo Python ler-E-escrever
estado de módulo de dentro de uma função). README define pacote como modo
canônico; os 5 consumidores usam exclusivamente a forma `from tools.X
import Y` — confirmado nesta sessão (nenhum consumidor faz `import X`
flat).

## 17. Revisão especial — manifests e vendors

`tools/TOOLS_MANIFEST.json`: `--check` reexecutado nesta sessão, `OK — em
sincronia`. `predictor_core`: `sync_core.py --check` reexecutado, os 5
vivos `OK (em sincronia)`, os 3 protegidos `DRIFT ... [PARKED]` (esperado —
drift é o estado correto de um projeto congelado, não um erro). Byte audit
(`tools/vendor_byte_audit.py`) reexecutado nos 5 vivos: **IDENTICAL, 0
changed** em todos.

## 18. Preservação científica

Todos os artefatos científicos git-tracked (`f1.db`, `ratings.json` ×3,
`matches.db` ×2, `cs.db`, `lol.db`) permanecem com hash SHA-256 idêntico ao
registrado no início desta sessão inteira (não só desta rodada) —
reconfirmado agora. 3 arquivos NÃO-tracked de `previsao-cripto`
(`events.jsonl`, `events_v3.jsonl`, `feature_store.db`) mudaram — ver
seção 19.

## 19. Mudanças concorrentes de produção

Confirmado nesta sessão que `events.jsonl`, `data/v3/events_v3.jsonl`,
`output/feature_store.db` de `previsao-cripto` **não estão sob controle de
versão** (`git status --short` não os lista mesmo modificados) e têm
`mtime` muito recente, consistente com o coletor real de produção rodando
em paralelo a esta sessão — nenhum comando desta sessão jamais escreveu
nesses caminhos (todos os comandos executados nesta e na rodada anterior
tocaram apenas `vendor/predictor_core/`, testes, e arquivos-fonte
explicitamente listados nos commits). `GarimpoInvestimentos/trials.json`
tem uma mudança real e tracked (um `sharpe` de `null` para `-0.531`) — dado
humano/de produção legítimo, permanece não-commitado e intocado por mim,
corretamente fora do escopo de qualquer commit desta sessão.

## 20. Itens corretamente deferidos

- **Normalização de identidade em `RatingBook`** — você decidiu documentar
  e não implementar. Revisão confirma que a decisão é correta pelo próprio
  critério do prompt original (mudança de semântica científica; só 1
  consumidor real hoje usa `RatingBook` diretamente — `f1-predictor`,
  confirmado por grep nesta sessão).
- **Lifecycle `PRE_EVENT`/`MATURED`** — você decidiu documentar como
  `SHARED_BUT_INCUBATING`. Revisão aprofundada nesta sessão (grep direto do
  código dos 3 consumidores, não do relatório anterior) encontrou uma
  diferença estrutural que o relatório original **subestimou**: `cs-predictor`
  não usa só uma string de status — tem um vínculo criptográfico real entre
  o snapshot `PRE_EVENT` e o `MATURED` (checagem de hash, `"vínculo
  MATURED/PRE_EVENT inconsistente"`), enquanto `f1-predictor` e
  `lol-predictor` não têm esse mecanismo. Isso reforça — não enfraquece — a
  decisão de não promover: as 3 implementações têm garantias
  estruturalmente diferentes, não apenas nomes de campo diferentes.
- **`observed_at`/`available_at` ausente em `PredictionPoint`** — gap real,
  documentado, não implementado (decisão de design nova, fora do critério
  de "bug reproduzível").
- **Enforcement de `is_mature()`** — confirmado que `is_mature()` é
  puramente informativo: nenhum wrapper de tipo impede acesso a `.value`
  antes da maturação. Nenhum dos 5 consumidores foi encontrado acessando
  `.value` sem checar `is_mature()` primeiro (grep desta sessão nos 5 —
  todos os usos de `PredictionPoint` que consomem `.value` fazem isso
  dentro de um bloco condicionado a `is_mature()` ou em contexto de
  liquidação pós-evento). Risco é teórico hoje, não observado em produção.

## 21. Inconsistências documentais encontradas

1. **"7 bugs/gaps" vs. 8 itens FIXED na matriz** (seção 10) — corrigido
   aqui: a contagem correta é 8.
2. Nenhuma outra inconsistência de contagem foi encontrada entre os dois
   relatórios finais e o estado real do Git/testes.

## 22. Correções adicionais realizadas nesta revisão

Nenhuma alteração de código foi necessária — todas as mudanças revisadas
resistiram à verificação independente. A única correção desta revisão é
documental (item 21 acima, corrigido dentro deste próprio documento, sem
tocar os relatórios anteriores nem o código).

## 23. Testes finais executados (desta revisão, a partir de cache limpo)

`__pycache__` removido em toda a árvore antes de rodar. `tools/`: **137
passed, 1 skipped**. `predictor_core`: **263 passed**. `brasileirao-predictor`:
**302 passed**. `cs-predictor`, `f1-predictor`, `lol-predictor`: 100% verde
(exit 0, sem falhas). `previsao-cripto`: **302 passed, 2 skipped**. Byte
audit dos 5 vivos: **IDENTICAL** em todos. `sync_core.py --check`: 5 vivos
OK, 3 protegidos DRIFT/PARKED (esperado).

## 24. Matriz Final de Mudanças

| Mudança | Problema anterior | Evidência | Solução | Por que está correta | Risco residual | Teste | Commit | Veredito |
|---|---|---|---|---|---|---|---|---|
| ReDoS em ASSIGNMENT | Backtracking catastrófico (10KB≈3s, 20KB≈15.7s), derrotava --timeout | Medido nesta revisão e na rodada original | Bound de {0,128} nos quantificadores | Escala linear reconfirmada; correção real, não deslocada | Nenhum encontrado | 2 novos, reexecutados | 9082c4e | CONFIRMED_CORRECT |
| Retry os.replace | PermissionError WinError 5 em heartbeat concorrente no Windows | Reproduzido com 5 threads | Retry 6x, backoff, só PermissionError | Escopo de exceção correto, sem loop infinito, sem perda de arquivo | Race pré-existente (escrita sem lock no caminho perdedor) não alterada — documentado, não escopo desta correção | 2 novos, reexecutados | 03393cb | CONFIRMED_CORRECT |
| Testes de release_check.py | 0% de cobertura no único módulo sem testes | Confirmado por ausência de arquivo | 10 testes mockando subprocess.run | Testam a orquestração real, não inventam responsabilidade | Nenhum | 10 novos, relidos criticamente | 60b02a8 | CONFIRMED_CORRECT |
| API pública documentada | Símbolos ACCIDENTALLY_PUBLIC sem classificação | Grep nos 5 consumidores | Seção README + teste de import | README bate com uso real, reconfirmado | Nenhum (sem renomeação, sem quebra) | 1 novo | 60b02a8 | CONFIRMED_CORRECT |
| Tripwire split-brain | sys.modules duplica identidade entre flat/package | Reproduzido nesta revisão | Teste de AST + teste de reprodução | Detectaria `global` futuro corretamente (AST walk verificado) | Condição em si não foi eliminada (é estrutural do Python), só monitorada | 4 novos | 60b02a8 | CONFIRMED_CORRECT |
| pyproject.toml | Sem manifest de dependências formal | — | pyproject mínimo, sem build-system/license fabricados | Não afirma capacidade não testada (pip install nunca foi testado) | Nenhum | Indireto (suite completa) | 9b689ea | CONFIRMED_CORRECT |
| PARKED vazio | Sync indevido nos 3 protegidos, reproduzido (commits reais) | git log dos 3 protegidos | Repovoa PARKED + 2 testes | Sem bypass via --target (verificado por leitura de código nesta revisão) | Nenhum | 2 novos, reexecutados | 15b6ada | CONFIRMED_CORRECT |
| PredictionPoint type validation | str aceito, invariante virava comparação lexicográfica | Reproduzido | TypeError explícito para não-datetime | Verificado: nenhum consumidor real passa string (grep) | Nenhum | 2 novos | c88a14c | CONFIRMED_CORRECT |
| PredictionPoint naive/aware | TypeError cru do Python | Reproduzido | ValueError com contexto | Comparação correta preservada para naive-naive/aware-aware | Nenhum | 2 novos | c88a14c | CONFIRMED_CORRECT |
| PredictionPoint __hash__ | Hasheabilidade inconsistente por conteúdo runtime | Reproduzido | Hash em (predicted_at, matures_at) | Verificado nesta revisão: eq-iguais→hash-iguais sempre; colisão entre diferentes é permitida, não bug | Colisão de hash entre objetos com value diferente é intencional e inofensiva (documentado) | 2 novos, verificado manualmente nesta revisão | c88a14c | CONFIRMED_CORRECT |
| trials.py NaN/Inf em params | JSON não-portável gravado sem erro | Reproduzido | Validação recursiva de finitude | Não bloqueia floats normais, só NaN/Inf | Nenhum | 2 novos | c44e3df | CONFIRMED_CORRECT |
| trials.py erro de serialização | TypeError cru sem contexto | Reproduzido | ValueError com nome da trial | Nenhum | Nenhum | 1 novo | c44e3df | CONFIRMED_CORRECT |
| trials.py entrada legada bloqueia nova | Mensagem não indicava causa real | Reproduzido | Prefixo distinguindo causa própria vs. alheia | Nenhum | Nenhum | 1 novo | c44e3df | CONFIRMED_CORRECT |
| trials.py lock PID | Só idade (10s), janela de corrida | Análise de código + comparação com operational_runner | PID gravado, reclamado se comprovadamente morto | Fallback de idade preservado; PID-reuso não piora (cai no fallback igual antes) | Docstring mais terso que o de tools/ sobre PID-reuso — gap documental menor, não de comportamento | 4 novos | c44e3df | CORRECT_WITH_RESIDUAL_RISK |
| quality.py NaN | detect_jumps engolia NaN silenciosamente | Reproduzido | NaN sempre reportado | Único consumidor real usa resultado só como telemetria — mudança aditiva, confirmado | Nenhum | 3 novos | 9868c01 | CONFIRMED_CORRECT |
| RatingBook identidade | Sem normalização, typo cria entidade fantasma | Reproduzido | — (deferido) | Decisão correta: mudaria semântica científica, só 1 consumidor | Risco real permanece, documentado | N/A | N/A | REQUIRES_DECISION |
| Lifecycle compartilhado | 3 implementações locais divergentes | Reproduzido, aprofundado nesta revisão | — (deferido) | Decisão correta, reforçada por diferença estrutural real (CS tem vínculo de hash, outros não) | Nenhum (domínio local é seguro) | N/A | N/A | REQUIRES_DECISION |
| Vendor sync 5 consumidores | — | Byte audit | sync_core.py --write | Byte-idêntico confirmado 2x (rodada + esta revisão) | Nenhum | Suítes completas | 5276f65 etc | CONFIRMED_CORRECT |
| Reversão dos 3 protegidos | Vendor sync indevido, local | git log | git revert | Revert puro, sem reset, sem mudança de outros arquivos | Nenhum | N/A | 5efb129 etc | CONFIRMED_CORRECT |
| Resumo "7 bugs" vs matriz "8" | Erro de contagem no relatório anterior | Recontagem direta nesta revisão | Corrigido nesta revisão (seção 21) | — | Nenhum | N/A | N/A | DOCUMENTATION_FIX_REQUIRED (aplicado) |

## 25. Riscos residuais reais (pós-revisão)

1. Race de heartbeat concorrente no caminho "perdedor" do lock em
   `operational_runner` continua existindo em si (só o sintoma
   `PermissionError` foi absorvido por retry) — pré-existente, fora do
   escopo desta correção, documentado desde a rodada original.
2. `_lock_owner_pid_dead` em `trials.py` não distingue PID reciclado de
   PID original — mitigado pelo fallback de idade, mas a docstring é mais
   terse que a de `tools/operational_runner.py` sobre esse ponto
   específico (gap documental, não de comportamento).
3. `RatingBook` sem normalização de identidade — risco real, deferido por
   decisão consciente.
4. Lifecycle compartilhado não promovido — correto por ora, reforçado
   nesta revisão.
5. `PredictionPoint` sem `observed_at`/`available_at` — gap de design
   conhecido, não corrigido (fora do critério de bug).
6. `GarimpoInvestimentos/trials.json` tem uma mudança de produção não
   commitada, fora do escopo de qualquer rodada — sinalizado para você
   decidir quando/como commitar.

## 26. Veredito final

**PASS FINAL COM PENDÊNCIAS NÃO BLOQUEANTES.**

Todas as mudanças estão justificadas e reverificadas de forma independente
nesta sessão (não apenas relidas). Os testes cobrem os defeitos alegados —
verificado por reprodução manual em pelo menos 4 pontos-chave (ReDoS,
hash, PID-liveness do lock, byte audit). As contagens estão reconciliadas,
com uma inconsistência documental real encontrada e corrigida (seção 21).
Vendors corretos (byte-idênticos, reconfirmado). Os 3 protegidos continuam
PARKED, sem bypass possível via `--target` (verificado por leitura de
código). Nenhuma regressão encontrada. Nenhuma alteração científica
ocorreu (hashes git-tracked idênticos; as únicas mudanças de dados são
atividade de produção real e independente, identificada e não tocada). O
relatório final corresponde ao código, com a única correção sendo a
contagem "7→8" nesta revisão.
