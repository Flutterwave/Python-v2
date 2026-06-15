from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference
from rave_python.rave_payment import Payment


class TZSMobile(Payment):
    def __init__(self, publicKey, secretKey, production, usingEnv):
        super(TZSMobile, self).__init__(publicKey, secretKey, production, usingEnv)

    def _handleChargeResponse(self, response, txRef, request=None):
        """This handles account charge responses"""
        # This checks if we can parse the json successfully
        res = self._preliminaryResponseChecks(response, AccountChargeError, txRef=txRef)

        response_json = res["json"]
        # change - added data before flwRef
        response_data = response_json["data"]
        flw_ref = response_data["data"]["flw_reference"]
        processor_message = response_data["response_message"]

        # If all preliminary checks are passed
        data = {
            "error": False,
            "validationRequired": False,
            "txRef": txRef,
            "flwref": flw_ref,
            "message": processor_message,
        }
        return data

    # Charge mobile money function
    def charge(self, accountDetails, hasFailed=False):
        """This is the TZS Mobile Money charge.
         Parameters include:\n
        accountDetails (dict) -- These are the parameters passed to the function for processing\n
        hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        endpoint = self._baseUrl + self._endpointMap["account"]["charge"]

        # It is faster to add boilerplate than to check if each one is present
        accountDetails.update(
            {
                "payment_type": "mobilemoneytanzania",
                "country": "TZ",
                "is_mobile_money_tz": True,
                "currency": "TZS",
            }
        )

        # If transaction reference is not set
        if "txRef" not in accountDetails:
            accountDetails.update({"txRef": generateTransactionReference()})

        # If order reference is not set
        if "orderRef" not in accountDetails:
            accountDetails.update({"orderRef": generateTransactionReference()})

        # Checking for required account components
        requiredParameters = ["amount", "email", "phonenumber"]

        return super(TZSMobile, self).charge(
            accountDetails, requiredParameters, endpoint
        )

    def refund(self, flwRef, amount):
        endpoint = self._baseUrl + self._endpointMap["refund"]
        return super(TZSMobile, self).refund(flwRef, amount)

    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap["verify"]
        return super(TZSMobile, self).verify(txRef)
