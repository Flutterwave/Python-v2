from python_rave import Rave, RaveExceptions, Misc
# rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "kwakujosh@gmail.com",
  "phonenumber": "233244300310",
  "network": "MTN",
  "redirect_url": "https://sleepy-escarpment-32720.herokuapp.com/mpesa",
  "IP":""
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