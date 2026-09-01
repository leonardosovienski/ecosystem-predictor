# Fechamento de implementação e reauditoria — 2026-08-31

## Resultado honesto

As lacunas de engenharia executáveis identificadas na auditoria e na revisão v2.1
foram implementadas nos seis repositórios. Evidência que exige tempo, credencial,
ação humana ou mercado real permanece explicitamente pendente. Nenhum dado
prospectivo, entrevista, rotação de chave ou aprovação econômica foi fabricado.

O prompt v2.1 é uma revisão deliberada do prompt anexado: separa verificação
técnica `T0–T5` de maturidade econômica `E0–E5`, adiciona o gate de dataset e
remove a ambiguidade da antiga escala única `L1–L6`. O ledger histórico foi
migrado para esse schema em `PREDICTORS_EVIDENCE_LEDGER_V2_1.csv`, preservando
claims e resultados originais.

## Implementado e verificado

- **Core 3.0.0:** reduzido a primitivas científicas neutras; módulos sem segundo
  consumidor removidos. Suíte completa: **224 passed**. Wheel e sdist publicados
  em GitHub Release `v3.0.0`.
- **Ops 4.0.0:** reduzido ao runtime operacional genérico local; Redis, hash-chain,
  compatibilidade legada, auditoria de vendor e scripts transitórios removidos.
  Suíte completa: **66 passed**. Wheel e sdist publicados em `v4.0.0`.
- **Consumidores:** Crypto e Brasileirão agora exigem Core `>=3,<4` e Ops
  `>=4,<5`; Stocks exige Core `>=3,<4` e não instala/importa Ops decorativamente.
  URLs, hashes, CI e lockfiles apontam para artefatos publicados reais.
- **Namespaces:** Stocks usa `stocks_predictor`; Brasileirão usa
  `brasileirao_predictor` e `brasileirao_scripts`. Entrypoints e CI foram
  reconciliados.
- **Ecosystem:** reduzido a contratos e registry; o gate instala e descobre os
  três plugins reais conjuntamente, eliminando a colisão silenciosa de `src`.
- **Stocks/RJ:** empresas sem trough deixaram de desaparecer. Antes do horizonte
  são registradas como `censored`; depois, como `no_candidate_control`, sem
  fabricar trough. Migração SQL, persistência, relatório e teste foram adicionados.
- **Crypto/multiplicidade:** cada combinação do threshold grid é pré-registrada
  antes de executar, entrando no denominador de tentativas.
- **Crypto/H6:** o gate científico congelado `n>=30` foi preservado, mas o snapshot
  agora expõe meta de poder `n=250`, `h6_power_adequate` e bloqueio explícito de
  avaliação de capital enquanto a meta não for atingida.
- **Crypto/H7:** calendário oficial 2026 contém 8 FOMC, 12 CPI e 13 releases PPI;
  o `DXYProvider` foi revalidado ao vivo em 2026-08-31 e retornou cinco pontos
  recentes válidos do FRED.
- **Brasileirão/A1:** os gates existentes de sete dias consecutivos e auditoria
  manual de 50 eventos foram preservados. A rotação de `ODDSPAPI_KEY` passou de
  texto de política a critério mecânico, exigindo atestação sem armazenar segredo.

## Evidência externa ainda pendente

| Evidência | Estado correto | Condição de fechamento |
|---|---|---|
| H6 prospectiva | PENDENTE | amostra real atingir a meta de poder e passar o gate congelado |
| H7 econômica | PENDENTE | coorte prospectiva e veredito pré-registrado; calendário/provider não provam edge |
| A1 sete dias | PENDENTE | sete arquivos diários reais, consecutivos e aprovados |
| A1 auditoria humana | PENDENTE | `manual_audit.json` atestar pelo menos 50 eventos reais |
| A1 rotação de chave | PENDENTE | revogação/rotação no provedor e atestação por responsável |
| Entrevistas comerciais | PENDENTE | entrevistas reais e respostas preservadas como evidência |

Todos esses estados continuam com `capital_enabled=false`. “Código pronto” não foi
tratado como “hipótese econômica confirmada”.

## Validação desta rodada

- Core: 224 passed.
- Ops: 66 passed.
- Stocks: **243 passed**.
- Crypto: **832 passed, 2 skipped**; cinco warnings de depreciação do runner.
- Brasileirão: **873 passed, 1 skipped, 1 deselected**.
- Ecosystem: **35 passed**.

Uma suíte parcial ou um gate técnico não eleva por si só o nível econômico do
ledger. A decisão transversal continua: **nenhum domínio está autorizado para
capital real**.

## Conferência final independente

A releitura integral do ZIP original, do prompt anexado, da revisão v2.1 e dos
diffs revelou que a primeira declaração de fechamento foi prematura: quatro CIs
remotos falharam apesar das suítes locais verdes. As falhas foram reproduzidas,
explicadas e corrigidas antes deste relatório final:

- Crypto ainda tinha referências Core 2.3/Ops 3.1 no Dockerfile e no verificador
  de wheels; ambas foram migradas para Core 3.0/Ops 4.0.
- Brasileirão tinha estilo não normalizado após a troca de namespace e os dois
  Dockerfiles de Compose ainda copiavam `src`/`scripts`; agora usam os pacotes
  canônicos e as releases atuais.
- Ecosystem confiava em `[tool.uv.sources]` durante uma instalação feita por
  `pip`; o CI agora instala explicitamente as duas wheels compartilhadas antes
  dos três plugins reais.
- Ops tinha um teste incompatível com o tipo `Literal["local"]` e uma imagem
  Alpine sem atualização de segurança; o teste preserva a rejeição em runtime
  sem violar a checagem estática, e ambas as etapas da imagem executam upgrade.

Depois dessas correções, os commits finais de Core, Ops, Stocks, Crypto,
Brasileirão e Ecosystem ficaram com seus workflows relevantes verdes. A suíte
local consolidada permanece em **2.273 testes aprovados, 3 ignorados e 1
desselecionado**.

O workflow de release do Ops também foi reexecutado manualmente sobre o commit
final: lint, tipos, testes, auditoria de dependências, build, instalação isolada
e atestação passaram. A etapa de publicação foi corretamente ignorada por não se
tratar de uma nova tag; a release `v4.0.0` já publicada permanece a distribuição
canônica.

### Julgamento de adequação

As mudanças mantidas correspondem às recomendações executáveis do relatório:
redução dos pacotes compartilhados, eliminação da colisão de namespace,
integração real dos plugins, censura explícita no RJ, contagem de tentativas no
grid, transparência de poder em H6 e gates fail-closed em A1. Nenhuma hipótese
congelada foi relaxada e nenhuma evidência futura foi simulada.

Core 3.0.0 e Ops 4.0.0 usam versões maiores, embora o relatório mencionasse uma
linha menor, porque houve remoção pública de módulos e backends: semanticamente,
uma major version é a forma correta de comunicar essa quebra. Os campos de poder
de H6 são observacionais e não mudam o gate científico pré-registrado. A
atestação de rotação A1 é propositalmente mecânica e fail-closed, mas não afirma
que a rotação externa já ocorreu.

O prompt original dizia que a fase de auditoria não deveria modificar os
repositórios. Essa restrição foi respeitada enquanto o trabalho era análise; as
alterações posteriores decorreram das solicitações explícitas do usuário para
implementar tudo. Portanto, mantenho as mudanças técnicas finais. Não declaro
concluídas as evidências externas listadas acima.
