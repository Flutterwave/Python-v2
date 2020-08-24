from rave_python import Rave, RaveExceptions, Misc


rave = Rave("FLWPUBK-94ac45ac8778fc8c6942eeaec7fdeb5d-X", "FLWSECK-3c90d25b67063699bdd1688caa14b56c-X", production = True, usingEnv = False)

payload = {
  "PBFPubKey": "FLWPUBK-94ac45ac8778fc8c6942eeaec7fdeb5d-X",
  "currency": "UGX",
  "payment_type": "mobilemoneyuganda",
  "country": "NG",
  "amount": "50",
  "email": "user@example.com",
  "phonenumber": "054709929220",
  "network": "UGX",
  "firstname": "Cornelius",
  "lastname": "Ashley",
  "IP": "355426087298442",
  "txRef": "MC-02",
  "orderRef": "MC_03",
  "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
}

try:
	res = rave.UGMobile.charge(payload)
	print(res)

except RaveExceptions.IncompleteCardDetailsError as e:
    print(e)

except RaveExceptions.ServerError as e:
    print(e.err)


