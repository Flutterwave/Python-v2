import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteCardDetailsError, RecipientCreationError, RecipientStatusError

class Recipient(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(Recipient, self).__init__(publicKey, secretKey, production, usingEnv)

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

    def _handleCreateResponse(self, response, details):
        responseJson = self._preliminaryResponseChecks(response, RecipientCreationError, details["account_number"])

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

        else:
            raise RecipientCreationError({"error": True, "data": responseJson["data"]})

    def _handleCardStatusRequests(self, type, endpoint, isPostRequest=False, data=None):
        #check if resposnse is a post response
        if isPostRequest:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(data))
        else:
            response = requests.get(endpoint, headers=self.headers)
        
        #check if it can be parsed to JSON
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            raise RecipientStatusError(type, {"error": True, "returnedData": responseJson })

    #function to create a beneficiary or transfer recipient 
    #Params: details - a dict containing currency, amount,
    def create(self, details):
        details = copy.copy(details)
        details.update({"seckey": self._getSecretKey()})
        
        requiredParameters = ["account_number", "account_bank"]
        checkIfParametersAreComplete(requiredParameters, details)

        endpoint = self._baseUrl + self._endpointMap["recipient"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(details))
        return self._handleCreateResponse(response, details)

    def all(self):
        endpoint = self._baseUrl + self._endpointMap["recipient"]["list"] + "?seckey=" + self._getSecretKey()
        return self._handleCardStatusRequests("List", endpoint)

    def fetch(self, recipient_id):
        endpoint = self._baseUrl + self._endpointMap["recipient"]["fetch"] + "/" + str(recipient_id) + "?seckey="+self._getSecretKey()
        return self._handleCardStatusRequests("Fetch", endpoint)

    def cancel(self, recipient_id):
        if not recipient_id:
            return "recipient id was not supplied. Kindly supply one"
        endpoint = self._baseUrl + self._endpointMap["recipient"]["delete"]
        data = {
            "seckey": self._getSecretKey(),
            "id": recipient_id,
        }
        return self._handleCardStatusRequests("Cancel", endpoint, isPostRequest=True, data=data)

    