from rave_python.rave_misc import generateTransactionReference
from rave_python.rave_payment import Payment


class Francophone(Payment):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(Francophone, self).__init__(publicKey, secretKey, production, usingEnv)

    # Charge mobile money function

    def charge(self, accountDetails, hasFailed=False):
        """This is the charge call for central francophone countries.
         Parameters include:\n
        accountDetails (dict) -- These are the parameters passed to the function for processing\n
        hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]

        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update(
            {"payment_type": "mobilemoneyfranco", "is_mobile_money_franco": "1"}
        )

        # If transaction reference is not set
        if "txRef" not in accountDetails:
            accountDetails.update({"txRef": generateTransactionReference()})

        # If order reference is not set
        if "orderRef" not in accountDetails:
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber"]
        return super(Francophone, self).charge(
            accountDetails, requiredParameters, endpoint
        )

    def refund(self, flwRef, amount):
        endpoint = self._baseUrl + self._endpointMap["refund"]
        return super(Francophone, self).refund(flwRef, amount)

    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap["verify"]
        return super(Francophone, self).verify(txRef)
