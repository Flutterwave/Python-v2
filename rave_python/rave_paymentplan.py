import requests, json, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete, generateTransactionReference
from rave_python.rave_exceptions import  ServerError, IncompletePaymentDetailsError, PlanCreationError, PlanStatusError

class PaymentPlan(RaveBase) :
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type': 'application/json'
        }
        super(PaymentPlan, self).__init__(publicKey, secretKey, production, usingEnv)
    
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
    
    def _handleCreateResponse(self, response, planDetails):
        responseJson = self._preliminaryResponseChecks(response, PlanCreationError, planDetails["name"])
        
        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        
        else:
            raise PlanCreationError({"error": True, "data": responseJson["data"]})

    # This makes and handles all requests pertaining to the status of your payment plans
    def _handlePlanStatusRequests(self, type, endpoint, isPostRequest=False, data=None):

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
    #Params: planDetails - a dict containing amount, name, interval, duration
    #if duration is not passed, any subscribed customer will be charged #indefinitely
    def create(self, planDetails):
        # Performing shallow copy of planDetails to avoid public exposing payload with secret key
        planDetails = copy.copy(planDetails)
        planDetails.update({"seckey": self._getSecretKey()})

        requiredParameters = ["amount", "name", "interval"]
        checkIfParametersAreComplete(requiredParameters, planDetails)

        endpoint = self._baseUrl + self._endpointMap["payment_plan"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(planDetails))
        return self._handleCreateResponse(response, planDetails)

    #gets all payment plans connected to a merchant's account
    def all(self):
        endpoint = self._baseUrl + self._endpointMap["payment_plan"]["list"] + "?seckey="+self._getSecretKey()
        return self._handlePlanStatusRequests("List", endpoint)
    
    def fetch(self, plan_id=None, plan_name=None):
        if plan_id:
            endpoint = self._baseUrl + self._endpointMap["payment_plan"]["fetch"] + "?seckey="+self._getSecretKey() + "&id="+str(plan_id)
        elif plan_name:
            endpoint = self._baseUrl + self._endpointMap["payment_plan"]["fetch"] + "?seckey="+self._getSecretKey() + "&1="+plan_name
        else:
            return "You must pass either plan id or plan name in order to fetch a plan's details"
        return self._handlePlanStatusRequests("Fetch", endpoint)
    
    def cancelPlan(self, plan_id):
        if not id:
            return "Plan id was not supplied. Kindly supply one"
        endpoint = self._baseUrl + self._endpointMap["payment_plan"]["cancel"] + str(plan_id) + "/cancel"
        data = {"seckey": self._getSecretKey()}
        return self._handlePlanStatusRequests("Cancel", endpoint, isPostRequest=True, data=data)
    
    # edits a payment plan
    # Params
    # id: payment plan id *required
    # newData: dict that contains the information to be updated i.e name and status-cancelled/active
    def edit(self, plan_id, newData={}):
        if not id:
            return "Plan id was not supplied. Kindly supply one"
        endpoint = self._baseUrl + self._endpointMap["payment_plan"]["edit"] + str(plan_id) + "/edit"
        data = {"seckey": self._getSecretKey(), "name": newData.get("name", None), "status": newData.get("status", None)}
        return self._handlePlanStatusRequests("Edit", endpoint, isPostRequest=True, data=data)
