from python_rave import Rave, Misc, RaveExceptions
rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)
try:

    # res = rave.PaymentPlan.createPlan({
    #     "amount": 1,
    #     "duration": 5,
    #     "name": "Ultimate Play",
    #     "interval": "dai"
    # })
    # print(res)
    
#     res = rave.SubAccount.createSubaccount({
# 	"account_bank": "044",
# 	"account_number": "0690000031",
# 	"business_name": "Jake Stores",
# 	"business_email": "kwakj@services.com",
# 	"business_contact": "Amy Parkers",
# 	"business_contact_mobile": "09083772",
# 	"business_mobile": "0188883882",
# 	"meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
# })
    res = rave.SubAccount.fetchSubaccount('RS_0A6C260E1A70934DE6EF2F8CEE46BBB3')
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

# except RaveExceptions.InitiateTransferError as e:
#     print(e.err)

# except RaveExceptions.TransferFetchError as e:
#     print(e.err)

# except RaveExceptions.ServerError as e:
#     print(e.err)
