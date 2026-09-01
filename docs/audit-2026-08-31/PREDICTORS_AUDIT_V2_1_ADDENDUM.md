# Adendo de migração da auditoria para o protocolo v2.1

O pacote de auditoria original permanece um registro histórico imutável. Seus níveis
`L0–L6` não devem ser reescritos mecanicamente, porque a v2.1 separa dimensões que a
escala antiga misturava.

Para novas auditorias e novas linhas do ledger, usar:

`ID, Projeto, Claim, Fonte, Verificação, Dataset, Nivel_T, Nivel_E, Resultado, Status, Confiança`

- `Dataset`: `PRESENTE`, `PARCIAL`, `AUSENTE`, `INACESSÍVEL` ou `N/A`.
- `Nivel_T`: força da verificação técnica `T0–T5`.
- `Nivel_E`: maturidade econômica `E0–E5` ou `N/A`.

Não converter níveis antigos por tabela automática. Cada claim histórico deve ser
reclassificado apenas quando voltar a participar de uma decisão. Exemplo da correção
implementada nesta sessão:

- Claim: os três plugins reais podem ser instalados e descobertos juntos sem colisão.
- Dataset: `N/A`.
- Verificação técnica: `T5` — wheels reais instalados conjuntamente, discovery e
  identidade exercitados ponta a ponta.
- Maturidade econômica: `N/A`.
- Status anterior: `INVALIDADO`.
- Status após a correção local: `CONFIRMADO`, condicionado à publicação coordenada dos
  novos wheels.

O prompt normativo integral está em `AUDITORIA_ESTRATEGICA_PREDICTORS_PROMPT_v2.1.md`.
