from rave_python import Rave, RaveExceptions, Misc
PublicKey = "FLWPUBK-45587fdb1c84335354ab0fa388b803d5-X"
SecretKey = "FLWSECK-2c9a2a781e56760b5d9c29c67ec22347-X"

rave = Rave(PublicKey, SecretKey, production=True, usingEnv=False)

payload = {
    "amount": 30,
    "PBFPubKey": PublicKey,
    "currency": "NGN",
    "email": "user@example.com",
    "meta": [{"metaname": "test", "metavalue": "12383"}],
    "ip": "123.0.1.3",
    "firstname": "Flutterwave",
    "lastname": "Tester",
    "is_token": False
}

payload_2 = {
    "currency": "TZS",
    "country": "TZ",
    "amount": 1000,
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "phonenumber": "255123456789",
}

payload_3 = {
  "cardno": "4187451811620618",
  "cvv": "306",
  "expirymonth": "05",
  "expiryyear": "25",
  "amount": "100",
  "email": "korneliosyaovi@gmail.com",
  "phonenumber": "08109328188",
  "firstname": "Cornelius",
  "lastname": "Ashley",
  "IP": "355426087298442",
  "pin": "7991",
  "currency": "NGN"
}

payload_4 = {
  "token": "flw-t1nf-45a7a6bfbe2fb30a70c1d974d84e31c5-k3n",
  "amount": "100",
  "email": "korneliosyaovi@gmail.com",
  "phonenumber": "08109328188",
  "firstname": "Cornelius",
  "lastname": "Ashley",
  "IP": "355426087298442",
  "currency": "NGN",
  "country": "NG"
}

payload_5 = {
   "amount": 30,
    "PBFPubKey": PublicKey,
    "currency": "NGN",
    "email": "user@example.com",
    "meta": [{"metaname": "test", "metavalue": "12383"}],
    "ip": "123.0.1.3",
    "firstname": "Flutterwave",
    "lastname": "Tester",
}

payload_6 = {
    "amount": 2,
    "PBFPubKey": PublicKey,
    "currency": "GBP",
    "email": "user@example.com",
    "meta": [{"metaname": "test", "metavalue": "12383"}],
    "ip": "123.0.1.3",
    "firstname": "Flutterwave",
    "lastname": "Tester"
}


# print(rave.Enaira.charge(payload))
print(rave.Enaira.charge(payload))
