from unittest.mock import Mock, patch

from rave_python.events import Env
from rave_python.telemetryClient import TelemetryClient


@patch("rave_python.telemetry.telemetry.emit")
def test_request_sent(mock_emit: Mock) -> None:

    client = TelemetryClient(app_id="app_123", environment=Env.SANDBOX)

    client.request_sent(
        api_version="v2",
        url="/charge",
        reference="ref-123",
        method="POST",
    )

    mock_emit.assert_called_once()
