from python_rave import Misc, Rave, RaveExceptions

# rave = Rave(
#     "RAVE_PUBLIC_KEY",
#     "RAVE_SECRET_KEY",
#     usingEnv=False
# )

rave = Rave(
    "FLWPUBK-92e93a5c487ad64939327052e113c813-X",
    "FLWSECK-61037cfe3cfc53b03e339ee201fa98f5-X",
    usingEnv = False
    )

# account payload
payload = {
    "accountbank": "044",  # get the bank code from the bank list endpoint.
    "accountnumber": "0690000031",
    "currency": "NGN",
    "country": "NG",
    "amount": "100",
    "email": "test@test.com",
    "phonenumber": "0902620185",
    "IP": "127.0.0.1",
}



# ACCOUNT TRANSACTION

try:
#   perform an account charge transaction

    res = rave.Account.charge(payload)
    authUrl = res['authUrl']
    validationRequired = res["validationRequired"]

    if authUrl:
        print(authUrl)

#   perform an otp validation on the transaction
    elif validationRequired:
        rave.Account.validate(res["flwRef"], "12345")

#   perform a verification if the transaction reference number is valid from when the charge or validation occured
    res = rave.Account.verify(res["txRef"])
    print(res)

#   flags an error message if there's an Account Charge Error
except RaveExceptions.AccountChargeError as e:
    print(e.err)
    print(e.err["flwRef"])

#   flags an error message if there's an Account Transaction Validation Error
except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

#   flags an error message if there's an Account Transaction Verification Error
except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
