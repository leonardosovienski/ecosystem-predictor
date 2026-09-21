# Relatório final de validação — CAIN ↔ CRIPTO

Estado final: `TARGET_STACK_READY=YES`, `GLOBAL_ECOSYSTEM_HEALTH=DEGRADED`, sem capital real, publicação ou alteração de runtime/dados canônicos.

## Correções da releitura integral

A releitura revogou o YES anterior até fechar cinco lacunas comprovadas:

1. O segredo HMAC estava em SQLite. Agora o SQLite guarda somente metadados e fingerprint; os bytes ficam em cofre de arquivos protegido por ACL, com integridade, rotação, revogação, backup e restore. Um schema legado com coluna `secret` falha fechado.
2. O journal confundia experimento lógico e tentativa física. Agora `experiment_id`, `attempt_id` e `ops_run_id` são identidades distintas.
3. A materialização não tinha recibo causal completo. `ReferenceMaterializationReceiptV1` preserva hash esperado/observado, resolver e versão, identidade CAS, destino, instante e verificação.
4. O resultado não provava handler/journal/materialização. O contrato agora exige essas identidades.
5. O CAIN armazenava resultados, mas não fechava sessão → recuperação → nova proposta. Agora há sessões autorizadas, busca multidimensional, recibos duráveis e teste A negativo → sessão fechada → B usa A → C contradiz A sem apagá-lo.

Os recibos F6–F10 antigos, contraditórios, foram preservados em `ARCHIVE/pre-compliance-reaudit-20260920` e substituídos por recibos com falha → causa → correção → reteste.

## Stack efetivamente testado

- CAIN `5fe340a41809ddbe3f0dc795c7d9eb258014eaa6`, `0.4.13rc4`
- CRIPTO `002ed71d36c631955072c1f52a0dd00097a78b30`, `1.1.1rc4`
- ECOSYSTEM `869f4d1d22191d4a62f51fe94e72b323fed8e7fc`
- protocolo `1.0.3rc1`
- CORE `3.2.1` e OPS `4.2.1`, bytes publicados pinados
- conjunto de artifacts: `4e8aae6f4b1068e9b9365afed2dbece3bbe698cb80412b969634847beef5cd47`

O arquivo `STACK_MANIFEST.json` contém hashes individuais.

## Evidência executada

- ECOSYSTEM: 186 testes; protocolo isolado: 26.
- CAIN: 920 passaram, 2 ignorados.
- CRIPTO: 1580 passaram, 7 ignorados.
- Ruff: PASS nos três repositórios.
- Pyright: PASS completo no CRIPTO, 0 erros/0 warnings.
- Duas construções a partir de worktrees destacadas e limpas: hashes idênticos.
- Venv nova, wheels exatas, `pip check`: PASS.
- Subconjunto instalado sem importar os fontes: 69 testes PASS.
- A primeira repetição desse subconjunto usou um TEMP cujo caminho ultrapassou o limite Win32 e falhou antes de criar dois arquivos temporários. O harness foi corrigido para um TEMP curto e vazio; a repetição completa passou 69/69. Isso está registrado, não omitido.
- Integridade histórica: comparação lógica anterior 4/4 continua aplicável; esta remediação alterou apenas source, testes, workflow e relatórios, nunca bases canônicas.

## Segurança e isolamento

PASS para autenticidade de task/result, publisher desconhecido/revogado, scope incorreto, rotação/revogação, segredo fora de SQLite/receipts/logs/manifest, conflito idempotente, referência mutada, symlink/junction boundary, artifact substituído, cross-identity, cross-scope, IDs coincidentes e egress negado por provider/classificação/revogação/segredo.

O backup do cofre contém material secreto apenas como backup protegido; não é artifact publicado nem evidence artifact. Seu manifest contém somente hashes.

## Ciência, operação e economia

O resultado mantém três taxonomias. `SUCCEEDED` não vira `SUPPORTED`; suporte não vira edge; edge não autoriza capital. O E2E usa handler local fechado, CORE real, OPS real, baseline e custos. CAIN continua `PROPOSE_ONLY`; admission pertence a CRIPTO/operador.

`EXACTLY_ONCE_LOGICAL_EFFECT` é confirmado somente para os crash windows testados, via entrega pelo menos uma vez, identidade estável, hash canônico, dedupe durável, journal recuperável, outbox replay-safe e reconciliador. Não há alegação de exactly-once físico.

## Gates e limites

Todos os 50 itens finais estão em PASS no `FINAL_STATE.json`. Não existe finding aberto com `blocking_scope=TARGET_STACK`.

O único finding aberto é execução hospedada do workflow, `blocking_scope=NONE`: os commits estão apenas na `main` local porque não houve autorização de push/publicação. O workflow contém os SHAs, versões, hashes, regressões, Pyright, rollback e cleanroom exatos, e seu equivalente local passou.

Nada foi enviado a broker/exchange; nenhuma chave privada, credencial de broker, ordem ou permissão de capital foi usada.
