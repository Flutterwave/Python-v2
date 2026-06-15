from typing import Any
from unittest.mock import Mock, patch

from rave_python.rave_payment import Payment


@patch("requests.post")
def test_validate_success(mock_post: Mock, payment_client: Payment) -> None:
    response_data: dict[str, Any] = {
        "status": "success",
        "message": "Validated",
        "data": {"txRef": "ref-123", "chargeResponseCode": "00"},
    }
    mock_post.return_value = Mock(
        ok=True,
        json=lambda: response_data,
    )

    result = payment_client.validate(
        flwRef="FLW123",
        otp="123456",
        endpoint="https://test.endpoint",
    )

    assert result["error"] is False
    assert result["txRef"] == "ref-123"
