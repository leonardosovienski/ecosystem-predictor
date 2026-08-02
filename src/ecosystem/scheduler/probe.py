"""The actual subprocess body invoked by ``probe_domains_job`` - discovers
the registry fresh (a new process, so a domain fixed since the last probe
is picked up without restarting the gateway) and prints a JSON health
snapshot to stdout for the caller (or predictor_ops's own log capture) to
persist."""

from __future__ import annotations

import json
import sys

from ecosystem.registry import Registry
from ecosystem.settings import get_settings


def main() -> int:
    settings = get_settings()
    registry = Registry.discover(group=settings.plugin_group)
    snapshot = {name: report.model_dump(mode="json") for name, report in registry.health_snapshot().items()}
    print(json.dumps(snapshot, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
