from python_rave import Rave, RaveExceptions, Misc

rave = Rave(
  "YOUR_PUBLIC_KEY", 
  "YOUR_SECRET_KEY", 
  usingEnv = False
  )

# Payload with pin
payload = {
  "cardno": "5399838383838381",
  "cvv": "470",
  "expirymonth": "10",
  "expiryyear": "22",
  "amount": "1400",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
  "IP": "355426087298442",
}

try:
    res = rave.Card.charge(payload)
    # print(res)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin": #put the customers pin here
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
        res = rave.Card.charge(payload)

    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "12345")# collect otp from customer

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
