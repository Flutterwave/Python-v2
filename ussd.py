from python_rave import Rave, RaveExceptions, Misc
rave = Rave(
    "FLWPUBK-92e93a5c487ad64939327052e113c813-X",
    "FLWSECK-61037cfe3cfc53b03e339ee201fa98f5-X",
    usingEnv=False
)

zenithPayload = {
    "accountbank": "057",
    "accountnumber": "0691008392",  # collect the customers account number for Zenith
    "currency": "NGN",
    "country": "NG",
    "amount": "10",
    "email": "dodez@xgmailoo.com",
    "phonenumber": "0902620185",
    "IP": "355426087298442",
}

furtherActionNeeded, action = rave.Ussd.charge(zenithPayload)
if furtherActionNeeded:
  completed = False
  while not completed:
    try:
      completed = rave.Ussd.verify(zenithPayload["txRef"])
    except RaveExceptions.TransactionVerificationError:
      print(action)

success, data = rave.Ussd.verify(zenithPayload["txRef"])
print(success)
