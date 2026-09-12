# Verificação de uma combinação candidata de wheels

O verificador original exige proveniência VCS para consumidores candidatos e usa
um manifesto fixo. Uma wheel construída e instalada separadamente tem identidade
de arquivo, e não `vcs_info.commit_id`; a versão nominal não basta para verificá-la.

`scripts/check_real_plugin_integration.py --manifest CAMINHO` aceita um manifesto
separado para a combinação em avaliação. Cada consumidor deve declarar a versão
e `wheel_sha256` com 64 caracteres hexadecimais minúsculos, ou um commit Git
completo para o modo VCS existente. O hash deve coincidir com a proveniência
`archive_info.hashes.sha256` gravada pelo instalador. Ausência de proveniência,
versão diferente ou hash diferente provoca recusa antes de carregar os plugins.

O arquivo de manifesto e seu SHA256 entram no recibo configurado por
`COMPATIBILITY_RECEIPT`. A origem Git e o processo de construção de cada wheel
devem ser demonstrados nos recibos de build da combinação; um hash de arquivo
sozinho não prova a origem do código.

O modo sem argumento conserva o manifesto corrente. `RELEASED_WHEELS=1` conserva
a conferência do registro de releases e não aceita um manifesto candidato.
Nenhum registro de release ou evidência histórica é substituído para verificar
um candidato novo. Health, capabilities, estados de domínio, hashes dos pacotes
compartilhados e isolamento dos três plugins mantêm suas verificações.

Na auditoria Crypto de 12/09/2026, a instalação inicial com uv não gravou hashes
em `direct_url.json` para essas wheels. O verificador recusou essa instalação.
Uma reinstalação real com pip, usando URLs com SHA256 explícito, registrou os
hashes e permitiu a conferência. Não edite `direct_url.json` para fabricar provas.

Validação local: 68 testes do Ecosystem; Ruff; invariantes offline; três plugins
reais instalados; recusa discriminante de um hash Crypto incorreto. Esta evidência
não substitui a CI do commit entregue nem certifica resultados econômicos.
