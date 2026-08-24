# Estado factual do ecossistema

> **ATUALIZAÇÃO DE ESCOPO — 2026-08-23.** A composição humana canônica atual está em
> [`ECOSYSTEM_CHARTER.md`](ECOSYSTEM_CHARTER.md): `ecosystem-predictor`,
> `core-predictor`, `predictor-ops`, `cripto-predictor`,
> `brasileirao-predictor` e `stocks-predictor`. O snapshot mecânico abaixo foi
> coletado em 2026-08-17, antes dessa decisão, e **não pode ser usado para excluir
> Stocks nem para reinserir CS/F1/LoL/WC no escopo canônico atual**.
>
> O bloco `mechanical-facts` é preservado exatamente como evidência histórica e
> para manter a reprodutibilidade do coletor da F1. Ele descreve o que foi
> verificado naquela reconciliação; não representa sozinho a composição vigente.

Evidência mecânica coletada em **2026-08-17**. O inventário abaixo é
reprodutível para a reconciliação F1; decisões humanas permanecem fora dele.
O ref completo de cada linha é obrigatório para evitar que um nome de arquivo
seja confundido com conteúdo efetivamente verificado.

## Escopo e método da reconciliação de 2026-08-17

Foram lidos checkouts limpos dos nove repositórios públicos então selecionados,
fixados nos HEADs abaixo, além das execuções concretas do GitHub Actions
associadas a esses HEADs. As classificações significam:

- `VERIFIED_FROM_GIT`: identidade, ref, árvore ou tag obtida do Git;
- `VERIFIED_FROM_CODE`: conteúdo lido no arquivo/símbolo indicado;
- `VERIFIED_FROM_CI`: execução concreta identificada por URL;
- `DOCUMENTED_NOT_EXECUTED`: estado declarado pelo projeto, não reproduzido na F1;
- `NOT_APPLICABLE`: capacidade deliberadamente ausente no projeto legado.

Naquela reconciliação, `stocks-predictor`, `nba-predictor` e `Claude` não eram
fontes de estado. **Isso é histórico, não a decisão vigente.** Desde 2026-08-23,
`stocks-predictor` integra os seis projetos canônicos; `nba-predictor` e
`Claude` continuam fora do escopo canônico atual.

## Inventário mecânico histórico da F1

<!-- mechanical-facts:start -->
_Snapshot mecânico `ecosystem-facts/1`; gerado em `2026-08-17T14:40:22+00:00`._
_Decisões humanas são preservadas e ignoradas pelo validador._

| Repositório | Branch / HEAD | Pacote / Python | Core / Ops | CI | Canônicos |
|---|---|---|---|---|---|
| `brasileirao-predictor` | `main` / `3336565692ff` | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | [success](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/32036979309) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `core-predictor` | `main` / `f6754957eaed` | `2.3.0` / `>=3.13` | Core `—` / Ops `—` | [success](https://github.com/leonardosovienski/core-predictor/actions/runs/31994598474) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `cripto-predictor` | `main` / `b77b5a3ca409` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.3.0,<3 (v2.3.0)` / Ops `>=3.1.0,<4 (v3.1.0)` | [success](https://github.com/leonardosovienski/cripto-predictor/actions/runs/32036806552) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `cs-predictor` | `main` / `e02d9064a6fa` | `3.1.0` / `>=3.13,<3.15` | Core `==2.3.0 (v2.3.0)` / Ops `==3.1.0 (v3.1.0)` | [success](https://github.com/leonardosovienski/cs-predictor/actions/runs/32036813304) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `ecosystem-predictor` | `main` / HEAD derivado em execução | `0.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | workflow atual | `ECOSYSTEM_CURRENT_STATE.md`, `ECOSYSTEM_HANDOFF.md`, `P4_CONSOLIDATION.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `f1-predictor` | `main` / `8fd1e3c83c96` | `1.0.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | [success](https://github.com/leonardosovienski/f1-predictor/actions/runs/32036817971) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `uv.lock` |
| `lol-predictor` | `main` / `eb7a06b5ce6c` | `2.1.0` / `>=3.13,<3.15` | Core `>=2.3,<3 (v2.3.0)` / Ops `>=3.1,<4 (v3.1.0)` | [success](https://github.com/leonardosovienski/lol-predictor/actions/runs/32036823457) | `HANDOFF.md`, `README.md`, `pyproject.toml`, `requirements.txt`, `uv.lock` |
| `predictor-ops` | `main` / `eff6fc795a12` | `3.1.0` / `>=3.13` | Core `—` / Ops `—` | [success](https://github.com/leonardosovienski/predictor-ops/actions/runs/32029908996) | `README.md`, `pyproject.toml`, `uv.lock` |
| `wc-predictor` | `main` / `40fe5135d14a` | `requirements` / `não declarado` | Core `legado vendorizado` / Ops `—` | NOT_APPLICABLE | `HANDOFF.md`, `README.md`, `requirements.txt` |
<!-- mechanical-facts:end -->

### Estados documentados na reconciliação de 2026-08-17

Esta tabela também é histórica. Os termos permanecem os dos próprios projetos
naquele snapshot e não são inferidos de CI, imports ou versões. Para escopo
vigente, use o Charter.

| Repositório | Estado documentado naquele snapshot |
|---|---|
| `ecosystem-predictor` | plataforma agregadora; `RunStatus` separado de `scientific_state` |
| `core-predictor` | pacote científico compartilhado |
| `predictor-ops` | camada operacional compartilhada; repositório renomeado, pacote `predictor-ops` |
| `brasileirao-predictor` | capital fechado; H9 era o trilho prospectivo vivo, ainda sem amostra liquidada; H10 fadiga formalizada |
| `cripto-predictor` | hipóteses correntes `NO-GO`; camada de trading adicionada, sem autorização de capital |
| `cs-predictor` | capital `CLOSED_BY_HUMAN_DECISION`; shadow econômico reaberto sem capital, pré/pós-veto |
| `f1-predictor` | mercado real ainda sem fonte aceita; gate real específico por estratégia; operação `NO-GO` |
| `lol-predictor` | capital `NO_GO`; shadow pré/pós-draft fail-closed, sem promoção econômica |
| `wc-predictor` | `ENCERRADO`; `PARKED` como registro histórico |

`stocks-predictor` não aparece nessa tabela porque não foi inspecionado na F1.
Sua ausência aqui **não é um veredito nem uma exclusão atual**.

## Evidência por alegação da F1

| ID | Alegação | Repositório | Arquivo/símbolo | Ref/commit | Método | Classificação |
|---|---|---|---|---|---|---|
| F1-E01 | O inventário usa o HEAD corrente de cada repositório selecionado na F1 | nove do snapshot | `HEAD`, branch padrão e árvore | refs da tabela acima | `git rev-parse`, `git branch`, checkout limpo | `VERIFIED_FROM_GIT` |
| F1-E02 | Core é pacote `predictor-core` 2.3.0 para Python >=3.13 e expõe contratos econômicos neutros | core-predictor | `pyproject.toml`; `contracts/economic.py`; ADR-002 | `f6754957eaed` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E03 | Ops é pacote/repositório `predictor-ops` 3.1.0 para Python >=3.13 | predictor-ops | `pyproject.toml`; `operations.py`; `audit.py` | `eff6fc795a12` | leitura direta | `VERIFIED_FROM_CODE` |
| F1-E04 | A plataforma resolve Core 2.3.0 e Ops 3.1.0 por wheels publicados e fixados no lock | ecosystem-predictor | `pyproject.toml`; `uv.lock` | worktree da migração de 2026-08-17 | leitura direta e validação do lock | `VERIFIED_FROM_CODE` |
| F1-E05 | Brasileirão, Cripto, F1 e LoL resolviam Core 2.3.0/Ops 3.1.0 por wheels | quatro domínios | `pyproject.toml`; `uv.lock` | worktrees da migração de 2026-08-17 | leitura direta e testes locais | `VERIFIED_FROM_CODE` |
| F1-E06 | CS resolvia Core 2.3.0/Ops 3.1.0 por wheels | cs-predictor | `pyproject.toml`; `uv.lock` | worktree da migração de 2026-08-17 | leitura direta e testes locais | `VERIFIED_FROM_CODE` |
| F1-E07 | WC era legado vendorizado e não possuía workflow | wc-predictor | `HANDOFF.md`; árvore | `40fe5135d14a` | leitura direta e árvore Git | `VERIFIED_FROM_CODE` |
| F1-E08 | A CI concreta observada foi registrada no snapshot | inventário mecânico | `.github/workflows/*.yml`; runs vinculadas | refs e runs da tabela | GitHub Actions | `VERIFIED_FROM_CI` |
| F1-E09 | Os termos de estado por domínio vieram de README/HANDOFF | domínios do snapshot | `README.md`, `HANDOFF.md` | refs da tabela | leitura direta | `DOCUMENTED_NOT_EXECUTED` |
| F1-E10 | A F0 alinhou Brasileirão para Core 2.2.0/Ops 3.0.0 e ficou verde em main | brasileirao-predictor | `pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`; PR #9 | `5a42d6c88298`; run `31462565846` | Git, código e CI | `VERIFIED_FROM_CI` |
| F1-E11 | Nenhuma conclusão científica foi reproduzida nesta F1 | ecosystem-predictor | escopo da F1 / este registro | `a9214d69f188` | controle de execução | `DOCUMENTED_NOT_EXECUTED` |

## Atualização arquitetural verificada em 2026-08-17

As mudanças daquela rodada fecharam parte relevante das lacunas de contrato e
operação, mas não comprovaram edge nem autorizaram dinheiro real:

| Componente | Mudança verificada | Limite preservado |
|---|---|---|
| Core 2.3.0 | `ProbabilisticForecast`, `MarketQuote`, `EconomicDecision`, `ExecutionRecord`, `SettlementRecord` e validação da cadeia | não implementa sizing, risco, aprovação, adapters ou regra de liquidação |
| Ops 3.1.0 | oito tipos de job, chave econômica idempotente, bloqueio de retry ambíguo, reconciliação, kill switches e audit log hash-chain | não julga hipótese nem rentabilidade |
| Brasileirão | pipeline H9 de emissão, snapshots de closing, settlement e qualidade de execução; H10 de descanso | naquele momento H9 ainda sem amostra liquidada; execução real e portfólio ausentes |
| Cripto | contratos locais, execução, microestrutura e portfólio | hipóteses correntes seguiam NO-GO; camada não autorizava capital |
| CS | liquidez persistida e pipeline shadow pré/pós-veto com economia separada | sem CLV externo verdadeiro; capital fechado |
| F1 | gate de dinheiro real passou a ser específico por estratégia | zero fontes de mercado aceitas e nenhuma estratégia aprovada contra preço |
| LoL | lifecycle de ordens endurecido e shadow pré/pós-draft fail-closed | H4 retrospectiva inconclusiva; capital NO-GO |
| WC | nenhuma mudança | encerrado e preservado como histórico |

A consequência arquitetural continua útil: integração compartilhada deve usar
os contratos do Core e os controles do Ops por estratégia, começando em shadow.
Isso não implica que todos os projetos históricos continuem no escopo atual.

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

## Matriz Core/Ops observada em 2026-08-17

| Consumidor | Core | Ops | Forma | Observação factual |
|---|---:|---:|---|---|
| ecosystem | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | migração integrada em 2026-08-17 |
| Brasileirão | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | migração local validada |
| Cripto | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | migração local validada |
| CS | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | histórico F1 |
| F1 | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | histórico F1 |
| LoL | 2.3.0 | 3.1.0 | wheel GitHub fixado por URL/lock | histórico F1 |
| WC | legado | não declarado | cópia vendorizada/requisitos | histórico |

`stocks-predictor` precisa de uma reconciliação mecânica própria após sua
reinclusão canônica; o Charter não finge que essa migração técnica já ocorreu.

## Fronteira factual/humana

Este arquivo prova fatos da coleta de 2026-08-17 e registra a mudança humana de
escopo de 2026-08-23. Ele não prova resultados numéricos, prontidão econômica,
equivalência científica entre domínios ou a tese completa do TCC. Imports e CI
demonstram arquitetura/operação, não validade científica.

Para composição, objetivo e autorização, vale
[ECOSYSTEM_CHARTER.md](ECOSYSTEM_CHARTER.md). Para fatos mecânicos novos, é
necessária nova coleta contra os HEADs atuais.
