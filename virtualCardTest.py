from rave_python import Rave, RaveExceptions, Misc


rave = Rave("FLWPUBK_TEST-********************************-X", "FLWSECK_TEST-********************************-X", production = False, usingEnv = False)

# payload = {
#     "currency": "NGN",
# 	"amount": "100",
# 	"billing_name": "Blessed Yahaya",
# 	"billing_address": "8, Providence Street",
# 	"billing_city": "Lekki",
# 	"billing_state": "Lagos",
# 	"billing_postal_code": "100001",
# 	"billing_country": "NG",
# }

try:
	res = rave.VirtualCard.allCards()
	print(res)

except RaveExceptions.IncompleteCardDetailsError as e:
    print(e)

except RaveExceptions.ServerError as e:
    print(e.err)
