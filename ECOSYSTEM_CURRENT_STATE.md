# Estado factual corrente do ecossistema

Evidência coletada em **2026-08-11**. O inventário abaixo é mecânico e
reprodutível; decisões humanas e propostas continuam fora dele. O ref completo
de cada linha é obrigatório para evitar que um nome de arquivo seja confundido
com conteúdo efetivamente verificado.

## Escopo e método

Foram lidos checkouts limpos dos nove repositórios públicos, fixados nos HEADs
abaixo, além das execuções concretas do GitHub Actions associadas a esses HEADs.
As classificações significam:

- `VERIFIED_FROM_GIT`: identidade, ref, árvore ou tag obtida do Git;
- `VERIFIED_FROM_CODE`: conteúdo lido no arquivo/símbolo indicado;
- `VERIFIED_FROM_CI`: execução concreta identificada por URL;
- `DOCUMENTED_NOT_EXECUTED`: estado declarado pelo projeto, não reproduzido na F1;
- `NOT_APPLICABLE`: capacidade deliberadamente ausente no projeto legado.

`stocks-predictor`, `nba-predictor` e `Claude` não são fontes de estado desta
reconciliação. Os dois primeiros estão fora do escopo humano; `Claude` não é
canônico.

## Inventário mecânico

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops efetivos | Estado declarado (sem normalização) | CI no HEAD |
|---|---|---|---|---|---|
| `ecosystem-predictor` | `master` / `a9214d69f188` | `0.1.0`; `>=3.13,<3.15` | Core `2.1.0`; Ops `2.0.1`, wheels por URL | plataforma agregadora; adoção dos domínios não é implícita | [CI 30857005048](https://github.com/leonardosovienski/ecosystem-predictor/actions/runs/30857005048), `success` |
| `core-predictor` | `main` / `7933e4aca0ce` | `2.2.1`; `>=3.13` | camada Core instalável | pacote científico compartilhado | [CI 31314327197](https://github.com/leonardosovienski/core-predictor/actions/runs/31314327197), `success` |
| `tools-predictor` | `main` / `3ca6995e3be1` | Ops `3.0.0`; `>=3.13` | camada Ops instalável | separação operacional/científica | [CI 31250681330](https://github.com/leonardosovienski/tools-predictor/actions/runs/31250681330), `success` |
| `brasileirao-predictor` | `main` / `5a42d6c88298` | `0.1.0`; `>=3.13,<3.15` | Core `2.2.0`; Ops `3.0.0`, wheels por URL | `NO-GO`; coleta `COLLECTION_ONLY` | [CI 31462565846](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/31462565846), `success` |
| `cripto-predictor` | `main` / `375fe6df903e` | `1.0.0`; `>=3.13,<3.15` | Core `2.2.0`; Ops `3.0.0`, wheels por URL | V3 com `NO-GO`; coleta exploratória `COLLECTION_ONLY` | [CI 31431935255](https://github.com/leonardosovienski/cripto-predictor/actions/runs/31431935255), `success` |
| `cs-predictor` | `main` / `07f14bfea27c` | `3.1.0`; `>=3.13,<3.15` | Core `2.2.1`; Ops `3.0.0`, wheels por URL | `CLOSED_BY_HUMAN_DECISION`, `NO_GO`, operação `COLLECTION_ONLY` | [CI 31314924862](https://github.com/leonardosovienski/cs-predictor/actions/runs/31314924862), `success` |
| `f1-predictor` | `main` / `617cb2c49cee` | `1.0.0`; `>=3.13,<3.15` | Core `2.2.0`; Ops `3.0.0`, wheels por URL | `SELADO`; operação `NO-GO`; mercado `COLLECTION_ONLY` | [CI 31303370467](https://github.com/leonardosovienski/f1-predictor/actions/runs/31303370467), `success` |
| `lol-predictor` | `main` / `bd8ed5d69b03` | `2.1.0`; `>=3.13,<3.15` | Core `2.2.0`; Ops `3.0.0`, wheels por URL | `CLOSED_BY_HUMAN_DECISION`; archival `COLLECTION_ONLY` | [CI 31343386513](https://github.com/leonardosovienski/lol-predictor/actions/runs/31343386513), `success` |
| `wc-predictor` | `main` / `40fe5135d14a` | requirements; Python não declarado em `pyproject.toml` | Core legado vendorizado; Ops não declarado | `ENCERRADO`; `PARKED` como registro histórico | sem workflow: `NOT_APPLICABLE` |

## Evidência por alegação

| ID | Alegação | Repositório | Arquivo/símbolo | Ref/commit | Método | Classificação |
|---|---|---|---|---|---|---|
| F1-E01 | O inventário usa o HEAD corrente de cada repositório | todos os nove | `HEAD`, branch padrão e árvore | refs da tabela acima | `git rev-parse`, `git branch`, checkout limpo | `VERIFIED_FROM_GIT` |
| F1-E02 | Core é pacote `predictor-core` 2.2.1 para Python >=3.13 | core-predictor | `pyproject.toml` / `[project]` | `7933e4aca0ce` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E03 | Ops é pacote `predictor-ops` 3.0.0 para Python >=3.13 | tools-predictor | `pyproject.toml` / `[project]` | `3ca6995e3be1` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E04 | A plataforma ainda resolve Core 2.1.0 e Ops 2.0.1 por wheels | ecosystem-predictor | `pyproject.toml` / dependencies e `tool.uv.sources`; `uv.lock` | `a9214d69f188` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E05 | Brasileirão, Cripto, F1 e LoL resolvem Core 2.2.0/Ops 3.0.0 por wheels | quatro domínios | `pyproject.toml` / `tool.uv.sources`; `uv.lock` | refs da tabela | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E06 | CS resolve Core 2.2.1/Ops 3.0.0 por wheels | cs-predictor | `pyproject.toml` / dependencies e sources; `uv.lock` | `07f14bfea27c` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E07 | WC é legado vendorizado e não possui workflow | wc-predictor | `HANDOFF.md`; ausência de `.github/workflows`; árvore | `40fe5135d14a` | leitura direta e árvore Git | `VERIFIED_FROM_CODE` |
| F1-E08 | Os oito repositórios com workflow tiveram CI concreta verde no HEAD | todos exceto WC | `.github/workflows/*.yml`; runs vinculadas na tabela | refs e runs da tabela | GitHub Actions | `VERIFIED_FROM_CI` |
| F1-E09 | Os termos de estado por domínio vêm de README/HANDOFF | domínios | `README.md`, `HANDOFF.md`, símbolos citados na tabela | refs da tabela | leitura direta | `DOCUMENTED_NOT_EXECUTED` |
| F1-E10 | A F0 alinhou Brasileirão para Core 2.2.0/Ops 3.0.0 e ficou verde em main | brasileirao-predictor | `pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`; PR #9 | `5a42d6c88298`; run `31462565846` | Git, código e CI | `VERIFIED_FROM_CI` |
| F1-E11 | Nenhuma conclusão científica foi reproduzida nesta F1 | ecosystem-predictor | escopo da F1 / este registro | `a9214d69f188` | controle de execução | `DOCUMENTED_NOT_EXECUTED` |

## Matriz Core/Ops real

| Consumidor | Core | Ops | Forma | Observação factual |
|---|---:|---:|---|---|
| ecosystem | 2.1.0 | 2.0.1 | wheel GitHub fixado por URL/lock | abaixo das releases correntes; mudança depende de F2/autorização própria |
| Brasileirão | 2.2.0 | 3.0.0 | wheel GitHub fixado por URL/lock | F0 reconciliada e CI verde |
| Cripto | 2.2.0 | 3.0.0 | wheel GitHub fixado por URL/lock | sem execução científica nesta F1 |
| CS | 2.2.1 | 3.0.0 | wheel GitHub fixado por URL/lock | único domínio no Core 2.2.1 |
| F1 | 2.2.0 | 3.0.0 | wheel GitHub fixado por URL/lock | sem execução científica nesta F1 |
| LoL | 2.2.0 | 3.0.0 | wheel GitHub fixado por URL/lock | sem execução científica nesta F1 |
| WC | legado | não declarado | cópia vendorizada/requisitos | histórico; nenhuma modernização autorizada |

## Fronteira factual/humana

Este arquivo prova versões, origens, estados documentados e CI identificada.
Não prova resultados numéricos, prontidão econômica, equivalência científica
entre domínios ou a tese completa do TCC. Imports demonstram arquitetura, não
validade científica. Qualquer decisão de padronização, promoção, atualização de
dependência ou seleção de estudo de caso pertence a uma F2 futura e depende de
autorização humana explícita.
