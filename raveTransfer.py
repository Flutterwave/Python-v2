from python_rave import Rave, RaveExceptions
try:
    rave = Rave("FLWPUBK-a5715a67d24e61ce3e7bf79ae22ef524-X", "FLWSECK-6577e947f692e979e2d306ab4ce0a282-X", usingEnv = False)

    res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    })

    res2 = rave.Transfer.bulk({
        "title": "test",
        "bulk_data":[
            {
                "account_bank": "044",
                "account_number": "0690000044",
                "amount": 500,
                "narration": "New transfer",
                "currency": "NGN",
            },
            {
                "account_bank": "044",
                "account_number": "0690000044",
                "amount": 500,
                "narration": "New transfer",
                "currency": "NGN",
            },
            {
                "account_bank": "044",
                "account_number": "0690000044",
                "amount": 500,
                "narration": "New transfer",
                "currency": "NGN",
            }
        ]
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
