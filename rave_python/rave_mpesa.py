from rave_python.rave_misc import generateTransactionReference
from rave_python.rave_payment import Payment


class Mpesa(Payment):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Mpesa, self).__init__(publicKey, secretKey, production, usingEnv)

    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        """This is the mpesa charge call.\n
         Parameters include:\n
        accountDetails (dict) -- These are the parameters passed to the function for processing\n
        hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """
        # feature logic
        # Setting the endpoint
        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]

        # Adding boilerplate mpesa requirements
        accountDetails.update(
            {
                "payment_type": "mpesa",
                "country": "KE",
                "is_mpesa": "1",
                "is_mpesa_lipa": "1",
                "currency": "KES",
            }
        )

        # If transaction reference is not set
        if "txRef" not in accountDetails:
            accountDetails.update({"txRef": generateTransactionReference()})

        # If order reference is not set
        if "orderRef" not in accountDetails:
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber", "IP"]
        res = super(Mpesa, self).charge(
            accountDetails, requiredParameters, endpoint, isMpesa=True
        )
        return res

    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap["account"]["verify"]
        return super(Mpesa, self).verify(txRef, endpoint)

    def refund(self, flwRef, amount):
        endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
        return super(Mpesa, self).refund(flwRef, amount)
