from python_rave import Rave
from python_rave import RaveExceptions
from python_rave import Misc


# initialise rave 
rave = Rave(
    "FLWPUBK-a5715a67d24e61ce3e7bf79ae22ef524-X", 
    "FLWSECK-6577e947f692e979e2d306ab4ce0a282-X",
    usingEnv = False)

#Card to charge

payload = {
    "cardno": "5061460410120223210",
    "cvv": "780",
    "expirymonth": "12",
    "expiryyear": "21",
    "amount": "100",
    "email": "codenuel@gmail.com",
    "phonenumber": "08030930236",
    "firstname": "Ikedieze",
    "lastname": "Ndukwe",
    "IP": "355426087298442",
    "pin" : "3310",
}

try:
    res = rave.Card.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
        res = rave.Card.charge(payload)

    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "12345")

    res = rave.Card.verify(res["txRef"])
    # print(res["transactionComplete"])
    print(res)

except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])


