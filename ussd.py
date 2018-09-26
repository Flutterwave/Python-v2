'''
- the service is down for ussd
'''
from python_rave import Rave, RaveExceptions, Misc

rave = Rave(
  "YOUR_PUBLIC_KEY", 
  "YOUR_SECRET_KEY", 
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