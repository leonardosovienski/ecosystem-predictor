# Crypto: integração e continuidade — 12/09/2026

O Crypto foi consolidado em main. Última fonte observada: `4c4d97ec9bfff185df089a6edb6da9ccd71f306f`. Runtime 1.1.0, exportador 1.0.1, Core 3.2.1 e Ops 4.2.0. A atualização documental posterior ao código auditado 9db8e93 tem CI própria:

- [CI](https://github.com/leonardosovienski/cripto-predictor/actions/runs/34727078793): success, SHA `4c4d97ec9bfff185df089a6edb6da9ccd71f306f`.
- [Installed Crypto CAIN integration](https://github.com/leonardosovienski/cripto-predictor/actions/runs/34727078857): success, SHA `4c4d97ec9bfff185df089a6edb6da9ccd71f306f`.

A combinação instalada nesses runs usa Ecosystem `6a998520825292895bcae71e589fa8ac0e02bb85` e CAIN `5ba4177a11b9312900e5035517aa5ef25d509859`. O Ecosystem incorporou depois atualizações de registros; não atribuir o teste dessa combinação automaticamente a outro SHA. A CI deste repositório valida cada nova publicação separadamente.

## Onde conferir

1. [Registro corrente de projetos](registries/project_registry.json): versões e último SHA observado; avanços posteriores de main são avisos do checker, não recertificação implícita.
2. [Compatibilidade de wheels](docs/CRYPTO_WHEEL_COMPATIBILITY.md): identidade de artefatos e recusas por hash/proveniência.
3. [Controles de engenharia](docs/engineering_controls/20260912/README.md) e [registro dos harnesses](registries/harness_registry.json): fontes, hashes, validade e escopo.
4. [Auditoria no Crypto](https://github.com/leonardosovienski/cripto-predictor/blob/4c4d97ec9bfff185df089a6edb6da9ccd71f306f/docs/FINAL_INTEGRATION_AUDIT.md): reprodução e limites da integração.

## Limites preservados

ALIGNED dos controles Core 3.2.1 certifica somente os braços sintéticos oficiais dos julgadores. Não substitui os atestados operacionais históricos nem reabre hipóteses. CR-01 e os demais registros científicos não foram fechados por esta correção documental. Capital permanece não autorizado pela integração.

A antiga falha Linux do candidato CAIN 7e6105e descreve outra fonte e outra rodada. Ela não é bloqueador da combinação acima. Relatos históricos conservam suas contagens e SHAs; as versões Snapshot 1.0.0/1.0.1 e Bundle 1.0.0 coexistem conforme os contratos testados.

Esta manutenção não remove branches Ecosystem, não cria releases, não atualiza instalações operacionais e não altera os projetos de outros domínios.
