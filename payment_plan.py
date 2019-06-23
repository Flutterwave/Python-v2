from rave_python import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK_TEST-e10b3814bd004570a499605cfc95bd67-X", "FLWSECK_TEST-afa4f993af3695bdef2e9d22e746b7c1-X", usingEnv = False)
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