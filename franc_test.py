from rave_python import Rave, RaveExceptions, Misc

rave = Rave("FLWPUBK_TEST-*********************-X", "FLWSECK_TEST-**************************-X", production=False, usingEnv = False)

payload = {
  "amount": "50",
  "email": "vokuduj@webmail24.top",
  "phonenumber": "243546576879",
  "country": "NG",
  "redirect_url": "https://flutterwaveprodv2.com/flwcinetpay/paymentServlet?reference=FLW844881566221068736",
  "IP":""
}

try:
  res = rave.Francophone.charge(payload)
  print (res)
  res = rave.Francophone.verify(res["txRef"])
  print(res)
  

except RaveExceptions.MobileChargeError as e:
  print(e.err)
  print(e.err["flwRef"])
  