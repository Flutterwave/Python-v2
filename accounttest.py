from python_rave import Rave , RaveExceptions

# initialization
OUR_PUBLIC_KEY = "FLWPUBK-3f9b0d8bc9eacc5ce6ee9e167c613c62-X"
YOUR_SECRET_KEY = "FLWSECK-cdbf6713ce1ceb507b1f03fa44040f56-X"

rave = Rave(OUR_PUBLIC_KEY, YOUR_SECRET_KEY, usingEnv = False)

# Acoount test

# account payload
payload = {
  "accountbank": "044",# get the bank code from the bank list endpoint.
  "accountnumber": "0690000031",
  "currency": "NGN",
  "country": "NG",
  "amount": "100",
  "email": "ifunanyaikemma@gmail.com",
  "phonenumber": "08134836828",
  "IP": "355426087298442",
}

try:

# account charge
    res = rave.Account.charge(payload)
    if res["authUrl"]:
        print(res["authUrl"])

    elif res["validationRequired"]:

# account validate
        rave.Account.validate(res["flwRef"], "12345")

# account verify
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

