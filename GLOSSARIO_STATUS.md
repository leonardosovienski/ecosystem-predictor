# GLOSSÁRIO DE STATUS CIENTÍFICO E OPERACIONAL

Documento único recomendado por `audit/13_FINAL_VERDICT.md` (item B-02) e
registrado como pendência OP-3 em `PENDENCIAS_ABERTAS.md`. Criado em
2026-07-19. Define formalmente os termos já usados de forma consistente
nos documentos do ecossistema — este glossário **classifica**, não
substitui, a análise quantitativa que sustenta cada rótulo.

Versionado neste repositório; alterações seguem o fluxo de errata da
seção 4 (não destrutivo — histórico nunca é apagado).

---

## 1. Vereditos científicos de hipótese

Aplicam-se a hipóteses pré-registradas (H1, H4, H5, H8 etc.) julgadas
contra critério estatístico definido **antes** da coleta.

| Termo | Definição | Exemplo real |
|---|---|---|
| **COMPROVADA** | O critério pré-registrado foi atingido com a amostra prevista; o efeito sobrevive ao teste definido a priori. Autoriza adoção no serving do domínio. | Governança N+1 no cs-predictor (a=0,68 achata; serving calibrado `elo-platt-fase1`) |
| **REFUTADA** | O critério pré-registrado foi testado com amostra suficiente e falhou. A hipótese é encerrada; o serving permanece como estava. | Platt N+1 no lol-predictor (DM p=0,36) |
| **NÃO COMPROVADA** | Julgada na janela prevista sem atingir o critério, sem evidência suficiente para refutação definitiva. Encerra a rodada; reabrir exige nova pré-registro. | H4/H5 do predictor-stocks (H5 com IC inteiramente adverso) |
| **INCONCLUSIVA** | A amostra ou o desenho não permitem veredito em nenhuma direção. Não encerra a hipótese; a coleta ou o desenho precisam mudar. | — |

Regras:

- Nenhum veredito é emitido antes da janela ou amostra pré-registrada
  (ex.: H8-F1 exige `H8_REQUIRED_RACES=15`; H5-cripto tem janela 28/07).
- Veredito não é retroativamente editado — correções entram como errata
  (seção 4).

## 2. Gates operacionais

| Termo | Definição |
|---|---|
| **GO** | Gate liberado: os critérios objetivos do gate (amostra, calibração, infraestrutura) foram verificados e a operação/decisão econômica pode prosseguir. |
| **NO-GO** | Gate fechado: pelo menos um critério objetivo não foi atingido. Não é veredito científico sobre o modelo — é bloqueio operacional reavaliável quando o critério mudar. |
| **GO/NO-GO** | O ponto de decisão em si (o gate), com critérios definidos antes da avaliação. |

## 3. Classificações de pendência

Vocabulário canônico de `PENDENCIAS_ABERTAS.md` — nunca misturadas num
mesmo item:

| Termo | Definição |
|---|---|
| `OPEN_SECURITY_INCIDENT` | Incidente de segurança confirmado, ainda não encerrado. |
| `OPEN_BUG` | Bug de código reproduzido e ainda não corrigido. |
| `BLOCKED_EXTERNAL_ACTION` | Só avança com ação humana ou externa (credencial, provedor, decisão do operador). |
| `OPEN_OPERATIONAL_GAP` | Lacuna operacional real, não investigada ou não resolvida, sem bug associado. |
| `OPEN_SCIENTIFIC_GAP` | Governança de pesquisa em andamento (amostra, janela, fonte de dados); aguardar é o comportamento correto. |
| `OPEN_DOCUMENTATION_GAP` | Falta documento ou definição formal; código e prática estão corretos. |
| `SHARED_BUT_INCUBATING` | Capacidade duplicada em 2+ domínios, ainda não promovida ao core por decisão explícita. |
| `DOMAIN_LOCAL` | Pertence legitimamente a um domínio; promover seria abstração errada. |
| `CORRECTLY_DEFERRED` | Analisado e adiado conscientemente, com justificativa registrada e condição de reabertura. |
| `NOT_CONFIRMED` | Alegação de rodada anterior sem evidência verificável no workspace. |
| `REJECTED` | Não objetivo deliberado; fazer causaria mais dano que benefício. |
| `RESOLVED_AND_VERIFIED` | Corrigido E verificado de forma independente (teste, execução real ou inspeção direta). |

## 4. Processo de errata (não destrutivo)

1. Documento histórico **nunca** é reescrito para "sempre ter estado
   certo". A correção entra como nota datada (`**Atualização AAAA-MM-DD**`
   ou seção de errata) no próprio documento, ou como reclassificação em
   `PENDENCIAS_ABERTAS.md` (padrão da seção 8, `NOT_CONFIRMED`).
2. Toda errata cita a evidência que motivou a correção (comando, teste,
   commit, arquivo).
3. Contagens e fatos corrigidos registram o valor antigo e o novo
   (ex.: "114→115").
4. Reclassificar um item exige trocar o rótulo inteiro — nunca manter
   dois rótulos simultâneos.
5. O Git do repositório raiz preserva o histórico integral; nenhuma
   errata usa rebase, squash ou force-push.
