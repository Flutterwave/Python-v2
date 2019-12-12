import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteCardDetailsError, CardCreationError, CardStatusError

class Settlement(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(Settlement, self).__init__(publicKey, secretKey, production, usingEnv)

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

    # def _handleCreateResponse(self, response, details):
    #     responseJson = self._preliminaryResponseChecks(response, CardCreationError, details["billing_name"])

    #     if responseJson["status"] == "success":
    #         return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

    #     else:
    #         raise CardCreationError({"error": True, "data": responseJson["data"]})

    def _handleCardStatusRequests(self, type, endpoint, isPostRequest=False, data=None):
        #check if response is a post response
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
            raise CardStatusError(type, {"error": True, "returnedData": responseJson })


    #function to list and fetch settlements
    #Params: details - a dict containing service, service_method, service_version, service_channel and service_payload
    def all(self):
        endpoint = self._baseUrl + self._endpointMap["settlements"]["list"] + "?seckey=" + self._getSecretKey()
        return self._handleCardStatusRequests("List", endpoint)

    def fetch(self, settlement_id):
        endpoint = self._baseUrl + self._endpointMap["settlements"]["fetch"] + str(settlement_id) + "?seckey="+self._getSecretKey()
        return self._handleCardStatusRequests("Fetch", endpoint)