from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

# mobile payload
payload = {
    "amount": "100",
    "phonenumber": "0926420185",
    "email": "user@exampe.com",
    "IP": "40.14.290",
    "narration": "funds payment",
}

try:
    res = rave.Mpesa.charge(payload)
    if res["validationRequired"]:
        transaction_ref = res["txRef"]
        res = rave.Mpesa.verify(transaction_ref)
        print(res)

except RaveExceptions.TransactionChargeError as e:
    print("Trans charge error")
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print("Trans Verif error")
    print(e.err["errMsg"])
    print(e.err["txRef"])
