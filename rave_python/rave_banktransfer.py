from rave_python.rave_payment import Payment
from rave_python.rave_exceptions import AccountChargeError
from rave_python.rave_misc import generateTransactionReference

class BankTransfer(Payment):
    """ This is the rave object for pay with bank transfer transactions. It contains the following public functions:\n
        .charge -- This is for making a pay with bank transfer charge\n
        .verify -- This checks the status of your transaction\n
        .refunds -- This initiates the refund for a PWBT transaction\n
    """

    def _handleChargeResponse(self, response, txRef, request=None):
        """ This handles account charge responses """
        # This checks if we can parse the json successfully
        res = self._preliminaryResponseChecks(
            response, AccountChargeError, txRef=txRef)

        response_json = res['json']
        # change - added data before flwRef
        response_data = response_json['data']
        flw_ref = response_data['flw_reference']
        bank_name = response_data['bankname']
        account_number = response_data['accountnumber']
        expiry = response_data['expiry_date']
        desc = response_data['note']

        # If all preliminary checks are passed
        data = {
            'error': False,
            'validationRequired': False,
            'txRef': txRef,
            'flwRef': flw_ref,
            'bankName': bank_name,
            'accountNumber': account_number,
            'expiresIn': expiry,
            'transferNote': desc
        }
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
        feature_name = "Pay with Bank Transfer"

        # It is faster to just update rather than check if it is already
        # present
        accountDetails.update({
            'payment_type': 'banktransfer',
            'is_bank_transfer': True,
            'country': 'NG'
            })

        # Generate transaction reference if txRef doesn't exist
        accountDetails.setdefault('txRef', generateTransactionReference())

        # Checking for required account components
        requiredParameters = [
            'amount',
            'email',
            'firstname',
            'lastname'
            ]

        return super(BankTransfer, self).charge(feature_name, accountDetails, requiredParameters, endpoint)

    def verify(self, txRef):
        endpoint = self._baseUrl + self._endpointMap['account']['verify']
        feature_name = "Verify PWBT"
        return super(BankTransfer, self).verify(feature_name, txRef, endpoint)

    def refund(self, flwRef, amount):
        feature_name = "Refund PWBT"
        endpoint = self._baseUrl + self._endpointMap["account"]["refund"]
        return super(BankTransfer, self).refund(feature_name, flwRef, amount)
 