# Organização do Ecosystem — 13/09/2026

Registro de manutenção documental e classificação anterior à limpeza. O resultado
efetivo de push/PR/merge/exclusões será registrado no PR e na entrega final, sem
nova branch apenas para atualizar este registro.

## Baseline e escopo

- Repositório confirmado: `leonardosovienski/ecosystem-predictor`; default `main`.
- SHA inicial: `9d34adf7054451e20170cc714a8db9d79ac6fd99`; `C:/CAIN/contrato` limpo.
- API paginada: 25 branches (main + 24 secundárias), 24 PRs históricos, zero abertos.
- Permissão de push/admin presente; proteção clássica retorna 404, nenhum ruleset
  de repositório ou regra efetiva de main. Isso não dispensa os gates de integração.
- CI baseline [34765919043](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765919043)
  e segurança [34765919056](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/34765919056): success.
- Sem `AGENTS.md` aplicável encontrado no checkout ou seus ancestrais examinados.
- Worktree isolada: `C:/CAIN/work/ecosystem-organization-20260913`, única branch
  temporária `docs/organize-ecosystem-20260913`. Outros projetos consultados em leitura.

## Inventário e autoridade

O [índice existente](../HISTORICAL_DOCUMENT_INDEX.md) foi ampliado; não há registro
estruturado paralelo. README é a entrada, CURRENT_STATE resume o presente, charter
reconcilia sete repositórios/dez pacotes/três domínios, runbook guarda procedimentos.
Seis fichas em `docs/projects/` resumem interfaces e remetem às fontes externas.
As páginas de integração existentes mantêm suas revisões e caminhos.

As tabelas/ações de 06/09 saíram de CURRENT_STATE para `docs/archive/` com o conteúdo
original preservado. A antiga tabela de versões e observações locais do runbook
é recuperável no Git da baseline; o runbook agora aponta aos registros e ao estado
oficial da instalação. Handoffs, auditorias e ADRs antigos permanecem classificados
no índice, sem movimentação em massa nem nova autoridade sobre o presente.

## Branches classificadas antes de editar

`git merge-base --is-ancestor`, commits `main..branch`, referências no conteúdo
versionado e PRs foram examinados. Nas três branches sem ancestralidade, as árvores
das pontas são idênticas aos respectivos squashes, todos ancestrais de main.
O PR usa exatamente a ponta observada, sem commits posteriores ocultos. `git cherry`
reconhece PR4; nos PR14/15 os patches individuais aparecem exclusivos porque foram
agregados: igualdade da árvore completa com a integração comprova incorporação.
Evolução posterior (registry mínimo e snapshots históricos) não é trabalho pendente.

| Branch | SHA observado | Relação com main | PR/evidência | Conteúdo exclusivo | Decisão condicionada | Recuperação |
|---|---|---|---|---|---|---|
| `agent/ecosystem-factual-staleness-gate` | `0cc9243f19d71d1488713dc7d59314b12f6874d0` | 1 — ancestral | #11, #10, #8 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/agent/ecosystem-factual-staleness-gate` |
| `agent/modernize-ecosystem-predictor` | `e9c18bc385003401d615468e218e68c1c3574fc1` | 1 — ancestral | #3, #2, #1 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/agent/modernize-ecosystem-predictor` |
| `agent/refresh-facts-after-core-tools` | `d2c297d0be7a6615b27698b62b37639cefdb99a2` | 1 — ancestral | #12 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/agent/refresh-facts-after-core-tools` |
| `agent/tcc-evidence-closure` | `3b7f0ef180780e13c71fa405931706a982f1837b` | 1 — ancestral | #9 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/agent/tcc-evidence-closure` |
| `architecture/complete-20260911` | `f586b5d29a0b31ed7d79943efcf744345a08e6d4` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/architecture/complete-20260911` |
| `audit/stocks-integration-20260912` | `71607e7770c9979610a32cb6448e1e76d231a1d0` | 1 — ancestral | #23 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/audit/stocks-integration-20260912` |
| `audit/stocks-primary-coherence-20260912` | `e3bca911baaa9b4beaf26dd92c7a6dcf23925ba0` | 1 — ancestral | #24 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/audit/stocks-primary-coherence-20260912` |
| `claude/auditoria-projetos-esr8na` | `6e0f66f4caa693e7482e94a4c455cb590b94d77d` | 1 — ancestral | #22, #21, #20 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/claude/auditoria-projetos-esr8na` |
| `claude/predictor-ecosystem-audit-srpwl3` | `c4b5dc62455ec564c11e842186d3257253a5f3ef` | 1 — ancestral | #13 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/claude/predictor-ecosystem-audit-srpwl3` |
| `claude/projeto-funcional-investimento-taq69q` | `23d1d9ebc321821d3698385d955c8531b8d21733` | 2 — squash equivalente | PR #4; árvore igual a `a9214d69f188ab63bdbf0764a1bc28d7b0661b60` | 1 commits de história; sem conteúdo pendente | remover após integração/CI | bundle: `refs/remotes/origin/claude/projeto-funcional-investimento-taq69q` |
| `docs/f1-reconcile-ecosystem` | `6143b93dd8b4890e68f1178c1be15d2809e997f2` | 1 — ancestral | #5 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/docs/f1-reconcile-ecosystem` |
| `docs/final-reconciliation-2026-08-24` | `3658604220428201a33dfd45482b6c93fdecae4b` | 1 — ancestral | #19 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/docs/final-reconciliation-2026-08-24` |
| `docs/p4-consolidation` | `7978b462d297ae93e570611cab43a5a53931c0b9` | 1 — ancestral | #7 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/docs/p4-consolidation` |
| `docs/track-current-handoff-2026-08-24` | `e690594e51543b608bea83b2ec71228e539dfc07` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/docs/track-current-handoff-2026-08-24` |
| `feature/research-bundle-v1` | `a9f6594c840482419d6c310f373813e0e71f17d0` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/feature/research-bundle-v1` |
| `fix/p0-canonical-ecosystem` | `1bfead9c202174b62fd90ff868f1339c2d854614` | 2 — squash equivalente | PR #14; árvore igual a `f109641dc6c21a7817574fbc9e7c54e41abea532` | 5 commits de história; sem conteúdo pendente | remover após integração/CI | bundle: `refs/remotes/origin/fix/p0-canonical-ecosystem` |
| `fix/p0-mechanical-six` | `2ad0f5dfd64836f3c4ab383bf1838d9e7c68567f` | 2 — squash equivalente | PR #15; árvore igual a `22dc663c253664f20baa05cb05a5eca9c262d733` | 11 commits de história; sem conteúdo pendente | remover após integração/CI | bundle: `refs/remotes/origin/fix/p0-mechanical-six` |
| `integration/crypto-wheel-audit-20260912` | `6a998520825292895bcae71e589fa8ac0e02bb85` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/integration/crypto-wheel-audit-20260912` |
| `local/l0-contract` | `1ddc9a51ce14339559e9a57fe6a6760a2cac2e62` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/local/l0-contract` |
| `p1/canonical-predictor-contract` | `4de2cfa5cd5a7638f055b697ae718fe9db6b3322` | 1 — ancestral | #17 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/p1/canonical-predictor-contract` |
| `p1/plugin-mechanical-reconciliation` | `3ccc4a53da1fcafe961c2ef0dfe0d4849ec90609` | 1 — ancestral | #18 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/p1/plugin-mechanical-reconciliation` |
| `reconcile/stocks-modernization-20260824` | `c18c2f2b1de69ba314b45c39cf27d1c8b0b5f29e` | 1 — ancestral | #16 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/reconcile/stocks-modernization-20260824` |
| `refactor/p1-migrate-ops3` | `9400fd734f7dfd0dc878bce228ee05498734d9d4` | 1 — ancestral | #6 | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/refactor/p1-migrate-ops3` |
| `validation/retest-six-20260911` | `8c62a07255dee103cbd2bc0ad847d68c4b053cdd` | 1 — ancestral | ancestralidade direta | nenhum | remover após integração/CI | main + bundle: `refs/remotes/origin/validation/retest-six-20260911` |

As referências internas a `agent/modernize-ecosystem-predictor`,
`docs/f1-reconcile-ecosystem` e `feature/research-bundle-v1` são registros históricos
classificados no índice. Workflows atuais do Ecosystem não selecionam essas branches.
Nos seis projetos externos, os workflows atuais foram lidos no SHA remoto observado.
Referências históricas homônimas de outros repositórios não são refs do Ecosystem.
CAIN usa SHAs fixos nos workflows históricos e `base_head`/hashes em
`.ci/completion/prepare_ci.py` e `restore_candidate.py`; o campo `branch` do manifesto
é descritivo. Nenhum consumidor ativo de nome de branch Ecosystem foi identificado.
Recibos, overlays, manifests e grants examinados ficam intactos; isso não é uma
varredura de acervos privados inacessíveis.

## Recuperação verificada

Um único bundle completo: `C:/CAIN/work/ecosystem-organization-evidence-20260913/before.bundle`.
SHA256: `6360c5b88bb5094fc5c9166ea9888df5abb256a981b08df8fd5b3db10824e230`.
`git bundle verify`, restauração `git clone --mirror` e `git fsck --full` passaram;
cada ref da tabela foi resolvida no clone restaurado e comparada ao SHA esperado.
O bundle inclui também branches locais e HEADs dos worktrees existentes. Para
recuperar, clone o bundle em destino novo e crie a branch a partir da ref indicada.
Os 17 commits originais das três branches squash ficam preservados nesse bundle;
seu conteúdo já existe em main. Não foram necessárias tags de arquivo, releases
ou automações adicionais. Este é backup Git local verificado, não backup offsite
nem cópia de arquivos ignorados/bancos de outros projetos.

## Compatibilidade e validação

Somente Markdown alterado. Preservados integralmente código, scripts, testes,
workflows, dependências, pins, schemas, registries, contratos, overlays e evidências.
`docs/core_integration_20260913/receipt.json` é lido pelo job
`Core official wheel functional integration`; caminho e bytes são mantidos.
CAIN admite fontes dos produtores e contratos vendorizados; não há mudança em
permissões, instalações ou dados. A evidência do Core permanece ligada a `3cfb74b`.

Baseline local em Python 3.13.12, sem instalar runtimes dos domínios:

- `python -m pytest -q tests packages/research-bundle/tests -p no:cacheprovider`:
  141 aprovados. `PYTHONPATH` aponta apenas a `src` e aos dois contratos deste checkout.
- `python scripts/check_ecosystem_drift.py --offline-check`: PASS.
- `python scripts/sync_canonical_ecosystem_facts.py --offline-check`: PASS.
- `python scripts/check_architecture_manifest.py`: sete repos/dez pacotes e fontes
  remotas imutáveis verificados.
- `check_ecosystem_drift.check_online(GitHubSource(token))`: PASS; somente avisos de
  main posterior em Ops, Brasileirão e Cripto. Token usado em memória, sem registro.
- A primeira invocação local de pytest apontava para `packages/research-snapshot/tests`,
  que não existe; corrigida para os testes reais acima, sem alterar o repositório.
  Isso foi erro de invocação, não falha da suíte. Logs foram recapturados em UTF-8.

Após a edição, os mesmos gates passaram: 141 testes, invariantes históricas/offline,
inventário remoto e drift online. Foram verificados 164 links locais/âncoras, com
zero regressões e um erro preexistente em `FINAL_DOCUMENTATION_CLOSURE.md` apontando
para `tools/HANDOFF.md`; o documento histórico foi preservado. Os 147 arquivos
versionados fora da edição foram comparados byte a byte ao checkout canônico.
Diferenças de materialização CRLF/LF da worktree foram alinhadas aos bytes originais,
sem alterar blobs Git. O bloco histórico foi comparado ao original da baseline.
A CI existente
deve passar no candidato antes do merge e na main antes de excluir branches.
`check_real_plugin_integration.py` foi lido e será exercitado nos ambientes Linux
da CI com os manifests existentes; não foi executado num ambiente Windows parcial.
Essa validação não reexecuta experimentos científicos ou o E2E operacional do CAIN.

## Fontes externas observadas em leitura

As seguintes pontas são observações de 13/09, não atualização da combinação validada:

| Repositório | Main remota observada |
|---|---|
| `core-predictor` | `9bf43efe92459a0b484cac00f51170b2c70d420f` |
| `predictor-ops` | `b19e69527c0fda5cb1f96281d3a984fea1431768` |
| `cripto-predictor` | `4eb96e141389b8390536716af3c4a0cb46edab23` |
| `brasileirao-predictor` | `f87806900d2aa3c5e267259a67f27ce56e18dc03` |
| `stocks-predictor` | `3066321e599ee15dd0ace4167d2791545ce6eb95` |
| `cain` | `f4991a1a63eb011e2d341ddf9f5e0386479487b9` |

Resultados detalhados de baseline, consultas paginadas, referências, comparação de
bytes e recuperação estão no diretório local do bundle. As fontes correntes de
cada domínio permanecem nos links oficiais das fichas. Avanço de main não autoriza
atualizar versões/pins ou reemitir evidência nesta manutenção.
