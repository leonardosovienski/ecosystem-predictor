"""Fixtures of the V2 envelope tests."""

from __future__ import annotations

import copy

import pytest
from vectors import REQUESTS


@pytest.fixture(params=sorted(REQUESTS))
def domain(request) -> str:
    return request.param


@pytest.fixture
def request_for():
    return lambda domain: copy.deepcopy(REQUESTS[domain])
