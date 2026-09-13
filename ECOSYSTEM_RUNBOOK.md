# Ecossistema — operação e combinações verificadas

[Estado atual](CURRENT_STATE.md) · [Charter](ECOSYSTEM_CHARTER.md) ·
[Autoridade e histórico](docs/HISTORICAL_DOCUMENT_INDEX.md).

Este runbook reúne procedimentos do Ecosystem. Manuais internos e instalações
dos projetos permanecem sob as fontes indicadas nas fichas.

Os sete repositórios permanecem independentes. Core fornece a biblioteca científica; Ops executa jobs locais; Crypto, Stocks e Brasileirão mantêm seus próprios dados e decisões; Ecosystem oferece diagnóstico opcional; CAIN recebe cópias de evidências admitidas. Não existe banco central nem obrigação de iniciar todos os projetos juntos.

As coordenadas de releases registradas estão em [released_architecture.json](registries/released_architecture.json), com URLs, versões, commits e hashes. O inventário de sete projetos/dez pacotes independentes está em [architecture_registry.json](registries/architecture_registry.json). O manifesto de candidatos guarda os commits efetivamente testados; não acompanha `main` silenciosamente.

As fichas [Core](docs/projects/core.md), [Ops](docs/projects/ops.md),
[Cripto](docs/projects/cripto.md), [Stocks](docs/projects/stocks.md),
[Brasileirão](docs/projects/brasileirao.md) e [CAIN](docs/projects/cain.md)
descrevem interfaces e evidências. Versões/SHAs/hashes devem ser lidos nos manifestos
acima, sem uma segunda tabela manual de versões. Release, combinação candidata e
instalação operacional são identidades distintas.

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

## Consulta Stocks — procedimento da instalação validada em 12/09/2026

Abra `C:/CAIN/ABRIR_CAIN.cmd` (porta 8877), usuário `leo`, projeto Geral.
Em Pesquisa, use `stocks-main-snapshot` e **Consultar acervo**, ou
`stocks-main-bundle` e **Consultar metadados Bundle**. São evidências admitidas,
com referências e limitações preservadas; a geração desses acervos está negada.
Não reimporte ou altere a política apenas para consultar o que já foi admitido.

## Operação e recuperação

As configurações e bancos reais permanecem nas raízes dos proprietários. `status`, ajuda e diagnóstico não iniciam coleta nem autorizam capital. Ausência de recursos deve produzir erro explícito. No Brasileirão, `BRASILEIRAO_PROJECT_ROOT`, `BRASILEIRAO_RUNTIME_ROOT` e a configuração externa permitem usar o pacote instalado. `brasileirao-shadow --task-name brasileirao-sombra-manha --check` verifica os módulos através do runner, com configuração e banco sintéticos quando usado em validação.

Antes de compartilhar um runtime root com Ops 4.2, parar runners antigos. Não misturar implementações de lease nem apagar tentativas para permitir retry. Uma tentativa econômica de efeito incerto permanece bloqueada. Rollback reinstala a versão anterior em ambiente separado, preservando bancos, publicações, IDs e recibos; não refaz resultado histórico.

Os gates são de engenharia. Coortes futuras, atestados de poder científico, observação natural de agendamentos e validação econômica continuam sob os protocolos originais. As releases não transformam `NO_GO`, `UNKNOWN` ou ausência de hipótese em autorização de operação.

A versão operacional atual pertence ao [estado do CAIN](https://github.com/leonardosovienski/cain/blob/main/ESTADO_DO_PROJETO.md).
Para reconferir apenas a identidade instalada neste PC, use
`C:/CAIN/.venv/Scripts/python.exe -I -c "from importlib.metadata import version; print(version('cain-research'))"`.
Essa leitura não revalida uma combinação. Dez pacotes no inventário não significa
dez releases publicadas.

## Combinação validada com a main final do Core

`registries/compatibility_candidate.json` corresponde à combinação validada com
Core main 9bf43ef, wheel 3.2.1, Ops 4.2.1 e CAIN 0.4.10 isolado. O CAIN declarado
nesse manifesto não identifica automaticamente a instalação operacional do PC.
A origem da release do Core continua 7bb212c; a main posterior contém os gates
funcionais e documentação, com 41 arquivos de runtime iguais ao wheel publicado.

Para reproduzir os três plugins em Linux, use os comandos de instalação acima
sem `--released` e execute o checker sem `RELEASED_WHEELS`. A CI também executa
o verificador funcional do core instalado fora dos checkouts, obtido do SHA
fixado no recibo. Relatório: [Core](CORE_INTEGRATION_20260913.md).

## Verificações do Ecosystem

Em ambiente separado, após `uv sync --all-extras`:

```sh
uv run pytest -q
uv run python scripts/sync_canonical_ecosystem_facts.py --offline-check
uv run python scripts/check_ecosystem_drift.py --offline-check
uv run python scripts/check_ecosystem_drift.py
uv run python scripts/check_architecture_manifest.py
```

O primeiro reconciliador preserva o snapshot histórico de seis repositórios.
O drift compara registries, versões, pins e atestados dos seis repositórios que
seu código cobre; CAIN é coberto pelo manifesto arquitetural de sete projetos.
Avanço de main é aviso, não aceite de nova combinação. Sem rede, `--from-clones`
usa `origin/main` dos clones disponíveis; confirme sua atualização separadamente.

`check_real_plugin_integration.py` exige os três predictors instalados juntos com
a proveniência do manifesto. Use Linux e o ambiente descartável descrito acima.
`--released` no instalador e `RELEASED_WHEELS=1` no checker selecionam distribuições
publicadas; sem ambos, a verificação usa o candidato fixado. Não execute o checker
num ambiente parcial nem troque pins para obter aprovação.

Os testes independentes de Bundle são `python -m pytest packages/research-bundle/tests -q`
após instalar os dois contratos em ambiente separado. Os testes de Snapshot também
estão em `tests/`; não existe `packages/research-snapshot/tests`. A
[CI existente](.github/workflows/ci.yml) cobre qualidade, contratos, inventário,
plugins, wheels e transporte. CI offline não prova o remoto, ciência ou capital.
