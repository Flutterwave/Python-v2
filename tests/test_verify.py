from unittest.mock import Mock, patch

from rave_python.rave_payment import Payment


@patch("requests.post")
def test_verify_success(mock_post: Mock, payment_client: Payment) -> None:
    mock_post.return_value = Mock(
        ok=True,
        status_code=200,
        json=lambda: {
            "status": "success",
            "data": {
                "status": "successful",
                "tx_ref": "ref-123",
                "flw_ref": "FLW123",
                "amount": 100,
                "charged_amount": 102,
                "transaction_currency": "NGN",
                "payment_entity": "card",
                "appfee": 2,
                "flwMeta": {
                    "chargeResponse": "00",
                    "chargeResponseMessage": "Approved by Financial Institution",
                },
            },
        },
    )

    result = payment_client.verify(txRef="ref-123")

    assert result["transactionComplete"] is True
    assert result["error"] is False
    assert result["chargecode"] == "00"
    assert result["txRef"] == "ref-123"
    assert result["flwRef"] == "FLW123"
