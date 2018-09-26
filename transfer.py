from python_rave import Rave, RaveExceptions, Misc
try:

    # test keys
    rave = Rave(
        "YOUR_PUBLIC_KEY", 
        "YOUR_SECRET_KEY", 
        usingEnv = False
        )

    # for single transfers
    res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    })

    print("Initiate Response--->") 
    print(res)

    # for bulk transfers
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
    print("Bulk Response--->")
    print(res2)

    print("Get Balance--->")
    rave.Transfer.getBalance()

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
