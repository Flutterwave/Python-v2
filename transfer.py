from python_rave import Rave, RaveExceptions, Misc
try:

    # test keys
    rave = Rave(
        "FLWPUBK-56e4a2c6c9a6b58364bfd07fc1993e2c-X", 
        "FLWSECK-ea81e705d82161de5b7757c897d96ba4-X", 
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
