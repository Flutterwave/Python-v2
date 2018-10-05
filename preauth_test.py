from python_rave import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

# Payload with pin
payload = {
  "token":"flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k",
    "country":"NG",
    "amount":1000,
    "email":"user@gmail.com",
    "firstname":"temi",
    "lastname":"Oyekole",
    "IP":"190.233.222.1",
    "txRef":"MC-7666-YU",
    "currency":"NGN",
}

try:
    res = rave.Preauth.charge(payload)
    print(res)
    res = rave.Preauth.refund(res["flwRef"], 500)
    print(res)
    # if res["suggestedAuth"]:
    #     arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

    #     if arg == "pin":
    #         Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
    #     if arg == "address":
    #         Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
    #     res = rave.Preauth.charge(payload)

    # if res["validationRequired"]:
    #     rave.Preauth.validate(res["flwRef"], "12345")

    # res = rave.Preauth.capture(res["flwRef"])
    # res = rave.Preauth.verify(res["txRef"])
    # print(res["transactionComplete"])

except RaveExceptions.CardChargeError as e:
    print(e)
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])