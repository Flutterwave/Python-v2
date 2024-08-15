import json
import requests
import copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteAccountDetailsError, AccountCreationError, AccountStatusError


class VirtualAccount(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type': 'application/json'
        }
        super(
            VirtualAccount,
            self).__init__(
            publicKey,
            secretKey,
            production,
            usingEnv)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):
        # check if we can get json
        try:
            responseJson = response.json()
        except BaseException:
            raise ServerError(
                {"error": True, "name": name, "errMsg": response})

        # check for data parameter in response
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True,
                                      "name": name,
                                      "errMsg": responseJson.get("message",
                                                                 "Server is down")})

        # check for 200 response
        if not response.ok:
            errMsg = response["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleCreateResponse(self, response, accountDetails):
        responseJson = self._preliminaryResponseChecks(
            response, AccountCreationError, accountDetails["email"])

        if responseJson["status"] == "success":
            tempResponse = {
                "error": False,
                "id": responseJson["data"].get(
                    "id",
                    None),
                "data": responseJson["data"]}
            
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
        endpoint = self._baseUrl + \
            self._endpointMap["virtual_account"]["create"]
        response = requests.post(
            endpoint,
            headers=self.headers,
            data=json.dumps(accountDetails))
        json_response = json.dumps(response.json(), ensure_ascii=False)

        # feature logging
        if not response.ok:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {
                "publicKey": self._getPublicKey(),
                "language": "Python v2",
                "version": "1.2.13",
                "title": "Create-virtual-account-error",
                "message": responseTime}
            tracking_response = requests.post(
                tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {
                "publicKey": self._getPublicKey(),
                "language": "Python v2",
                "version": "1.2.13",
                "title": "Create-virtual-account",
                "message": responseTime}
            tracking_response = requests.post(
                tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleCreateResponse(response, accountDetails)
