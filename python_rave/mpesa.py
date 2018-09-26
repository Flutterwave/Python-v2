'''
- there is a need for a real number
'''

from python_rave import Rave, RaveExceptions, Misc
rave = Rave("ENTIRE_YOUR_PUBLIC_KEY", "ENTIRE_YOUR_SECRET_KEY", usingEnv = False)

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
    res = rave.Mpesa.verify(res["txRef"])
    print(res)

except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])