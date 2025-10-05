from typing import Annotated
from fastapi import Header, HTTPException, status

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
    token = authorization.split(" ", 1)[1].strip()
    # TODO: maybe http error mapping here
    return await identify(token=token)
