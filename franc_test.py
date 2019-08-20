from rave_python import Rave, RaveExceptions, Misc

rave = Rave("FLWPUBK-8bf84c62ed00abccc4ce37e12638ad63-X", "FLWSECK-370389724fd2d6573c1a4295ad61814f-X", production=True, usingEnv = False)

payload = {
  "amount": "50",
  "email": "vokuduj@webmail24.top",
  "phonenumber": "243546576879",
  "redirect_url": "https://flutterwaveprodv2.com/flwcinetpay/paymentServlet?reference=FLW844881566221068736",
  "IP":""
}

try:
  res = rave.Francophone.charge(payload)
  print (res)
  res = rave.Francophone.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
