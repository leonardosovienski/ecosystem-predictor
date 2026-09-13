# Ecossistema — operação e combinações verificadas

Os sete repositórios permanecem independentes. Core fornece a biblioteca científica; Ops executa jobs locais; Crypto, Stocks e Brasileirão mantêm seus próprios dados e decisões; Ecosystem oferece diagnóstico opcional; CAIN recebe cópias de evidências admitidas. Não existe banco central nem obrigação de iniciar todos os projetos juntos.

A combinação histórica de releases está em [released_architecture.json](registries/released_architecture.json), com URLs, versões, commits e hashes. O inventário de sete projetos/nove distribuições está em [architecture_registry.json](registries/architecture_registry.json). O manifesto de candidatos guarda os commits efetivamente testados; não acompanha `main` silenciosamente.

| Projeto | Versão publicada | Papel e entrada |
|---|---|---|
| Core | 3.2.1 | Imports explícitos em `predictor_core.contracts.scientific` e `predictor_core.measurement`; instalação mínima independente |
| Ops | 4.2.0 | `predictor-ops --help`; schema 3 genérico, execução econômica exige política e risco explícitos |
| Crypto | 1.1.0 | `cripto-predictor status`; modos separados de ingestão, análise, histórico e migração |
| Stocks | 0.2.0 | `python -m stocks_predictor --help`; `simulate-selected` conecta seleção explícita ao simulador |
| Brasileirão | 0.2.0 | `brasileirao-predict --help`; previsão formal identificada, shadow externo ao checkout |
| Ecosystem | 0.2.0 | `Registry.discover().diagnostic_snapshot()` preserva estados nativos e identifica erros |
| CAIN | 0.4.5 | `cain research --help`; importação, consulta, referências, histórico e backup sem modelo obrigatório |

O contrato `predictor-research-snapshot` 1.0.1 e o exportador `crypto-research-export` 1.0.1 são wheels separados. Na combinação histórica de releases, o CAIN conservava seu leitor 1.0.0. A instalação principal atual usa CAIN 0.4.7, Snapshot 1.0.1 e Bundle 1.0.0, conforme a [integração Stocks](STOCKS_INTEGRATION_20260912.md). A tabela de releases acima não identifica o wheel operacional instalado.

## Instalação e diagnóstico

Cada projeto usa seu próprio ambiente e diretório de dados. Neste computador, Crypto fica em `C:\Cripto`, Stocks em `C:\STOCKS`, Brasileirão em `C:\BRASILEIRAO`, Core/Ops em `C:\PREDICTORS` e CAIN/Ecosystem em `C:\CAIN`. Stocks executa seu runtime em Linux/CI; não instalar o runtime Stocks no Windows desta estação.

Para reproduzir a integração em **Linux**, a partir deste checkout, use um ambiente descartável:

```sh
python3.13 -m venv /tmp/predictors-released
python scripts/install_compatibility_candidate.py --released --python /tmp/predictors-released/bin/python
CRIPTO_ROOT=/tmp/crypto-diagnostic RELEASED_WHEELS=1 COMPATIBILITY_RECEIPT=/tmp/compatibility.json /tmp/predictors-released/bin/python scripts/check_real_plugin_integration.py
```

O instalador verifica os hashes no download e o checker verifica a identidade instalada e os payloads. Esse ambiente conjunto é uma prova de compatibilidade; os ambientes cotidianos continuam separados. CAIN e exportador são testados em ambientes mínimos distintos.

## Intercâmbio de evidências

1. O produtor recebe a admissão explícita das fontes documentais e seus hashes. O exportador recusa fontes fora da lista, conteúdo alterado e destino dentro da origem científica.
2. A publicação valida o contrato, sincroniza staging e cria o nome final sem substituir arquivo existente. Mesmo conteúdo e instante de exportação produzem recuperação idempotente; outro conteúdo no mesmo destino é conflito.
3. O CAIN recebe um `import_root` e grants para usuário, coleção, produtor, fontes e política. `cain research --policy POLICY --db DB --collection COLLECTION import PUBLICATION.json` usa caminho relativo à raiz admitida.
4. `query --source-id ID --status STATUS` filtra registros; `evidence REFERENCE` abre o trecho recebido; `receipts`, `verify` e `backup DESTINATION` oferecem rastreabilidade. Consulta de evidência recebida independe de modelo e de predictor instalado.
5. Revogar grants também restringe o histórico derivado. Repetir a importação não duplica revisão. Backup/restore usa destino novo; arquivos e bancos não são uma transação distribuída.

## Consulta Stocks na instalação principal

Abra `C:/CAIN/ABRIR_CAIN.cmd` (porta 8877), usuário `leo`, projeto Geral.
Em Pesquisa, use `stocks-main-snapshot` e **Consultar acervo**, ou
`stocks-main-bundle` e **Consultar metadados Bundle**. São evidências admitidas,
com referências e limitações preservadas; a geração desses acervos está negada.
Não reimporte ou altere a política apenas para consultar o que já foi admitido.

## Operação e recuperação

As configurações e bancos reais permanecem nas raízes dos proprietários. `status`, ajuda e diagnóstico não iniciam coleta nem autorizam capital. Ausência de recursos deve produzir erro explícito. No Brasileirão, `BRASILEIRAO_PROJECT_ROOT`, `BRASILEIRAO_RUNTIME_ROOT` e a configuração externa permitem usar o pacote instalado. `brasileirao-shadow --task-name brasileirao-sombra-manha --check` verifica os módulos através do runner, com configuração e banco sintéticos quando usado em validação.

Antes de compartilhar um runtime root com Ops 4.2, parar runners antigos. Não misturar implementações de lease nem apagar tentativas para permitir retry. Uma tentativa econômica de efeito incerto permanece bloqueada. Rollback reinstala a versão anterior em ambiente separado, preservando bancos, publicações, IDs e recibos; não refaz resultado histórico.

Os gates são de engenharia. Coortes futuras, atestados de poder científico, observação natural de agendamentos e validação econômica continuam sob os protocolos originais. As releases não transformam `NO_GO`, `UNKNOWN` ou ausência de hipótese em autorização de operação.
