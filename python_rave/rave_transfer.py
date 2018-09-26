import requests, json, copy
from python_rave.rave_base import RaveBase
from python_rave.rave_misc import checkIfParametersAreComplete, generateTransactionReference
from python_rave.rave_exceptions import InitiateTransferError, ServerError, TransferFetchError
class Transfer(RaveBase):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Transfer, self).__init__(publicKey, secretKey, production, usingEnv)
    
    
    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, reference):
        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "reference": txRef, "errMsg": response})

        # Check if the response contains data parameter
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True, "reference": reference, "errMsg": responseJson.get("message", "Server is down")})
        
        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": errMsg})

        return responseJson


    def _handleInitiateResponse(self, response, transferDetails):
        responseJson = self._preliminaryResponseChecks(response, InitiateTransferError, transferDetails["reference"])
        
        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        
        else:
            raise InitiateTransferError({"error": True, data: responseJson["data"]})

    def _handleBulkResponse(self, response, bulkDetails):
        responseJson = self._preliminaryResponseChecks(response, InitiateTransferError, None)

        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        else:
            raise InitiateTransferError({"error": True, data: responseJson["data"]})

            
    def initiate(self, transferDetails):
        # Performing shallow copy of transferDetails to avoid public exposing payload with secret key
        transferDetails = copy.copy(transferDetails)

        # adding reference if not already included
        if not ("reference" in transferDetails):
            transferDetails.update({"reference": generateTransactionReference()})
        transferDetails.update({"seckey": self._getSecretKey()})

        # These are the parameters required to initiate a transfer
        requiredParameters = ["amount", "currency"]
        checkIfParametersAreComplete(requiredParameters, transferDetails)

        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        
        endpoint = self._baseUrl + self._endpointMap["transfer"]["initiate"]
        response = requests.post(endpoint, headers=headers, data=json.dumps(transferDetails))
        return self._handleInitiateResponse(response, transferDetails)



    def bulk(self, bulkDetails):
        
        bulkDetails = copy.copy(bulkDetails)
        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }

        bulkDetails.update({"seckey": self._getSecretKey()})

        requiredParameters = ["title", "bulk_data"]

        checkIfParametersAreComplete(requiredParameters, bulkDetails)

        endpoint = self._baseUrl + self._endpointMap["transfer"]["bulk"]
        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(bulkDetails))
        return self._handleBulkResponse(response, bulkDetails)

    
    # This makes and handles all requests pertaining to the status of your transfer or account
    def _handleTransferStatusRequests(self, endpoint, isPostRequest=False, data=None):
        # Request headers
        headers = {
            'content-type': 'application/json',
        }

        # Checks if it is a post request
        if isPostRequest:
            response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        else:
            response = requests.get(endpoint, headers=headers)

        # Checks if it can be parsed to json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text })

        # Checks if it returns a 2xx code
        if response.ok:
            return {"error": False, "returnedData": responseJson}
        else:
            raise TransferFetchError({"error": True, "returnedData": responseJson })

    # Not elegant but supports python 2 and 3
    def fetch(self, id=None, q=None, reference=None, page=None, status=None, batch_id=None):
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fetch"] + "?seckey="+self._getSecretKey()+"&id="+str(id)+"&q="+str(q)+"&reference="+str(reference)+"&page="+str(page)+"&status="+str(status)+"&batch_id="+str(batch_id)
        return self._handleTransferStatusRequests(endpoint)

    def getFee(self, currency=None):
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fee"] + "?seckey="+self._getSecretKey() + "&currency="+str(currency)
        return self._handleTransferStatusRequests(endpoint)
        
    def getBalance(self, currency=None):
        endpoint = self._baseUrl + self._endpointMap["transfer"]["balance"] 
        data = {
            "seckey": self._getSecretKey(),
            "currency": currency
        }
        return self._handleTransferStatusRequests(endpoint, data=data, isPostRequest=True)

    

