"""Permission helpers for IdentityContext entitlements."""

from collections.abc import Iterable
from typing import Literal

try:
    from fastapi import Depends, HTTPException, status
except ImportError as e:
    raise RuntimeError(
        "`ab_identity_context.permissions` requires FastAPI dependency."
        " Please install ab-identity-context[fastapi] to use this module."
    ) from e

from fnmatch import fnmatchcase

from .models import EntitlementMode


def normalise_entitlement(value: str) -> str:
    """Normalise a single entitlement string."""
    return value.strip().lower()


def normalise_entitlements(values: Iterable[str] | None) -> tuple[str, ...]:
    """Normalise entitlements into a stable tuple."""
    if not values:
        return ()

    return tuple(normalise_entitlement(value) for value in values if value and value.strip())


def match_granted_entitlement(granted: str, required: str) -> bool:
    """Return True if one granted entitlement satisfies one required entitlement.

    The granted entitlement may contain wildcard patterns.
    The required entitlement must be concrete.
    """
    granted = normalise_entitlement(granted)
    required = normalise_entitlement(required)

    if not granted or not required:
        return False

    return fnmatchcase(required, granted)


def has_required_entitlement(
    granted_entitlements: Iterable[str] | None,
    required_entitlement: str,
) -> bool:
    """Return True if any granted entitlement satisfies the required entitlement."""
    granted = normalise_entitlements(granted_entitlements)
    required = normalise_entitlement(required_entitlement)

    return any(match_granted_entitlement(item, required) for item in granted)


def check_required_entitlements(
    granted_entitlements: Iterable[str] | None,
    required_entitlements: Iterable[str],
    *,
    mode: EntitlementMode | Literal["any", "all"] = EntitlementMode.ALL,
) -> bool:
    """Check granted entitlements against required endpoint entitlements."""
    required = normalise_entitlements(required_entitlements)

    if not required:
        return True

    resolved_mode = EntitlementMode(mode)
    results = (has_required_entitlement(granted_entitlements, item) for item in required)

    if resolved_mode == EntitlementMode.ALL:
        return all(results)
    if resolved_mode == EntitlementMode.ANY:
        return any(results)
    raise ValueError(f"Unsupported entitlement mode: {mode}")
