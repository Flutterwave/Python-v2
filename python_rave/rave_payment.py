import requests, json, copy
from python_rave.rave_base import RaveBase
from python_rave.rave_exceptions import RaveError, IncompletePaymentDetailsError, AuthMethodNotSupportedError, TransactionChargeError, TransactionVerificationError, TransactionValidationError, ServerError, RefundError
from python_rave.rave_misc import checkIfParametersAreComplete

# All payment subclasses are encrypted classes
class Payment(RaveBase):
    """ This is the base class for all the payments """
    def __init__(self, publicKey, secretKey, production, usingEnv):
        # Instantiating the base class
        super(Payment, self).__init__(publicKey, secretKey, production, usingEnv)


    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, txRef=None, flwRef=None):
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

    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles transaction charge responses """

        # If we cannot parse the json, it means there is a server error
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)

        responseJson = res["json"]
        flwRef = res["flwRef"]
        
        # if all preliminary tests pass
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            return {"error": False,  "validationRequired": True, "txRef": txRef, "flwRef": flwRef}
        else:
            return {"error": False,  "validationRequired": False, "txRef": txRef, "flwRef": flwRef}


    # This can be altered by implementing classes but this is the default behaviour
    # Returns True and the data if successful
    def _handleVerifyResponse(self, response, txRef):
        """ This handles all responses from the verify call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the verify call
         """

        res = self._preliminaryResponseChecks(response, TransactionVerificationError, txRef=txRef)


        responseJson = res["json"]
        flwRef = responseJson["data"]["flwref"]
        acctmessage = responseJson["data"]["acctmessage"]
        chargecode = responseJson["data"]["chargecode"]
        # print(responseJson)

        # Check if the chargecode is 00
        if not (responseJson["data"].get("chargecode", None) == "00"):
            return {"error": False, "transactionComplete": False, "txRef": txRef, "flwRef":flwRef}
        
        else:
            return {"error": False, "transactionComplete": True, "txRef": txRef, "flwRef":flwRef, "acctmessage": acctmessage, "chargecode": chargecode}

    
    # returns true if further action is required, false if it isn't    
    def _handleValidateResponse(self, response, flwRef, request=None):
        """ This handles validation responses """

        # If json is not parseable, it means there is a problem in server
            
        res = self._preliminaryResponseChecks(response, TransactionValidationError, flwRef=flwRef)

        responseJson = res["json"]
        txRef = res["txRef"]

        # Of all preliminary checks passed
        if not (responseJson["data"].get("tx", responseJson["data"]).get("chargeResponseCode", None) == "00"):
            errMsg = responseJson["data"].get("tx", responseJson["data"]).get("chargeResponseMessage", None)
            raise TransactionValidationError({"error": True, "txRef": txRef, "flwRef": flwRef , "errMsg": errMsg})

        else:
            return {"error": False, "txRef": txRef, "flwRef": flwRef}


    # Charge function (hasFailed is a flag that indicates there is a timeout), shouldReturnRequest indicates whether to send the request back to the _handleResponses function
    def charge(self, paymentDetails, requiredParameters, endpoint, shouldReturnRequest=False):
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

        # Encrypting payment details (_encrypt is inherited from RaveEncryption)
        encryptedPaymentDetails = self._encrypt(json.dumps(paymentDetails))

        # Collating request headers
        headers = {
            'content-type': 'application/json',
        }
        
        # Collating the payload for the request
        payload = {
            "PBFPubKey": paymentDetails["PBFPubKey"],
            "client": encryptedPaymentDetails,
            "alg": "3DES-24"
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        if shouldReturnRequest:
            return self._handleChargeResponse(response, paymentDetails["txRef"], paymentDetails)
        else:
            return self._handleChargeResponse(response, paymentDetails["txRef"])
       

    def validate(self, flwRef, otp, endpoint=None):
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
        return self._handleValidateResponse(response, flwRef)
        
    # Verify charge
    def verify(self, txRef, endpoint=None):
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
        return self._handleVerifyResponse(response, txRef)

    # Refund call
    # def refund(self, flwRef):
    #     """ This is used to refund a transaction from any of Rave's component objects.\n 
    #          Parameters include:\n
    #         flwRef (string) -- This is the flutterwave reference returned from a successful call from any component. You can access this from action["flwRef"] returned from the charge call
    #     """
    #     payload = {
    #         "ref": flwRef,
    #         "seckey": self._getSecretKey(),
    #     }
    #     headers = {
    #         "Content-Type":"application/json"
    #     }
    #     endpoint = self._baseUrl+self._endpointMap["refund"]

    #     response = requests.post(endpoint, headers = headers, data=json.dumps(payload))

    #     try:
    #         responseJson = response.json()
    #     except ValueError:
    #         raise ServerError(response)
        
    #     if responseJson.get("status", None) == "error":
    #         raise RefundError(responseJson.get("message", None))
    #     elif responseJson.get("status", None) == "success":
    #         return True, responseJson.get("data", None)


        


