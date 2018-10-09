from python_rave import Rave, Misc, RaveExceptions
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_PRIVATE_KEY", usingEnv = False)
try:

    res = rave.PaymentPlan.createPlan({
        "amount": 1,
        "duration": 5,
        "name": "Ultimate Plan",
        "interval": "dai"
    })
    
    res = rave.PaymentPlan.editPlan(880, {
        "name": "Jack's Plan",
        "status": "active"
    })
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
