from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json

class GhMobile(Payment):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(GhMobile, self).__init__(publicKey, secretKey, production, usingEnv)


    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        """ This is the ghMobile charge call.
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]
        
        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update({"payment_type": "mobilemoneygh", "country":"GH", "is_mobile_money_gh":"1", "currency":"GHS"})
        
        # If transaction reference is not set 
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})
        # If order reference is not set
        if not ("orderRef" in accountDetails):
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber", "network", "IP", "redirect_url"]
        return super(GhMobile, self).charge(accountDetails, requiredParameters, endpoint)

