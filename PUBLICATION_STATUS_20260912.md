# Continuidade atual — Ecosystem em main

> **Reconciliação em 13/09/2026:** inventário de dez pacotes, gate contra metadados reais, versões observadas e erratas de navegação corrigidos. Consulte a seção de 13/09 no [HANDOFF](HANDOFF.md) e o [runbook atual](ECOSYSTEM_RUNBOOK.md). Os relatos e combinações anteriores abaixo continuam datados.

> **Brasileirão — entrega consolidada em main:** [versões, integração CAIN, CI, backups e reprodução](BRASILEIRAO_INTEGRATION_20260912.md). A aprovação é técnica/documental; ciência, produção e capital conservam seus gates próprios.

O checkout canônico deste notebook é `C:\CAIN\contrato`, na branch `main`. As correções de compatibilidade estão incorporadas à main do Ecosystem. Leia [a combinação Crypto e seus recibos de CI](CRYPTO_INTEGRATION_20260912.md), [CURRENT_STATE](CURRENT_STATE.md) e os registros correntes. O histórico abaixo é uma etapa anterior, não uma indicação de branch de trabalho atual ou bloqueio vigente da combinação testada.

Para conferir publicação após novos commits: `git status --short`, `git rev-parse HEAD` e `git ls-remote origin refs/heads/main`. SHA observado, SHA certificado, release e instalação operacional são identidades distintas. A entrega Stocks mantém sua [continuidade própria](STOCKS_INTEGRATION_20260912.md), agora incluindo instalação principal e restauração offline validadas.

Checkout canônico no computador: `C:/CAIN/contrato`, branch `main`, alinhado a `origin/main`. Worktrees auxiliares e branches históricas foram preservados; eles não definem a pasta principal. O fechamento executável Stocks usou Ecosystem `dda782761c430af654b59208d3e41faf6ee7fe28`; os commits posteriores de Markdown atualizam a navegação, sem alterar os contratos ou reemitir evidências. Esta atualização documental parte de `73111a1` e não representa nova release.

Recibos locais da organização documental: `C:/CAIN/work/ecosystem-md-main-20260912`. Backup dos Markdown anteriores, inventário de hashes e conferência local/remota ficam nessa pasta.

---

## Registro histórico anterior — superado para esta integração

# Estado de publicação e continuidade — Ecosystem

Conferência documental de 12/09/2026. Este registro complementa os protocolos científicos e substitui apenas afirmações anteriores de que o candidato ainda não teve commit/push.

- Checkout de trabalho: `C:\CAIN\contrato`.
- Branch de trabalho: `feature/research-bundle-v1`. Não presumir que `main` contém esta entrega.
- HEAD conferido antes desta atualização documental: `0dd0d5f7515238ed0f2bc88f27a3d569a57dbbb5`.
- O código deste projeto foi publicado na branch indicada. O candidato CAIN Supply permanece sem aprovação de estabilização.
- Sem merge, release, instalação operacional ou nova execução científica nesta conferência.

## Validação e pendências

A [CI geral do CAIN](https://github.com/leonardosovienski/cain/actions/runs/34674661122) passou para `7e6105e`.
O [gate Linux dedicado](https://github.com/leonardosovienski/cain/actions/runs/34674661161) falhou na suíte completa em Python 3.13 e 3.14.
No artefato 3.13, equivalência do candidato confirmada e 187 testes direcionados passaram sem skips. A suíte completa registrou 547 passes, 13 falhas, 4 erros e 2 skips: faltam arquivos de cenários na instalação isolada do wheel CAIN. Esses resultados não certificam o runtime científico deste projeto.
As etapas posteriores de E2E instalado, restore offline, testes dos produtores e mini-auditoria não foram alcançadas nessa execução. Próximo gate: corrigir a localização/empacotamento dos cenários, congelar o candidato corrigido, repetir os testes afetados e concluir o Linux antes de discutir estabilização.

## Preservação e retomada

Foram inventariados 57 Markdown versionados antes da atualização, com hashes e verificação de leitura UTF-8. Inventário local: `C:\CAIN\work\ecosystem-documentation-sync-20260912`.
Inventário não é recertificação semântica de cada relatório histórico nem prova de backup dos arquivos ignorados pelo Git. Relatórios datados, fontes, bancos, manifests e snapshots congelados conservam seus bytes e contexto. Outros worktrees são checkouts de outras branches; não devem receber cópia cega desta branch.
Leia os documentos de entrada deste checkout e seus protocolos antes de executar trabalho de domínio. Para verificar publicação após novos commits: `git status --short`, `git rev-parse HEAD` e `git ls-remote origin refs/heads/feature/research-bundle-v1`; os dois SHAs devem coincidir e o status deve estar vazio.


## Encerramento e retomada da sessão

Registro consolidado: [decisões, acertos, erros, pendências e próximo prompt](https://github.com/leonardosovienski/cain/blob/feature/research-bundle-v1/docs/research/SESSION_HANDOFF_20260912.md). O gate Linux permanece reprovado. A conferência documental não foi uma revisão semântica integral dos relatórios históricos. Os dois skips conferidos no XML Linux 3.13 são testes exclusivos do launcher Windows; não incluem o teste obrigatório de symlink, que passou.
