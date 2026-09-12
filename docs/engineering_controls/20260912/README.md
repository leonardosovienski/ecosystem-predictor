# Controles sintéticos dos julgadores Crypto com Core 3.2.1

Os quatro braços oficiais (edge/ruído, V3/Fase 1) foram executados em 12/09/2026
com o harness instalado da wheel Crypto 1.1.0 e Core 3.2.1, contra a fonte limpa
Crypto 22219e3db8130bfe81abe95b38ecfbc3cacdb5f9. O arquivo instalado foi comparado
à fonte, explicitando normalização CRLF/LF. As seeds e critérios oficiais não mudaram.

Os novos JSONs `synthetic-control-*` são os bytes emitidos pelo harness, em destino
isolado. `historical-source-*` preservam os bytes dos atestados admitidos anteriores,
sem renovar sua validade ou alterar o domínio. O registry referencia cada arquivo
por SHA256 e os campos são conferidos pelo checker. `provenance.json` identifica
fonte, escopo e recibo de execução privado. O campo `code_version` é a representação
produzida pelo Core: `package:3.2.1` identifica o Core; o Git SHA identifica o domínio.

Reprodução: executar `python -I -m GarimpoInvestimentos.operational.attest_harness`
em ambiente instalado, com `CRIPTO_SOURCE_ROOT` apontando à fonte limpa e
`CRIPTO_TRIALS_PATH` para um destino novo e isolado. TEMP/TMP devem ficar em área
autorizada. Não apontar esses parâmetros aos trials ou atestados operacionais.

ALIGNED nessas duas entradas descreve somente o controle sintético dos julgadores.
Não é validação de edge de mercado, novo experimento, atualização de hipóteses,
reativação de trials ou permissão de capital. Expiração e demais guardas permanecem.
O gate anterior falhou por falta dessa evidência; não foi removido nem relaxado.
