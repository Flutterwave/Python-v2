from rave_python.rave_account import Account
from rave_python.rave_bills import Bills
from rave_python.rave_card import Card
from rave_python.rave_ebills import Ebills
from rave_python.rave_francophone import Francophone
from rave_python.rave_ghmobile import GhMobile
from rave_python.rave_mpesa import Mpesa
from rave_python.rave_paymentplan import PaymentPlan
from rave_python.rave_preauth import Preauth
from rave_python.rave_base import RaveBase
from rave_python.rave_recipient import Recipient
from rave_python.rave_rwmobile import RWMobile
from rave_python.rave_settlement import Settlement
from rave_python.rave_subaccounts import SubAccount
from rave_python.rave_subscription import Subscriptions
from rave_python.rave_transfer import Transfer
from rave_python.rave_ugmobile import UGMobile
from rave_python.rave_ussd import Ussd
from rave_python.rave_verify import Verify
from rave_python.rave_virtualaccount import VirtualAccount
from rave_python.rave_virtualcard import VirtualCard
from rave_python.rave_zbmobile import ZBMobile


class Rave:
    
    def __init__(self, publicKey, secretKey, production=False, usingEnv=True):
        """ This is main organizing object. It contains the following:\n
            rave.Account -- For bank account transactions\n
            rave.Bills -- For Bills payments\n
            rave.Card -- For card transactions\n
            rave.Francophone -- For West African Francophone mobile money transactions\n
            rave.GhMobile -- For Ghana mobile money transactions\n
            rave.Mpesa -- For mpesa transactions\n
            rave.PaymentPlan -- For payment plan creation and operation\n
            rave.Preauth -- For preauthorized transactions\n
            rave.RWMobile -- For Rwanda mobile money transactions\n
            rave.Settlement -- For settled transactions\n
            rave.SubAccount -- For creation of subaccounts for split payment operations\n
            rave.Transfer -- For Payouts and transfers\n
            rave.UGMobile -- For Uganda mobile money transactions\n
            rave.Ussd -- For ussd transactions\n
            rave.VirtualAccount -- For virtual account transactions\n
            rave.VirtualCard -- For virtual card transactions\n 
            rave.ZBMobile -- For Zambia mobile money transactions\n
            
        """

        classes = (
            Account, Bills, Card, Ebills, Francophone, GhMobile, Mpesa, PaymentPlan, Preauth, Recipient, RWMobile, Settlement, SubAccount, Subscriptions, Transfer, UGMobile, Ussd, Verify, VirtualAccount, VirtualCard, ZBMobile
        )

        for _class in classes:
            attr = _class(publicKey, secretKey, production, usingEnv)
            setattr(self, _class.__name__, attr)
        
      
