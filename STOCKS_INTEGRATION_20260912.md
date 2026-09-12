# Stocks: integração observada em 12/09/2026

Esta atualização corrige a representação de software do Stocks. Não recertifica
estados científicos históricos nem altera os demais domínios.

- Main Stocks observada: `938f646b82eb999ee4513ccad13b0c93cac310f0`; pacote 0.2.0,
  Core canônico 3.2.1. A declaração corrente 0.1.0 do project_registry era obsoleta.
- Candidato PR85: `2c91ff442d8aebe92c47ca5d8d1dc667a890a0fb`. Corrige inventário R8;
  o runtime científico tem os mesmos bytes da main. Checks finais são por SHA.
- CAIN consumidor: `5ba4177a11b9312900e5035517aa5ef25d509859`, árvore real executada
  em instância isolada, com dependências existentes. Instalação principal não atualizada.
- Snapshot novo: `c6d4cfa158416b2cc8ee09796d329e572aafdcdd4c7ae443dc8c1e6236bac4ab`.
  Importação/reimportação pela CLI, consulta/evidência, interface web e archive restore
  sem raízes do produtor demonstrados. Um relato parcial, sem modelo necessário.
- Bundle 1.0.0 ainda depende do candidato canônico Ecosystem
  `a9f6594c840482419d6c310f373813e0e71f17d0`, fora desta main. O pin no workflow Stocks
  torna essa dependência explícita. Não declarar os contratos Snapshot e Bundle equivalentes.
  A admissão do Bundle novo requer aprovação administrativa específica; sem ela o CAIN
  recusou com NOT_AUTHORIZED. Fontes B3 são referências, sem preços copiados/licença inferida.

Evidências locais: `C:/STOCKS/work/audit-main-20260912`, especialmente
`snapshot-e2e.json`, `local-checks.json` e os logs correspondentes.
O checker offline aprovado demonstra invariantes internas, não drift online dos
outros projetos. A conferência do Stocks compara pyproject/lock/HEAD atuais e os
campos de software declarados; os registros de releases continuam vinculados aos
seus artefatos históricos, não ao candidato. Não foi lançada nova release.

Os campos científicos anteriores do registry descrevem a fase histórica H1-H19;
não são uma declaração atualizada sobre H20-H22. Para estados científicos atuais,
a autoridade permanece nos protocolos e documentos do Stocks. Lucro e capital
não foram certificados por esta auditoria de integração.
