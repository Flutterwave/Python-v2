from rave_python import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK_TEST-******************************-X", "FLWSECK_TEST-********************************-X", usingEnv = False)
try:

    # res = rave.PaymentPlan.createPlan({
    #     "amount": 10,
    #     "duration": 5,
    #     "name": "New Plan",
    #     "interval": "daily"
    # })
    
    res = rave.PaymentPlan.editPlan(2115, {
        "name": "Today's Plan",
        "status": "active"
    })
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)