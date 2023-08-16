from rave_python.rave_payment import Payment
from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference

class ApplePay(Payment):
    """ This is the rave object for Apple Pay transactions. It contains the following public functions:\n
        .charge -- This is for charging a Customer with Apple Pay\n
        .verify -- This checks the status of your transaction\n
        .refund -- This initiates the refund for the transaction\n
    """

    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles account charge responses """
        # This checks if we can parse the json successfully
        res = self._preliminaryResponseChecks(
            response, AccountChargeError, txRef=txRef)

        response_json = res['json']
        # change - added data before flwRef
        response_data = response_json['data']
        flw_ref = response_data['flwRef']
        auth_url = response_data['authurl']

        # If all preliminary checks are passed
        data = {
            'error': False,
            'validationRequired': True,
            'authurl': auth_url,
            'txRef': txRef,
            'flwRef': flw_ref,
            'message': "Kindly redirect your user to the authurl. This url is only supported by Safari browsers and Apple Pay enabled devices."
        }

        return data
    
    def charge(self, requestDetails, hasFailed=False):
        """ This is the charge method for Apple Pay payments.\n
             Parameters include:\n
            requestDetails (dict) -- The request parameters for charging your customers with this payment method\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        # setting the endpoint
        endpoint = self._baseUrl + self._endpointMap['account']['charge']
        feature_name = "ApplePay"

        # It is faster to just update rather than check if it is already
        # present

        requestDetails.update({'payment_type': 'applepay'})

        # Generate transaction reference if txRef doesn't exist
        requestDetails.setdefault('txRef', generateTransactionReference())

        # Checking for required account components
        requiredParameters = [
            'amount',
            'email',
            'firstname',
            'lastname',
            'currency'
            ]

        return super(ApplePay, self).charge(feature_name, requestDetails, requiredParameters, endpoint)
    
    """
        TO DOs
        1. Get mocking credentials to test the verify and refund methods for Apple Pay Transactions.
        2. Add unittests for verify and refund methods.
    """

    # def verify(self, txRef):
    #     endpoint = self._baseUrl + self._endpointMap['account']['verify']
    #     feature_name = "Verify eNaira"
    #     return super(ApplePay, self).verify(feature_name, txRef, endpoint)

    # def refund(self, flwRef, amount):
    #     feature_name = "Refund eNaira"
    #     endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
    #     return super(ApplePay, self).refund(feature_name, flwRef, amount)