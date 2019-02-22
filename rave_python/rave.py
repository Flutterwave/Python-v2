from rave_python.rave_base import RaveBase
from rave_python.rave_card import Card
from rave_python.rave_account import Account
from rave_python.rave_ussd import Ussd
from rave_python.rave_ghmobile import GhMobile
from rave_python.rave_ghmobile import GhMobile
from rave_python.rave_ugmobile import UGMobile
from rave_python.rave_zbmobile import ZBMobile
from rave_python.rave_mpesa import Mpesa
from rave_python.rave_preauth import Preauth
from rave_python.rave_transfer import Transfer
from rave_python.rave_paymentplan import PaymentPlan
from rave_python.rave_subaccounts import SubAccount
from rave_python.rave_subscription import Subscriptions

class Rave:
    
    def __init__(self, publicKey, secretKey, production=False, usingEnv=True):
        """ This is main organizing object. It contains the following:\n
            rave.Card -- For card transactions\n
            rave.Preauth -- For preauthorized transactions\n
            rave.Account -- For bank account transactions\n
            rave.Ussd -- For ussd transactions\n
            rave.GhMobile -- For Ghana mobile money transactions\n
            rave.UGMobile -- For Uganda mobile money transactions\n
            rave.ZBMobile -- For Zambia mobile money transactions\n
            rave.Mpesa -- For mpesa transactions\n
        """
        
        # Creating member objects already initiated with the publicKey and secretKey
        self.Card = Card(publicKey, secretKey, production, usingEnv)
        self.Preauth = Preauth(publicKey, secretKey, production, usingEnv)
        self.PaymentPlan = PaymentPlan(publicKey, secretKey, production, usingEnv)
        self.SubAccount = SubAccount(publicKey, secretKey, production, usingEnv)
        self.Subscriptions = Subscriptions(publicKey, secretKey, production, usingEnv)
        # These all use the account endpoint till further changes, the enpoint maps are defined in rave_base
        self.Account = Account(publicKey, secretKey, production, usingEnv)
        self.Ussd = Ussd(publicKey, secretKey, production, usingEnv)
        self.GhMobile = GhMobile(publicKey, secretKey, production, usingEnv)
        self.ZBMobile = ZBMobile(publicKey, secretKey, production, usingEnv)
        self.UGMobile = UGMobile(publicKey, secretKey, production, usingEnv)
        self.Mpesa = Mpesa(publicKey, secretKey, production, usingEnv)
        # Transfer endpoint
        self.Transfer = Transfer(publicKey, secretKey, production, usingEnv)
        
        
