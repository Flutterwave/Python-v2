
from python_rave import Rave , Misc, RaveExceptions 

# initialization
YOUR_PUBLIC_KEY = "FLWPUBK-3f9b0d8bc9eacc5ce6ee9e167c613c62-X"
YOUR_SECRET_KEY = "FLWSECK-cdbf6713ce1ceb507b1f03fa44040f56-X"

rave = Rave(YOUR_PUBLIC_KEY, YOUR_SECRET_KEY, usingEnv = False)

# Payload with pin
payload = {
  "cardno": "5438898014560229",
  "cvv": "789",
  "expirymonth": "09",
  "expiryyear": "19",
  "amount": "10",
  "email": "ifunanyaikemma@gmail.com",
  "phonenumber": "08134836828",
  "firstname": "ifunanya",
  "lastname": "Ikemma",
  "IP": "355426087298442",
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
    print(res["transactionComplete"])

except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])