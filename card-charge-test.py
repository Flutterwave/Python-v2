# CARD TRANSACTION

from python_rave import Rave, RaveExceptions, Misc
    rave = Rave(
        "RAVE_PUBLIC_KEY",
        "RAVE_SECRET_KEY",
        usingEnv=False
    )

# Payload with pin
payload = {
  "cardno": "5438898014560229",
  "cvv": "890",
  "expirymonth": "09",
  "expiryyear": "19",
  "amount": "10",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
  "IP": "355426087298442",
  "PIN": "3310"
}


try:
#     perfom a card charge transaction
    res = rave.Card.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})

        res = rave.Card.charge(payload)

#    perform an otp validation on the transaction
    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "12345")

#    perform a verification if the transaction reference number is valid from when the card was charge or validated
    res = rave.Card.verify(res["txRef"])
    print(res["transactionComplete"])
    print(res)

#   flags an error message if there's a card charge error
except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

#   flags an error message if there's a card Transaction Validation Error
except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

#   flags an error message if there's a card Transaction Verification Error
except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
