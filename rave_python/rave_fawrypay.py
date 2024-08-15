from rave_python.rave_payment import Payment
from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference

class FawryPay(Payment):
    """ This is the rave object for Fawry Pay transactions. It contains the following public functions:\n
        .charge -- Charge your Customers with Fawry Pay. This is only supported in Egypt.\n
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

        # If all preliminary checks are passed
        data = {
            'error': False,
            'validationRequired': True,
            'txRef': txRef,
            'flwRef': flw_ref,
            'message': "Please make payment with the flwRef returned in the response which should be the same as the reference sent via SMS"
        }

        return data
    
    def charge(self, requestDetails, hasFailed=False):
        """ This is the charge method for Fawry Pay payments.\n
             Parameters include:\n
            requestDetails (dict) -- The request parameters for charging your customers with this payment method\n
            hasFailed (boolean) -- This is a flag to determine if the attempt had previously failed due to a timeout\n
        """

        # setting the endpoint
        endpoint = self._baseUrl + self._endpointMap['account']['charge']
        feature_name = "FawryPay"

        # It is faster to just update rather than check if it is already
        # present

        requestDetails.update(
            {
                'payment_type': 'fawry_pay',
                'currency': 'EGP'
            }
        )

        # Generate transaction reference if txRef doesn't exist
        requestDetails.setdefault('txRef', generateTransactionReference())

        # Checking for required account components
        requiredParameters = [
            'amount',
            'email',
            'firstname',
            'lastname',
            'phonenumber'
            ]

        return super(FawryPay, self).charge(feature_name, requestDetails, requiredParameters, endpoint)
    
    """
        TO DOs
        1. Get mocking credentials to test the verify and refund methods for FawryPay Transactions.
        2. Add unittests for verify and refund methods.
    """

    # def verify(self, txRef):
    #     endpoint = self._baseUrl + self._endpointMap['account']['verify']
    #     feature_name = "Verify eNaira"
    #     return super(FawryPay, self).verify(feature_name, txRef, endpoint)

    # def refund(self, flwRef, amount):
    #     feature_name = "Refund eNaira"
    #     endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
    #     return super(FawryPay, self).refund(feature_name, flwRef, amount)