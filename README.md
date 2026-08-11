# Predictor ecosystem

Ponto de entrada factual, verificado em **2026-08-11**. Este repositório é a
plataforma agregadora e a fonte de governança do ecossistema; não é um monorepo
dos domínios.

Para retomar o trabalho, leia nesta ordem:

1. [ECOSYSTEM_CURRENT_STATE.md](ECOSYSTEM_CURRENT_STATE.md) — inventário
   mecânico, refs, dependências e CI no HEAD;
2. [ECOSYSTEM_HANDOFF.md](ECOSYSTEM_HANDOFF.md) — continuidade e limites de
   autorização;
3. [PENDENCIAS_ABERTAS.md](PENDENCIAS_ABERTAS.md) — pendências factuais que
   ainda exigem decisão;
4. [P4_CONSOLIDATION.md](P4_CONSOLIDATION.md) — contrato temporal comparado,
   decisão sobre Core, proveniência e limites da P4;
5. [TCC_EVIDENCE_CLOSURE.md](TCC_EVIDENCE_CLOSURE.md) — contribuições,
   alegações permitidas e limitações acadêmicas;
6. o README/HANDOFF do repositório que será analisado;
7. Git e código no ref registrado.

## Arquitetura atual

```text
core-predictor 2.2.x ─┐
                      ├─ wheels versionados ─> consumidores ativos
tools-predictor 3.0.0 ┘

ecosystem-predictor ───> registry, gateway, scheduler e infraestrutura própria

wc-predictor ──────────> projeto histórico encerrado, com Core legado vendorizado
```

- [core-predictor](https://github.com/leonardosovienski/core-predictor) é o
  pacote científico compartilhado instalável. A release corrente observada é
  `2.2.1`.
- [tools-predictor](https://github.com/leonardosovienski/tools-predictor) é o
  pacote operacional compartilhado instalável `predictor-ops`. A release
  corrente observada é `3.0.0`.
- [ecosystem-predictor](https://github.com/leonardosovienski/ecosystem-predictor)
  contém registry, gateway, scheduler, storage e contratos da plataforma. No
  HEAD desta migração preserva Core `2.1.0` e consome Ops `3.0.0`, com estado
  operacional (`RunStatus`) separado de `scientific_state` opaco.
- Brasileirão, Cripto, CS, F1 e LoL consomem wheels oficiais por URL e lockfile.
  A versão exata varia conforme a matriz factual.
- WC permanece encerrado e vendorizado. A F1 não propõe modernização.

Não há importação direta entre domínios demonstrada por esta arquitetura. A
presença de um import compartilhado também não constitui prova científica.

## Repositórios no escopo corrente

| Repositório | Papel | Ref verificado em 2026-08-11 |
|---|---|---|
| `ecosystem-predictor` | plataforma e governança | commit deste documento |
| `core-predictor` | Core científico compartilhado | `main@7933e4aca0ce` |
| `tools-predictor` | Ops operacional compartilhado | `main@3ca6995e3be1` |
| `brasileirao-predictor` | domínio | `main@5a42d6c88298` |
| `cripto-predictor` | domínio | `main@375fe6df903e` |
| `cs-predictor` | domínio | `main@f7bb21411450` |
| `f1-predictor` | domínio | `main@d6e54cc9997b` |
| `lol-predictor` | domínio | `main@17425a75101c` |
| `wc-predictor` | histórico encerrado | `main@40fe5135d14a` |

`stocks-predictor` e `nba-predictor` estão fora do escopo desta linha de
trabalho. Menções em documentos históricos não os reinserem no inventário.
`Claude` é snapshot histórico não canônico.

## Estado verificável

O estado completo — incluindo Python, Core/Ops, forma de consumo, termos
declarados por cada domínio e URLs das execuções de CI — está em
[ECOSYSTEM_CURRENT_STATE.md](ECOSYSTEM_CURRENT_STATE.md). O resumo é:

- CI verde e concreta no HEAD dos oito repositórios que possuem workflow;
- WC sem workflow, de modo coerente com seu papel histórico;
- Core `2.2.1` e Ops `3.0.0` são as releases correntes observadas;
- CS já consome Core `2.2.1`; os demais domínios ativos consomem `2.2.0`;
- a própria plataforma preserva Core `2.1.0` e consome Ops `3.0.0`;
- nenhuma conclusão científica ou econômica foi reproduzida nesta F1.

## F0 encerrada

A F0 corrigiu exclusivamente a integridade dos wheels do
`brasileirao-predictor`, preservando Core `2.2.0` e Ops `3.0.0`. O merge em
`main` é `5a42d6c882985ef06ba1bb8056201d4d95436626`, e a execução pós-merge
[31462565846](https://github.com/leonardosovienski/brasileirao-predictor/actions/runs/31462565846)
terminou com sucesso. A F1 não reabre nem amplia essa implementação.

## P4 encerrada sem mudança no Core

Os pilotos temporais F1, LoL e CS e sua consolidação foram concluídos. O estado
aprovado é `P4_COMPLETED_NO_CORE_CHANGE`. `PredictionPoint` e `replay` já
cobrem o contrato comum pertencente ao Core; cutoff, disponibilidade do
resultado, identidade, vínculos, métricas e seleção de hashes permanecem
locais. Canonicalização/hash foi classificada como padrão reutilizável, ainda
não como API pública madura. Consulte [P4_CONSOLIDATION.md](P4_CONSOLIDATION.md).

A matriz CS mantém uma dívida factual: pytest do job remoto rotulado 3.14
executou em 3.13.13; apenas o smoke do wheel usou 3.14.5. A P4 não comprovou
qualidade científica, equivalência estatística, valor econômico ou operação
ao vivo.

## Comandos oficiais deste repositório

O ambiente está travado por `uv.lock`; a CI usa Python 3.13 e 3.14.

```bash
uv sync --locked --all-extras --python 3.13
uv run ruff check src tests
uv run ruff format --check src tests
uv run pyright
uv run coverage run -m pytest -q
uv run coverage report --fail-under=0
uv build
```

Compose, container e smoke são definidos em
[`.github/workflows/ci.yml`](.github/workflows/ci.yml). Executá-los pode exigir
Docker; o fato de constarem no workflow não equivale a execução local.

## Fontes correntes e arquivo histórico

As fontes correntes são este README, `ECOSYSTEM_CURRENT_STATE.md`,
`ECOSYSTEM_HANDOFF.md`, `PENDENCIAS_ABERTAS.md` e `P4_CONSOLIDATION.md`. A classificação editorial
que fundamentou a F1 está em
[F1_SECTION_CLASSIFICATION.md](F1_SECTION_CLASSIFICATION.md).

Documentos `FINAL_*`, `FECHAMENTO_*`, `VEREDITOS_*`, `BLOQUEIOS_*`, o
inventário de artefatos e os runbooks antigos foram preservados como registros
históricos. Seus números e resultados não foram recalculados. Quando houver
conflito temporal, o estado corrente deve ser obtido do código/Git no ref
registrado; o documento histórico continua válido somente para sua data.

## Limites

CI verde demonstra os checks que o workflow executou, não prontidão para
capital, validade de hipótese ou reprodução de dataset/resultado. Decisões de
Uma promoção adicional para Core/Ops, alteração de dependências, novo piloto
ou qualquer implementação adicional exige decisão humana separada. O
encerramento da P4 não autoriza P2, P3, P5 ou P6.
