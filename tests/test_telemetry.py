from unittest.mock import Mock, patch

from rave_python.telemetry import telemetry


@patch("requests.post")
def test_telemetry_emit(mock_post: Mock) -> None:
    telemetry.emit("test.event", {"key": "value"})

    mock_post.assert_called_once()
