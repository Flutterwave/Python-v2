from rave_python.rave_base import RaveBase
from rave_python.rave_card import Card
from rave_python.rave_account import Account
from rave_python.rave_ussd import Ussd
from rave_python.rave_ghmobile import GhMobile
from rave_python.rave_ugmobile import UGMobile
from rave_python.rave_zbmobile import ZBMobile
from rave_python.rave_rwmobile import RWMobile
from rave_python.rave_mpesa import Mpesa
from rave_python.rave_preauth import Preauth
from rave_python.rave_transfer import Transfer
from rave_python.rave_paymentplan import PaymentPlan
from rave_python.rave_subaccounts import SubAccount
from rave_python.rave_subscription import Subscriptions

class Rave:
    
    def __init__(self, publicKey, secretKey, usingEnv=True):
        """ This is main organizing object. It contains the following:\n
            rave.Card -- For card transactions\n
            rave.Preauth -- For preauthorized transactions\n
            rave.Account -- For bank account transactions\n
            rave.Ussd -- For ussd transactions\n
            rave.GhMobile -- For Ghana mobile money transactions\n
            rave.UGMobile -- For Uganda mobile money transactions\n
            rave.ZBMobile -- For Zambia mobile money transactions\n
            rave.RWMobile -- For Rwanda mobile money transactions\n
            rave.Mpesa -- For mpesa transactions\n
        """
        
        # Creating member objects already initiated with the publicKey and secretKey
        self.Card = Card(publicKey, secretKey, usingEnv)
        self.Preauth = Preauth(publicKey, secretKey, usingEnv)
        self.PaymentPlan = PaymentPlan(publicKey, secretKey, usingEnv)
        self.SubAccount = SubAccount(publicKey, secretKey, usingEnv)
        self.Subscriptions = Subscriptions(publicKey, secretKey, usingEnv)
        # These all use the account endpoint till further changes, the enpoint maps are defined in rave_base
        self.Account = Account(publicKey, secretKey, usingEnv)
        self.Ussd = Ussd(publicKey, secretKey, usingEnv)
        self.GhMobile = GhMobile(publicKey, secretKey, usingEnv)
        self.ZBMobile = ZBMobile(publicKey, secretKey, usingEnv)
        self.RWMobile = RWMobile(publicKey, secretKey, usingEnv)
        self.UGMobile = UGMobile(publicKey, secretKey, usingEnv)
        self.Mpesa = Mpesa(publicKey, secretKey, usingEnv)
        # Transfer endpoint
        self.Transfer = Transfer(publicKey, secretKey, usingEnv)
        
        
