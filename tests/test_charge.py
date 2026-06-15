from typing import Any
from unittest.mock import Mock, patch

from rave_python.rave_payment import Payment


def mock_response(json_data: dict[str, Any], status: int = 200) -> Mock:
    response = Mock()
    response.json.return_value = json_data
    response.status_code = status
    response.ok = status == 200
    return response


@patch("requests.post")
def test_charge_success(mock_post: Mock, payment_client: Payment) -> None:
    mock_post.return_value = mock_response(
        {
            "status": "success",
            "data": {
                "chargeResponseCode": "00",
                "flwRef": "FLW123",
            },
        },
    )

    payload: dict[str, Any] = {
        "amount": 100,
        "currency": "NGN",
        "txRef": "ref-123",
    }

    result = payment_client.charge(
        paymentDetails=payload,
        requiredParameters=["amount", "currency", "txRef"],
        endpoint="https://test.endpoint",
    )

    assert result["error"] is True
    assert result["flwRef"] == "FLW123"
