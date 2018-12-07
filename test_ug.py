from python_rave import Rave, RaveExceptions, Misc
from python_rave.rave_exceptions import RaveError, IncompletePaymentDetailsError, AccountChargeError,TransactionVerificationError, TransactionValidationError, ServerError, CardChargeError, InitiateTransferError, SubaccountCreationError

rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

print(rave.UGMobile.charge({
            "amount": "hdgddd",
            "email": "user@example.com",
            "phonenumber": "08075376980",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
            "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
}))
