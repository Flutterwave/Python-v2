import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
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

    def _handleCardStatusRequests(self, type, endpoint, feature_name, isPostRequest=False, data=None):
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
            #feature logging
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name,"message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

            return {"error": False, "returnedData": responseJson}
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

            raise CardStatusError(type, {"error": True, "returnedData": responseJson })


    
    #function to create a virtual card 
    #Params: vcardDetails - a dict containing currency, amount, billing_name, billing_address, billing_city, billing_state, billing_postal_code, billing_country
    def create(self, vcardDetails):
        
        #card creating logic
        vcardDetails = copy.copy(vcardDetails)
        vcardDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["currency", "amount", "billing_name", "billing_address", "billing_city", "billing_state", "billing_postal_code", "billing_country"]
        checkIfParametersAreComplete(requiredParameters, vcardDetails)
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(vcardDetails))
        
        #feature logging
        if response.ok == False:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": "Create-card-error", "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": "Create-card","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleCreateResponse(response, vcardDetails)

    
    #gets all virtual cards connected to a merchant's account
    def all(self):
        
        #logic for listing all cards
        label = "List-all-cards"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["list"] + "?seckey="+ self._getSecretKey()
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("List", endpoint, label, isPostRequest=True, data=data)

    
    #permanently deletes a card with specified id 
    def cancel(self, card_id):
        
        if not card_id:
            return "Card id was not supplied. Kindly supply one"
        
        #card cancel feature logic
        label = "Delete-card"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["terminate"] + str(card_id) + "/terminate"
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("Cancel", endpoint, label, isPostRequest=True, data=data)

    
    #fetches Card details and transactions for a cars with specified id
    def get(self, card_id):
        
        #fetch card logic
        label = "Fetch-card"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["get"]
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("Get", endpoint, label, isPostRequest=True, data=data)

    
    #temporarily suspends the use of card
    def freeze(self, card_id):
        
        #feature logic
        label = "Block-card"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["freeze"] + str(card_id) + "/status/block"
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("Freeze", endpoint, label, isPostRequest=True, data=data)

    
    #reverses the freeze card operation
    def unfreeze(self, card_id):
        
        #feature logic
        label = "Unblock-card"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["unfreeze"] + str(card_id) + "/status/unblock"
        data = {"seckey": self._getSecretKey()}
        return self._handleCardStatusRequests("Unfreeze", endpoint, label, isPostRequest=True, data=data)

    
    #funds a card with specified balance for online transactions
    def fund(self, card_id, currency, amount):
        
        #feature logic
        data = {
            "card_id": card_id,
            "amount" : amount,
            "debit_currency": currency,
            "seckey": self._getSecretKey(),
        }
        label = "Fund-card"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["fund"]
        return self._handleCardStatusRequests("Fund", endpoint, label, isPostRequest=True, data=data)

    #withdraws funds from Virtual card. Withdrawn funds are added to Rave Balance
    def withdraw(self, card_id, amount):
        
        #feature logic
        data = {
            "card_id": card_id,
            "amount" : amount,
            "seckey": self._getSecretKey(),
        }
        label = "Withdraw-card-funds"
        endpoint = self._baseUrl + self._endpointMap["virtual_card"]["withdraw"]
        return self._handleCardStatusRequests("Fund", endpoint, label, isPostRequest=True, data=data)
