# Segurança do Ecosystem

Política reconciliada em 13/09/2026 com o registry opcional e os contratos de transporte.

Segredos pertencem à configuração local ignorada pelo Git ou ao ambiente do
proprietário. Nunca devem entrar em código, documentação, recibos ou publicações.
O Ecosystem não depende do antigo namespace `tools.secret_redaction` do Ops.

## Exceções e diagnósticos

O registry não registra nem devolve mensagens de exceções de plugins: conserva
somente o nome do tipo em falhas de carga, health e capabilities. Isso evita
persistir URLs, tokens ou conteúdo de entradas presentes nas mensagens, inclusive
erros de validação. Não registrar `str(exc)`, traceback ou `exc_info` nessas
fronteiras. Testes usam exclusivamente marcadores sintéticos.

Payloads de produtores são preservados pelo diagnóstico V2; isso não é um
sanitizador geral. Produtores devem fornecer payloads sem segredos. Identidades
de entry points e nomes de tipos também devem ser metadados públicos do pacote.

## Transporte e publicação

Admissão explícita, hashes e confinamento de caminhos delimitam a exportação.
As verificações do exportador de Bundle são locais ao contrato, não uma promessa
de detectar todo segredo arbitrário. Não exportar configurações, bancos ou logs
operacionais como documentos. A revisão da fonte admitida permanece necessária.

## Verificação e incidentes

A CI executa Gitleaks. Relatórios compartilhados devem conter somente categorias,
quantidades e referências, nunca valores encontrados. Não usar credenciais reais
em testes. Antes de publicar, conferir arquivos e diff para impedir a inclusão
acidental de configuração local.

Em incidente, interromper a publicação afetada, delimitar o objeto, corrigir a
origem e testar com conteúdo sintético. A rotação ocorre no provedor pelo
responsável autorizado; registrar a resolução sem repetir o segredo.

`SECURITY_INCIDENT_SECRET_ROTATION.md` é evidência histórica, marcada SUPERSEDED
em 03/09/2026. Sua referência não significa incidente ativo nesta revisão.
