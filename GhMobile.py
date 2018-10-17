from python_rave import Rave, RaveExceptions, Misc

rave = Rave("FLWPUBK-a5715a67d24e61ce3e7bf79ae22ef524-X", 
            "FLWSECK-6577e947f692e979e2d306ab4ce0a282-X", 
            usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "e.ikedieze@gmail.com",
  "phonenumber": "054709929220",
  "network": "MTN",
  "redirect_url": "https://whispering-spire-31708.herokuapp.com/ghmobile",
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