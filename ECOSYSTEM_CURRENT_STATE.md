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

<!-- mechanical-facts:start -->
_Bloco mecânico gerado por `scripts/sync_ecosystem_facts.py`; decisões humanas não são geradas._

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | CI | Canônicos |
|---|---|---|---|---|---|
| `ecosystem-predictor` | `master` / commit deste documento | `0.1.0` / `>=3.13,<3.15` | Core `>=2.1,<3 (v2.1.0)` / Ops `>=3.0.0,<4 (v3.0.0)` | workflow atual | `ECOSYSTEM_CURRENT_STATE.md`, `ECOSYSTEM_HANDOFF.md`, `P4_CONSOLIDATION.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `core-predictor` | `main` / `7933e4aca0ce` | `2.2.1` / `>=3.13` | Core `—` / Ops `—` | [success](https://github.com/leonardosovienski/core-predictor/actions/runs/31314327197) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `tools-predictor` | `main` / `3ca6995e3be1` | `3.0.0` / `>=3.13` | Core `—` / Ops `—` | [success](https://github.com/leonardosovienski/tools-predictor/actions/runs/31250680200) | `README.md`, `pyproject.toml`, `uv.lock` |
| `brasileirao-predictor` | `main` / `5a42d6c88298` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.2,<3 (v2.2.0)` / Ops `>=3,<4 (v3.0.0)` | [success](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/31462565846) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `cripto-predictor` | `main` / `375fe6df903e` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.2.0,<2.3 (v2.2.0)` / Ops `>=3.0.0,<3.1 (v3.0.0)` | [success](https://github.com/leonardosovienski/cripto-predictor/actions/runs/31431935255) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `cs-predictor` | `main` / `f7bb21411450` | `3.1.0` / `>=3.13,<3.15` | Core `==2.2.1 (v2.2.1)` / Ops `==3.0.0 (v3.0.0)` | [success](https://github.com/leonardosovienski/cs-predictor/actions/runs/31490882633) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `f1-predictor` | `main` / `d6e54cc9997b` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.2,<3 (v2.2.0)` / Ops `>=3,<4 (v3.0.0)` | [success](https://github.com/leonardosovienski/f1-predictor/actions/runs/31486487656) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `lol-predictor` | `main` / `17425a75101c` | `2.1.0` / `>=3.13,<3.15` | Core `>=2.2,<3 (v2.2.0)` / Ops `>=3,<4 (v3.0.0)` | [success](https://github.com/leonardosovienski/lol-predictor/actions/runs/31488598943) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `wc-predictor` | `main` / `40fe5135d14a` | `requirements` / `não declarado` | Core `legado vendorizado` / Ops `—` | NOT_APPLICABLE | `HANDOFF.md`, `README.md`, `requirements.txt` |
<!-- mechanical-facts:end -->

### Estados documentados — autoria humana

Esta tabela não é alterada pelo coletor mecânico. Os termos permanecem os dos
próprios projetos e não são inferidos de CI, imports ou versões.

| Repositório | Estado documentado corrente |
|---|---|
| `ecosystem-predictor` | plataforma agregadora; `RunStatus` separado de `scientific_state` |
| `core-predictor` | pacote científico compartilhado |
| `tools-predictor` | camada operacional compartilhada |
| `brasileirao-predictor` | `NO-GO`; coleta `COLLECTION_ONLY` |
| `cripto-predictor` | V3 com `NO-GO`; coleta exploratória `COLLECTION_ONLY` |
| `cs-predictor` | `CLOSED_BY_HUMAN_DECISION`, `NO_GO`, operação `COLLECTION_ONLY`; P4-CS validada |
| `f1-predictor` | `SELADO`; operação `NO-GO`; mercado `COLLECTION_ONLY`; P4-A/P4-A.1 validadas |
| `lol-predictor` | `CLOSED_BY_HUMAN_DECISION`; archival `COLLECTION_ONLY`; P4-B validada |
| `wc-predictor` | `ENCERRADO`; `PARKED` como registro histórico |

## Evidência por alegação

| ID | Alegação | Repositório | Arquivo/símbolo | Ref/commit | Método | Classificação |
|---|---|---|---|---|---|---|
| F1-E01 | O inventário usa o HEAD corrente de cada repositório | todos os nove | `HEAD`, branch padrão e árvore | refs da tabela acima | `git rev-parse`, `git branch`, checkout limpo | `VERIFIED_FROM_GIT` |
| F1-E02 | Core é pacote `predictor-core` 2.2.1 para Python >=3.13 | core-predictor | `pyproject.toml` / `[project]` | `7933e4aca0ce` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E03 | Ops é pacote `predictor-ops` 3.0.0 para Python >=3.13 | tools-predictor | `pyproject.toml` / `[project]` | `3ca6995e3be1` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E04 | A plataforma preserva Core 2.1.0 e resolve Ops 3.0.0 por wheels | ecosystem-predictor | `pyproject.toml` / dependencies e `tool.uv.sources`; `uv.lock` | branch P1 sobre `0cde8662714a` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E05 | Brasileirão, Cripto, F1 e LoL resolvem Core 2.2.0/Ops 3.0.0 por wheels | quatro domínios | `pyproject.toml` / `tool.uv.sources`; `uv.lock` | refs da tabela | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E06 | CS resolve Core 2.2.1/Ops 3.0.0 por wheels | cs-predictor | `pyproject.toml` / dependencies e sources; `uv.lock` | `07f14bfea27c` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E07 | WC é legado vendorizado e não possui workflow | wc-predictor | `HANDOFF.md`; ausência de `.github/workflows`; árvore | `40fe5135d14a` | leitura direta e árvore Git | `VERIFIED_FROM_CODE` |
| F1-E08 | Os oito repositórios com workflow tiveram CI concreta verde no HEAD | todos exceto WC | `.github/workflows/*.yml`; runs vinculadas na tabela | refs e runs da tabela | GitHub Actions | `VERIFIED_FROM_CI` |
| F1-E09 | Os termos de estado por domínio vêm de README/HANDOFF | domínios | `README.md`, `HANDOFF.md`, símbolos citados na tabela | refs da tabela | leitura direta | `DOCUMENTED_NOT_EXECUTED` |
| F1-E10 | A F0 alinhou Brasileirão para Core 2.2.0/Ops 3.0.0 e ficou verde em main | brasileirao-predictor | `pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`; PR #9 | `5a42d6c88298`; run `31462565846` | Git, código e CI | `VERIFIED_FROM_CI` |
| F1-E11 | Nenhuma conclusão científica foi reproduzida nesta F1 | ecosystem-predictor | escopo da F1 / este registro | `a9214d69f188` | controle de execução | `DOCUMENTED_NOT_EXECUTED` |

## Atualização factual P4 — 2026-08-11

A fonte detalhada é [P4_CONSOLIDATION.md](P4_CONSOLIDATION.md), com
rastreabilidade `P4E001–P4E034`. P4-A/F1, P4-A.1, P4-B/LoL e P4-CS foram
mescladas e validadas. A comparação aprovou
`P4_COMPLETED_NO_CORE_CHANGE`: `PredictionPoint` e `replay` já cobrem a parte
comum do Core; adapters e semânticas de domínio permanecem locais.

A alegação de pytest remoto CS em Python 3.14 é `CONTRADICTED`: no run
`31490882633`, o job instalou 3.14.5, mas pytest executou em 3.13.13; somente o
smoke do wheel usou 3.14.5. Execução local 3.14 existe separadamente como
`VERIFIED_BY_EXECUTION`. Nenhuma evidência P4 confirma ciência, equivalência
estatística, valor econômico ou comportamento ao vivo.

## Matriz Core/Ops real

| Consumidor | Core | Ops | Forma | Observação factual |
|---|---:|---:|---|---|
| ecosystem | 2.1.0 | 3.0.0 | wheel GitHub fixado por URL/lock | Ops reconciliado no P1; Core deliberadamente preservado |
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
