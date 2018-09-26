from python_rave import Rave, RaveExceptions, Misc

YOUR_PUBLIC_KEY = "#"
YOUR_SECRET_KEY = "#"

rave = Rave(YOUR_PUBLIC_KEY, YOUR_SECRET_KEY, usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "ifunanya@gmail.com",
  "phonenumber": "054709929220",
  "network": "MTN",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
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