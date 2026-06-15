import copy
import json

import requests

from rave_python.errors import HTTP_ERROR_MAP, ErrorCode
from rave_python.rave_base import RaveBase
from rave_python.rave_exceptions import (
    IncompletePaymentDetailsError,
    InitiateTransferError,
    ServerError,
    TransferFetchError,
)
from rave_python.rave_misc import (
    checkIfParametersAreComplete,
    checkTransferParameters,
    generateTransactionReference,
)


class Transfer(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Transfer, self).__init__(publicKey, secretKey, production, usingEnv)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, reference):
        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except BaseException:
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message="Invalid JSON response from transfer endpoint",
            )
            raise ServerError(
                {"error": True, "reference": reference, "errMsg": response}
            )

        # Check if the response contains data parameter
        if not responseJson.get("data", None):
            self._telemetry.error(
                code=ErrorCode.API_SERVER_ERROR,
                message=responseJson.get("message", "Server is down"),
            )
            raise TypeOfErrorToRaise(
                {
                    "error": True,
                    "reference": reference,
                    "errMsg": responseJson.get("message", "Server is down"),
                }
            )

        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson["data"].get("message", None)
            self._telemetry.error(
                code=HTTP_ERROR_MAP.get(
                    response.status_code, ErrorCode.API_SERVER_ERROR
                ),
                message=str(errMsg),
            )
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleInitiateResponse(self, response, transferDetails):
        responseJson = self._preliminaryResponseChecks(
            response, InitiateTransferError, transferDetails["reference"]
        )

        if responseJson["status"] == "success":
            return {
                "error": False,
                "id": responseJson["data"].get("id", None),
                "data": responseJson["data"],
            }

        else:
            raise InitiateTransferError({"error": True, "data": responseJson["data"]})

    def _handleBulkResponse(self, response, bulkDetails):
        responseJson = self._preliminaryResponseChecks(
            response, InitiateTransferError, None
        )

        if responseJson["status"] == "success":
            return {
                "error": False,
                "status": responseJson["status"],
                "message": responseJson["message"],
                "id": responseJson["data"].get("id", None),
                "data": responseJson["data"],
            }
        else:
            raise InitiateTransferError({"error": True, "data": responseJson["data"]})

    # This makes and handles all requests pertaining to the status of your
    # transfer or account
    def _handleTransferStatusRequests(
        self, endpoint: str, isPostRequest: bool = False, data=None
    ):

        # Request headers
        headers = {
            "content-type": "application/json",
        }

        http_method = "POST" if isPostRequest else "GET"
        self._telemetry.request_sent(endpoint, http_method, "", "v2")

        # Checks if it is a post request
        if isPostRequest:
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        else:
            response = requests.get(endpoint, headers=headers)

        # Checks if it can be parsed to json
        try:
            responseJson = response.json()
        except BaseException:
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message="Invalid JSON response",
            )
            raise ServerError({"error": True, "errMsg": response.text})

        # Checks if it returns a 2xx code
        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            self._telemetry.error(
                code=HTTP_ERROR_MAP.get(
                    response.status_code, ErrorCode.API_SERVER_ERROR
                ),
                message=responseJson.get("message", "Transfer status request failed"),
            )
            raise TransferFetchError({"error": True, "returnedData": responseJson})

    def _handleTransferRetriesRequests(self, endpoint, isPostRequest=False, data=None):

        # Request headers
        headers = {
            "content-type": "application/json",
        }

        http_method = "POST" if isPostRequest else "GET"
        self._telemetry.request_sent(endpoint, http_method, "", "v2")

        # Checks if it is a post request
        if isPostRequest:
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        else:
            response = requests.get(endpoint, headers=headers)

        # Checks if it can be parsed to json
        try:
            responseJson = response.json()
            errorMessage = responseJson["message"]
        except BaseException:
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message="Invalid JSON response",
            )
            raise ServerError({"error": True, "errMsg": response.text})

        # Checks if it returns a 2xx code
        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            self._telemetry.error(
                code=HTTP_ERROR_MAP.get(
                    response.status_code, ErrorCode.API_SERVER_ERROR
                ),
                message=responseJson.get("message", "Transfer status request failed"),
            )
            return {"error": True, "returnedData": errorMessage}

    def initiate(self, transferDetails):

        # feature logic
        # Performing shallow copy of transferDetails to avoid public exposing
        # payload with secret key
        transferDetails = copy.copy(transferDetails)

        # adding reference if not already included
        if "reference" not in transferDetails:
            transferDetails.update({"reference": generateTransactionReference()})
        transferDetails.update({"seckey": self._getSecretKey()})

        # These are the parameters required to initiate a transfer
        requiredParameters = ["amount", "currency", "beneficiary_name"]
        checkIfParametersAreComplete(requiredParameters, transferDetails)
        checkTransferParameters(requiredParameters, transferDetails)

        # Collating request headers
        headers = {
            "content-type": "application/json",
        }

        endpoint = self._baseUrl + self._endpointMap["transfer"]["initiate"]
        self._telemetry.request_sent(
            endpoint, "POST", transferDetails.get("reference", ""), "v2"
        )
        response = requests.post(
            endpoint, headers=headers, data=json.dumps(transferDetails)
        )

        return self._handleInitiateResponse(response, transferDetails)

    def bulk(self, bulkDetails):

        # feature logic
        bulkDetails = copy.copy(bulkDetails)

        bulkDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["title", "bulk_data"]
        checkIfParametersAreComplete(requiredParameters, bulkDetails)
        checkTransferParameters(requiredParameters, bulkDetails)
        endpoint = self._baseUrl + self._endpointMap["transfer"]["bulk"]

        # Collating request headers
        headers = {
            "content-type": "application/json",
        }
        self._telemetry.request_sent(endpoint, "POST", "", "v2")
        response = requests.post(
            endpoint, headers=headers, data=json.dumps(bulkDetails)
        )

        return self._handleBulkResponse(response, bulkDetails)

    # Not elegant but supports python 2 and 3
    def fetch(self, reference=None):

        # feature logic
        endpoint = (
            self._baseUrl
            + self._endpointMap["transfer"]["fetch"]
            + "?seckey="
            + self._getSecretKey()
            + "&reference="
            + str(reference)
        )
        return self._handleTransferStatusRequests(endpoint)

    def all(self, page=None):

        # feature logic
        endpoint = (
            self._baseUrl
            + self._endpointMap["transfer"]["fetch"]
            + "?seckey="
            + self._getSecretKey()
            + "&page="
            + str(page)
        )
        return self._handleTransferStatusRequests(endpoint)

    def getFee(self, currency=None):

        # feature logic
        endpoint = (
            self._baseUrl
            + self._endpointMap["transfer"]["fee"]
            + "?seckey="
            + self._getSecretKey()
            + "&currency="
            + str(currency)
        )
        return self._handleTransferStatusRequests(endpoint)

    def getBalance(self, currency):

        # feature logic
        if not currency:  # i made currency compulsory because if it is not assed in, an error message is returned from the server
            raise IncompletePaymentDetailsError("currency", ["currency"])
        endpoint = self._baseUrl + self._endpointMap["transfer"]["balance"]
        data = {"seckey": self._getSecretKey(), "currency": currency}

        return self._handleTransferStatusRequests(
            endpoint, data=data, isPostRequest=True
        )

    def retryTransfer(self, transfer_id):

        # feature logic
        endpoint = self._baseUrl + self._endpointMap["transfer"]["retry"]
        data = {"seckey": self._getSecretKey(), "id": transfer_id}
        return self._handleTransferRetriesRequests(
            endpoint, data=data, isPostRequest=True
        )

    def fetchRetries(self, transfer_id):
        endpoint = (
            self._baseUrl
            + self._endpointMap["transfer"]["fetch"]
            + "/"
            + str(transfer_id)
            + "/retries?seckey="
            + self._getSecretKey()
        )
        return self._handleTransferRetriesRequests(endpoint)

    # def walletTransfer(self, transferDetails):
    #     data = {
    #         "seckey": self._getSecretKey(),
    #         "currency": transferDetails["currency"],
    #         "amount": transferDetails["amount"],
    #         "merchant_id": transferDetails["merchant_id"]
    #     }

    #     headers = {
    #         'content-type': 'application/json',
    #     }

    #     endpoint = self._baseUrl + self._endpointMap["transfer"]["inter_wallet"]
    #     response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    #     if response.ok == False:
    #         #feature logging
    #         tracking_endpoint = self._trackingMap
    #         responseTime = response.elapsed.total_seconds()
    #         tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.13", "title": "interwallet_transfers-error","message": responseTime}
    #         tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
    #     else:
    #         tracking_endpoint = self._trackingMap
    #         responseTime = response.elapsed.total_seconds()
    #         tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.13", "title": "interwallet_transfers","message": responseTime}
    #         tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
    #     return self._handleInitiateInterWalletResponse(response, data)
