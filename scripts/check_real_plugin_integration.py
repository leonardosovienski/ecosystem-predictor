"""Fail-closed integration check for the three real domain distributions.

Run this only in an environment where cripto-predictor,
brasileirao-predictor and stocks-predictor are installed together.
"""

from ecosystem.registry import Registry

EXPECTED_DOMAINS = {
    "cripto": "crypto",  # public entry-point name is Portuguese; domain contract is English
    "brasileirao": "brasileirao",
    "stocks": "stocks",
}


def main() -> int:
    registry = Registry.discover()
    missing = set(EXPECTED_DOMAINS).difference(registry.records)
    if missing:
        raise SystemExit(f"missing real plugins: {sorted(missing)}")

    records = {name: registry.get(name) for name in EXPECTED_DOMAINS}
    for name, record in records.items():
        if record is None or not record.loaded:
            error = None if record is None else record.error
            raise SystemExit(f"plugin {name!r} failed to load: {error}")

    instances = [records[name].instance for name in sorted(EXPECTED_DOMAINS)]
    if len({id(instance) for instance in instances}) != len(instances):
        raise SystemExit("plugin identity collision: two domains loaded the same object")

    health = registry.health_snapshot()
    capabilities = registry.capability_snapshot()
    for name, expected_domain in EXPECTED_DOMAINS.items():
        if health[name].domain != expected_domain:
            raise SystemExit(f"health domain mismatch for {name!r}: {health[name].domain!r}")
        if capabilities[name].domain != expected_domain:
            raise SystemExit(f"capability domain mismatch for {name!r}: {capabilities[name].domain!r}")

    print("real plugin integration OK: cripto, brasileirao and stocks are isolated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
