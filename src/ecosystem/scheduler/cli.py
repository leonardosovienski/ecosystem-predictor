from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ecosystem.scheduler import run_probe_domains


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ecosystem-scheduler")
    parser.add_argument("job", choices=["probe-domains"])
    parser.add_argument("--runtime-root", type=Path, default=Path(".ecosystem-runtime"))
    args = parser.parse_args(argv)

    if args.job == "probe-domains":
        return run_probe_domains(runtime_root=args.runtime_root)
    return 1


if __name__ == "__main__":
    sys.exit(main())
