"""Identity Context Models."""

from ab_client.token_validator import ValidatedOIDCClaims
from ab_client.user import User
from pydantic import BaseModel, Field


class IdentityContext(BaseModel):
    """Per-request identity context resolved from the bearer token."""

    token: str = Field(..., description="Raw Bearer token")
    claims: ValidatedOIDCClaims = Field(..., description="Claims from validated token")
    user: User = Field(..., description="The current user")
