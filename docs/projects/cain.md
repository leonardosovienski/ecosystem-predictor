# CAIN — consumo de evidências e acesso

Ficha do Ecosystem revisada em 13/09/2026. [Mapa e estado atual](../../CURRENT_STATE.md).

## Responsabilidade e limites

Assistente local independente, consumidor de evidências admitidas. Organiza
consulta, referências, histórico e recuperação; não se torna autoridade sobre
a ciência dos produtores ou modifica suas fontes.

## Interfaces, dependências e consumidores

Recebe ResearchSnapshotV1 e ResearchBundleV1 em uma raiz de importação explícita.
Os contratos são distribuídos separadamente pelo Ecosystem. Grants delimitam
usuário, coleção, produtor, fontes e política; geração é uma permissão separada.
Produz registros recebidos, consultas e recibos com proveniência. Revogação
restringe conteúdo derivado; reimportação é idempotente. Não requer predictor
instalado nem dependência direta do Core para consultar evidências recebidas.

## Componentes e capacidades principais

O assistente também oferece conversa, preferências e memória de contexto,
projetos/documentos e workflows retomáveis. Há superfícies API, CLI, web e MCP;
consulte README e `pyproject.toml` oficiais. Elas não são funcionalmente
equivalentes: MCP oferece pesquisa com escopo fixo. A instalação e a main podem
avançar separadamente; código local não publicado não é combinação homologada.

## Fontes e integração comprovada

[Repositório e documentação oficial](https://github.com/leonardosovienski/cain)
· [README oficial](https://github.com/leonardosovienski/cain/blob/main/README.md).
As URLs em `main` dão acesso ao presente do proprietário; a evidência datada abaixo
identifica a revisão efetivamente testada.

O CAIN fixado no [manifesto](../../registries/compatibility_candidate.json) foi
exercitado isoladamente na [integração Core](../../CORE_INTEGRATION_20260913.md).
Os percursos datados [Cripto](../../CRYPTO_INTEGRATION_20260912.md),
[Brasileirão](../../BRASILEIRAO_INTEGRATION_20260912.md) e
[Stocks](../../STOCKS_INTEGRATION_20260912.md) conservam combinações próprias.
Esses recibos não identificam automaticamente o pacote operacional atual.
Consulte o [estado oficial da instalação](https://github.com/leonardosovienski/cain/blob/main/ESTADO_DO_PROJETO.md)
e a [continuidade](https://github.com/leonardosovienski/cain/blob/main/CONTINUIDADE.md).
Extração literal e transporte validados não certificam interpretação causal,
qualidade geral de modelos ou permissão de capital.
