# RUNBOOK_SECRET_INCIDENT.md

Procedimento para o incidente ativo (e para qualquer incidente futuro do
mesmo tipo). Sem nenhum valor secreto. Verificado 2026-07-18.

## Identificação (sem abrir o log)

```bash
python -c "
import sys; sys.path.insert(0, '.')
from tools.secret_redaction import scan_path
from pathlib import Path
r = scan_path(Path('previsao-cripto/logs/garimpo_fase1_20260713.log'))
print(r['occurrence_count'], r['kinds'])
"
```
Retorna só contagem e categoria (`sensitive_assignment`, `sensitive_url`,
etc.) — nunca o valor. Para saber o NOME do campo (não o valor, seguro de
exibir): usar `ASSIGNMENT.finditer(text)` e extrair só `match.group('key')`.
Para saber o host/path de uma URL sensível (nunca a query string): usar
`urlsplit(...).scheme/netloc/path`, nunca `.query`.

## Contenção

1. Confirmar que os arquivos afetados nunca entraram no Git:
   `git check-ignore -v <arquivo>` (deve mostrar a regra que os ignora) e
   `git ls-files <arquivo>` (deve retornar vazio).
2. Confirmar a causa raiz no código (ver seção "Causa raiz" abaixo) e que
   já foi corrigida.
3. Verificar a correção com credencial **sintética** (nunca real) — ver
   `previsao-cripto/tests/test_ops_hardening.py`.

## Causa raiz (deste incidente específico)

`GarimpoInvestimentos/collectors/serpapi_news.py` passa a chave como
parâmetro de query HTTP. Uma exceção de rede (`httpx`) embute a URL
completa (com a chave) em `str(exc)`. Antes de `737d97d`/`8055667`
(2026-07-17), essa exceção chegava a `log.warning(...)` sem redação. Hoje,
`_RedactSecrets` (filtro de logging) aplica `tools.secret_redaction` a
toda mensagem antes de persistir — verificado funcionando com credencial
sintética e com evidência de produção real (log de 2026-07-18 limpo).

## Rotação (só ação humana, fora deste workspace)

1. Acessar o painel do provedor (SerpAPI).
2. Revogar/rotacionar a chave exposta.
3. Confirmar que a chave antiga retorna 401/403 numa chamada de teste.
4. Configurar a chave nova pelo mecanismo já usado pelo projeto (variável
   de ambiente / config local ignorada pelo Git — nunca hardcoded em
   arquivo versionado).

## Validação pós-rotação

Rodar um ciclo real de `GarimpoFase1` (o próximo ciclo agendado natural já
serve) e confirmar `LastTaskResult=0` + heartbeat `SUCCEEDED`. Rodar o
scanner seguro (seção "Identificação") contra o log do dia — deve retornar
`0` ocorrências de `api_key`/`sensitive_url` relacionadas à SerpAPI.

## Invalidação da credencial anterior

Confirmar explicitamente (não presumir) que a chave antiga não funciona
mais — uma chamada de teste com ela deve falhar.

## Tratamento dos logs históricos

5 arquivos afetados: `garimpo_fase1_20260713.log` a `_17.log`. Nunca
entraram no Git. Opções, do menor para o maior impacto:
(a) manter como estão — depois da rotação, o valor neles é uma credencial
    revogada, inofensiva;
(b) sanitizar in-place: `python -m tools.secret_redaction sanitize
    <arquivo> --replace --confirm-replace` (ferramenta já existe, testada,
    nunca imprime o valor);
(c) remover os arquivos.
Decisão é do responsável humano, registrada em
`SECURITY_INCIDENT_SECRET_ROTATION.md`.

## Scan sanitizado (evidência para o encerramento)

Reexecutar o scanner seguro (seção "Identificação") contra os logs
afetados + o log mais recente, registrar os números (sem valores) no
documento de incidente.

## Evidência a registrar no encerramento

Data, responsável, confirmação de que a chave antiga foi revogada,
confirmação de que a chave nova funciona, decisão tomada sobre os logs
históricos, resultado do scan sanitizado pós-rotação.

## Critério de encerramento

Ver `SECURITY.md`, seção "Critérios de encerramento de um incidente" —
não declarar resolvido sem os 6 itens confirmados.
