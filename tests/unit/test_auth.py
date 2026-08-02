from __future__ import annotations

import jwt
import pytest
from fastapi import HTTPException

from ecosystem.gateway.auth import _decode


def test_valid_token_decodes_to_principal(settings, token_factory):
    principal = _decode(token_factory(scopes="domains:read"), settings)
    assert principal.subject == "test-user"
    assert principal.has_scope("domains:read")
    assert not principal.has_scope("domains:predict")


def test_expired_or_garbage_token_is_rejected(settings):
    with pytest.raises(HTTPException) as exc:
        _decode("not-a-real-token", settings)
    assert exc.value.status_code == 401


def test_wrong_secret_is_rejected(settings):
    token = jwt.encode(
        {"sub": "x", "aud": settings.jwt_audience},
        "wrong-secret-also-at-least-32-bytes-xx",
        algorithm="HS256",
    )
    with pytest.raises(HTTPException) as exc:
        _decode(token, settings)
    assert exc.value.status_code == 401


def test_token_without_subject_is_rejected(settings):
    token = jwt.encode({"aud": settings.jwt_audience}, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    with pytest.raises(HTTPException) as exc:
        _decode(token, settings)
    assert exc.value.status_code == 401
