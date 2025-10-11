"""Tests for template entrypoint."""

import os
from unittest.mock import patch


async def test_identify():
    """Test a function in the entrypoint is callable."""
    from ab_core.identity_context.identify import identify

    await identify(
        "fake-token"
    )
