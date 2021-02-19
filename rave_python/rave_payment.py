import requests, json, copy
from rave_python.rave_base import RaveBase
from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, AuthMethodNotSupportedError, TransactionChargeError, TransactionVerificationError, TransactionValidationError, ServerError, RefundError, PreauthCaptureError
from rave_python.rave_misc import checkIfParametersAreComplete

response_object = {
    "error": False,
    "transactionComplete": False,
    "flwRef": "",
    "txRef": "",
    "chargecode": '00',
    "status": "",
    "vbvcode": "",
    "vbvmessage": "",
    "acctmessage": "",
    "currency": "",
    "chargedamount": 00,
    "chargemessage": ""
}

# All payment subclasses are encrypted classes
class Payment(RaveBase):
    """ This is the base class for all the payments """
    def __init__(self, publicKey, secretKey, production, usingEnv):
        # Instantiating the base class
        super(Payment, self).__init__(publicKey, secretKey, production, usingEnv)

    @classmethod
    def retrieve(cls, mapping, *keys): 
        return (mapping[key] for key in keys) 

    @classmethod
    def deleteUnnecessaryKeys(cls,response_dict, *keys):
        for key in keys:
            del response_dict[key]
        return response_dict

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, txRef=None, flwRef=None):
        preliminary_error_response = copy.deepcopy(response_object)
        preliminary_error_response = Payment.deleteUnnecessaryKeys(preliminary_error_response, "transactionComplete", "chargecode", "vbvmessage", "vbvcode", "acctmessage", "currency")

        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": response})


        # Check if the response contains data parameter
        if responseJson.get("data", None):
            if txRef:
                flwRef = responseJson["data"].get("flwRef", None)
            if flwRef:
                txRef = responseJson["data"].get("txRef", None)
        else:
            raise TypeOfErrorToRaise({"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": responseJson.get("message", "Server is down")})
        
        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "txRef": txRef, "flwRef": flwRef, "errMsg": errMsg})
        
        return {"json": responseJson, "flwRef": flwRef, "txRef": txRef}

    def _handleChargeResponse(self, response, txRef, request=None, isMpesa=False):
        """ This handles transaction charge responses """

        # If we cannot parse the json, it means there is a server error
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)
        
        
        responseJson = res["json"]

        if isMpesa:
            return {
                "error": False, 
                "status": responseJson["status"], 
                "validationRequired": True, 
                "txRef": txRef, 
                "flwRef": responseJson["data"]["flwRef"], 
                "narration": responseJson["data"]["narration"]
                }
        else:
            # if all preliminary tests pass
            if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
                if responseJson.get("message", 'None') == 'Momo initiated':
                    return {
                            "error": False, 
                            "status": responseJson["status"],  
                            "message": responseJson["message"],
                            "code": responseJson["data"]["code"],
                            "transaction status": responseJson["data"]["status"],
                            "ts": responseJson["data"]["ts"],
                            "link": responseJson["data"]["link"]
                        }

                return {"error": False, "status": responseJson["status"],"validationRequired": True, "txRef": txRef, "flwRef": responseJson["data"]["flwRef"], "chargeResponseMessage": responseJson["data"]["chargeResponseMessage"]}
            else:
                return {"error": True,  "validationRequired": False, "txRef": txRef, "flwRef": responseJson["data"]["flwRef"]}
    
    def _handleCaptureResponse(self, response, request=None):
        """ This handles transaction charge responses """

        # If we cannot parse the json, it means there is a server error
        res = self._preliminaryResponseChecks(response, PreauthCaptureError, txRef='')
        
        responseJson = res["json"]
        flwRef = responseJson["data"]["flwRef"]
        txRef = responseJson["data"]["txRef"]
        
        # if all preliminary tests pass
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            return {"error": False,  "validationRequired": True, "txRef": txRef, "flwRef": flwRef}
        else:
            return {"error": False, "status":responseJson["status"], "message": responseJson["message"],  "validationRequired": False, "txRef": txRef, "flwRef": flwRef}


    # This can be altered by implementing classes but this is the default behaviour
    # Returns True and the data if successful
    def _handleVerifyResponse(self, response, txRef):
        """ This handles all responses from the verify call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the verify call
         """
        verify_response = copy.deepcopy(response_object)
        res = self._preliminaryResponseChecks(response, TransactionVerificationError, txRef=txRef)


        responseJson = res["json"]
        # retrieve necessary properties from response 
        verify_response["status"] = responseJson['status']
        verify_response['flwRef'], verify_response["txRef"], verify_response["vbvcode"], verify_response["vbvmessage"], verify_response["acctmessage"], verify_response["currency"], verify_response["chargecode"], verify_response["amount"], verify_response["chargedamount"], verify_response["chargemessage"] = Payment.retrieve(responseJson['data'], "flwref", "txref", "vbvcode", "vbvmessage", "acctmessage", "currency", "chargecode", "amount", "chargedamount", "chargemessage")

        # Check if the chargecode is 00
        if verify_response['chargecode'] == "00":
            verify_response["error"] = False
            verify_response["transactionComplete"] = True
            return verify_response
        
        else:
            verify_response["error"] = True # changed to True on 15/10/2018
            verify_response["transactionComplete"] = False
            return verify_response
        
        # # Check if the chargecode is 00
        # if not (responseJson["data"].get("chargecode", None) == "00"):
        #     return {"error": False, "transactionComplete": False, "txRef": txRef, "flwRef":flwRef}
        
        # else:
        #     return {"error": False, "transactionComplete": True, "txRef": txRef, "flwRef":flwRef}

    
    # returns true if further action is required, false if it isn't    
    def _handleValidateResponse(self, response, flwRef, request=None):
        """ This handles validation responses """

        # If json is not parseable, it means there is a problem in server
            
        res = self._preliminaryResponseChecks(response, TransactionValidationError, flwRef=flwRef)

        responseJson = res["json"]
        if responseJson["data"].get("tx") == None:
            txRef = responseJson["data"]["txRef"]
        else:
            txRef = responseJson["data"]["tx"]["txRef"]

        # Of all preliminary checks passed
        if not (responseJson["data"].get("tx", responseJson["data"]).get("chargeResponseCode", None) == "00"):
            errMsg = responseJson["data"].get("tx", responseJson["data"]).get("chargeResponseMessage", None)
            raise TransactionValidationError({"error": True, "txRef": txRef, "flwRef": flwRef , "errMsg": errMsg})

        else:
            return {"status": responseJson["status"], "message": responseJson["message"], "error": False, "txRef": txRef, "flwRef": flwRef}


    # Charge function (hasFailed is a flag that indicates there is a timeout), shouldReturnRequest indicates whether to send the request back to the _handleResponses function
    def charge(self, feature_name, paymentDetails, requiredParameters, endpoint, shouldReturnRequest=False, isMpesa=False):
        """ This is the base charge call. It is usually overridden by implementing classes.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
            requiredParameters (list) -- These are the parameters required for the specific call\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
            shouldReturnRequest -- This determines whether a request is passed to _handleResponses\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
        except: 
            raise
        
        # Performing shallow copy of payment details to prevent tampering with original
        paymentDetails = copy.copy(paymentDetails)
        
        # Adding PBFPubKey param to paymentDetails
        paymentDetails.update({"PBFPubKey": self._getPublicKey()})

        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        if "token" in paymentDetails:
            paymentDetails.update({"SECKEY": self._getSecretKey()})
            # print(json.dumps(paymentDetails))
            response = requests.post(endpoint, headers=headers, data=json.dumps(paymentDetails))
        else:
            # Encrypting payment details (_encrypt is inherited from RaveEncryption)
            encryptedPaymentDetails = self._encrypt(json.dumps(paymentDetails))
            
            # Collating the payload for the request
            payload = {
                "PBFPubKey": paymentDetails["PBFPubKey"],
                "client": encryptedPaymentDetails,
                "alg": "3DES-24"
            }
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            
            #feature logging
            if response.ok:
                tracking_endpoint = self._trackingMap
                responseTime = response.elapsed.total_seconds()
                tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name, "message": responseTime}
                tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
            else:
                tracking_endpoint = self._trackingMap
                responseTime = response.elapsed.total_seconds()
                tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error", "message": responseTime}
                tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        
        if shouldReturnRequest:
            if isMpesa:
                return self._handleChargeResponse(response, paymentDetails["txRef"], paymentDetails, True)
            return self._handleChargeResponse(response, paymentDetails["txRef"], paymentDetails)
        else:
            if isMpesa:
                return self._handleChargeResponse(response, paymentDetails["txRef"], paymentDetails, True)
            return self._handleChargeResponse(response, paymentDetails["txRef"])
        
       

    def validate(self, feature_name, flwRef, otp, endpoint=None):
        """ This is the base validate call.\n
             Parameters include:\n
            flwRef (string) -- This is the flutterwave reference returned from a successful charge call. You can access this from action["flwRef"] returned from the charge call\n
            otp (string) -- This is the otp sent to the user \n
        """

        if not endpoint: 
            endpoint = self._baseUrl + self._endpointMap["account"]["validate"]
            
        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        
        payload = {
            "PBFPubKey": self._getPublicKey(),
            "transactionreference": flwRef, 
            "transaction_reference": flwRef,
            "otp": otp
        }
        
        response = requests.post(endpoint, headers = headers, data=json.dumps(payload))

        #feature logging
        if response.ok:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name, "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error", "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleValidateResponse(response, flwRef)
        
    # Verify charge
    def verify(self, feature_name, txRef, endpoint=None):
        """ This is used to check the status of a transaction.\n
             Parameters include:\n
            txRef (string) -- This is the transaction reference that you passed to your charge call. If you didn't define a reference, you can access the auto-generated one from payload["txRef"] or action["txRef"] from the charge call\n
        """
        if not endpoint:
            endpoint = self._baseUrl + self._endpointMap["verify"]

        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }

        # Payload for the request headers
        payload = {
            "txref": txRef,
            "SECKEY": self._getSecretKey()
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

        #feature logging
        if response.ok:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name, "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error", "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        return self._handleVerifyResponse(response, txRef)

    #Refund call
    def refund(self, feature_name, flwRef, amount, ):
        """ This is used to refund a transaction from any of Rave's component objects.\n 
             Parameters include:\n
            flwRef (string) -- This is the flutterwave reference returned from a successful call from any component. You can access this from action["flwRef"] returned from the charge call
        """
        payload = {
            "ref": flwRef,
            "seckey": self._getSecretKey(),
            "amount": amount,
        }
        headers = {
            "Content-Type":"application/json"
        }
        endpoint = self._baseUrl + self._endpointMap["refund"]

        response = requests.post(endpoint, headers = headers, data=json.dumps(payload))

        #feature logging
        if response.ok:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name, "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        else:
            tracking_endpoint = self._trackingMap
            responseTime = response.elapsed.total_seconds()
            tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.10", "title": feature_name + "-error", "message": responseTime}
            tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))

        try:
            responseJson = response.json()
        except ValueError:
            raise ServerError(response)
        
        if responseJson.get("status", None) == "error":
            raise RefundError(responseJson.get("message", None))
        elif responseJson.get("status", None) == "success":
            return True, responseJson.get("data", None)

        # responseJson =response.json()
        # return responseJson.get("data", None)
        


