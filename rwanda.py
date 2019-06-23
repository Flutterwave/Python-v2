from rave_python import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK_TEST-e10b3814bd004570a499605cfc95bd67-X", "FLWSECK_TEST-afa4f993af3695bdef2e9d22e746b7c1-X", usingEnv = False)

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
