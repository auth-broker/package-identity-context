"""API Context Manager for IdentityContext."""

from typing import Annotated

try:
    from fastapi import Cookie, Depends, Header, HTTPException, status
except ImportError as e:
    raise RuntimeError(
        "`ab_core.identity_context.dependency::get_identity_context` requires FastAPI dependency."
        " Please install ab-identity-context[fastapi] to use this module."
    ) from e

from .exceptions import IdentificationError
from .identify import identify
from .models import EntitlementMode, IdentityContext, UnauthorisedErrorReason
from .permission import check_required_entitlements, normalise_entitlements


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


def require_entitlements(
    *required_entitlements: str,
    mode: EntitlementMode = EntitlementMode.ALL,
):
    """FastAPI dependency factory enforcing entitlement requirements.

    Endpoint entitlements should be concrete, for example:
        - "read:me"
        - "read:token_issuer"
        - "write:token"

    User entitlements may be wildcard grants, for example:
        - "read:*"
        - "write:*"
        - "*"
    """

    async def dependency(
        identity: Annotated[IdentityContext, Depends(get_identity_context)],
    ) -> None:
        granted = identity.claims.entitlements or ()

        allowed = check_required_entitlements(
            granted,
            required_entitlements,
            mode=mode,
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "detail": "Insufficient entitlements",
                    "reason": UnauthorisedErrorReason.INSUFFICIENT_ENTITLEMENTS.value,
                    "required_entitlements": list(required_entitlements),
                    "granted_entitlements": list(normalise_entitlements(granted)),
                    "mode": mode.value,
                },
            )

    return dependency
