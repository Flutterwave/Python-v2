from rave_python import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK_TEST-*********************-X", "FLWSECK_TEST-**************************-X", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "vokuduj@webmail24.top",
  "phonenumber": "243546576879",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
  "IP":""
}

try:
  res = rave.RWMobile.charge(payload)
  print (res)
  res = rave.RWMobile.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
