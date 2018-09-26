'''
- the service is down for ussd
'''
from python_rave import Rave, RaveExceptions, Misc

rave = Rave(
  "FLWPUBK-56e4a2c6c9a6b58364bfd07fc1993e2c-X", 
  "FLWSECK-ea81e705d82161de5b7757c897d96ba4-X", 
  usingEnv = False
  )

zenithPayload = {
  "accountbank": "057",
  "accountnumber": "0691008392",#collect the customers account number for Zenith
  "currency": "NGN",
  "country": "NG",
  "amount": "10",
  "email": "desola.ade1@gmail.com",
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