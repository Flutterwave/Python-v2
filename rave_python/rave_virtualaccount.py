import copy
import json

import requests

from rave_python.errors import HTTP_ERROR_MAP, ErrorCode
from rave_python.rave_base import RaveBase
from rave_python.rave_exceptions import AccountCreationError, ServerError
from rave_python.rave_misc import checkIfParametersAreComplete


class VirtualAccount(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {"content-type": "application/json"}
        super(VirtualAccount, self).__init__(publicKey, secretKey, production, usingEnv)

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

    def _handleCreateResponse(self, response, accountDetails):
        responseJson = self._preliminaryResponseChecks(
            response, AccountCreationError, accountDetails["email"]
        )

        if responseJson["status"] == "success":
            tempResponse = {
                "error": False,
                "id": responseJson["data"].get("id", None),
                "data": responseJson["data"],
            }

            formattedResponse = json.dumps(tempResponse, ensure_ascii=False)
            return formattedResponse

    # function to create a virtual account
    # Params: accountDetails - a dict containing email, is_permanent, frequency,
    # duration, narration and BVN.

    def create(self, accountDetails):

        # feature logic
        accountDetails = copy.copy(accountDetails)
        accountDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["email", "bvn"]
        checkIfParametersAreComplete(requiredParameters, accountDetails)
        endpoint = self._baseUrl + self._endpointMap["virtual_account"]["create"]
        self._telemetry.request_sent(
            endpoint, "POST", accountDetails.get("email", ""), "v2"
        )

        response = requests.post(
            endpoint, headers=self.headers, data=json.dumps(accountDetails)
        )

        if not response.ok:
            self._telemetry.error(
                code=HTTP_ERROR_MAP.get(
                    response.status_code, ErrorCode.API_SERVER_ERROR
                ),
                message=response.text[:100],
            )

        return self._handleCreateResponse(response, accountDetails)
