from collections.abc import Sequence
from typing import Any


class RaveError(Exception):
    """The root of all Rave errors."""

    def __init__(self, msg: str):
        super().__init__(msg)


class RaveDictError(RaveError):
    """Base for errors that take a dictionary: (err: Dict)"""

    def __init__(self, err: dict[str, Any]):
        self.err = err
        # Pre-extract message for the base Exception class
        msg = err.get("errMsg", "An unknown error occurred")
        super().__init__(msg)


class RaveStatusError(RaveError):
    """Base for errors that take a type and a dictionary: (type: str, err: Dict)"""

    def __init__(self, type_name: str, err: dict[str, Any]):
        self.err = err
        self.type_name = type_name
        msg = f"{type_name}ing failed: {err.get('errMsg', 'Unknown error')}"
        super().__init__(msg)


class RaveIncompleteError(RaveError):
    """Base for errors regarding missing parameters: (value: str, params: Sequence)"""

    def __init__(self, value: str, requiredParameters: Sequence[str]):
        self.value = value
        self.requiredParameters = requiredParameters
        msg = f'"{value}" missing. Required: {", ".join(requiredParameters)}'
        super().__init__(msg)


# DICTIONARY-BASED ERRORS (Type: RaveDictError)
class AccountChargeError(RaveDictError):
    def __str__(self):
        return f"Your account charge call failed with message: {self.err['errMsg']}"


class AccountCreationError(RaveDictError):
    def __str__(self):
        return f"Virtual account creation failed with error: {self.err['errMsg']}"


class BillCreationError(RaveDictError):
    def __str__(self):
        return f"Bill creation failed with error: {self.err['errMsg']}"


class BVNFetchError(RaveDictError):
    def __str__(self):
        return f"BVN fetch failed with error: {self.err['errMsg']}"


class CardCreationError(RaveDictError):
    def __str__(self):
        return f"Virtual Card creation failed with error: {self.err['errMsg']}"


class CardChargeError(RaveDictError):
    def __str__(self):
        return f"Your card charge call failed with message: {self.err['errMsg']}"


class InitiateTransferError(RaveDictError):
    def __str__(self):
        return f"Transfer initiation failed with error: {self.err['errMsg']}"


class MobileChargeError(RaveDictError):
    def __str__(self):
        return (
            f"Your mobile money charge call failed with message: {self.err['errMsg']}"
        )


class PlanCreationError(RaveDictError):
    def __str__(self):
        return f"Plan Creation failed with error: {self.err['errMsg']}"


class PreauthCaptureError(RaveDictError):
    def __str__(self):
        return f"Your preauth capture call failed with message: {self.err['errMsg']}"


class PreauthRefundVoidError(RaveDictError):
    def __str__(self):
        return (
            f"Your preauth refund/void call failed with message: {self.err['errMsg']}"
        )


class RecipientCreationError(RaveDictError):
    def __str__(self):
        return f"Recepient Creation failed with error: {self.err['errMsg']}"


class ServerError(RaveDictError):
    def __str__(self):
        return f" Server is down with error: {self.err['errMsg']}"


class SubaccountCreationError(RaveDictError):
    def __str__(self):
        return f"Subaccount Creation failed with error: {self.err['errMsg']}"


class TransactionChargeError(RaveDictError):
    def __str__(self):
        return f"Your account charge call failed with message: {self.err['errMsg']}"


class TransferFetchError(RaveDictError):
    def __str__(self):
        return f"Transfer fetch failed with error: {self.err['errMsg']}"


class TransactionValidationError(RaveDictError):
    def __str__(self):
        return f"Your transaction validation call failed with message: {self.err['errMsg']}"


class TransactionVerificationError(RaveDictError):
    def __str__(self):
        return f"Your transaction verification call failed with message: {self.err['errMsg']}"


class UssdChargeError(RaveDictError):
    def __str__(self):
        return f"Your ussd charge call failed with message: {self.err['errMsg']}"


# STATUS-BASED ERRORS (Type: RaveStatusError)
class AccountStatusError(RaveStatusError):
    def __str__(self):
        return f"{self.type_name}ing account failed with error: {self.err['errMsg']}"


class BillStatusError(RaveStatusError):
    def __str__(self):
        return f"{self.type_name}ing bill failed with error: {self.err['errMsg']}"


class CardStatusError(RaveStatusError):
    def __str__(self):
        return f"{self.type_name}ing card failed with error: {self.err['errMsg']}"


class PlanStatusError(RaveStatusError):
    def __str__(self):
        return f"{self.type_name}ing plan failed with error: {self.err['errMsg']}"


class RecipientStatusError(RaveStatusError):
    def __str__(self):
        return f"{self.type_name}ing recepient failed with error: {self.err['errMsg']}"


# INCOMPLETE-DATA ERRORS (Type: RaveIncompleteError)
class IncompleteAccountDetailsError(RaveIncompleteError):
    pass


class IncompleteCardDetailsError(RaveIncompleteError):
    pass


class IncompletePaymentDetailsError(RaveIncompleteError):
    pass


# STRING-BASED ERRORS (Type: RaveError)
class AuthMethodNotSupportedError(RaveError):
    def __init__(self, message: str):
        msg = f'\n We do not currently support authMethod: "{message}". If you need this to be supported, please report on GitHub.'
        super().__init__(msg)


class RefundError(RaveError):
    def __init__(self, message: str):
        msg = f"Your refund call failed with message: {message}"
        super().__init__(msg)
