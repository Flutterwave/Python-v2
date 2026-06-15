import pytest  # type:ignore

from rave_python.rave_exceptions import TransactionChargeError


def test_transaction_charge_error() -> None:
    with pytest.raises(TransactionChargeError):  # type:ignore
        raise TransactionChargeError({"error": True})
