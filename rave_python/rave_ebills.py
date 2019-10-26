import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteCardDetailsError, BillCreationError, BillStatusError

class Ebills(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(Ebills, self).__init__(publicKey, secretKey, production, usingEnv)

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
        responseJson = self._preliminaryResponseChecks(response, BillCreationError, details["SECKEY"])

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

        else:
            raise BillCreationError({"error": True, "data": responseJson["data"]})

    def _handleBillStatusRequests(self, type, endpoint, isPostRequest=False, data=None):
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
            raise BillStatusError(type, {"error": True, "returnedData": responseJson })

    
    # def createOrder(self, order_details):
    #     # Performing shallow copy of planDetails to avoid public exposing payload with secret key
    #     order_details = copy.copy(order_details)
    #     order_details.update({"seckey": self._getSecretKey()})

    #     requiredParameters = ["seckey", "numberofunits", "currency", "amount", "email", "txRef", "country"]
    #     checkIfParametersAreComplete(requiredParameters, order_details)

    #     endpoint = self._baseUrl + self._endpointMap["ebills"]["create"]
    #     response = requests.post(endpoint, headers=self.headers, data=json.dumps(order_details))
    #     return self._handleCreateResponse(response, order_details)

    def create(self, details):
        # Performing shallow copy of planDetails to avoid public exposing payload with secret key
        details = copy.copy(details)
        details.update({"SECKEY": self._getSecretKey()})

        requiredParameters = ["numberofunits", "currency", "amount", "email", "txRef", "country"]
        checkIfParametersAreComplete(requiredParameters, details)

        endpoint = self._baseUrl + self._endpointMap["ebills"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(details))
        return self._handleCreateResponse(response, details)