# TRANSFER TRANSACTION

from python_rave import Rave, RaveExceptions
try:
    rave = Rave(
        "RAVE_PUBLIC_KEY",
        "RAVE_SECRET_KEY",
        usingEnv=False
    )

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
            {
                "Bank": "044",
                "Account Number": "0690000032",
                "Amount": 500,
                "Currency": "NGN",
                "Narration": "Bulk transfer 1",
                "reference": "mk-82973029"
            },
            {
                "Bank": "044",
                "Account Number": "0690000034",
                "Amount": 500,
                "Currency": "NGN",
                "Narration": "Bulk transfer 2",
                "reference": "mk-283874750"
            }
        ]
    })
    print(res)
    # print(res2)
    rave.Transfer.getBalance()

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
