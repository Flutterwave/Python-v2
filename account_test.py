from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)
# account payload
payload = {
    "accountbank":"044",
    "accountnumber":"0690000031",
    "amount":"500",
    "country":"NG",
    "email":"varisiv@gmail.com",
    "phonenumber":"08031142735",
    "IP":"127.0.0.1"
}
try:
    res = rave.Account.charge(payload)
    print(res)
    if res["authUrl"]:
        print(res["authUrl"])

    elif res["validationRequired"]:
        rave.Account.validate(res["flwRef"], "12345")

    res = rave.Account.verify(res["txRef"])
    print(res)

except RaveExceptions.AccountChargeError as e:
    print("Acc charge error")
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print("Trans charge error")
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print("Trans Verif charge error")
    print(e.err["errMsg"])
    print(e.err["txRef"])
