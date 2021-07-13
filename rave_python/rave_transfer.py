import requests, json, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_misc import checkIfParametersAreComplete, generateTransactionReference, checkTransferParameters
from rave_python.rave_exceptions import InitiateTransferError, ServerError, TransferFetchError, IncompletePaymentDetailsError


class Transfer(RaveBase):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Transfer, self).__init__(publicKey, secretKey, production, usingEnv)
    
    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, reference):
        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "reference": reference, "errMsg": response})

        # Check if the response contains data parameter
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True, "reference": reference, "errMsg": responseJson.get("message", "Server is down")})
        
        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson


    def _handleInitiateResponse(self, response, transferDetails):
        responseJson = self._preliminaryResponseChecks(response, InitiateTransferError, transferDetails["reference"])
        
        if responseJson["status"] == "success":
            return {"error": False, "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        
        else:
            raise InitiateTransferError({"error": True, "data": responseJson["data"]})

    def _handleBulkResponse(self, response, bulkDetails):
        responseJson = self._preliminaryResponseChecks(response, InitiateTransferError, None)

        if responseJson["status"] == "success":
            return {"error": False, "status": responseJson["status"], "message":responseJson["message"], "id": responseJson["data"].get("id", None), "data": responseJson["data"]}
        else:
            raise InitiateTransferError({"error": True, "data": responseJson["data"]})
    
    # This makes and handles all requests pertaining to the status of your transfer or account
    def _handleTransferStatusRequests(self, feature_name, endpoint, isPostRequest=False, data=None):
        
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
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": feature_name,"message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
            return {"error": False, "returnedData": responseJson}
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": feature_name + "-error","message": responseTime}
            raise TransferFetchError({"error": True, "returnedData": responseJson })

    def _handleTransferRetriesRequests(self, feature_name, endpoint, isPostRequest=False, data=None):
        
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
            errorMessage = responseJson["message"]
        except:
            raise ServerError({"error": True, "errMsg": response.text })

        # Checks if it returns a 2xx code
        if response.ok:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": feature_name,"message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
            return {"error": False, "returnedData": responseJson}
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": feature_name + "-error","message": responseTime}
            return {"error": True, "returnedData": errorMessage }


    def initiate(self, transferDetails):
        
        
        ## feature logic
        # Performing shallow copy of transferDetails to avoid public exposing payload with secret key
        transferDetails = copy.copy(transferDetails)
        
        # adding reference if not already included
        if not ("reference" in transferDetails):
            transferDetails.update({"reference": generateTransactionReference()})
        transferDetails.update({"seckey": self._getSecretKey()})
        
        # These are the parameters required to initiate a transfer
        requiredParameters = ["amount", "currency","beneficiary_name"]
        checkIfParametersAreComplete(requiredParameters, transferDetails)
        checkTransferParameters(requiredParameters, transferDetails)
        
        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }

        endpoint = self._baseUrl + self._endpointMap["transfer"]["initiate"]
        response = requests.post(endpoint, headers=headers, data=json.dumps(transferDetails))

        if response.ok == False:
            #feature logging
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "Initiate-Transfer-error","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "Initiate-Transfer","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        return self._handleInitiateResponse(response, transferDetails)



    def bulk(self, bulkDetails):
        
        # feature logic
        bulkDetails = copy.copy(bulkDetails)
    
        bulkDetails.update({"seckey": self._getSecretKey()})
        requiredParameters = ["title", "bulk_data"]
        checkIfParametersAreComplete(requiredParameters, bulkDetails)
        checkTransferParameters(requiredParameters, bulkDetails)
        endpoint = self._baseUrl + self._endpointMap["transfer"]["bulk"]
        
        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(bulkDetails))
        
        if response.ok == False:
            #feature logging
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "Initiate-Bulk-error","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "Initiate-Bulk","message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleBulkResponse(response, bulkDetails)

    # Not elegant but supports python 2 and 3
    def fetch(self, reference=None):
        
        #feature logic
        label = "Fetch-Transfer"
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fetch"] + "?seckey="+self._getSecretKey()+'&reference='+str(reference)
        return self._handleTransferStatusRequests(label, endpoint)

    def all(self):
        
        #feature logic
        label = "List-all-Transfers"
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fetch"] + "?seckey="+self._getSecretKey()
        return self._handleTransferStatusRequests(label, endpoint)

    def getFee(self, currency=None):
        
        # feature logic
        label = "Get-Transfer-fee-by-Currency"
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fee"] + "?seckey="+self._getSecretKey() + "&currency="+str(currency)
        return self._handleTransferStatusRequests(label, endpoint)
        
    def getBalance(self, currency):
        
        # feature logic
        label = "Get-Balance-fee-by-Currency"
        if not currency: # i made currency compulsory because if it is not assed in, an error message is returned from the server
            raise IncompletePaymentDetailsError("currency", ["currency"])
        endpoint =  self._baseUrl + self._endpointMap["transfer"]["balance"] 
        data = {
            "seckey": self._getSecretKey(),
            "currency": currency
        }

        return self._handleTransferStatusRequests(label, endpoint, data=data, isPostRequest=True)
    
    def retryTransfer(self, transfer_id):
        
        #feature logic
        label = "retry_failed_transfer"
        endpoint = self._baseUrl + self._endpointMap["transfer"]["retry"]
        data = {
            "seckey": self._getSecretKey(),
            "id": transfer_id
        }
        return self._handleTransferRetriesRequests(label, endpoint, data=data, isPostRequest=True)

    def fetchRetries(self, transfer_id):
        label = "fetch_transfer_retries"
        endpoint = self._baseUrl + self._endpointMap["transfer"]["fetch"] + "/" + str(transfer_id) + "/retries?seckey=" + self._getSecretKey()
        return self._handleTransferRetriesRequests(label, endpoint)

    # def walletTransfer(self, transferDetails):
    #     data = {
    #         "seckey": self._getSecretKey(),
    #         "currency": transferDetails["currency"],
    #         "amount": transferDetails["amount"],
    #         "merchant_id": transferDetails["merchant_id"]
    #     }

    #     headers = {
    #         'content-type': 'application/json',
    #     }


    #     endpoint = self._baseUrl + self._endpointMap["transfer"]["inter_wallet"]
    #     response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    #     if response.ok == False:
    #         #feature logging
    #         tracking_endpoint = self._trackingMap
    #         responseTime = response.elapsed.total_seconds()
    #         tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "interwallet_transfers-error","message": responseTime}
    #         tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
    #     else:
    #         tracking_endpoint = self._trackingMap
    #         responseTime = response.elapsed.total_seconds()
    #         tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.12", "title": "interwallet_transfers","message": responseTime}
    #         tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
    #     return self._handleInitiateInterWalletResponse(response, data)

    

