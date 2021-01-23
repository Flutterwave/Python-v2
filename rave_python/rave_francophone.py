from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, MobileChargeError, TransactionVerificationError, TransactionValidationError, ServerError
from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json
import webbrowser

class Francophone(Payment):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Francophone, self).__init__(publicKey, secretKey, production, usingEnv)


    # returns true if further action is required, false if it isn't    
    # def _handleChargeResponse(self, response, txRef, request=None):
    #     """ This handles charge responses """
    #     res =  self._preliminaryResponseChecks(response, MobileChargeError, txRef=txRef)

    #     responseJson = res["json"]
    #     flwRef = res["flwRef"]

    #     # Checking if there is redirect url

    #     if responseJson["data"]["data"].get("redirect_url", "N/A") == "N/A":
    #         redirectUrl = None
    #     else:
    #         redirectUrl = responseJson["data"]["data"]["redirect_url"]

    #     # If all preliminary checks passed
    #     if not (responseJson["data"].get("chargeResponseCode", None) == "00"):
    #         # Otherwise we return that further action is required, along with the response
    #         # suggestedAuth = responseJson["data"].get("suggested_auth", None)
    #         return {
    #                     "error": False, 
    #                     "status": responseJson["status"],  
    #                     "message": responseJson["message"],
    #                     "code": responseJson["data"]["code"],
    #                     "transaction status": responseJson["data"]["status"],
    #                     "ts": responseJson["data"]["ts"],
    #                     "link": responseJson["data"]["link"]
    #                 }
    #     else:
    #         return {"error": False, "status": responseJson["status"],  "validationRequired": False, "txRef": txRef, "flwRef": flwRef, "suggestedAuth": None, "redirectUrl": redirectUrl}
    
    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        """ This is the charge call for central francophone countries.
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        feature_name = "Initiate-Francophone-mobile-money-charge"
        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]

        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update({"payment_type": "mobilemoneyfrancophone", "is_mobile_money_franco":"1"})
        
        # If transaction reference is not set 
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})

        # If order reference is not set
        if not ("orderRef" in accountDetails):
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        # requiredParameters = ["amount", "email", "phonenumber", "IP", "redirect_url"]
        requiredParameters = ["amount"]
        return super(Francophone, self).charge(feature_name, accountDetails, requiredParameters, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Francophone-charge-refund"
        endpoint = self._baseUrl + self._endpointMap["refund"]
        return super(Francophone, self).refund(feature_name, flwRef, amount)
