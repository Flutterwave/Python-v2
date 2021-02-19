import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, IncompleteCardDetailsError, BillCreationError, BillStatusError

class Bills(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        self.headers = {
            'content-type' : 'application/json'
        }
        super(Bills, self).__init__(publicKey, secretKey, production, usingEnv)

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
        responseJson = self._preliminaryResponseChecks(response, BillCreationError, details["service"])

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"] }

        else:
            raise BillCreationError({"error": True, "data": responseJson["data"]})


    #function to create a Bill
    #Params: details - a dict containing service, service_method, service_version, service_channel and service_payload
    def create(self, details):
        
        # Performing shallow copy of planDetails to avoid public exposing payload with secret key
        details = copy.copy(details)
        details.update({"seckey": self._getSecretKey()})
        requiredParameters = ["service", "service_method", "service_version", "service_channel"]
        checkIfParametersAreComplete(requiredParameters, details)
        endpoint = self._baseUrl + self._endpointMap["bills"]["create"]
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(details))

        # feature logging
        if response.ok == False:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {
                "publicKey": self._getPublicKey(),
                "language": "Python v2", 
                "version": "1.2.10", 
                "title": "Create-Bills-error", 
                "message": responseTime
                }
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {
                "publicKey": self._getPublicKey(),
                "language": "Python v2", 
                "version": "1.2.10", 
                "title": "Create-Bills", 
                "message": responseTime
                }
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleCreateResponse(response, details)
