import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteAccountDetailsError, AccountCreationError, AccountStatusError

class VirtualAccount(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(VirtualAccount, self).__init__(publicKey, secretKey, production, usingEnv)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):
        #check if we can get json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "name": name, "errMsg": response})

        #check for data parameter in response 
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True, "name": name, "errMsg": responseJson.get("message", "Server is down")})

        #check for 200 response
        if not response.ok:
            errMsg = response["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleCreateResponse(self, response, accountDetails):
        responseJson = self._preliminaryResponseChecks(response, AccountCreationError, accountDetails["email"])

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

        else:
            raise AccountCreationError({"error": True, "data": responseJson["data"]})

    # def _handleCardStatusRequests(self, type, endpoint, isPostRequest=False, data=None):
    #     #check if response is a post response
    #     if isPostRequest:
    #         response = requests.post(endpoint, headers=self.headers, data=json.dumps(data))
    #     else:
    #         response = requests.get(endpoint, headers=self.headers)
        
    #     #check if it can be parsed to JSON
    #     try:
    #         responseJson = response.json()
    #     except:
    #         raise ServerError({"error": True, "errMsg": response.text})

    #     if response.ok:
    #         return {"error": False, "returnedData": responseJson}
    #     else:
    #         raise AccountStatusError(type, {"error": True, "returnedData": responseJson })


    #function to create a virtual card 
    #Params: cardDetails - a dict containing email, is_permanent, frequency, duration, narration
    def create(self, accountDetails):

        # feature logic
        accountDetails = copy.copy(accountDetails)
        accountDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["email", "narration"]
        checkIfParametersAreComplete(requiredParameters, accountDetails)
        endpoint = self._baseUrl + self._endpointMap["virtual_account"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(accountDetails))

        #feature logging
        if response.ok == False:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": "Create-virtual-account-error","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": "Create-virtual-account","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleCreateResponse(response, accountDetails)