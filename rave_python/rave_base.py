import os, hashlib, warnings, requests, json
from rave_python.rave_exceptions import ServerError, RefundError
import base64
from Crypto.Cipher import DES3
class RaveBase(object):
    """ This is the core of the implementation. It contains the encryption and initialization functions. It also contains all direct rave functions that require publicKey or secretKey (refund) """
    def __init__(self, publicKey=None, secretKey=None, production=False, usingEnv=True):

        # config variables (protected)
        self._baseUrlMap = ["https://ravesandboxapi.flutterwave.com/", "https://api.ravepay.co/"]
        self._trackingMap = "https://kgelfdz7mf.execute-api.us-east-1.amazonaws.com/staging/sendevent"
        self._endpointMap = {
            "bills": {
                "create":"v2/services/confluence",
            },
            "bvn": {
                "verify": "v2/kyc/bvn/",
            },
            "card": {
                "charge": "flwv3-pug/getpaidx/api/charge",
                "validate": "flwv3-pug/getpaidx/api/validatecharge",
                "verify": "flwv3-pug/getpaidx/api/v2/verify",
                "chargeSavedCard": "flwv3-pug/getpaidx/api/tokenized/charge",
                "refund": "gpx/merchant/transactions/refund"
            },
            "ebills": {
                "create": "flwv3-pug/getpaidx/api/ebills/generateorder/",
                "update": "flwv3-pug/getpaidx/api/ebills/update/",
            },
            "preauth": {
                "charge": "flwv3-pug/getpaidx/api/tokenized/preauth_charge",
                "capture": "flwv3-pug/getpaidx/api/capture",
                "refundorvoid": "flwv3-pug/getpaidx/api/refundorvoid"
            },
            "account": {
                "charge": "flwv3-pug/getpaidx/api/charge",
                "validate": "flwv3-pug/getpaidx/api/validate",
                "verify": "flwv3-pug/getpaidx/api/v2/verify",
                "refund": "gpx/merchant/transactions/refund"
            },
            "payment_plan": {
                "create": "v2/gpx/paymentplans/create",
                "fetch": "v2/gpx/paymentplans/query",
                "list": "v2/gpx/paymentplans/query",
                "cancel": "v2/gpx/paymentplans/",
                "edit" :  "v2/gpx/paymentplans/"
            },
            "subscriptions": {
                "fetch": "v2/gpx/subscriptions/query",
                "list": "v2/gpx/subscriptions/query",
                "cancel": "v2/gpx/subscriptions/",
                "activate" : "v2/gpx/subscriptions/"
            },
            "settlements": {
                "list": "v2/merchant/settlements",
                "fetch": "v2/merchant/settlements/",
            },
            "subaccount": {
                "create": "v2/gpx/subaccounts/create",
                "list": "v2/gpx/subaccounts/",
                "fetch": "v2/gpx/subaccounts/get",
                "update": "v2/gpx/subaccounts/edit",
                "delete": "v2/gpx/subaccounts/delete",
            },
            "transfer": {
                "initiate": "v2/gpx/transfers/create",
                "bulk": "v2/gpx/transfers/create_bulk",
                "fetch": "v2/gpx/transfers",
                "fee": "v2/gpx/transfers/fee",
                "balance": "v2/gpx/balance",
                "accountVerification": "flwv3-pug/getpaidx/api/resolve_account",
                "retry": "v2/gpx/transfers/retry",
                "inter_wallet": "v2/gpx/transfers/wallet"
            },
            "recipient":{
                "create": "v2/gpx/transfers/beneficiaries/create",
                "list": "v2/gpx/transfers/beneficiaries",
                "fetch": "v2/gpx/transfers/beneficiaries",
                "delete": "v2/gpx/transfers/beneficiaries/delete",
            },
            "virtual_card": {
                "create": "v2/services/virtualcards/new",
                "list": "v2/services/virtualcards/search",
                "get": "v2/services/virtualcards/get",
                "terminate": "v2/services/virtualcards/",
                "fund": "v2/services/virtualcards/fund",
                "transactions": "v2/services/virtualcards/",
                "withdraw": "v2/services/virtualcards/withdraw",
                "freeze": "v2/services/virtualcards/",
                "unfreeze": "v2/services/virtualcards/",
            },
            "virtual_account":{
                "create" : "v2/banktransfers/accountnumbers",
            },
            "verify": "flwv3-pug/getpaidx/api/v2/verify",
            "refund": "gpx/merchant/transactions/refund"
            
        }
        

        # Setting up public and private keys (private)
        # If we are using environment variables to store secretKey
        if(usingEnv):  
            self.__publicKey = publicKey
            self.__secretKey = os.getenv("RAVE_SECRET_KEY", None)

            if (not self.__publicKey) or (not self.__secretKey):
                raise ValueError("Please set your RAVE_SECRET_KEY environment variable. Otherwise, pass publicKey and secretKey as arguments and set usingEnv to false")

        # If we are not using environment variables
        else:
            if (not publicKey) or (not secretKey):
                raise ValueError("\n Please provide as arguments your publicKey and secretKey. \n It is advised however that you provide secret key as an environment variables. \n To do this, remove the usingEnv flag and save your keys as environment variables, RAVE_PUBLIC_KEY and RAVE_SECRET_KEY")
    
            else:
                self.__publicKey = publicKey
                self.__secretKey = secretKey

                # Raise warning about not using environment variables
                warnings.warn("Though you can use the usingEnv flag to pass secretKey as an argument, it is advised to store it in an environment variable, especially in production.", SyntaxWarning)

        # Setting instance variables
        # 
        # production/non-production variables (protected)
        self._isProduction = production 
        self._baseUrl = self._baseUrlMap[production]

        # encryption key (protected)
        self._encryptionKey = self.__getEncryptionKey()

    

    # This generates the encryption key (private)
    def __getEncryptionKey(self):
        """ This generates the encryption key """
        if(self.__secretKey):
            hashedseckey = hashlib.md5(self.__secretKey.encode("utf-8")).hexdigest()
            hashedseckeylast12 = hashedseckey[-12:]
            seckeyadjusted = self.__secretKey.replace('FLWSECK-', '')
            seckeyadjustedfirst12 = seckeyadjusted[:12]
            key = seckeyadjustedfirst12 + hashedseckeylast12
            return key

        raise ValueError("Please initialize RavePay")
    
    # This returns the public key
    def _getPublicKey(self):
        return self.__publicKey
    
    # This returns the secret key
    def _getSecretKey(self):
        return self.__secretKey

    # This encrypts text
    def _encrypt(self, plainText):
        """ This is the encryption function.\n
             Parameters include:\n 
            plainText (string) -- This is the text you wish to encrypt
        """
        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        key = self.__getEncryptionKey()
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, hence the need for the conversion below
        test = plainText.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted
        





    