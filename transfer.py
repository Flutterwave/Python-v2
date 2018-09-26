from python_rave import Rave, RaveExceptions
try:
    YOUR_PUBLIC_KEY = "#"
    YOUR_SECRET_KEY = "#"

    rave = Rave(YOUR_PUBLIC_KEY, YOUR_SECRET_KEY, usingEnv = False)

    res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    })
    print(res)
    rave.Transfer.getBalance()

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
