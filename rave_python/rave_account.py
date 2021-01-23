from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference
from rave_python.rave_payment import Payment


class Account(Payment):
    """ This is the rave object for account transactions. It contains the following public functions:\n
        .charge -- This is for making an account charge\n
        .validate -- This is called if further action is required i.e. OTP validation\n
        .verify -- This checks the status of your transaction\n
    """
    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles account charge responses """
        # This checks if we can parse the json successfully
        res =  self._preliminaryResponseChecks(response, AccountChargeError, txRef=txRef)

        response_json = res['json']
        # change - added data before flwRef
        response_data = response_json['data']
        flw_ref = response_data['flwRef']

        # If all preliminary checks are passed
        data = {
            'error': False,
            'validationRequired': True,
            'txRef': txRef,
            'flwRef': flw_ref,
            'authUrl': None,
        }
        if response_data.get("chargeResponseCode") != "00":
            # If contains authurl
            data['authUrl'] = response_data.get("authurl")  # None by default
        else:
            data['validateInstructions'] = response_data['validateInstructions']
        return data

    # Charge account function
    def charge(self, accountDetails, hasFailed=False):
        """ This is the direct account charge call.\n
             Parameters include:\n
            accountDetails (dict) -- These are the parameters passed to the function for processing\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        # setting the endpoint
        endpoint = self._baseUrl + self._endpointMap['account']['charge']
        feature_name = "Initiate-Account-charge"

        # It is faster to just update rather than check if it is already present
        accountDetails.update({'payment_type': 'account'})

        # Generate transaction reference if txRef doesn't exist
        accountDetails.setdefault('txRef', generateTransactionReference())

        # Checking for required account components
        requiredParameters = ['accountbank', 'accountnumber', 'amount', 'email', 'phonenumber', 'IP']

        return super().charge(feature_name, accountDetails, requiredParameters, endpoint)

    def validate(self, flwRef, otp):
        endpoint = self._baseUrl + self._endpointMap['account']['validate']
        feature_name = "Account-charge-validate"
        return super().validate(feature_name, flwRef, endpoint)

    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap['account']['verify']
        feature_name = "Account-charge-verify"
        return super().verify(feature_name, txRef, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Account-charge-refund"
        endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
        return super().refund(feature_name, flwRef, amount)