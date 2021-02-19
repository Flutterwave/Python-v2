import json, requests, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete
from rave_python.rave_exceptions import ServerError, BVNFetchError

class Verify(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Verify, self).__init__(publicKey, secretKey, production, usingEnv)

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

    def _handleVerifyStatusRequests(self, endpoint, feature_name, isPostRequest=False, data=None):
        self.headers = {
            'content-type' : 'application/json'
        }
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
            #feature logging
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name,"message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
            return {"error": False, "returnedData": responseJson}
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error", "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

            raise BVNFetchError({"error": True, "returnedData": responseJson })

    def bvnVerify(self, bvn):

        # feature logic
        if not bvn:
            return "BVN was not supplied. Kindly supply one"
        feature_name = "BVN-verification"
        endpoint = self._baseUrl + self._endpointMap["bvn"]["verify"] +str(bvn)+"?seckey=" + self._getSecretKey()
        return self._handleVerifyStatusRequests(endpoint, feature_name)
