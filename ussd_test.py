from python_rave import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)


zenithPayload = {
  "accountbank": "057",
  "accountnumber": "0691008392",#collect the customers account number for Zenith
  "currency": "NGN",
  "country": "NG",
  "amount": "10",
  "email": "kwakujosh@gmail.com",
  "phonenumber": "08075376980", 
  "IP": "355426087298442",
}
test = rave.Ussd.charge(zenithPayload)
print(test)

# furtherActionNeeded, action = rave.Ussd.charge(zenithPayload)
# if furtherActionNeeded:
#   completed = False
#   while not completed:
#     try:
#       completed = rave.Ussd.verify(zenithPayload["txRef"])
#     except RaveExceptions.TransactionVerificationError:
#       print(action)
    
# success, data = rave.Ussd.verify(zenithPayload["txRef"])
# print(success)