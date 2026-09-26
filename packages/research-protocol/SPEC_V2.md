# Envelope V2 — `ResearchTaskV2` / `ResearchResultV2`

Especificação da preparação do envelope V2 (`prompts/prompt_preparacao_envelope_v2_rev8.md`), derivada dos três
`DOMAIN_RESEARCH_CONTRACT.json` da Etapa A (C24) e feita para servir às **três orquestrações de pesquisa** da
Etapa B (D-22, `prompts/prompt_etapa_b_comum_rev9.md`): `integration-crypto`, `integration-stocks` e
`integration-brasileirao`. Implementação de referência: `research_protocol.v2` (stdlib pura) neste pacote,
`predictor-research-protocol` **2.0.0rc2**. JSON Schemas: `src/research_protocol/v2/data/research-task-2.schema.json`
e `research-result-2.schema.json`. Registro dos domínios: `src/research_protocol/v2/data/domains.json`, gerado por
`tools/build_v2_domain_registry.py` a partir dos contratos no `main` do `predictor-qualification`.

Normativo: este texto + `research_protocol.v2.validate_task` / `validate_result`. Os JSON Schemas descrevem só a
estrutura; as regras cruzadas (hash, derivação de IDs, domínio de cada ID, correlação, schema do domínio) estão no
código e nos testes.

## 1. Papel e limites

O envelope leva um pedido do CAIN até um domínio e traz de volta o que o domínio respondeu. Ele **não**:

- escolhe handler, budget, prioridade final, recurso ou capital (isso é da `admission_policy` do domínio);
- interpreta, traduz ou promove os estados operacional, científico e econômico (copia os estados como vieram);
- recalcula ou re-serializa o resultado do domínio (carrega os bytes exatos);
- decide nada do CAIN: a DecisionPolicy, a memória e a numeração dos episódios são do CAIN; o envelope só carrega
  e confere a correlação;
- autentica o transporte. Autenticação (HMAC) **não é requisito** nesta qualificação, porque tudo roda local.
  O envelope V1 autenticado (`research_protocol`, `ResearchTaskV1`) continua no pacote sem mudança, mas é
  histórico (D-13) e não é usado pela V2.

## 2. Serialização canônica

- JSON UTF-8, chaves ordenadas, sem espaços (`separators=(",", ":")`), `ensure_ascii=False`, sem NaN/Infinity.
  É a mesma forma canônica dos três domínios (`research_contract.canonical`).
- No envelope (fora do payload do resultado), **números de ponto flutuante são proibidos** (`FLOAT_FORBIDDEN`).
  Os três `request_schema` só têm inteiros e strings.
- Entrada que não é canônica é rejeitada (`NON_CANONICAL`), assim como chave duplicada, JSON inválido ou
  não UTF-8 (`SCHEMA_INVALID`). Por isso, serializar de novo um envelope aceito devolve os mesmos bytes.

## 3. Três orquestrações, um envelope (D-22)

A Etapa B é uma orquestração de pesquisa **por domínio** sobre o mesmo ecossistema. O envelope é o mesmo para as três,
e cada task e cada resultado pertencem a **um** domínio:

- **`domain` é obrigatório** (`crypto` | `brasileirao` | `stocks`, o `domain_prefix` do contrato). Todo ID que o
  envelope carrega tem o prefixo desse domínio: `task_id`, `episode_id`, `previous_task_id`, cada item de
  `based_on`, `request_id`, `research_id`, `hypothesis_id` e os IDs do resultado. ID de outro domínio →
  `DOMAIN_MISMATCH`; ID sem domínio → `ID_NOT_QUALIFIED` (C18). Só `proposal_id` é do CAIN (`cain:`).
- **Episódio.** Cada ciclo proposta → task → resultado → decisão é um episódio numerado **por domínio**. O
  `<domínio>/episode-<n>` do prompt da Etapa B circula no envelope na forma do C18:
  `episode_id = "<domínio>:episode-<n>"`, com `n` inteiro ≥ 1, decimal, sem zero à esquerda (`episode_id_for`,
  `episode_number`). O CAIN atribui o número; o envelope confere a forma e o domínio (`EPISODE_INVALID`,
  `DOMAIN_MISMATCH`). A task carrega o `episode_id`, e o resultado o devolve igual (com a task em mãos, outro
  episódio → `CORRELATION_MISMATCH`).
- **Encadeamento dos episódios de um domínio**, reconstruível só com os envelopes do log:
  - ordem: `episode_number(episode_id)`;
  - elo: `previous_task_id` = `task_id` da task do episódio anterior **do mesmo domínio** que emitiu task, ou `null`
    na primeira task do domínio. Episódios que não emitem task (decisão `BLOCK`, `ABSTAIN`, `DUPLICATE`,
    `COOLDOWN` ou `REQUIRE_HUMAN`) ficam só no log do CAIN, com o receipt; por isso o elo aponta para a última task,
    não para `n − 1`. O elo não é redundante com a ordem: como um número de episódio sem task é legítimo, só pela
    ordem uma task perdida no log ficaria igual a um episódio sem task; com o elo, a task seguinte aponta para uma
    task que falta e a lacuna aparece;
  - evidência: `based_on` lista os IDs **do mesmo domínio** que a decisão usou (por exemplo, o `result_id` do
    episódio anterior);
  - linha de pesquisa: `research_id` (do pedido do contrato) agrupa episódios da mesma pesquisa dentro do domínio.
- **O que o envelope confere e o que fica para o consumidor.** O envelope confere forma, domínio e que
  `previous_task_id` não aponta para a própria task. O CAIN (`CAIN_INGESTION`) confere o resto contra o próprio
  outbox do domínio: `previous_task_id` existe e tem episódio menor; um episódio tem uma task só; todo resultado
  corresponde a uma task existente do mesmo domínio e do mesmo episódio.
- **Isolamento.** Um resultado de um domínio nunca satisfaz a task de outro, mesmo com o mesmo número de episódio e
  os mesmos IDs locais (`crypto:H9`, `stocks:H9`, `brasileirao:H9`): `DOMAIN_MISMATCH`. As fixtures V2 congeladas dos
  domínios ainda não integrados (isolamento, C9) são montadas com `build_task`/`build_result` a partir dos vetores
  da Etapa A deles e validadas pelo mesmo código.
- **Fora do envelope.** Aprendizado entre domínios, índice global de experimentos, memória metodológica
  cross-domain e capital não passam pelo envelope (Etapa B comum, seção 2).

## 4. `ResearchTaskV2` (`schema = "research-task/2"`)

| Campo | Regra |
|---|---|
| `schema` | `"research-task/2"`; qualquer outro valor → `VERSION_UNSUPPORTED` |
| `domain` | `crypto` \| `brasileirao` \| `stocks` (o `domain_prefix` do contrato); outro → `DOMAIN_UNKNOWN` |
| `task_id` | `<domain>:TASK-<32 hex>` = `sha256(canonical({domain, episode_id, payload_sha256, request_id}))[:32]`; divergente → `TASK_ID_MISMATCH` |
| `episode_id` | `<domain>:episode-<n>` (seção 3); forma errada → `EPISODE_INVALID`; outro domínio → `DOMAIN_MISMATCH` |
| `previous_task_id` | `null` ou `<domain>:TASK-<32 hex>` da task do episódio anterior do mesmo domínio (seção 3); outro domínio → `DOMAIN_MISMATCH`; outra forma → `ID_NOT_QUALIFIED`; a própria task → `CORRELATION_MISMATCH` |
| `proposal_id` | `cain:<id>`: proposta do CAIN que originou a task |
| `based_on` | lista (≤ 64, sem repetição) de IDs **do mesmo domínio** que motivaram a proposta; ID de outro domínio → `DOMAIN_MISMATCH` |
| `request_id`, `research_id`, `hypothesis_id` | iguais aos do payload e qualificados com o domínio (C18) |
| `created_at` | UTC `YYYY-MM-DDTHH:MM:SSZ` |
| `producer` | `"cain"` |
| `payload_schema` | o `request_schema.$id` do domínio; outro → `PAYLOAD_SCHEMA_MISMATCH` |
| `payload` | o **pedido do contrato**, validado contra o `request_schema` copiado sem alteração do contrato → senão `PAYLOAD_INVALID` |
| `payload.client_ref` | sempre `{"schema": "research-client-ref/2", "task_id": <task_id>}`. O envelope é dono do `client_ref`: um pedido que já traga `client_ref` é recusado na construção (`CLIENT_REF_RESERVED`) |
| `payload_sha256` | `sha256(canonical(payload sem client_ref))` = `request_content_hash` do domínio → senão `PAYLOAD_HASH_MISMATCH` |

Campo desconhecido → `UNKNOWN_FIELD`; campo faltando → `SCHEMA_INVALID`. Tamanho: pedido ≤ 256 KiB (o limite do
entrypoint dos domínios), task ≤ 320 KiB (`SIZE_LIMIT`).

**Bytes enviados ao domínio:** `request_bytes(task) = canonical(task.payload)`. O pedido que o adapter gera tem,
portanto, o mesmo hash canônico sem `client_ref` que o vetor da Etapa A (C24.3 d), e o `client_ref` é o do envelope.
O episódio não entra no pedido: o domínio nunca vê CAIN, episódio nem transporte (`no_cain_envelope_or_transport`
dos contratos).

## 5. `ResearchResultV2` (`schema = "research-result/2"`)

| Campo | Regra |
|---|---|
| `schema` | `"research-result/2"` |
| `domain`, `task_id`, `episode_id`, `request_id`, `research_id`, `hypothesis_id` | da task; com a task em mãos, domínio diferente → `DOMAIN_MISMATCH`, task diferente → `TASK_MISMATCH`, episódio ou ID diferente → `CORRELATION_MISMATCH` |
| `outcome.status` | um dos status que **aquele** domínio declara (tabela da seção 10); outro → `OUTCOME_INVALID` |
| `outcome.exit_code` | o exit code do domínio para o status; divergente → `OUTCOME_INVALID` |
| `outcome.reason` | o `reason` do domínio (≤ 300 caracteres) ou `null` |
| `client_ref` | o eco do domínio. Tem de ser o `client_ref` da task. `null` só quando o domínio respondeu **antes de ler o pedido**: `REJECTED` (pedido recusado antes da interpretação, nos três domínios) e `STATE_BUSY_RETRYABLE` (banco de estado ocupado durante a admission, só no `stocks`). Nos outros status → `CLIENT_REF_MISMATCH` |
| `result` | `null` exceto em `RESULT`/`DUPLICATE`. Nesses: `result_id`, `experiment_id`, `admission_id`, os 4 estados e `capital_permission=false`, copiados do resultado do domínio e conferidos contra ele; `payload_schema` = `result_schema.id`; `payload_canonical` = **bytes exatos** `canonical(resultado do domínio)` como string; `payload_sha256` = sha256 desses bytes |
| `produced_at` | UTC |
| `adapter` | `distribution`, `version`, `module` do adapter que produziu o envelope |

O payload do resultado vai como string, e não como objeto, porque os resultados dos domínios têm números de
ponto flutuante: carregar a string canônica garante que o payload no V2 é **byte-idêntico** ao do `adapter_api`
(C24.3 d) e que `payload_sha256` é igual ao `result_sha256` de `Circuit.show` (fonte autoritativa). O validador
confere que a string é a forma canônica do domínio (`NON_CANONICAL`), que os campos são exatamente os de
`result_schema.top_level` do contrato, que os estados estão nos enums do contrato (`PAYLOAD_INVALID`), que os IDs
têm o prefixo do domínio e que `capital_permission` é `false` no cabeçalho e no payload (`CAPITAL_FORBIDDEN`).

Tamanho: resultado ≤ 32 MiB (`SIZE_LIMIT`).

## 6. Classes de outcome

A decisão é sempre do domínio; o envelope só classifica o status para quem consome:

| Classe | Status | Tratamento esperado |
|---|---|---|
| `TERMINAL_RESULT` | `RESULT`, `DUPLICATE` | resultado autoritativo; `DUPLICATE` = o mesmo resultado, sem segundo efeito |
| `TERMINAL_REFUSAL` | `REJECTED`, `CONFLICT`, `TEMPORAL_INTEGRITY_VIOLATION` | não repetir a mesma task |
| `RETRYABLE` | `NOT_READY`, `OPS_FAILED_RETRYABLE`, `STATE_BUSY_RETRYABLE`¹, `STORAGE_FAILED_RETRYABLE`¹ | a mesma task pode ser reenviada (mesmos bytes) |
| `REQUIRES_HUMAN` | `RECONCILIATION_REQUIRED` | parar e registrar; nunca reparar em silêncio |

¹ só o `stocks` declara.

## 7. Idempotência, restart e releitura

- A chave de idempotência continua sendo a do domínio (`request_id`, conteúdo sem `client_ref`). O `task_id` é
  derivado de `(domain, episode_id, request_id, payload_sha256)`: uma task por episódio e conteúdo de pedido.
- **Reenvio no mesmo episódio** (retry, restart, entrega duplicada): o CAIN guarda os bytes da task no outbox e
  reenvia **os mesmos bytes**. O domínio responde `DUPLICATE` com o mesmo resultado, e o envelope tem o mesmo payload.
  `proposal_id`, `based_on`, `previous_task_id` e `created_at` ficam fixos quando a task é criada: o mesmo `task_id`
  com outros bytes é conflito no outbox, nunca uma task nova.
- **O mesmo pedido num episódio posterior** gera outro `task_id` (e outro `client_ref`), mas o domínio vê o mesmo
  `request_id` com o mesmo conteúdo e responde `DUPLICATE` com o mesmo `result_id`: nenhum segundo experimento,
  efeito ou resultado. Normalmente a DecisionPolicy já o teria barrado como `DUPLICATE` antes de emitir a task.
- O mesmo `request_id` com outro conteúdo gera outro `task_id`, e o domínio responde `CONFLICT`.
- Depois de um restart, o adapter **reenvia a mesma task** pelo `adapter_api` em vez de montar o V2 a partir de
  `Circuit.show`: o `show` não ecoa `client_ref`. O domínio devolve `DUPLICATE` (resultado já existia) ou conclui
  a execução pendente. `show` serve para conferir: `payload_sha256 == show().result_sha256`.

## 8. IDs (C18)

- Todo ID que atravessa o envelope tem o prefixo do domínio: `crypto:`, `brasileirao:`, `stocks:`. O CAIN usa
  `cain:` só em `proposal_id`.
- O casamento de padrões é integral. O `$` final de um `pattern` segue ECMA-262 e nunca aceita `\n` no fim:
  `crypto:H9\n` é recusado. O `jsonschema` do Python aceita esse caso, por isso o validador normativo é o do pacote.
- `crypto:H9`, `brasileirao:H9` e `stocks:H9` geram tasks distintas, e `crypto:episode-7`, `stocks:episode-7` e
  `brasileirao:episode-7` são episódios distintos. Um ID sem domínio é rejeitado (`ID_NOT_QUALIFIED`), e um ID de
  outro domínio também (`DOMAIN_MISMATCH`).

## 9. Adapters e `adapter_paths` (D-12, C24.1, C24.3)

- O adapter de cada domínio fica **só** em `adapter_paths` (`GarimpoInvestimentos/adapters/`,
  `brasileirao_predictor/adapters/`, `stocks_predictor/adapters/`). Ele chama o domínio só pelo `adapter_api`:
  `Circuit(state, policy, objects).submit_request(request_bytes(task), source=...)`, e `Circuit(state).show(...)`
  para conferência.
- **Sem console script novo no domínio.** O teste congelado de cada domínio
  `tests/conformance/test_import_closure.py::test_no_entrypoint_reaches_envelope_cain_or_adapter_paths` percorre
  **todos** os `console_scripts` da distribuição. Um `*-research-adapter` apontando para `adapters/` alcançaria
  `adapters/` e `research_protocol` e quebraria a suíte de conformidade congelada, o que viola o C24.3 (c).
  Isso vale para o cripto e o brasileirão, cujos contratos permitem criar esse script; o stocks não permite
  nenhum. Por isso, na Etapa B o adapter é carregado **pelo nome do módulo** pelo consumidor do transporte
  (ecosystem), sem entry point novo no domínio. É um desvio do que o contrato *permite*, não do que ele *exige*:
  nenhum domínio muda fora de `adapter_paths`.
- A dependência do domínio em `predictor-research-protocol` (para o adapter) é a exceção prevista no C24.3 (a):
  `pyproject`/`uv.lock`, sem mudança de código fora de `adapter_paths`.
- Nenhuma parte desta especificação exige mudança num domínio fora de `adapter_paths`.

## 10. Mapeamento V2 ↔ contrato por domínio

O payload da task **é** o pedido do contrato, e o payload do resultado **é** o resultado do contrato, em bytes
exatos. Todo campo obrigatório é representável sem perda por construção. As tabelas abaixo mostram onde cada
campo obrigatório aparece e quais campos o cabeçalho repete (sempre conferidos contra o payload). Os campos só do
envelope (`task_id`, `episode_id`, `previous_task_id`, `proposal_id`, `based_on`, `created_at`, `producer`) não
existem no contrato e não entram no pedido.

<!-- MAPPING:BEGIN (gerado por tools/render_v2_mapping.py; não editar à mão) -->

Fonte: `predictor-qualification@ec02315a75e614e6d631dd4d852699340a91794c`.

#### `brasileirao`

- Contrato: `qualification/brasileirao/DOMAIN_RESEARCH_CONTRACT.json`, sha256 `1c75fc4507df8d48f1278e3c9475c627e8fce7cf25483395fe760e480cc752ec`
- `payload_schema` da task: `brasileirao-research-request/1` (schema copiado sem alteração)
- `payload_schema` do resultado: `brasileirao-research-result/1`
- `adapter_api`: `brasileirao_predictor.research_runtime.runner.Circuit(state, policy, objects).submit_request(raw: bytes, *, source: str) -> outcome`
- `adapter_paths`: `brasileirao_predictor/adapters/`

| Campo obrigatório do pedido | Na `ResearchTaskV2` |
|---|---|
| `schema_version` | `payload.schema_version`; `payload_schema` (igual, conferido) |
| `request_id` | `payload.request_id`; `request_id` (igual, conferido) |
| `request_type` | `payload.request_type`; só no `payload` |
| `research_id` | `payload.research_id`; `research_id` (igual, conferido) |
| `hypothesis_id` | `payload.hypothesis_id`; `hypothesis_id` (igual, conferido) |
| `competition` | `payload.competition`; só no `payload` |
| `season` | `payload.season`; só no `payload` |
| `target` | `payload.target`; só no `payload` |
| `events` | `payload.events`; só no `payload` |
| `data_cutoff` | `payload.data_cutoff`; só no `payload` |
| `decision_lead_minutes` | `payload.decision_lead_minutes`; só no `payload` |
| `references` | `payload.references`; só no `payload` |
| `priority_hint` | `payload.priority_hint`; só no `payload` |
| `client_ref` (opcional no contrato) | `payload.client_ref` = `{schema: research-client-ref/2, task_id}` (do envelope) |

| Campo do resultado | Na `ResearchResultV2` |
|---|---|
| `admission_id` | bytes exatos em `result.payload_canonical`; `result.admission_id` |
| `capital_permission` | bytes exatos em `result.payload_canonical`; `result.capital_permission` (sempre `false`) |
| `core_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `domain_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `economic_state` | bytes exatos em `result.payload_canonical`; `result.economic_state` |
| `experiment_id` | bytes exatos em `result.payload_canonical`; `result.experiment_id` |
| `hypothesis_id` | bytes exatos em `result.payload_canonical`; `hypothesis_id` |
| `operational_state` | bytes exatos em `result.payload_canonical`; `result.operational_state` |
| `ops_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `produced_at` | bytes exatos em `result.payload_canonical`; só no payload |
| `provenance` | bytes exatos em `result.payload_canonical`; só no payload |
| `request_id` | bytes exatos em `result.payload_canonical`; `request_id` |
| `research_id` | bytes exatos em `result.payload_canonical`; `research_id` |
| `result_id` | bytes exatos em `result.payload_canonical`; `result.result_id` |
| `result_state` | bytes exatos em `result.payload_canonical`; `result.result_state` |
| `schema_version` | bytes exatos em `result.payload_canonical`; `result.payload_schema` |
| `scientific_state` | bytes exatos em `result.payload_canonical`; `result.scientific_state` |

| Status do outcome | exit | Classe V2 |
|---|--:|---|
| `DUPLICATE` | 0 | `TERMINAL_RESULT` |
| `RESULT` | 0 | `TERMINAL_RESULT` |
| `CONFLICT` | 2 | `TERMINAL_REFUSAL` |
| `REJECTED` | 2 | `TERMINAL_REFUSAL` |
| `NOT_READY` | 3 | `RETRYABLE` |
| `OPS_FAILED_RETRYABLE` | 3 | `RETRYABLE` |
| `TEMPORAL_INTEGRITY_VIOLATION` | 4 | `TERMINAL_REFUSAL` |
| `RECONCILIATION_REQUIRED` | 5 | `REQUIRES_HUMAN` |

Estados (copiados, nunca traduzidos): `result_state` ∈ {WATCH_NO_CAPITAL, NO_EDGE, INCONCLUSIVE, REFUTED, CLOSED_INSUFFICIENT_SAMPLE, INCONCLUSIVE_DATA_QUALITY, FORECAST_ONLY, FAILED_OPERATIONAL}; `operational_state` ∈ {SUCCEEDED, FAILED, TIMEOUT, SKIPPED_ALREADY_SUCCEEDED}; `scientific_state` ∈ {SUPPORTED, REFUTED, INCONCLUSIVE, INSUFFICIENT_SAMPLE, NOT_EVALUATED}; `economic_state` ∈ {WATCH, NO_EDGE, NOT_EVALUATED}.

#### `crypto`

- Contrato: `qualification/crypto/DOMAIN_RESEARCH_CONTRACT.json`, sha256 `0831fe3db2b7ca41a26ff7665f93c07b0edda3c937ac4ce83fe0e96720a9eb55`
- `payload_schema` da task: `crypto-research-request/1` (schema copiado sem alteração)
- `payload_schema` do resultado: `crypto-research-result/1`
- `adapter_api`: `GarimpoInvestimentos.research_runner.Circuit(state, policy, objects).submit_request(raw: bytes, *, source: str) -> outcome`
- `adapter_paths`: `GarimpoInvestimentos/adapters/`

| Campo obrigatório do pedido | Na `ResearchTaskV2` |
|---|---|
| `schema_version` | `payload.schema_version`; `payload_schema` (igual, conferido) |
| `request_id` | `payload.request_id`; `request_id` (igual, conferido) |
| `request_type` | `payload.request_type`; só no `payload` |
| `research_id` | `payload.research_id`; `research_id` (igual, conferido) |
| `hypothesis_id` | `payload.hypothesis_id`; `hypothesis_id` (igual, conferido) |
| `references` | `payload.references`; só no `payload` |
| `data_cutoff` | `payload.data_cutoff`; só no `payload` |
| `parameters` | `payload.parameters`; só no `payload` |
| `priority_hint` | `payload.priority_hint`; só no `payload` |
| `client_ref` (opcional no contrato) | `payload.client_ref` = `{schema: research-client-ref/2, task_id}` (do envelope) |

| Campo do resultado | Na `ResearchResultV2` |
|---|---|
| `admission_id` | bytes exatos em `result.payload_canonical`; `result.admission_id` |
| `capital_permission` | bytes exatos em `result.payload_canonical`; `result.capital_permission` (sempre `false`) |
| `core_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `domain_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `economic_state` | bytes exatos em `result.payload_canonical`; `result.economic_state` |
| `experiment_id` | bytes exatos em `result.payload_canonical`; `result.experiment_id` |
| `hypothesis_id` | bytes exatos em `result.payload_canonical`; `hypothesis_id` |
| `operational_state` | bytes exatos em `result.payload_canonical`; `result.operational_state` |
| `ops_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `produced_at` | bytes exatos em `result.payload_canonical`; só no payload |
| `provenance` | bytes exatos em `result.payload_canonical`; só no payload |
| `request_id` | bytes exatos em `result.payload_canonical`; `request_id` |
| `research_id` | bytes exatos em `result.payload_canonical`; `research_id` |
| `result_id` | bytes exatos em `result.payload_canonical`; `result.result_id` |
| `result_state` | bytes exatos em `result.payload_canonical`; `result.result_state` |
| `schema_version` | bytes exatos em `result.payload_canonical`; `result.payload_schema` |
| `scientific_state` | bytes exatos em `result.payload_canonical`; `result.scientific_state` |

| Status do outcome | exit | Classe V2 |
|---|--:|---|
| `DUPLICATE` | 0 | `TERMINAL_RESULT` |
| `RESULT` | 0 | `TERMINAL_RESULT` |
| `CONFLICT` | 2 | `TERMINAL_REFUSAL` |
| `REJECTED` | 2 | `TERMINAL_REFUSAL` |
| `NOT_READY` | 3 | `RETRYABLE` |
| `OPS_FAILED_RETRYABLE` | 3 | `RETRYABLE` |
| `TEMPORAL_INTEGRITY_VIOLATION` | 4 | `TERMINAL_REFUSAL` |
| `RECONCILIATION_REQUIRED` | 5 | `REQUIRES_HUMAN` |

Estados (copiados, nunca traduzidos): `result_state` ∈ {WATCH_NO_CAPITAL, NO_EDGE, INCONCLUSIVE, REFUTED, CLOSED_INSUFFICIENT_SAMPLE, INCONCLUSIVE_DATA_QUALITY, FAILED_OPERATIONAL}; `operational_state` ∈ {SUCCEEDED, FAILED, TIMEOUT, SKIPPED_ALREADY_SUCCEEDED}; `scientific_state` ∈ {SUPPORTED, REFUTED, INCONCLUSIVE, INSUFFICIENT_SAMPLE, NOT_EVALUATED}; `economic_state` ∈ {WATCH, NO_EDGE, NOT_EVALUATED}.

#### `stocks`

- Contrato: `qualification/stocks/DOMAIN_RESEARCH_CONTRACT.json`, sha256 `76fa8227dd83eb9a9e74697caa73e4d61c68d207f1df5f94135c76508192d66c`
- `payload_schema` da task: `stocks-research-request/1` (schema copiado sem alteração)
- `payload_schema` do resultado: `stocks-research-result/1`
- `adapter_api`: `stocks_predictor.research_runner.Circuit(state, policy, objects).submit_request(raw: bytes, *, source: str) -> outcome`
- `adapter_paths`: `stocks_predictor/adapters/`

| Campo obrigatório do pedido | Na `ResearchTaskV2` |
|---|---|
| `schema_version` | `payload.schema_version`; `payload_schema` (igual, conferido) |
| `request_id` | `payload.request_id`; `request_id` (igual, conferido) |
| `request_type` | `payload.request_type`; só no `payload` |
| `research_id` | `payload.research_id`; `research_id` (igual, conferido) |
| `hypothesis_id` | `payload.hypothesis_id`; `hypothesis_id` (igual, conferido) |
| `references` | `payload.references`; só no `payload` |
| `as_of` | `payload.as_of`; só no `payload` |
| `pit` | `payload.pit`; só no `payload` |
| `parameters` | `payload.parameters`; só no `payload` |
| `priority_hint` | `payload.priority_hint`; só no `payload` |
| `client_ref` (opcional no contrato) | `payload.client_ref` = `{schema: research-client-ref/2, task_id}` (do envelope) |

| Campo do resultado | Na `ResearchResultV2` |
|---|---|
| `admission_id` | bytes exatos em `result.payload_canonical`; `result.admission_id` |
| `as_of` | bytes exatos em `result.payload_canonical`; só no payload |
| `capital_permission` | bytes exatos em `result.payload_canonical`; `result.capital_permission` (sempre `false`) |
| `core_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `domain_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `economic_state` | bytes exatos em `result.payload_canonical`; `result.economic_state` |
| `experiment_id` | bytes exatos em `result.payload_canonical`; `result.experiment_id` |
| `hypothesis_id` | bytes exatos em `result.payload_canonical`; `hypothesis_id` |
| `operational_state` | bytes exatos em `result.payload_canonical`; `result.operational_state` |
| `ops_facts` | bytes exatos em `result.payload_canonical`; só no payload |
| `produced_at` | bytes exatos em `result.payload_canonical`; só no payload |
| `provenance` | bytes exatos em `result.payload_canonical`; só no payload |
| `request_id` | bytes exatos em `result.payload_canonical`; `request_id` |
| `request_type` | bytes exatos em `result.payload_canonical`; só no payload |
| `research_id` | bytes exatos em `result.payload_canonical`; `research_id` |
| `result_id` | bytes exatos em `result.payload_canonical`; `result.result_id` |
| `result_state` | bytes exatos em `result.payload_canonical`; `result.result_state` |
| `schema_version` | bytes exatos em `result.payload_canonical`; `result.payload_schema` |
| `scientific_state` | bytes exatos em `result.payload_canonical`; `result.scientific_state` |
| `trial_eligible` | bytes exatos em `result.payload_canonical`; só no payload |

| Status do outcome | exit | Classe V2 |
|---|--:|---|
| `DUPLICATE` | 0 | `TERMINAL_RESULT` |
| `RESULT` | 0 | `TERMINAL_RESULT` |
| `CONFLICT` | 2 | `TERMINAL_REFUSAL` |
| `REJECTED` | 2 | `TERMINAL_REFUSAL` |
| `NOT_READY` | 3 | `RETRYABLE` |
| `OPS_FAILED_RETRYABLE` | 3 | `RETRYABLE` |
| `STATE_BUSY_RETRYABLE` | 3 | `RETRYABLE` |
| `STORAGE_FAILED_RETRYABLE` | 3 | `RETRYABLE` |
| `TEMPORAL_INTEGRITY_VIOLATION` | 4 | `TERMINAL_REFUSAL` |
| `RECONCILIATION_REQUIRED` | 5 | `REQUIRES_HUMAN` |

Estados (copiados, nunca traduzidos): `result_state` ∈ {WATCH_NO_CAPITAL, NO_EDGE, INCONCLUSIVE, REFUTED, NOT_READY, CLOSED_INSUFFICIENT_SAMPLE, INCONCLUSIVE_DATA_QUALITY, FAILED_OPERATIONAL, COLLECTION_RECORDED}; `operational_state` ∈ {SUCCEEDED, FAILED, TIMEOUT, SKIPPED_ALREADY_SUCCEEDED}; `scientific_state` ∈ {SUPPORTED, REFUTED, INCONCLUSIVE, INSUFFICIENT_SAMPLE, NOT_EVALUATED}; `economic_state` ∈ {WATCH, NO_EDGE, NOT_EVALUATED}.

<!-- MAPPING:END -->

## 11. Códigos de rejeição

`SCHEMA_INVALID`, `UNKNOWN_FIELD`, `VERSION_UNSUPPORTED`, `NON_CANONICAL`, `FLOAT_FORBIDDEN`, `SIZE_LIMIT`,
`DOMAIN_UNKNOWN`, `DOMAIN_MISMATCH`, `ID_NOT_QUALIFIED`, `EPISODE_INVALID`, `PAYLOAD_SCHEMA_MISMATCH`,
`PAYLOAD_INVALID`, `PAYLOAD_HASH_MISMATCH`, `CLIENT_REF_RESERVED`, `CLIENT_REF_MISMATCH`, `TASK_ID_MISMATCH`,
`TASK_MISMATCH`, `CORRELATION_MISMATCH`, `OUTCOME_INVALID`, `CAPITAL_FORBIDDEN`. Toda rejeição é uma exceção
`V2Error` com `code`. Não há caminho de fallback.

## 12. Fora desta especificação (Etapa B)

Transporte (spool local no `ecosystem-predictor`), consumidor por domínio, `TaskOutbox`/`ResultInbox` V2 do CAIN,
memória por domínio, numeração dos episódios, retrieval, DecisionPolicy e `decision-receipt`. O pacote do protocolo
é consumido da release congelada (`qualification/shared/ENVELOPE_V2_FREEZE.json`) e não muda na Etapa B.

## 13. Versão

`predictor-research-protocol` **2.0.0rc2** (substitui a 2.0.0rc1, que não deve ser usada na Etapa B):

1. correlação por episódio para as três orquestrações (D-22): `episode_id` e `previous_task_id` na task,
   `episode_id` no resultado, código `EPISODE_INVALID` (seção 3);
2. `task_id` derivado também do `episode_id` (seção 7);
3. `client_ref` nulo aceito também em `STATE_BUSY_RETRYABLE`: na rc1, o outcome real do `stocks` com o banco de estado
   ocupado durante a admission (sem `client_ref`, `request_id` nulo) era recusado com `CLIENT_REF_MISMATCH` e não
   tinha representação V2;
4. `domains.json` regenerado dos contratos do `main` (`ec02315`): só o sha256 do contrato do `brasileirao` mudou
   (`e6f98ca2…` → `1c75fc45…`, bloco `implementation` rc2 → rc3); schemas, estados e status idênticos.

O módulo V1 fica sem mudança. Mudar esta especificação depois do congelamento = C14 (`cain`, `ecosystem-predictor`
ou envelope V2).
