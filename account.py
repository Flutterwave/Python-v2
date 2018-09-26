from python_rave import Rave, RaveExceptions, Misc

rave = Rave(
  "YOUR_PUBLIC_KEY", 
  "YOUR_SECRET_KEY", 
  usingEnv = False
  )

# account payload
payload = {
  "accountbank": "044",#bank code
  "accountnumber": "0690000031",
  "currency": "NGN",
  "country": "NG",
  "amount": "100",
  "email": "test@test.com",
  "phonenumber": "07031056082",
  "IP": "355426087298442",
}

# res = rave.Account.charge(payload)
# print(res)

try:
    res = rave.Account.charge(payload)
    if res["authUrl"]:
        print(res["authUrl"])

    elif res["validationRequired"]:
        rave.Account.validate(res["flwRef"], "12345")

    res = rave.Account.verify(res["txRef"])
    print(res)

except RaveExceptions.AccountChargeError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
