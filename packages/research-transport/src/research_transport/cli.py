"""`predictor-research-consumer`: deliver the spooled V2 tasks of one domain to its adapter, once.

    predictor-research-consumer --domain crypto --spool DIR --ledger FILE
                                --state DIR --policy FILE --objects DIR

``--state/--policy/--objects`` are the domain operator's arguments of the adapter_api (``Circuit(state,
policy, objects)`` in the three contracts); they are passed to the adapter unchanged and never come from a
task. One JSON line per task file on stdout, and nothing else: while the domain works, file descriptor 1 is
redirected to stderr, so logs a domain writes to stdout (in-process handlers or child processes) never mix
with the report. Exit code: 0; 2 if a task file was rejected; 5 if a task is held for a human (the consumer
stops trusting it: byte identity, adapter bytes, or an invalid domain outcome); 6 if another consumer of the
domain is running (one line ``{"action": "busy", "code": "CONSUMER_BUSY"}``; nothing read, sent or
published); 1 for a configuration error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from research_transport.adapters import AdapterUnavailable, load
from research_transport.consumer import Consumer, ConsumerBusy
from research_transport.spool import Spool


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="predictor-research-consumer", description=(__doc__ or "").splitlines()[0]
    )
    parser.add_argument("--domain", required=True)
    parser.add_argument("--spool", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--objects", type=Path, required=True)
    args = parser.parse_args(argv)
    sys.stdout.flush()
    saved_stdout = sys.stdout
    report_fd = os.dup(1)
    os.dup2(2, 1)  # file descriptor 1: handlers bound earlier and child processes
    sys.stdout = sys.stderr  # Python level: print and handlers created while the domain works
    try:
        return _run(args, report_fd)
    finally:
        sys.stdout.flush()
        sys.stdout = saved_stdout
        os.dup2(report_fd, 1)
        os.close(report_fd)


def _run(args, report_fd: int) -> int:
    def report(value: dict) -> None:
        line = json.dumps(value, sort_keys=True, ensure_ascii=False) + "\n"
        os.write(report_fd, line.encode("utf-8"))

    try:
        adapter = load(args.domain)
    except AdapterUnavailable as exc:
        print(json.dumps({"error": exc.code, "detail": str(exc)}), file=sys.stderr)
        return 1
    config = {"state": str(args.state), "policy": str(args.policy), "objects": str(args.objects)}
    consumer = Consumer(args.domain, Spool(args.spool), args.ledger, adapter, config)
    try:
        lines = consumer.run_once()
    except ConsumerBusy as exc:
        report({"action": "busy", "code": exc.code, "domain": args.domain})
        return 6
    code = 0
    for line in lines:
        report(line)
        if line["action"] == "rejected":
            code = max(code, 2)
        elif line["action"] == "held":
            code = max(code, 5)
    return code


if __name__ == "__main__":
    sys.exit(main())
