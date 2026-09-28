# predictor-research-transport

Transporte local do envelope V2 da Etapa B (`research_protocol.v2`, release congelada 2.0.0rc2): um spool de
arquivos write-once por domínio e um consumidor por domínio que entrega cada `ResearchTaskV2` ao adapter do
domínio e devolve o `ResearchResultV2`.

```text
CAIN (TaskOutbox) → <spool>/<domínio>/tasks/TASK-*.json
predictor-research-consumer → adapter do domínio (adapter_paths, pelo nome do módulo) → adapter_api
                           → <spool>/<domínio>/results/TASK-*.<sha16>.json → CAIN (ResultInbox)
```

- **Spool** (`research_transport.spool.Spool`): publicação atômica (arquivo temporário + `os.link`), nunca
  sobrescreve; os mesmos bytes são no-op e bytes diferentes com o mesmo nome são `SpoolConflict`.
- **Consumidor** (`predictor-research-consumer`): valida a task (fail closed), confere que o domínio recebeu
  exatamente `request_bytes(task)`, embala o outcome com o `build_result` normativo e confere que o payload é
  byte a byte o da releitura autoritativa do domínio (`show`). Uma task interrompida é reenviada pelo `adapter_api`
  (o domínio responde `DUPLICATE`); uma `RETRYABLE` só é reenviada quando o CAIN pede
  (`<spool>/<domínio>/retries/`).
- **Adapters**: allowlist fixa em `research_transport.adapters.ADAPTERS` (hoje `crypto →
  GarimpoInvestimentos.adapters.research_v2`, `stocks → stocks_predictor.adapters.research_v2` e
  `brasileirao → brasileirao_predictor.adapters.research_v2`). O domínio não ganha console script nem dependência deste pacote
  (SPEC V2 §9).

O transporte não escolhe handler, budget, prioridade nem capital e não interpreta os estados do domínio.
Falhas de qualificação na borda: `PREDICTOR_RESEARCH_TRANSPORT_FAULT=<ponto>` (sem a variável, inativo).
