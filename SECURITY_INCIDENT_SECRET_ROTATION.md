# SECURITY_INCIDENT_SECRET_ROTATION.md

**Nenhum valor de segredo aparece neste documento ou em qualquer comando
usado para produzi-lo.** Toda verificação foi feita por metadados (tamanho,
timestamp, status Git, contagem de ocorrências por padrão estrutural, e
nome do campo/host da URL — nunca o valor). Ver seção 6 para o método exato.

> **Nota de priorização (2026-07-18):** confirmado explicitamente com o
> responsável que a rotação da credencial **não é prioridade no momento**
> — decisão consciente, não esquecimento. Os 5 logs históricos também
> foram deixados como estão, por decisão explícita (opção "manter",
> já era a recomendação deste documento). Nada muda no risco técnico: os
> logs nunca entraram no Git, o mecanismo de redação já impede vazamento
> novo, e a chave só permanece sensível até ser rotacionada — sem prazo
> definido para isso. `SECURITY_INCIDENT_STATUS` permanece
> `BLOCKED_PENDING_SECRET_ROTATION`, agora explicitamente de baixa
> prioridade por decisão humana, não por bloqueio técnico.

## 1. Resumo

**Estado: `BLOCKED_PENDING_SECRET_ROTATION`.** Uma chave de API (usada pelo
provedor de busca de notícias do `previsao-cripto`, via SerpAPI) foi gravada
em texto plano dentro da query string de URLs registradas em logs
operacionais locais, antes de uma correção de redação de logs ter sido
aplicada ao código. A correção já está em produção e foi **verificada
funcionando** nesta rodada (seção 5). O que resta é inteiramente uma ação
humana fora deste workspace: revogar/rotacionar a credencial e decidir o
destino dos logs históricos.

## 2. Origem e histórico

- Descoberto originalmente em `audit/38_CRYPTO_SECRET_INCIDENT_CLOSURE.md`
  (2026-07-15): scan seguro (sem exibir valor) encontrou 0 ocorrências em
  `garimpo_fase1_20260712.log` e 29 ocorrências potenciais em cada um dos
  logs de 13, 14 e 15/07.
- **Achado novo desta rodada**: reexecutei o mesmo tipo de scan seguro
  (via `tools/secret_redaction.py::scan_path`, que só retorna contagem e
  categoria do padrão — nunca o valor) contra todos os logs
  `garimpo_fase1_*.log` existentes hoje. O escopo real do incidente é maior
  do que o catalogado em 2026-07-15:

| Log | Ocorrências (padrão estrutural) | Campo/host identificado (seguro) |
|---|---|---|
| `garimpo_fase1_20260712.log` | 0 | — |
| `garimpo_fase1_20260713.log` | 29 | `api_key` em `https://serpapi.com/search` |
| `garimpo_fase1_20260714.log` | 29 | idem |
| `garimpo_fase1_20260715.log` | 29 | idem |
| `garimpo_fase1_20260716.log` | 29 | idem — **não catalogado no incidente original** |
| `garimpo_fase1_20260717.log` | **115** (corrigido em 2026-07-18; a rodada anterior registrou 114 — recontagem por classificação de cada match: 115 valores reais, 0 falsos positivos) | idem — **não catalogado no incidente original** |
| `garimpo_fase1_20260718.log` | 0 reais (a única ocorrência estrutural é o próprio marcador `[REDACTED]` — ou seja, o filtro de redação **interceptou** um vazamento em produção; a explicação anterior, "falso positivo polygon-ecosystem-token", foi corrigida em 2026-07-18 por classificação do valor do match) | — |

> **Varredura ampliada (2026-07-18, rodada de evolução final do previsao-cripto):**
> todos os logs NUNCA catalogados foram escaneados pela primeira vez com o mesmo
> método sanitizado (contagem/classificação, nunca o valor): `garimpo.log`
> (era pré-DPL, parado em 30/06), `cron_*.log` (ColetaDiaria 18:00, até 11/07),
> `v3_daily_*.log`, `watchdog.log`, `logs/operations/*.log` e os 3 JSONL de
> eventos (`events.jsonl`, `data/v3/events_v3.jsonl`, `logs/operations/events.jsonl`)
> — **0 segredos reais em todos**. O log do runner
> (`logs/operations/GarimpoFase1.log`, 15→18/07) tem 144 matches estruturais,
> **todos com valor `[REDACTED]`** — evidência adicional de que a redação do
> `operational_runner` funciona em produção. O escopo do incidente permanece
> exatamente os 5 logs da tabela acima (total corrigido: **231** ocorrências
> reais, não 230).

**Total real: 5 logs afetados** (13, 14, 15, 16, 17/07), não 3 como
catalogado originalmente. O log de 18/07 é o primeiro genuinamente limpo.

## 3. Causa raiz identificada

A chave da SerpAPI é passada como parâmetro de query (`api_key=...`) em
`previsao-cripto/GarimpoInvestimentos/collectors/serpapi_news.py:20`. Quando
uma chamada falha (rate limit, erro transitório), a exceção do `httpx`
inclui a URL completa — incluindo o `api_key` — na sua representação em
string. Antes da correção (commit `737d97d`, 2026-07-17), essa exceção
chegava a `log.warning(...)` em `scripts/garimpo_fase1.py` (dentro de
`analyze_pending()`) sem nenhuma redação, e o arquivo de log correspondente
gravava o valor em texto plano.

## 4. Correção de código já aplicada (antes desta rodada, verificada nesta rodada)

- Commit `737d97d` (2026-07-17): introduziu `_RedactSecrets`, um
  `logging.Filter` que aplica `tools.secret_redaction.safe_redact_text` a
  toda mensagem de log antes de persistir, anexado a todos os handlers do
  logger raiz em `_setup_logging()`.
- Commit `8055667` (2026-07-17): refatorou para usar exclusivamente a
  implementação canônica de `tools/secret_redaction.py` (sem regex/lista
  própria duplicada).
- Este mecanismo já existia antes desta rodada de remediação — não foi
  criado agora. O que esta rodada fez foi **verificá-lo empiricamente**.

## 5. Verificação empírica desta rodada (sem tocar segredo real)

Reproduzi o caminho de código exato (`_RedactSecrets`, `log.warning` com a
mesma assinatura usada em `analyze_pending()`) com uma **chave sintética
fictícia** (`sk-FAKE-SECRET-TESTE-9988776655`, nunca usada em nenhum sistema
real) simulando uma mensagem de exceção do `httpx` com a URL da SerpAPI.
Resultado: a chave fictícia **não aparece** no arquivo de log produzido;
`[REDACTED]` aparece no lugar. Isso confirma que o mecanismo de redação
atual funciona corretamente para exatamente este cenário.

**Confirmação adicional**: a tarefa agendada `GarimpoFase1` rodou às
2026-07-17 22:00 local (execução mais recente antes desta verificação,
`LastTaskResult=0`, sucesso) — produzindo `garimpo_fase1_20260718.log`
(UTC), que está confirmado limpo (0 ocorrências reais). Isto é evidência
de produção real, não só de teste sintético: **o primeiro ciclo agendado
real após a correção já não vazou o segredo.**

Testes de regressão já existentes e reexecutados nesta rodada (todos
passam, `previsao-cripto/tests/test_ops_hardening.py`, 22 testes, incluindo
`test_redact_filter_url_com_query_param_sensivel` e um teste específico
para `serpapi.com`) — usam exclusivamente valores sintéticos, nunca a
credencial real.

## 6. Método de verificação — nenhum valor exposto

Toda verificação usou exclusivamente:
- `stat`/`ls -la` para tamanho e timestamp dos 3→5 arquivos afetados (nunca
  o conteúdo).
- `git check-ignore`/`git ls-files` para confirmar que nenhum dos logs
  jamais entrou no histórico do Git (não rastreados, sempre gitignored —
  **o segredo nunca esteve em nenhum commit**).
- `tools.secret_redaction.scan_path()` sem lista de valores conhecidos —
  só detecção estrutural (nome do campo: `api_key`; host da URL:
  `serpapi.com/search`; contagem de ocorrências) — a função nunca retorna
  o valor capturado, só contagem e categoria.
- Extração manual, restrita a `match.group('key')` (nome do campo, nunca
  `match.group('value')`) e a `urlsplit(...).scheme/netloc/path` (nunca
  `.query`) — confirmando que apenas metadados estruturais foram
  observados em qualquer momento desta investigação.
- Reprodução com credencial 100% sintética/fictícia para testar o
  mecanismo de redação — nunca a credencial real.

## 7. O que está resolvido localmente

- [x] Prevenção de vazamento NOVO: confirmada funcionando (código +
      execução real).
- [x] Testes de regressão com valores sintéticos: já existiam, reexecutados
      e verdes.
- [x] Escopo do incidente reconciliado: 5 logs, não 3 (corrigido nesta
      rodada).
- [x] Nenhum dos logs afetados jamais entrou no Git (confirmado).
- [x] Nenhum novo vazamento detectado desde a correção (log de 18/07
      limpo, confirmado por execução real de produção).

## 8. Ações humanas obrigatórias — checklist objetivo

Nada abaixo pode ser feito por código ou por mim. `SECURITY_INCIDENT_STATUS`
permanece `BLOCKED_PENDING_SECRET_ROTATION` até que TODOS os itens estejam
marcados por você (ou por quem tiver acesso ao provedor):

- [ ] **1. Revogar/rotacionar a chave da SerpAPI** diretamente no painel do
      provedor (serpapi.com).
- [ ] **2. Confirmar que a credencial antiga não funciona mais** (uma
      chamada de teste com a chave antiga deve falhar com 401/403).
- [ ] **3. Configurar a credencial nova** através do mecanismo já usado pelo
      projeto (variável de ambiente / arquivo de configuração local
      ignorado pelo Git — `previsao-cripto/GarimpoInvestimentos/config.py`
      já lê `SERP_API_KEY` de lá; não hardcode em nenhum arquivo rastreado).
- [ ] **4. Rodar um ciclo real** de `GarimpoFase1` com a credencial nova e
      confirmar exit 0 (já será o ciclo natural de 2026-07-18 22:00, ou
      dispare manualmente se preferir confirmar antes).
- [ ] **5. Decidir o destino dos 5 logs históricos**
      (`garimpo_fase1_20260713.log` a `_17.log`): opções, na ordem de menor
      para maior perda de informação —
      (a) manter como estão (já são gitignored, nunca entraram no Git, e o
          risco real é só quem tiver acesso ao filesystem local — depois da
          rotação do item 1, o valor neles se torna inofensivo, uma chave
          revogada);
      (b) sanitizar in-place usando `python -m tools.secret_redaction
          sanitize <arquivo> --replace --confirm-replace` (a ferramenta já
          existe, testada, nunca imprime o valor);
      (c) remover os 5 arquivos.
      **Recomendação**: (a) é suficiente e mais simples assim que o item 1
      estiver feito — a chave antiga se torna um segredo revogado, não mais
      um segredo válido. Só faça (b)/(c) se política de retenção de dados
      exigir.
- [ ] **6. Registrar aqui** (editar este arquivo, ou anotar em outro lugar
      de sua escolha) a data, quem executou e qual evidência confirma que
      os itens 1-5 foram concluídos.

## 9. Critério de encerramento

Este incidente só pode ser marcado `RESOLVED` quando os 6 itens da seção 8
estiverem marcados, com evidência (mesmo que só a sua palavra registrada
aqui — não preciso ver a credencial, só a confirmação de que a rotação
aconteceu). Até lá, todo veredito de qualquer relatório deste ecossistema
que envolva `previsao-cripto` deve citar este estado explicitamente, nunca
como "resolvido" ou "dívida técnica menor".
