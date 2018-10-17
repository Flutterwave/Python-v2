from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-a5715a67d24e61ce3e7bf79ae22ef524-X", 
            "FLWSECK-6577e947f692e979e2d306ab4ce0a282-X", 
            usingEnv = False)

# mobile payload
payload = {
    "amount": "100",
    "phonenumber": "0926420185",
    "email": "e.ikedieze@gmail.com",
    "IP": "40.14.290",
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