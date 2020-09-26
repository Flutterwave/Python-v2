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

        #feature logging
        tracking_endpoint = self._trackingMap
        tracking_payload = {"publicKey": self._getPublicKey(),"language": "Python v2", "version": "1.2.5", "title": "Incoming call","message": "Initiate-Uganda-mobile-money-charge"}
        tracking_response = requests.post(tracking_endpoint, data=json.dumps(tracking_payload))
        
        ## feature logic
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
        return super(UGMobile, self).charge(accountDetails, requiredParameters, endpoint)

