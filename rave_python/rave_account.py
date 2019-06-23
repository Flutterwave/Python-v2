from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, AccountChargeError, TransactionVerificationError, TransactionValidationError, ServerError

from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json

class Account(Payment):
    """ This is the rave object for account transactions. It contains the following public functions:\n
        .charge -- This is for making an account charge\n
        .validate -- This is called if further action is required i.e. OTP validation\n
        .verify -- This checks the status of your transaction\n
    """
    def __init__(self, publicKey, secretKey, production, usingEnv):
            super(Account, self).__init__(publicKey, secretKey, production, usingEnv)


    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles account charge responses """
        # This checks if we can parse the json successfully
        res =  self._preliminaryResponseChecks(response, AccountChargeError, txRef=txRef)

        responseJson = res["json"]
        # change - added data before flwRef
        flwRef = responseJson['data']["flwRef"]
        
        # If all preliminary checks are passed
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            # If contains authurl
            if not (responseJson["data"].get("authurl", "NO-URL") == "NO-URL"):
                authUrl = responseJson["data"].get("authurl", "NO-URL")
                return {"error": False, "validationRequired": True, "txRef": txRef, "flwRef": flwRef, "authUrl": authUrl}
            # If it doesn't
            else:
                return {"error": False, "validationRequired": True, "txRef": txRef, "flwRef": flwRef, "authUrl": None}

        else:
            return {"error": False, "validationRequired": False, "txRef": txRef, "flwRef": flwRef, "authUrl": None, "validateInstructions": responseJson['data']["validateInstructions"]}
    


    # Charge account function
    def charge(self, accountDetails, hasFailed=False):
        """ This is the ghMobile charge call.\n
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        # setting the endpoint
        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]

        # It is faster to just update rather than check if it is already present
        accountDetails.update({"payment_type": "account"})
        # Here we check because txRef could be set by user
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})
        # Checking for required account components
        requiredParameters = ["accountbank", "accountnumber", "amount", "email", "phonenumber", "IP"]
        return super(Account, self).charge(accountDetails, requiredParameters, endpoint)



