from python_rave import Rave, RaveExceptions, Misc
rave = Rave(
    "FLWPUBK-92e93a5c487ad64939327052e113c813-X",
    "FLWSECK-61037cfe3cfc53b03e339ee201fa98f5-X",
    usingEnv=False
)

# mobile payload
payload = {
    "amount": "100",
    "phonenumber": "0926420185",
    "email": "dodez@xgmailoo.com",
    "IP": "127.0.0.1",
    "narration": "funds payment",
}

try:
    res = rave.Mpesa.charge(payload)
    res = rave.Mpesa.verify(res["txRef"])
    print(res)

except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
