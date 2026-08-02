"""JWT bearer authentication/authorization, centralized here per
ECOSYSTEM_RULES.md ("Autenticação, autorização e CORS serão centralizados
no agregador") - no domain repository implements its own auth; the
gateway is the single point where a request is authenticated before any
dispatch to a plugin."""

from __future__ import annotations

from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ecosystem.settings import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class Principal:
    subject: str
    scopes: frozenset[str]

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes


def _decode(token: str, settings: Settings) -> Principal:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], audience=settings.jwt_audience
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token missing 'sub'")
    scopes = frozenset(payload.get("scope", "").split())
    return Principal(subject=subject, scopes=scopes)


def current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    settings: Settings = Depends(get_settings),
) -> Principal:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")
    return _decode(credentials.credentials, settings)


def require_scope(scope: str):
    def _dependency(principal: Principal = Depends(current_principal)) -> Principal:
        if not principal.has_scope(scope):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"missing scope: {scope}")
        return principal

    return _dependency
