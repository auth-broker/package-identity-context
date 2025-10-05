"""Tests for template entrypoint."""

from ab_core.dependency.pydanticize import pydanticize_type
from ab_client_user.client import Client
PydanticClient = pydanticize_type(Client)

import os
from unittest.mock import patch


async def test_identify():
    """Test a function in the entrypoint is callable."""
    from ab_core.identity_context.identify import identify


    with patch.dict(
        os.environ,
        {
            "TOKEN_VALIDATOR_CLIENT_BASE_URL": "http://localhost:8001",
            "USER_CLIENT_BASE_URL": "http://localhost:8002",
        },
        clear=False,
    ):
        await identify(
            "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwYmE2Yjg0MGNhY2ZlNjQzNDY4NmQ4YTJjOTk1NDI2IiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2F1dGhlbnRpay5tYXR0aGV3Y291bHRlci5kZXYvYXBwbGljYXRpb24vby9vYXV0aDItYnJva2VyLyIsInN1YiI6IjBlODE0OTMxNjQ0NTk4YjVkNTJjNWQzN2NlZmI3MGZmZGI4Y2JhNDk0OTc0NTcyODA1YjA4ZWM5YmJkYWVjOTMiLCJhdWQiOiJjVWRyM1pOU1JFdnFkWTRpQzVaaVI4TlNOdU5YYjB5N2xpeTF0a0IwIiwiZXhwIjoxNzU5NjU3MzE1LCJpYXQiOjE3NTk2NTcwMTUsImF1dGhfdGltZSI6MTc1OTY0ODE1OSwiYWNyIjoiZ29hdXRoZW50aWsuaW8vcHJvdmlkZXJzL29hdXRoMi9kZWZhdWx0IiwiYW1yIjpbInB3ZCJdLCJzaWQiOiJiYjMwM2NkYmFhNDYzYmIxYmM2ZjQxNzlmMTBjMjRkNDJiOWZiZWM2Njg5Njc2NWI0MWZiMmM1MDllMTA0NzRlIiwiZW1haWwiOiJtYXR0Y291bDdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiIiLCJnaXZlbl9uYW1lIjoiIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWF0dGNvdWx0ZXI3Iiwibmlja25hbWUiOiJtYXR0Y291bHRlcjciLCJncm91cHMiOlsiYXV0aGVudGlrIEFkbWlucyJdLCJhenAiOiJjVWRyM1pOU1JFdnFkWTRpQzVaaVI4TlNOdU5YYjB5N2xpeTF0a0IwIiwidWlkIjoiRFAzeWkzeEpHSDE5Q3I2NUVOVUNSUTdLUlBJVlVYTENOWGhLOE9aZCJ9.X95mR3dt-PqIqcUDwOj43oc5PrS6zGNkfZDrpaapW2g_MWAw8B4vnoo0rip-vC4blOLGW5_XU-dJOq-u0w-K1Gm2C0sSuaZr_kfUG-Q2Wm1clzzJI0cJDO1w91C7t64BR2TfgqPohJblVUITrPkzrPvzmhXhxhjxm5_5X9oMDNgFrRB4N7XQTKgoF273yPKmRqkRRZTT7VPfc1K23wKd3LKTSUcZWz63LrFmmoVsR9j4mTslT4-pxzKHBkE83A1I0ZVbt0qY2dtlhKpxdG-ydRwvQUafkn8I6Ot8IJcyTA8hFx8gxgQX-Bsl086kLj_Jhw-iCH_Dy9_OdbU_88UAYco6dmP_njRaWBGScPv28DK_je2KeSWcgM3F1bMxjbUclylm2X0n03zGKTSpwpuvLU38AGyVFDN73AKmyBMhmfeD1jaxMwY_ZX-dbNvAOu89ozVb40YUUjh6DqEw8eeFwVnRHwCV-xxBU1yILPzbdn0Yiy97esvFLo06shhpx1_o6IbymLln-0h2KsGLd9jCugCQtrDpMhU0hAd6LlaPiB5tculF6sBvfTM5pEGyW5i-4xvsfquPUwMPZ5Bhk-dYdlw_VKn8dtRgWFMPsANgQ5Bbij0K2zK4-5HZCtCUO1yMoGn34-7JvKi9p1g2LzgTfgLjN8ibrLSBYdHuuIP-_J8",
        )
