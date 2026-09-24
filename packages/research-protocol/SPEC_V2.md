# Envelope V2 — `ResearchTaskV2` / `ResearchResultV2`

Especificação da preparação do envelope V2 (`prompts/prompt_preparacao_envelope_v2_rev8.md`), derivada dos três
`DOMAIN_RESEARCH_CONTRACT.json` da Etapa A (C24). Implementação de referência: `research_protocol.v2`
(stdlib pura) neste pacote, `predictor-research-protocol` **2.0.0rc1**. JSON Schemas:
`src/research_protocol/v2/data/research-task-2.schema.json` e `research-result-2.schema.json`. Registro dos
domínios: `src/research_protocol/v2/data/domains.json`, gerado por `tools/build_v2_domain_registry.py`.

Normativo: este texto + `research_protocol.v2.validate_task` / `validate_result`. Os JSON Schemas descrevem só a
estrutura; as regras cruzadas (hash, derivação de IDs, correlação, schema do domínio) estão no código e nos testes.

## 1. Papel e limites

O envelope leva um pedido do CAIN até um domínio e traz de volta o que o domínio respondeu. Ele **não**:

- escolhe handler, budget, prioridade final, recurso ou capital (isso é da `admission_policy` do domínio);
- interpreta, traduz ou promove os estados operacional, científico e econômico (copia os estados como vieram);
- recalcula ou re-serializa o resultado do domínio (carrega os bytes exatos);
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

## 3. `ResearchTaskV2` (`schema = "research-task/2"`)

| Campo | Regra |
|---|---|
| `schema` | `"research-task/2"`; qualquer outro valor → `VERSION_UNSUPPORTED` |
| `domain` | `crypto` \| `brasileirao` \| `stocks` (o `domain_prefix` do contrato); outro → `DOMAIN_UNKNOWN` |
| `task_id` | `<domain>:TASK-<32 hex>` = `sha256(canonical({domain, payload_sha256, request_id}))[:32]`; divergente → `TASK_ID_MISMATCH` |
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

## 4. `ResearchResultV2` (`schema = "research-result/2"`)

| Campo | Regra |
|---|---|
| `schema` | `"research-result/2"` |
| `domain`, `task_id`, `request_id`, `research_id`, `hypothesis_id` | da task; com a task em mãos, domínio diferente → `DOMAIN_MISMATCH`, task diferente → `TASK_MISMATCH`, ID diferente → `CORRELATION_MISMATCH` |
| `outcome.status` | um dos status que **aquele** domínio declara (tabela da seção 9); outro → `OUTCOME_INVALID` |
| `outcome.exit_code` | o exit code do domínio para o status; divergente → `OUTCOME_INVALID` |
| `outcome.reason` | o `reason` do domínio (≤ 300 caracteres) ou `null` |
| `client_ref` | o eco do domínio. Tem de ser o `client_ref` da task; `null` só em `REJECTED`, quando o domínio recusou o pedido antes de interpretá-lo |
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

## 5. Classes de outcome

A decisão é sempre do domínio; o envelope só classifica o status para quem consome:

| Classe | Status | Tratamento esperado |
|---|---|---|
| `TERMINAL_RESULT` | `RESULT`, `DUPLICATE` | resultado autoritativo; `DUPLICATE` = o mesmo resultado, sem segundo efeito |
| `TERMINAL_REFUSAL` | `REJECTED`, `CONFLICT`, `TEMPORAL_INTEGRITY_VIOLATION` | não repetir a mesma task |
| `RETRYABLE` | `NOT_READY`, `OPS_FAILED_RETRYABLE`, `STATE_BUSY_RETRYABLE`¹, `STORAGE_FAILED_RETRYABLE`¹ | a mesma task pode ser reenviada (mesmos bytes) |
| `REQUIRES_HUMAN` | `RECONCILIATION_REQUIRED` | parar e registrar; nunca reparar em silêncio |

¹ só o `stocks` declara.

## 6. Idempotência, restart e releitura

- A chave de idempotência continua sendo a do domínio (`request_id`, conteúdo sem `client_ref`). `task_id` é
  derivado de `(domain, request_id, payload_sha256)`: reenviar a mesma task gera os mesmos bytes, o domínio
  responde `DUPLICATE` com o mesmo resultado e o envelope tem o mesmo payload. O mesmo `request_id` com outro
  conteúdo gera outro `task_id`, e o domínio responde `CONFLICT`.
- Depois de um restart, o adapter **reenvia a mesma task** pelo `adapter_api` em vez de montar o V2 a partir de
  `Circuit.show`: o `show` não ecoa `client_ref`. O domínio devolve `DUPLICATE` (resultado já existia) ou conclui
  a execução pendente. `show` serve para conferir: `payload_sha256 == show().result_sha256`.

## 7. IDs (C18)

- Todo ID que atravessa o envelope tem o prefixo do domínio: `crypto:`, `brasileirao:`, `stocks:`. O CAIN usa
  `cain:` só em `proposal_id`.
- O casamento de padrões é integral. O `$` final de um `pattern` segue ECMA-262 e nunca aceita `\n` no fim:
  `crypto:H9\n` é recusado. O `jsonschema` do Python aceita esse caso, por isso o validador normativo é o do pacote.
- `crypto:H9`, `brasileirao:H9` e `stocks:H9` geram tasks distintas. Um ID sem domínio é rejeitado
  (`ID_NOT_QUALIFIED`), e um ID de outro domínio também (`DOMAIN_MISMATCH`).

## 8. Adapters e `adapter_paths` (D-12, C24.1, C24.3)

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

## 9. Mapeamento V2 ↔ contrato por domínio

O payload da task **é** o pedido do contrato, e o payload do resultado **é** o resultado do contrato, em bytes
exatos. Todo campo obrigatório é representável sem perda por construção. As tabelas abaixo mostram onde cada
campo obrigatório aparece e quais campos o cabeçalho repete (sempre conferidos contra o payload).

<!-- MAPPING:BEGIN (gerado por tools/render_v2_mapping.py; não editar à mão) -->

Fonte: `predictor-qualification@cb28674f21f416724ea33cf2f5db7e6f70962b0e`.

#### `brasileirao`

- Contrato: `qualification/brasileirao/DOMAIN_RESEARCH_CONTRACT.json`, sha256 `e6f98ca28e50555f57c65adb030cc90ea9141249daebe44a333ca69970b1d824`
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

## 10. Códigos de rejeição

`SCHEMA_INVALID`, `UNKNOWN_FIELD`, `VERSION_UNSUPPORTED`, `NON_CANONICAL`, `FLOAT_FORBIDDEN`, `SIZE_LIMIT`,
`DOMAIN_UNKNOWN`, `DOMAIN_MISMATCH`, `ID_NOT_QUALIFIED`, `PAYLOAD_SCHEMA_MISMATCH`, `PAYLOAD_INVALID`,
`PAYLOAD_HASH_MISMATCH`, `CLIENT_REF_RESERVED`, `CLIENT_REF_MISMATCH`, `TASK_ID_MISMATCH`, `TASK_MISMATCH`,
`CORRELATION_MISMATCH`, `OUTCOME_INVALID`, `CAPITAL_FORBIDDEN`. Toda rejeição é uma exceção `V2Error` com
`code`. Não há caminho de fallback.

## 11. Fora desta especificação (Etapa B)

Transporte (spool local no `ecosystem-predictor`), consumidor por domínio, `TaskOutbox`/`ResultInbox` V2 do CAIN,
memória, retrieval, DecisionPolicy e `decision-receipt`. O pacote do protocolo é consumido da release congelada
(`ENVELOPE_V2_FREEZE.json`) e não muda na Etapa B.

## 12. Versão

`predictor-research-protocol` 2.0.0rc1: acrescenta `research_protocol.v2`; o módulo V1 fica sem mudança. Mudar
esta especificação depois do congelamento = C14 (`cain`, `ecosystem-predictor` ou envelope V2).
