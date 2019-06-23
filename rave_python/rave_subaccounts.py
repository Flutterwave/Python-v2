import requests, json, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete, generateTransactionReference
from rave_python.rave_exceptions import  ServerError, IncompletePaymentDetailsError, SubaccountCreationError, PlanStatusError

class SubAccount(RaveBase) :
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type': 'application/json'
        }
        super(SubAccount, self).__init__(publicKey, secretKey, production, usingEnv)
    
    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):
        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "name": name, "errMsg": response})

        # Check if the response contains data parameter
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True, "name": name, "errMsg": responseJson.get("message", "Server is down")})
        
        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})
        
        return responseJson
    
    def _handleCreateResponse(self, response, accountDetails):
        responseJson = self._preliminaryResponseChecks(response, SubaccountCreationError, accountDetails["business_email"])
        
        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        
        else:
            raise SubaccountCreationError({"error": True, "data": responseJson["data"]})

    # This makes and handles all requests pertaining to the status of your payment plans
    def _handleAccountStatusRequests(self, type, endpoint, isPostRequest=False, data=None):

        # Checks if it is a post request
        if isPostRequest:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(data))
        else:
            response = requests.get(endpoint, headers=self.headers)

        # Checks if it can be parsed to json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text })

        # Checks if it returns a 2xx code
        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            raise PlanStatusError(type, {"error": True, "returnedData": responseJson })
    
    #function to create a payment plan
    #Params: accountDetails - a dict containing account_bank, account_number, business_name, business_email, business_contact, business_contact_mobile, business_mobile, split_type, split_value
    #if duration is not passed, any subscribed customer will be charged #indefinitely
    def createSubaccount(self, accountDetails):
        # Performing shallow copy of planDetails to avoid public exposing payload with secret key
        accountDetails = copy.copy(accountDetails)
        accountDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["account_bank", "account_number", "business_name", "business_email", "business_contact", "business_contact_mobile", "business_mobile", "split_type", "split_value"]
        checkIfParametersAreComplete(requiredParameters, accountDetails)

        endpoint = self._baseUrl + self._endpointMap["subaccount"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(accountDetails))
        return self._handleCreateResponse(response, accountDetails)

    #gets all subaccounts connected to a merchant's account
    def allSubaccounts(self):
        endpoint = self._baseUrl + self._endpointMap["subaccount"]["list"] + "?seckey="+self._getSecretKey()
        return self._handleAccountStatusRequests("List", endpoint)
    
    def fetchSubaccount(self, subaccount_id):
        if not subaccount_id:
            return "No subaccount id supplied. Kindly pass one in"
        endpoint = self._baseUrl + self._endpointMap["subaccount"]["fetch"] + "/"+str(subaccount_id) + "?seckey="+self._getSecretKey()
        return self._handleAccountStatusRequests("Fetch", endpoint)
    
