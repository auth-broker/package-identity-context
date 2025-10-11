"""API Context Manager for IdentityContext."""

from typing import Annotated

from fastapi import Header, HTTPException, status

from .exceptions import IdentificationError
from .identify import identify
from .models import IdentityContext


async def get_identity_context(
    authorization: Annotated[str | None, Header()] = None,
) -> IdentityContext:
    """FastAPI dependency that returns IdentityContext.

    Usage:
        identity: Annotated[IdentityContext, Depends(identity_context)]
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    _, token = authorization.split(" ", 1)
    try:
        return await identify(
            token=token,
        )
    except IdentificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e
