from python_rave import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)
try:

    # res = rave.Transfer.initiate({
    # "account_bank": "044",
    # "account_number": "0690000044",
    # "amount": 500,
    # "narration": "New transfer",
    # "currency": "NGN",
    # })
    
    # res = rave.Transfer.getBalance('EUR')
    # print(res)

    res2 = rave.Transfer.bulk({
        "title":"May Staff Salary",
        "bulk_data":[
            {
                "Ban":"044",
                "Account Number": "0690000032",
                "Amount":500,
                "Currency":"NGN",
                "Narration":"Bulk transfer 1",
                "reference": "mk-82973029"
            },
            {
                "Bank":"044",
                "Account Number": "0690000034",
                "Amount":500,
                "Currency":"NGN",
                "Narration":"Bulk transfer 2",
                "reference": "mk-283874750"
            }
        ]
        })
    print(res2)
    # rave.Transfer.getBalance()

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
