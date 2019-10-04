import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete, generateTransactionReference
from rave_python.rave_exceptions import ServerError, IncompleteCardDetailsError, CardCreationError, CardStatusError

class VirtualCard(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(VirtualCard, self).__init__(publicKey, secretKey, production, usingEnv)

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

    def _handleCreateResponse(self, response, vcardDetails):
        responseJson = self._preliminaryResponseChecks(response, CardCreationError, vcardDetails["billing_name"])

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

        else:
            raise CardCreationError({"error": True, "data": responseJson["data"]})

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
            raise CardStatusError(type, {"error": True, "returnedData": responseJson })



    
    #function to create a virtual card 
    #Params: cardDetails - a dict containing currency, amount, billing_name, billing_address, billing_city, billing_state, billing_postal_code, billing_country
    def Create(self, vcardDetails):
        vcardDetails = copy.copy(vcardDetails)
        vcardDetails.update({"seckey": self._getSecretKey()})
        
        requiredParameters = ["currency", "amount", "billing_name", "billing_address", "billing_city", "billing_state", "billing_postal_code", "billing_country"]
        checkIfParametersAreComplete(requiredParameters, vcardDetails)

        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(vcardDetails))
        return self._handleCreateResponse(response, vcardDetails)

    # #gets all subaccounts connected to a merchant's account
    def allCards(self):
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["list"] + "?seckey="+ self._getSecretKey()
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("List", endpoint, isPostRequest=True, data=data)

    def cancelCard(self, card_id):
        if not card_id:
            return "Card id was not supplied. Kindly supply one"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["terminate"] + str(card_id) + "/terminate"
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("Cancel", endpoint, isPostRequest=True, data=data)

    