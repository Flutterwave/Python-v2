from python_rave import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)
try:

    # res = rave.PaymentPlan.createPlan({
    #     "amount": 1,
    #     "duration": 5,
    #     "name": "Ultimate Play",
    #     "interval": "dai"
    # })
    # print(res)
    
    res = rave.PaymentPlan.fetchPlan('Ultimate Play')
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

# except RaveExceptions.InitiateTransferError as e:
#     print(e.err)

# except RaveExceptions.TransferFetchError as e:
#     print(e.err)

# except RaveExceptions.ServerError as e:
#     print(e.err)
