"""API Context Manager for IdentityContext."""

from typing import Annotated

try:
    from fastapi import Cookie, Header, HTTPException, status
except ImportError as e:
    raise RuntimeError(
        "`ab_core.identity_context.dependency::get_identity_context` requires FastAPI dependency."
        " Please install ab-identity-context[fastapi] to use this module."
    ) from e

from .exceptions import IdentificationError
from .identify import identify
from .models import IdentityContext


async def get_identity_context(
    access_token: Annotated[str | None, Cookie(alias="access_token")] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> IdentityContext:
    """FastAPI dependency that returns IdentityContext.

    Usage:
        identity: Annotated[IdentityContext, Depends(get_identity_context)]
    """
    token: str | None = None

    if access_token:
        token = access_token
    elif authorization and authorization.lower().startswith("bearer "):
        _, token = authorization.split(" ", 1)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    try:
        return await identify(token=token)
    except IdentificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e
