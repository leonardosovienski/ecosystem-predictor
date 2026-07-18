# SECURITY.md

Política de segurança do ecossistema. Verificado em 2026-07-18. Nenhum
valor de segredo aparece neste documento.

## Política de segredos

- Segredos vivem em configuração local ignorada pelo Git (variáveis de
  ambiente / arquivo de config local), nunca em código, nunca em Markdown,
  nunca em commit.
- `tools.secret_redaction` é o mecanismo canônico de redação — toda
  persistência de log deve passar por ele antes de gravar.
- Nenhum consumidor deve manter regex ou lista de nomes sensíveis própria
  — sempre delegar a `tools.secret_redaction`.

## Armazenamento permitido

Variáveis de ambiente do processo, arquivos `.env`/config locais
explicitamente listados no `.gitignore` de cada projeto. Nunca em
`data/`, `docs/`, ou qualquer caminho versionado.

## Arquivos proibidos no Git

`.env`, qualquer arquivo de log operacional (`logs/`), bancos de dados
(`*.db`), dumps de debug, saída de scanner de segredo contendo o valor
encontrado (só metadados — contagem, categoria, nome de campo — podem
aparecer em documentação).

## Redação

`tools/secret_redaction.py`:
- `redact_text`/`safe_redact_text`: nunca levanta exceção, degrada para
  `[REDACTED]`/`REDACTION_FAILED`.
- `redact_mapping`/`safe_redact_mapping`: trata dicts aninhados, listas,
  chaves que contenham um valor sensível conhecido.
- `scan_path`: varredura segura — retorna só contagem e categoria do
  padrão (`sensitive_assignment`, `sensitive_url`, `bearer`,
  `authorization_header`, `known_value`), **nunca o valor capturado**.
- ReDoS corrigido em 2026-07-17 (`ASSIGNMENT` regex, bound de 128
  caracteres) — verificado com escala linear até 160KB.

## Subprocessos e exceções

Mensagens de exceção de bibliotecas HTTP (ex.: `httpx`) podem embutir a
URL completa da requisição, incluindo query params sensíveis — já houve
um incidente real disso (ver `SECURITY_INCIDENT_SECRET_ROTATION.md`).
Qualquer `logger.warning`/`.error` que logue uma exceção de rede deve
passar pelo filtro `_RedactSecrets`/`safe_redact_text` antes de persistir.

## Git

Nenhum arquivo com segredo real deve nunca ser adicionado ao índice.
Antes de `git add`, revisar `git status`/`git diff` para confirmar que
nenhum arquivo de log/config local está sendo incluído por engano.

## Resposta a incidente

1. Identificar escopo real (quais arquivos, sem abri-los em texto bruto —
   usar `tools.secret_redaction.scan_path` para contagem/categoria).
2. Confirmar que o vazamento nunca entrou no Git (`git ls-files`/
   `git check-ignore`).
3. Corrigir a causa raiz no código (redação ausente/incompleta).
4. Verificar a correção com credencial **sintética**, nunca real.
5. Documentar em `SECURITY_INCIDENT_SECRET_ROTATION.md` (ou equivalente),
   sem incluir nenhum valor.
6. Ação humana: revogar/rotacionar a credencial real no provedor —
   nenhuma ferramenta local pode fazer isso.
7. Decidir o destino de qualquer log histórico afetado.

## Rotação

Sempre no provedor da credencial, nunca localmente. Nenhuma ferramenta
deste workspace tem ou deveria ter acesso a painéis de provedor externo.

## Retenção

Logs que nunca entraram no Git (gitignored) não exigem ação de retenção
por si só — decisão de manter/sanitizar/remover é do responsável pelo
projeto, registrada no documento de incidente específico.

## Responsáveis

O responsável humano pelo workspace decide rotação, retenção e
priorização de qualquer incidente. Nenhuma automação decide isso sozinha.

## Exemplos sintéticos

Testes de redação usam sempre valores fictícios
(`sk-FAKE-SECRET-TESTE-...`, `fake_api_key_123456789`) — nunca uma
credencial real, mesmo revogada.

## Critérios de encerramento de um incidente

Só é `RESOLVED` quando houver evidência humana de: credencial antiga
revogada/inválida, credencial nova configurada por mecanismo seguro,
ciclo real validado, decisão tomada sobre qualquer log histórico. Até lá,
o estado correto é `BLOCKED_PENDING_SECRET_ROTATION` (ou equivalente), não
"resolvido" nem "dívida técnica menor".

## Incidente ativo

Ver [SECURITY_INCIDENT_SECRET_ROTATION.md](SECURITY_INCIDENT_SECRET_ROTATION.md).
