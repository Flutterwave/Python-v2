from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, AccountChargeError, TransactionVerificationError, TransactionValidationError, ServerError
from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference
import json, requests

class Mpesa(Payment):
    
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Mpesa, self).__init__(publicKey, secretKey, production, usingEnv)

    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        
        """ This is the mpesa charge call.\n
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """
        ## feature logic
        # Setting the endpoint
        feature_name = "Initiate-Mpesa-charge"
        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]
        
        # Adding boilerplate mpesa requirements
        accountDetails.update({"payment_type": "mpesa", "country":"KE", "is_mpesa":"1", "is_mpesa_lipa":"1", "currency":"KES"})
        
        # If transaction reference is not set 
        if not ("txRef" in accountDetails):
            accountDetails.update({"txRef": generateTransactionReference()})
        
        # If order reference is not set
        if not ("orderRef" in accountDetails):
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber", "IP"]
        res = super(Mpesa, self).charge(feature_name, accountDetails, requiredParameters, endpoint, isMpesa=True)
        return res

    def verify(self, txRef):
        feature_name = "Verify-Mpesa_charge"
        endpoint = self._baseUrl + self._endpointMap["account"]["verify"]
        return super(Mpesa, self).verify(feature_name, txRef, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Mpesa-charge-refund"
        endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
        return super(Mpesa, self).refund(feature_name, flwRef, amount)
