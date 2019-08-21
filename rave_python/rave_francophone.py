from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, MobileChargeError, TransactionVerificationError, TransactionValidationError, ServerError
from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json
import webbrowser

class Francophone(Payment):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Francophone, self).__init__(publicKey, secretKey, production, usingEnv)


    # returns true if further action is required, false if it isn't    
    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles charge responses """
        res =  self._preliminaryResponseChecks(response, MobileChargeError, txRef=txRef)

        responseJson = res["json"]
        flwRef = res["flwRef"]

        # Checking if there is redirect url
        if responseJson["data"]["data"].get("redirect_url", "N/A") == "N/A":
            redirectUrl = None
        else:
            redirectUrl = responseJson["data"]["data"]["redirect_url"]

        # If all preliminary checks passed
        if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
            # Otherwise we return that further action is required, along with the response
            suggestedAuth = responseJson["data"].get("suggested_auth", None)
            return {"error": False,  "validationRequired": True, "txRef": txRef, "flwRef": flwRef, "suggestedAuth": suggestedAuth, "redirectUrl": redirectUrl}
        else:
            return {"error": False, "status": responseJson["status"],  "validationRequired": False, "txRef": txRef, "flwRef": flwRef, "suggestedAuth": None, "redirectUrl": redirectUrl}
    
    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        """ This is the charge call for central francophone countries.
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]
        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update({"payment_type": "mobilemoneyfrancophone", "is_mobile_money_franco":"1", "currency":"XOF"})
        
        # If transaction reference is not set 
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})
        # If order reference is not set
        if not ("orderRef" in accountDetails):
            accountDetails.update({"orderRef": generateTransactionReference()})
        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber", "IP", "redirect_url"]
        return super(Francophone, self).charge(accountDetails, requiredParameters, endpoint)
