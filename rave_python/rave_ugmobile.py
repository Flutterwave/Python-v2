from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json, requests

class UGMobile(Payment):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(UGMobile, self).__init__(publicKey, secretKey, production, usingEnv)

    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        
        """ This is the ghMobile charge call.
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """
        
        feature_name = "Uganda-MoMo-charge"
        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]
        
        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update({"payment_type": "mobilemoneyuganda", "country":"NG", "is_mobile_money_ug":"1", "currency":"UGX", "network": "UGX"})
        
        # If transaction reference is not set 
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})
        
        # If order reference is not set
        if not ("orderRef" in accountDetails):
            accountDetails.update({"orderRef": generateTransactionReference()})
        
        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber", "network", "IP"]
        return super(UGMobile, self).charge(feature_name, accountDetails, requiredParameters, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Uganda-MoMo-refund"
        endpoint = self._baseUrl + self._endpointMap["refund"]
        return super(UGMobile, self).refund(feature_name, flwRef, amount)

    def verify(self, txRef):
        feature_name = "Uganda-MoMo-verify"
        endpoint = self._baseUrl + self._endpointMap["verify"]
        return super(UGMobile, self).verify(feature_name, txRef)

