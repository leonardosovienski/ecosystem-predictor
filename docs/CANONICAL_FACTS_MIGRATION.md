# Migração do inventário mecânico canônico

A reconciliação F1 de 2026-08-17 usava `scripts/sync_ecosystem_facts.py` e `audit/ecosystem-facts.json` para nove repositórios. Após a decisão humana de 2026-08-23, esse universo deixou de representar o escopo canônico.

O inventário corrente passa a ser:

- `ECOSYSTEM_MECHANICAL_STATE.md`;
- `audit/canonical-ecosystem-facts.json`;
- `scripts/sync_canonical_ecosystem_facts.py`.

O coletor novo contém exatamente os seis nomes definidos no Charter. Ele falha se o snapshot não contiver exatamente os seis, registra Stocks na forma técnica que existe hoje (requirements/Core vendorizado/sem Ops declarado) e não tenta inferir promoção arquitetural.

O coletor anterior e seu snapshot não são apagados: permanecem como evidência da F1 e não são mais usados pela CI corrente.
