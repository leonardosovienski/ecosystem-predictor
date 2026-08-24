# Handoff corrente do PREDICTORS — 2026-08-24

Este é o ponto de retomada corrente após a reconciliação P0/P1. Documentos anteriores permanecem preservados como histórico e não devem ser reescritos para parecer atuais.

## Autoridade e escopo

A ordem de leitura é:

1. `ECOSYSTEM_CHARTER.md` — decisão humana sobre os seis projetos, papéis e objetivo;
2. `PREDICTOR_CONTRACT.md` — contrato comum dos predictors e estados globais;
3. `ECOSYSTEM_MECHANICAL_STATE.md` + `audit/canonical-ecosystem-facts.json` — fatos mecânicos correntes;
4. README/current-state/HANDOFF do domínio analisado;
5. código, dados, commits e CI no ref correspondente.

Os seis projetos canônicos são `ecosystem-predictor`, `core-predictor`, `predictor-ops`, `cripto-predictor`, `brasileirao-predictor` e `stocks-predictor`. Os três últimos são predictors econômicos.

## Estado arquitetural após P1

- Core compartilhado: linha 2.3.x;
- Ops compartilhado: linha 3.1.x;
- Cripto, Brasileirão e Stocks declaram Python `>=3.13,<3.15` e consomem Core/Ops por dependência moderna;
- os três predictors publicam adapter em `[project.entry-points."predictor.plugins"]`;
- o Ecosystem coleta mecanicamente esses entry-points no snapshot canônico;
- `PREDICTOR_CONTRACT.md` e `src/ecosystem/contracts/` separam ciência, predição, economia, operação e permissão de capital;
- ausência de estado falha fechada e `NO_OPPORTUNITY` é resultado válido;
- compatibilidade arquitetural não promove hipótese nem comprova lucro.

## Estados de alto nível conhecidos

Estes são apenas pontos de partida documentais para nova auditoria; não devem ser aceitos sem reproduzir a evidência:

- Cripto: H6 ativa/imatura; histórico econômico principal contém NO-GOs; `PROSPECTIVE_OBSERVATION`; capital proibido;
- Brasileirão: existe evidência documentada de skill preditiva vs. climatologia, mas validação econômica/prospectiva continua separada e houve gargalos operacionais registrados para H9;
- Stocks: linha ativa `predictor-rj`, ainda em estágio inicial de validação real; domínio cross-sectional anterior permanece histórico; capital proibido.

## Dívidas que NÃO devem ser confundidas com P0/P1

- verificar cientificamente, do zero, cada hipótese e resultado dos três predictors;
- distinguir skill preditiva de edge econômico;
- reconstruir coortes prospectivas e settlement sem hindsight;
- testar custos, preços disponíveis e liquidez quando aplicável;
- provar uso efetivo de Core/Ops onde o domínio diz consumi-los;
- confirmar que o estado operacional real corresponde ao que está versionado;
- manter histórico datado, mas corrigir qualquer documento que se apresente como corrente e contradiga fatos atuais.

## Regra para próxima auditoria

Não confiar em README, HANDOFF, Charter, trial registry, relatório, teste verde ou comentário por autoridade própria. Cada afirmação é um claim. Classificar como `CONFIRMED`, `PROVISIONAL`, `CONFLICT`, `MISSING_EVIDENCE`, `RISK` ou `OPEN_QUESTION` e buscar evidência primária no código, dados, commits, CI e artefatos reproduzíveis.

Nenhum resultado desta reconciliação autoriza capital real.
