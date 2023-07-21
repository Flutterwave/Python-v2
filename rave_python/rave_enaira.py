from rave_python.rave_payment import Payment
from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference

class Enaira(Payment):
    """ This is the rave object for eNaira wallet transactions. It contains the following public functions:\n
        .charge -- This is for charging the eNaira wallet\n
        .verify -- This checks the status of your transaction\n
        .refunds -- This initiates the refund for the transaction\n
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

        data = {
            'error': False,
            'validationRequired': True,
            'txRef': txRef,
            'flwref': flw_ref
        }
        
        if 'qr_image' in response_data:
            data.update({
                'validateInstructions': "Please scan the qr image in your eNaira app.",
                'image': response_data['qr_image']
                })
        else:
            data.update({
                'validateInstructions': response_data['validate_instructions'],
                'image': None
                })

        # If all preliminary checks are passed
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
        feature_name = "eNaira Payments"

        # It is faster to just update rather than check if it is already
        # present

        if accountDetails.get("is_token") == True:
            accountDetails.update({'payment_type': 'enaira', 'is_token': True, 'country': 'NG'})
        else:
            accountDetails.update({'payment_type': 'enaira', 'is_qr': True, 'country': 'NG'})

        # Generate transaction reference if txRef doesn't exist
        accountDetails.setdefault('txRef', generateTransactionReference())

        # Checking for required account components
        requiredParameters = [
            'amount',
            'email',
            'firstname',
            'lastname'
            ]

        return super(Enaira, self).charge(feature_name, accountDetails, requiredParameters, endpoint)

    def validate(self, flwRef, otp):
        endpoint = self._baseUrl + self._endpointMap['account']['validate']
        feature_name = "Account-charge-validate"
        return super().validate(feature_name, flwRef, endpoint)
    
    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap['account']['verify']
        feature_name = "Verify eNaira"
        return super(Enaira, self).verify(feature_name, txRef, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Refund eNaira"
        endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
        return super(Enaira, self).refund(feature_name, flwRef, amount)
 