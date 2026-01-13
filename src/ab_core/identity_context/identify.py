"""Sample entrypoint for template package."""

from typing import Annotated


from ab_client.token_validator import (
    AsyncClient as TokenValidatorClient,
    ValidateTokenRequest,
    ValidatedOIDCClaims,
)
from ab_client.user import (
    AsyncClient as UserClient,
    UpsertByOIDCRequest,
    User,
)

from ab_core.dependency import Depends, inject, pydanticize_type
from ab_core.dependency.loaders import ObjectLoaderEnvironment

from .exceptions import IdentificationError
from .models import IdentityContext


@inject
async def identify(
    token: str,
    token_validator_client: Annotated[
        TokenValidatorClient,
        Depends(
            ObjectLoaderEnvironment[pydanticize_type(TokenValidatorClient)](env_prefix="TOKEN_VALIDATOR_CLIENT"),
            persist=True,
        ),
    ],
    user_client: Annotated[
        UserClient,
        Depends(ObjectLoaderEnvironment[pydanticize_type(UserClient)](env_prefix="USER_CLIENT"), persist=True),
    ],
) -> IdentityContext:
    """Identity a user given a valid token."""
    # 1. validate the token
    claims = await token_validator_client.validate_token_validate_post(
        data=ValidateTokenRequest(
            token=token,
        ),
    )

    # 2. upsert the user
    user = await user_client.upsert_user_by_oidc_user_oidc_put(
        data=UpsertByOIDCRequest(
            oidc_sub=claims.sub,
            oidc_iss=claims.iss,
            email=claims.email,
            display_name=claims.given_name or claims.name or claims.nickname,
            preferred_username=claims.nickname or claims.name or claims.given_name,
        ),
    )

    return IdentityContext(
        token=token,
        claims=claims,
        user=user,
    )
