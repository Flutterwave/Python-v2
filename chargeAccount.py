from python_rave import Rave
from python_rave import RaveExceptions
from python_rave import Misc


# initialise rave 
rave = Rave(
    "FLWPUBK-a5715a67d24e61ce3e7bf79ae22ef524-X", 
    "FLWSECK-6577e947f692e979e2d306ab4ce0a282-X", 
    usingEnv = False)

#Account to charge
payload = {
    "accountbank": "044",
    "accountnumber": "0690000031",
    "amount":"100",
    "email":"e.ikedieze@gmail.com",
    "phonenumber":"08030930236",
    "country":"Nigeria",
    "IP":"355426087298442"
}

try: 
    #Charge call
    res = rave.Account.charge(payload)
    if res["authUrl"]:
        print(res["authUrl"])

    elif res["validationRequired"]:
        rave.Account.validate(res["flwRef"], "12345")

    res = rave.Account.verify(res["txRef"])
    print(res)

except RaveExceptions.AccountChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])