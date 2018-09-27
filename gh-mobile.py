from python_rave import Rave, RaveExceptions, Misc
rave = Rave(
    "FLWPUBK-92e93a5c487ad64939327052e113c813-X",
    "FLWSECK-61037cfe3cfc53b03e339ee201fa98f5-X",
    usingEnv=False
)

# mobile payload
payload = {
    "amount": "50",
    "email": "dodez@xgmailoo.com",
    "phonenumber": "054709929220",
    "network": "MTN",
    "redirect_url": "https://loggly-webhook.herokuapp.com/ghmobile",
    "IP": ""
}

try:
  res = rave.GhMobile.charge(payload)
  res = rave.GhMobile.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
