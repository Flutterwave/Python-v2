from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

# Payload with pin
payload = {
  "cardno": "5399838383838381",
  "cvv": "470",
  "expirymonth": "10",
  "expiryyear": "22",
  "amount": "100",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
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