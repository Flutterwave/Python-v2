import copy
import json
from collections.abc import Sequence
from decimal import Decimal
from typing import Any, cast

import requests

from rave_python.errors import HTTP_ERROR_MAP, ErrorCode
from rave_python.rave_base import RaveBase
from rave_python.rave_exceptions import (
    PreauthCaptureError,
    RaveDictError,
    RefundError,
    ServerError,
    TransactionChargeError,
    TransactionValidationError,
    TransactionVerificationError,
)
from rave_python.rave_misc import checkIfParametersAreComplete

response_object: dict[str, Any] = {
    "error": False,
    "transactionComplete": False,
    "flwRef": "",
    "txRef": "",
    "chargecode": "00",
    "status": "",
    "vbvcode": "",
    "vbvmessage": "",
    "acctmessage": "",
    "currency": "",
    "chargedamount": 00,
    "chargemessage": "",
    "meta": "",
}


def getDefaultResponse() -> dict[str, Any]:
    return {
        "error": False,
        "transactionComplete": False,
        "flwRef": "",
        "txRef": "",
        "chargecode": "00",
        "status": "",
        "vbvcode": "",
        "vbvmessage": "",
        "acctmessage": "",
        "currency": "",
        "chargedamount": 00,
        "chargemessage": "",
        "meta": "",
    }


# All payment subclasses are encrypted classes
class Payment(RaveBase):
    """This is the base class for all the payments"""

    def __init__(
        self, publicKey: str, secretKey: str, production: bool, usingEnv: bool
    ) -> None:
        # Instantiating the base class
        super().__init__(publicKey, secretKey, production, usingEnv)

    @classmethod
    def retrieve(cls, mapping: dict[Any, Any], *keys: str) -> tuple[Any, ...]:
        return tuple(mapping.get(key) for key in keys)

    @classmethod
    def deleteUnnecessaryKeys(
        cls, response_dict: dict[str, Any], keys: Sequence[str]
    ) -> dict[str, Any]:
        for key in keys:
            response_dict.pop(key, None)
        return response_dict

    def _preliminaryResponseChecks(
        self,
        response: requests.Response,
        TypeOfErrorToRaise: type[RaveDictError],
        txRef: str | None = None,
        flwRef: str | None = None,
    ) -> dict[str, Any]:

        # Check if we can obtain a json
        try:
            responseJson = cast("dict[str, Any]", response.json())
        except (ValueError, json.JSONDecodeError):
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message=f"Invalid JSON response: {response.text[:100]}",
            )
            raise ServerError(
                {
                    "error": True,
                    "txRef": txRef,
                    "flwRef": flwRef,
                    "errMsg": f"Invalid JSON response: {response.text[:100]}",
                }
            )

        data = cast("dict[str, Any]", responseJson.get("data", {}))

        flwRef = data.get("flwRef", flwRef)
        txRef = data.get("txRef", txRef)

        error_code = HTTP_ERROR_MAP.get(
            response.status_code, ErrorCode.API_SERVER_ERROR
        )

        if not response.ok:
            self._telemetry.error(
                code=error_code,
                message=responseJson.get("message", "Server Error"),
            )
            raise TypeOfErrorToRaise(
                {
                    "error": True,
                    "txRef": txRef,
                    "flwRef": flwRef,
                    "errMsg": responseJson.get("message", "Server Error"),
                }
            )

        if not response.ok:
            # Handle non-200 responses with data present
            self._telemetry.error(
                code=error_code,
                message=responseJson.get("message", "Server Error"),
            )
            errMsg = data.get("message") if data else responseJson.get("message")

            raise TypeOfErrorToRaise(
                {"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": errMsg}
            )

        return {"json": responseJson, "flwRef": flwRef, "txRef": txRef}

    def _handleChargeResponse(
        self, response: requests.Response, txRef: str, isMpesa: bool = False
    ) -> dict[str, Any]:
        """This handles transaction charge responses"""

        # If we cannot parse the json, it means there is a server error
        res = self._preliminaryResponseChecks(
            response, TransactionChargeError, txRef=txRef
        )
        responseJson = res["json"]

        if isMpesa:
            return {
                "error": False,
                "status": responseJson["status"],
                "validationRequired": True,
                "txRef": txRef,
                "flwRef": responseJson["data"]["flwRef"],
                "narration": responseJson["data"]["narration"],
            }
        else:
            # if all preliminary tests pass
            if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
                if responseJson.get("message", "None") == "Momo initiated":
                    return {
                        "error": False,
                        "status": responseJson["status"],
                        "message": responseJson["message"],
                        "code": responseJson["data"]["code"],
                        "transaction status": responseJson["data"]["status"],
                        "ts": responseJson["data"]["ts"],
                        "link": responseJson["data"]["link"],
                    }
                return {
                    "error": False,
                    "status": responseJson["status"],
                    "validationRequired": True,
                    "txRef": txRef,
                    "flwRef": responseJson["data"]["data"]["flw_reference"],
                    "chargeResponseMessage": responseJson["data"]["response_message"],
                    "redirect": responseJson["data"]["data"]["redirect"],
                    "type": responseJson["data"]["data"]["type"],
                    "provider": responseJson["data"]["data"]["provider"],
                }

            else:
                return {
                    "error": True,
                    "validationRequired": False,
                    "txRef": txRef,
                    "flwRef": responseJson["data"]["flwRef"],
                }

    def _handleCaptureResponse(self, response: requests.Response) -> dict[str, Any]:
        """This handles transaction charge responses"""

        # If we cannot parse the json, it means there is a server error
        res = self._preliminaryResponseChecks(response, PreauthCaptureError, txRef="")

        responseJson = res["json"]
        flwRef = responseJson["data"]["flwRef"]
        txRef = responseJson["data"]["txRef"]

        # if all preliminary tests pass
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            return {
                "error": False,
                "validationRequired": True,
                "txRef": txRef,
                "flwRef": flwRef,
            }
        else:
            return {
                "error": False,
                "status": responseJson["status"],
                "message": responseJson["message"],
                "validationRequired": False,
                "txRef": txRef,
                "flwRef": flwRef,
            }

    # This can be altered by implementing classes but this is the default behaviour
    # Returns True and the data if successful

    def _handleVerifyResponse(
        self, response: requests.Response, txRef: str
    ) -> dict[str, Any]:
        """This handles all responses from the verify call.\n
         Parameters include:\n
        response (dict) -- This is the response Http object returned from the verify call
        """
        res = self._preliminaryResponseChecks(
            response, TransactionVerificationError, txRef=txRef
        )

        responseJson = res["json"]
        data = responseJson["data"]
        flw_meta = data.get("flwMeta", {})

        flwRef = data.get("flw_ref")
        txRef = data.get("tx_ref", txRef)
        amount = data.get("amount")
        chargedamount = data.get("charged_amount")
        currency = data.get("transaction_currency")
        paymenttype = data.get("payment_entity")
        appfee = data.get("appfee", 0)
        meta = data.get("meta")
        acctmessage = data.get("acctmessage")

        chargecode = flw_meta.get("chargeResponse") or data.get("chargecode")
        chargemessage = flw_meta.get("chargeResponseMessage") or data.get(
            "chargemessage"
        )
        vbvcode = flw_meta.get("VBVRESPONSECODE") or data.get("vbvcode")
        vbvmessage = flw_meta.get("VBVRESPONSEMESSAGE") or data.get("vbvmessage")

        custname = data.get("customer.fullName")
        custemail = data.get("customer.email")
        custphone = data.get("customer.phone")

        transaction_complete = (
            responseJson.get("status") == "success"
            and data.get("status") == "successful"
            and chargecode == "00"
        )

        if transaction_complete:
            self._telemetry.transaction(
                reference=txRef,
                currency=currency or "",
                amount=Decimal(str(amount or 0)),
                fee=Decimal(str(appfee or 0)),
                method=paymenttype or "unknown",
            )
        else:
            self._telemetry.error(
                code=ErrorCode.VERIFY_FAILED,
                message=chargemessage or "Verification failed",
            )

        return {
            "error": not transaction_complete,
            "transactionComplete": transaction_complete,
            "status": responseJson.get("status"),
            "txRef": txRef,
            "flwRef": flwRef,
            "amount": amount,
            "chargedamount": chargedamount,
            "currency": currency,
            "paymenttype": paymenttype,
            "appfee": appfee,
            "chargecode": chargecode,
            "chargemessage": chargemessage,
            "vbvcode": vbvcode,
            "vbvmessage": vbvmessage,
            "acctmessage": acctmessage,
            "custname": custname,
            "custemail": custemail,
            "custphone": custphone,
            "meta": meta,
        }

    # returns true if further action is required, false if it isn't

    def _handleValidateResponse(
        self, response: requests.Response, flwRef: str
    ) -> dict[str, Any]:
        """This handles validation responses"""

        # If json is not parseable, it means there is a problem in server

        res = self._preliminaryResponseChecks(
            response, TransactionValidationError, flwRef=flwRef
        )

        responseJson = res["json"]
        if responseJson["data"].get("tx") is None:
            txRef = responseJson["data"]["txRef"]
        else:
            txRef = responseJson["data"]["tx"]["txRef"]

        # Of all preliminary checks passed
        if not (
            responseJson["data"]
            .get("tx", responseJson["data"])
            .get("chargeResponseCode", None)
            == "00"
        ):
            errMsg = (
                responseJson["data"]
                .get("tx", responseJson["data"])
                .get("chargeResponseMessage", None)
            )

            self._telemetry.error(
                code=ErrorCode.VALIDATION_INVALID_OTP,
                message=errMsg,
            )

            raise TransactionValidationError(
                {"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": errMsg}
            )

        else:
            return {
                "status": responseJson["status"],
                "message": responseJson["message"],
                "error": False,
                "txRef": txRef,
                "flwRef": flwRef,
            }

    def charge(
        self,
        paymentDetails: dict[str, Any],
        requiredParameters: Sequence[str],
        endpoint: str,
        shouldReturnRequest: bool = False,
        isMpesa: bool = False,
    ) -> dict[str, Any]:
        """This is the base charge call. It is usually overridden by implementing classes.\n
         Parameters include:\n
        paymentDetails (dict) -- These are the parameters passed to the function for processing\n
        requiredParameters (list) -- These are the parameters required for the specific call\n
        hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        shouldReturnRequest -- This determines whether a request is passed to _handleResponses\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
        except BaseException:
            raise

        # Performing shallow copy of payment details to prevent tampering with
        # original
        paymentDetails = copy.copy(paymentDetails)

        # Adding PBFPubKey param to paymentDetails
        paymentDetails.update({"PBFPubKey": self._getPublicKey()})

        # Collating request headers
        headers = {
            "content-type": "application/json",
        }
        if "token" in paymentDetails:
            paymentDetails.update({"SECKEY": self._getSecretKey()})
            self._telemetry.request_sent(
                endpoint, "POST", paymentDetails.get("txRef", ""), "v2"
            )
            response = requests.post(
                endpoint, headers=headers, data=json.dumps(paymentDetails)
            )

        else:
            # Encrypting payment details (_encrypt is inherited from
            # RaveEncryption)
            encryptedPaymentDetails = self._encrypt(json.dumps(paymentDetails))

            # Collating the payload for the request
            payload: dict[str, Any] = {
                "PBFPubKey": paymentDetails["PBFPubKey"],
                "client": encryptedPaymentDetails,
                "alg": "3DES-24",
            }
            self._telemetry.request_sent(
                endpoint, "POST", paymentDetails.get("txRef", ""), "v2"
            )
            response = requests.post(
                endpoint, headers=headers, data=json.dumps(payload)
            )

        if shouldReturnRequest:
            if isMpesa:
                return self._handleChargeResponse(
                    response, paymentDetails["txRef"], True
                )
            return self._handleChargeResponse(response, paymentDetails["txRef"])
        else:
            if isMpesa:
                return self._handleChargeResponse(
                    response, paymentDetails["txRef"], True
                )
            return self._handleChargeResponse(response, paymentDetails["txRef"])

    def validate(self, flwRef: str, otp: str, endpoint: str | None) -> dict[str, Any]:
        """This is the base validate call.\n
         Parameters include:\n
        flwRef (string) -- This is the flutterwave reference returned from a successful charge call. You can access this from action["flwRef"] returned from the charge call\n
        otp (string) -- This is the otp sent to the user \n
        """

        if not endpoint:
            endpoint = self._baseUrl + self._endpointMap["account"]["validate"]

        # Collating request headers
        headers = {
            "content-type": "application/json",
        }

        payload: dict[str, Any] = {
            "PBFPubKey": self._getPublicKey(),
            "transactionreference": flwRef,
            "transaction_reference": flwRef,
            "otp": otp,
        }
        self._telemetry.request_sent(endpoint, "POST", flwRef, "v2")  # type: ignore
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))  # type: ignore

        return self._handleValidateResponse(response, flwRef)

    # Verify charge
    def verify(self, txRef: str, endpoint: str | None = None) -> dict[str, Any]:
        """This is used to check the status of a transaction.\n
         Parameters include:\n
        txRef (string) -- This is the transaction reference that you passed to your charge call. If you didn't define a reference, you can access the auto-generated one from payload["txRef"] or action["txRef"] from the charge call\n
        """

        endpoint = self._baseUrl + self._endpointMap["verify"]

        # Collating request headers
        headers = {
            "content-type": "application/json",
        }

        # Payload for the request headers
        payload: dict[str, Any] = {"txref": txRef, "SECKEY": self._getSecretKey()}
        self._telemetry.request_sent(endpoint, "POST", txRef, "v2")  # type: ignore
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))  # type: ignore

        return self._handleVerifyResponse(response, txRef)

    # Refund call
    def refund(
        self, flwRef: str, amount: Decimal, endpoint: str | None = None
    ) -> tuple[bool, dict[str, Any]] | None:
        """This is used to refund a transaction from any of Rave's component objects.\n
         Parameters include:\n
        flwRef (string) -- This is the flutterwave reference returned from a successful call from any component. You can access this from action["flwRef"] returned from the charge call
        """

        payload: dict[str, Any] = {
            "ref": flwRef,
            "seckey": self._getSecretKey(),
            "amount": amount,
        }
        headers = {"Content-Type": "application/json"}
        endpoint: str = self._baseUrl + self._endpointMap["refund"]
        self._telemetry.request_sent(endpoint, "POST", flwRef, "v2")
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

        try:
            responseJson = response.json()
        except ValueError:
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message=f"Invalid JSON response: {response.text[:100]}",
            )
            raise ServerError(
                {
                    "error": True,
                    "errMsg": f"Invalid JSON response: {response.text[:100]}",
                }
            )

        if responseJson.get("status", None) == "error":
            self._telemetry.error(
                code=ErrorCode.API_BAD_REQUEST,
                message=responseJson.get("message", None),
            )

            raise RefundError(responseJson.get("message", None))
        elif responseJson.get("status", None) == "success":
            return True, responseJson.get("data", None)
