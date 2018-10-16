from python_rave import Rave, RaveExceptions
try:
    rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X",
                "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv=False)

    res = rave.Transfer.initiate({
        "account_bank": "044",
        "account_number": "0690000044",
        "amount": 500,
        "narration": "New transfer",
        "currency": "NGN",
    })

    res2 = rave.Transfer.bulk({
        "title": "test",
        "bulk_data": [
        ]
    })
    print(res)

    balanceresponse = rave.Transfer.getBalance("NGN")
    print(balanceresponse)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
