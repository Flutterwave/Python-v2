import json

import requests

from rave_python.errors import HTTP_ERROR_MAP, ErrorCode
from rave_python.rave_base import RaveBase
from rave_python.rave_exceptions import BVNFetchError, ServerError


class Verify(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Verify, self).__init__(publicKey, secretKey, production, usingEnv)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):
        # check if we can get json
        try:
            responseJson = response.json()
        except BaseException:
            raise ServerError({"error": True, "name": name, "errMsg": response})

        # check for data parameter in response
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise(
                {
                    "error": True,
                    "name": name,
                    "errMsg": responseJson.get("message", "Server is down"),
                }
            )

        # check for 200 response
        if not response.ok:
            errMsg = response["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleVerifyStatusRequests(
        self, endpoint: str, isPostRequest: bool = False, data=None
    ):
        self.headers = {"content-type": "application/json"}

        http_method = "POST" if isPostRequest else "GET"
        self._telemetry.request_sent(endpoint, http_method, "", "v2")

        # check if resposnse is a post response
        if isPostRequest:
            response = requests.post(
                endpoint, headers=self.headers, data=json.dumps(data)
            )
        else:
            response = requests.get(endpoint, headers=self.headers)

        # check if it can be parsed to JSON
        try:
            responseJson = response.json()
        except BaseException:
            self._telemetry.error(
                code=ErrorCode.SDK_JSON_PARSE_ERROR,
                message="Invalid JSON response from verify endpoint",
            )
            raise ServerError({"error": True, "errMsg": response.text})

        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            self._telemetry.error(
                code=HTTP_ERROR_MAP.get(
                    response.status_code, ErrorCode.API_SERVER_ERROR
                ),
                message=responseJson.get("message", "BVN verification failed"),
            )
            raise BVNFetchError({"error": True, "returnedData": responseJson})

    def bvnVerify(self, bvn):
        # feature logic
        if not bvn:
            return "BVN was not supplied. Kindly supply one"
        endpoint = (
            self._baseUrl
            + self._endpointMap["bvn"]["verify"]
            + str(bvn)
            + "?seckey="
            + self._getSecretKey()
        )
        return self._handleVerifyStatusRequests(endpoint)
