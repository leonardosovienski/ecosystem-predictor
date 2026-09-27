"""Qualification fault injection at the consumer edge (inactive without the variable).

``PREDICTOR_RESEARCH_TRANSPORT_FAULT=<point>`` makes the consumer process die at that point with exit code
86 and no cleanup, the same convention as the domains' ``research_faults``.
"""

from __future__ import annotations

import os

ENV = "PREDICTOR_RESEARCH_TRANSPORT_FAULT"
EXIT_CODE = 86
POINTS = frozenset({"before_domain", "after_domain_before_result_write", "after_result_write"})


def fault(point: str) -> None:
    if point not in POINTS:
        raise ValueError(f"unknown fault point {point!r}")
    if os.environ.get(ENV) == point:
        os._exit(EXIT_CODE)
