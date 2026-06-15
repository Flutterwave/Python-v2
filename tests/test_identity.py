import os
from unittest.mock import Mock, patch

from rave_python.identity import AppIdentityClient

PUBLIC_KEY = str(os.getenv("PUBLIC_KEY"))


@patch("requests.get")
def test_identity_fetch(mock_get: Mock) -> None:
    mock_get.return_value = Mock(
        ok=True,
        json=lambda: {"mn": "app_123"},
    )

    client = AppIdentityClient(PUBLIC_KEY)
    app_id = client.get_app_id()

    assert app_id == "Cornelius_Ashley-Osuzoka"
