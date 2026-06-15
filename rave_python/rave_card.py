# ruff: noqa: ERA001, ARG002
from decimal import Decimal
from typing import Any

import requests

from rave_python.rave_exceptions import CardChargeError, TransactionVerificationError
from rave_python.rave_misc import generateTransactionReference
from rave_python.rave_payment import Payment


class Card(Payment):
    """This is the rave object for card transactions. It contains the following public functions:\n
    .charge -- This is for making a card charge\n
    .validate -- This is called if further action is required i.e. OTP validation\n
    .verify -- This checks the status of your transaction\n
    """

    def __init__(
        self, publicKey: str, secretKey: str, production: bool, usingEnv: bool
    ):
        super().__init__(publicKey, secretKey, production, usingEnv)

    # returns true if further action is required, false if it isn't

    def _handleChargeResponse(
        self,
        response: requests.Response,
        txRef: str,
        request: requests.Request | None = None,
    ) -> dict[str, Any]:
        """This handles charge responses"""
        res = self._preliminaryResponseChecks(response, CardChargeError, txRef=txRef)

        responseJson = res["json"]
        flwRef = res["flwRef"]

        # Checking if there is auth url
        if responseJson["data"].get("authurl", "N/A") == "N/A":
            authUrl = None
        else:
            authUrl = responseJson["data"]["authurl"]

        # If all preliminary checks passed
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            # Otherwise we return that further action is required, along with
            # the response
            suggestedAuth = responseJson["data"].get("suggested_auth", None)
            return {
                "error": False,
                "validationRequired": True,
                "txRef": txRef,
                "flwRef": flwRef,
                "suggestedAuth": suggestedAuth,
                "authUrl": authUrl,
            }
        else:
            return {
                "error": False,
                "status": responseJson["status"],
                "validationRequired": False,
                "txRef": txRef,
                "flwRef": flwRef,
                "suggestedAuth": None,
                "authUrl": authUrl,
            }

    def _handleRefundorVoidResponse(
        self,
        response: requests.Response,
        txRef: str,
        request: requests.Request | None = None,
    ) -> dict[str, Any]:
        """This handles charge responses"""
        res = self._preliminaryResponseChecks(response, CardChargeError, txRef=txRef)

        responseJson = res["json"]
        flwRef = responseJson["data"]["data"]["authorizeId"]

        # If all preliminary checks passed
        if not (responseJson["data"]["data"].get("responsecode", None) == "RR"):
            # Refund or Void could not be completed
            return {
                "error": True,
                "status": responseJson["status"],
                "message": responseJson["message"],
                "flwRef": flwRef,
            }
        else:
            return {
                "error": False,
                "status": responseJson["status"],
                "message": responseJson["message"],
                "flwRef": flwRef,
            }

    # This can be altered by implementing classes but this is the default behaviour
    # Returns True and the data if successful

    def _handleVerifyResponse(
        self,
        response: requests.Response,
        txRef: str,
        request: requests.Request | None = None,
    ) -> dict[str, Any]:
        """Handle all responses from the card verify call."""
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

        chargecode = flw_meta.get("chargeResponse") or data.get("chargecode")
        chargemessage = flw_meta.get("chargeResponseMessage") or data.get(
            "chargemessage"
        )
        vbvcode = flw_meta.get("VBVRESPONSECODE") or data.get("vbvcode")
        vbvmessage = flw_meta.get("VBVRESPONSEMESSAGE") or data.get("vbvmessage")

        custname = data.get("customer.fullName")
        custemail = data.get("customer.email")
        custphone = data.get("customer.phone")

        card = data.get("card", {})
        card_tokens = card.get("card_tokens", [])
        cardToken = card_tokens[0].get("embedtoken") if card_tokens else None

        if not response.ok:
            errMsg = data.get("message", "Your call failed with no response")
            raise TransactionVerificationError(
                {"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": errMsg}
            )

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
                method=paymenttype or "card",
            )

        # logging.getLogger("rave_python.card").debug(
        #     "[card verify] status=%s data.status=%s chargecode=%s",
        #     responseJson.get("status"),
        #     data.get("status"),
        #     flw_meta.get("chargeResponse"),
        # )

        return {
            "error": not transaction_complete,
            "transactionComplete": transaction_complete,
            "txRef": txRef,
            "flwRef": flwRef,
            "amount": amount,
            "chargedamount": chargedamount,
            "cardToken": cardToken,
            "vbvcode": vbvcode,
            "vbvmessage": vbvmessage,
            "chargemessage": chargemessage,
            "chargecode": chargecode,
            "currency": currency,
            "paymenttype": paymenttype,
            "appfee": appfee,
            "custname": custname,
            "custemail": custemail,
            "custphone": custphone,
            "meta": meta,
        }

    # Charge card function

    def charge(
        self,
        cardDetails: dict[str, Any],
        hasFailed: bool = False,
        chargeWithToken: bool = False,
    ) -> dict[str, Any]:
        """This is called to initiate the charge process.\n
         Parameters include:\n
        cardDetails (dict) -- This is a dictionary comprising payload parameters.\n
        hasFailed (bool) -- This indicates whether the request had previously failed for timeout handling
        """
        # setting the endpoint
        if not chargeWithToken:
            endpoint = self._baseUrl + self._endpointMap["card"]["charge"]
            requiredParameters = [
                "cardno",
                "cvv",
                "expirymonth",
                "expiryyear",
                "amount",
                "email",
            ]
            # optionalParameters = ["phonenumber", "firstname", "lastname"]
        else:
            if "charge_type" in cardDetails and cardDetails["charge_type"] == "preauth":
                endpoint = self._baseUrl + self._endpointMap["preauth"]["charge"]
            else:
                endpoint = self._baseUrl + self._endpointMap["card"]["chargeSavedCard"]

            requiredParameters = [
                "currency",
                "token",
                "country",
                "amount",
                "email",
                "txRef",
            ]
            # optionalParameters = ["firstname", "lastname"]
            # add token to requiredParameters
            # requiredParameters.append("token")

        if "txRef" not in cardDetails:
            cardDetails.update({"txRef": generateTransactionReference()})

        return super().charge(cardDetails, requiredParameters, endpoint)

    def validate(self, flwRef: str, otp: str) -> dict[str, Any]:
        endpoint = self._baseUrl + self._endpointMap["card"]["validate"]
        return super().validate(flwRef, otp, endpoint)

    def verify(self, txRef: str, endpoint: str | None = None) -> dict[str, Any]:
        endpoint = self._baseUrl + self._endpointMap["card"]["verify"]
        return super().verify(txRef, endpoint)

    def refund(
        self, flwRef: str, amount: Decimal
    ) -> tuple[bool, dict[str, Any]] | None:
        endpoint = self._baseUrl + self._endpointMap["card"]["refund"]
        return super().refund(flwRef, amount, endpoint)
