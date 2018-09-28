from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

def account(payload):
# account payload
    try:
        res = rave.Account.charge(payload)
        print("Account Charge ")
        print(res)
        if res["authUrl"]:
            print(res["authUrl"])

        elif res["validationRequired"]:
            print(rave.Account.validate(res["flwRef"], "12345"))
            
        res = rave.Account.verify(res["txRef"])
        print(res)
        return res
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


if __name__ == __name__:
    account(payload = {
    "accountbank":"044",
    "accountnumber":"0690000031",
    "amount":"500",
    "country":"NG",
    "email":"varisiv@gmail.com",
    "phonenumber":"08031142735",
    "IP":"127.0.0.1"
})