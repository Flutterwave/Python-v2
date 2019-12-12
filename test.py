import unittest
from rave_python import Rave, RaveExceptions, Misc
from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError, AccountChargeError,TransactionVerificationError, TransactionValidationError, ServerError, CardChargeError, InitiateTransferError, SubaccountCreationError, CardCreationError

# This class tests card and account payment options on Rave. It uses mock data

class TestRavePaymentOptions(unittest.TestCase):
    def setUp(self):
        self.account_details = {
            "payment_type": "account",
            "firstname": "yemen_test",
            "country": "NG",
            "lastname": "yemen_test",
            "accountnumber": "0690000031",
            "email": "nigeia_test@yopmail.com",
            "currency": "NGN",
            "accountbank": "044",
            "phonenumber": "+234 90 87417",
            "amount": "400.0",
            "txRef": "GAT-161",
            "IP":"190.233.222.1"
        }
        self.faulty_account_details = {
            "accountbank":"044",
            "currency": "NGN",
            "accountnumber":"0690000031",
            "amount":"invalid_amount",
            "country":"NG",
            "email":"varisiv@gmail.com",
            "phonenumber":"08031142735",
            "IP":"127.0.0.1"
        }
        self.card_details = {
            "cardno": "5399838383838381",
            "cvv": "470",
            "expirymonth": "10",
            "expiryyear": "22",
            "currency": "NGN",
            "amount": "100",
            "email": "user@gmail.com",
            "phonenumber": "0902620185",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
        }
        self.faulty_card_details = {
            "cardno": "5399838383838381",
            "cvv": "470",
            "expirymonth": "10",
            "currency": "NGN",
            "expiryyear": "22",
            "phonenumber": "0902620185",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
        }
        self.saved_card_details = {
            "token":"flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k",
            "country":"NG",
            "amount":1000,
            "currency": "NGN",
            "email":"user@gmail.com",
            "firstname":"temi",
            "lastname":"desola",
            "IP":"190.233.222.1",
            "txRef":"MC-7666-YU",
            "currency":"NGN",
        }
        self.faulty_saved_card_details = {
            "token":"flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k",
            "country":"NG",
            "amount":1000,
            "currency": "NGN",
            "firstname":"temi",
            "lastname":"Oyekole",
            "IP":"190.233.222.1",
            "txRef":"MC-7666-YU",
            "currency":"NGN",
        }

        self.transferDetails = {
            "account_bank": "044",
            "account_number": "0690000044",
            "amount": 500,
            "narration": "New transfer",
            "currency": "NGN",
            "beneficiary_name": "Mark Cuban",
            "meta": [
                {
                "AccountNumber": "09182972BH",
                "RoutingNumber": "0000000002993",
                "SwiftCode": "ABJG190",
                "BankName": "BANK OF AMERICA, N.A., SAN FRANCISCO, CA",
                "BeneficiaryName": "Mark Cuban",
                "BeneficiaryAddress": "San Francisco, 4 Newton",
                "BeneficiaryCountry": "US"
                }
            ]
        }
        self.faulty_transferDetails = {
            "account_bank": "044",
            "amount": 500,
            "narration": "New transfer",
            "currency": "NGN",
        }
     
        self.bulk_transferDetails = {
            "title":"May Staff Salary",
            "bulk_data":[
                {
                    "Bank":"044",
                    "Account Number": "0690000032",
                    "Amount":500,
                    "Currency":"NGN",
                    "Narration":"Bulk transfer 1",
                    "reference": "mk-82973029",
                    "beneficiary_name": "Mark Cuban",
                    "meta": [
                        {
                        "AccountNumber": "09182972BH",
                        "RoutingNumber": "0000000002993",
                        "SwiftCode": "ABJG190",
                        "BankName": "BANK OF AMERICA, N.A., SAN FRANCISCO, CA",
                        "BeneficiaryName": "Mark Cuban",
                        "BeneficiaryAddress": "San Francisco, 4 Newton",
                        "BeneficiaryCountry": "US"
                        }
                    ]
                },
                {
                    "Bank":"044",
                    "Account Number": "0690000034",
                    "Amount":500,
                    "Currency":"NGN",
                    "Narration":"Bulk transfer 2",
                    "reference": "mk-283874750",
                    "beneficiary_name": "Mark Cuban",
                    "meta": [
                        {
                        "AccountNumber": "09182972BH",
                        "RoutingNumber": "0000000002993",
                        "SwiftCode": "ABJG190",
                        "BankName": "BANK OF AMERICA, N.A., SAN FRANCISCO, CA",
                        "BeneficiaryName": "Mark Cuban",
                        "BeneficiaryAddress": "San Francisco, 4 Newton",
                        "BeneficiaryCountry": "US"
                        }
                    ]
                }
            ]
        }
        self.faulty_bulk_transferDetails = {
            "title":"May Staff Salary",
            "bulk_data":""
        }

        self.planDetails = {
            "amount": 1,
            "duration": 5,
            "name": "Ultimate Plan",
            "interval": "dai"
        }

        self.faulty_planDetails = {
            "duration": 5,
            "name": "Ultimate Plan",
            "interval": "dai"
        }

        self.subaccountDetails = {
            "account_bank": "044",
            "account_number": "0690000037",
            "currency": "NGN",
            "business_name": "Jake Stores",
            "business_email": "jdhhd@services.com",
            "business_contact": "Amy Parkers",
            "business_contact_mobile": "09083772",
            "business_mobile": "0188883882",
            "split_type": "flat",
            "split_value": 3000,
            "meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
        }

        self.faulty_subaccountDetails_1 = {
            "business_email": "jdhhd@services.com",
            "currency": "NGN",
            "business_contact": "Amy Parkers",
            "business_contact_mobile": "09083772",
            "business_mobile": "0188883882",
            "split_type": "flat",
            "split_value": 3000,
            "meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
        }

        self.faulty_subaccountDetails_2 = {
            "account_bank": "044",
            "account_number": "0690000032",
            "business_name": "Jake Stores",
            "currency": "NGN",
            "business_email": "jdhhd@services.com",
            "business_contact": "Amy Parkers",
            "business_contact_mobile": "09083772",
            "business_mobile": "0188883882",
            "split_type": "flat",
            "split_value": 3000,
            "meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
        }

        self.preauthDetails = {
            "token":"flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k",
            "country":"NG",
            "amount":1000,
            "email":"user@gmail.com",
            "firstname":"temi",
            "lastname":"Oyekole",
            "IP":"190.233.222.1",
            "txRef":"MC-7666-YU",
            "currency":"NGN",
        }

        self.faulty_preauthDetails = {
            "country":"NG",
            "amount":1000,
            "email":"user@gmail.com",
            "firstname":"temi",
            "lastname":"Oyekole",
            "IP":"190.233.222.1",
            "txRef":"MC-7666-YU",
            "currency":"NGN",
        }

        self.faulty_preauthDetails_2 = {
            "token":"flw-t1nf-5bf12d565cd961f73c51370b1340f1f-m03k",
            "country":"NG",
            "amount":1000,
            "email":"user@gmail.com",
            "firstname":"temi",
            "lastname":"Oyekole",
            "IP":"190.233.222.1",
            "txRef":"MC-7666-YU",
            "currency":"NGN",
        }

        self.ugDetails = {
            "amount": "50",
            "network": "UGX",
            "email": "user@example.com",
            "phonenumber": "08075376980",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
            "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        self.ghDetails = {
            "currency": "GHS",
            "payment_type": "mobilemoneygh",
            "country": "GH",
            "amount": "50",
            "email": "user@example.com",
            "phonenumber": "054709929220",
            "network": "MTN",
            "firstname": "temi",
            "lastname": "desola",
            "voucher": "128373",
            "IP": "355426087298442",
            "txRef": "MC-1520528216374",
            "orderRef": "MC_90929",
            "is_mobile_money_gh": 1,
            "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        self.virtual_card_details = {
            "currency": "NGN",
            "amount": "350",
            "billing_name": "Cornelius Ashley",
            "billing_address": "19, Olubunmi Olurotimi street",
            "billing_city": "Lagos",
            "billing_state": "Lagos",
            "billing_postal_code": "100001",
            "billing_country": "NG"
        }
        
        self.faulty_virtual_card_details_1 = {
            "amount": "350",
            "billing_name": "Cornelius Ashley",
            "billing_address": "19, Olubunmi Olurotimi street",
            "billing_city": "Lagos",
            "billing_state": "Lagos",
            "billing_postal_code": "100001",
            "billing_country": "NG"
        }

        self.faulty_virtual_card_details_2 = {
            "currency": "NGN",
            "amount": "350",
            "billing_name": "Cornelius Ashley",
            "billing_address": "19, Olubunmi Olurotimi street",
            "billing_state": "Lagos",
            "billing_postal_code": "100001",
            "billing_country": "NG"
        }
        self.bills_payment_details_1 = {
            "service": "fly_buy",
            "service_method": "post",
            "service_version": "v1",
            "service_channel": "rave",
            "service_payload": {
                "Country": "NG",
                "CustomerId": "+23490803840303",
                "Reference": "9300049404465",
                "Amount": 100,
                "RecurringType": 0,
                "IsAirtime": True,
                "BillerName": "AIRTIME"
            }
        }

        self.faulty_bills_payment_details_1 = {
            "service": "fly_buy",
            "service_method": "post",
            "service_channel": "rave",
            "service_payload": {
                "Country": "NG",
                "CustomerId": "+23490803840303",
                "Reference": "9300049404490",
                "Amount": 100,
                "RecurringType": 0,
                "IsAirtime": True,
                "BillerName": "AIRTIME"
            }
        }

        self.bills_payment_details_2 = {
            "service": "fly_buy_bulk",
            "service_method": "post",
            "service_version": "v1",
            "service_channel": "rave",
            "service_payload": {
                "BatchReference": "batch-rave-150928302799933928",
                "CallBackUrl": "https://rave-webhook.herokuapp.com/newregistration",
                "Requests": [
                    {
                        "Country": "NG",
                        "CustomerId": "+23490803840303",
                        "Amount": 100,
                        "RecurringType": 0,
                        "IsAirtime": True,
                        "BillerName": "AIRTIME",
                        "Reference": "9300049404450"
                    },
                    {
                        "Country": "GH",
                        "CustomerId": "+233276081163",
                        "Amount": 10,
                        "RecurringType": 0,
                        "IsAirtime": True,
                        "BillerName": "AIRTIME",
                        "Reference": "9300049405561"
                    },
                    {
                        "Country": "US",
                        "CustomerId": "+190830030",
                        "Amount": 20,
                        "RecurringType": 0,
                        "IsAirtime": True,
                        "BillerName": "AIRTIME",
                        "Reference": "9300049406681"
                    }
                ]
            }
        }

        self.francophone_mobile_charge_details={
            "currency": "XAF",
            "country":"NG",
            "payment_type":"mobilemoneyfranco",
            "amount": "250",
            "email": "user@example.com",
            "phonenumber": "054709929220",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
            "redirect_url": "https://www.google.com",
            "txRef": "01002",
            "orderRef": "12122019",
            "is_mobile_money_franco": 1,
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        self.faulty_francophone_mobile_charge_details={
            "currency": "XAF",
            "country":"NG",
            "payment_type":"mobilemoneyfranco",
            "amount": "250",
            "email": "user@example.com",
            "phonenumber": "054709929220",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
            "txRef": "01002",
            "orderRef": "12122019",
            "is_mobile_money_franco": 1,
        }

        #please replace the keys with your public and secret keys
        self.rave = Rave("FLWPUBK_TEST-0db01907c1b990c273c365a696c1613d-X", "FLWSECK_TEST-624d8f04393b01cac90d02f562b26389-X", production=False, usingEnv = False)

    # def test_account(self):
    #     # This test case checks that on initiating a payment, the user is requested to validate the payment
    #     res = self.rave.Account.charge(self.account_details)
    #     self.assertEqual(res["validationRequired"], True)
    #     with self.assertRaises(AccountChargeError):
    #         self.rave.Account.charge(self.faulty_account_details) 

    #     # This test case checks that a user validates a transaction appropriately
    #     self.assertEqual(self.rave.Account.validate(res["flwRef"], "12345")["error"], False)
    #     with self.assertRaises(TransactionValidationError):
    #         self.rave.Account.validate(res["flwRef"], "123") # a wrong otp to ensure TransactionValidationError is raised anytime a wrong otp is passed

    #     self.assertEqual(self.rave.Account.verify(res["txRef"])["transactionComplete"], True)
    #     with self.assertRaises(TransactionVerificationError):
    #         self.rave.Account.verify("MC-8883838388881") # a wrong txRef to ensure TransactionVerificationError is raised anytime a wrong transaction reference is passed
        
    # def test_card(self):

    #     res = self.rave.Card.charge(self.card_details)
    #     self.assertIsNotNone(res["suggestedAuth"])
    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.Card.charge(self.faulty_card_details)

    #     arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])
    #     if arg == "pin":
    #         Misc.updatePayload(res["suggestedAuth"], self.card_details, pin="3310")
    #     if arg == "address":
    #         Misc.updatePayload(res["suggestedAuth"], self.card_details, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})

    #     res = self.rave.Card.charge(self.card_details)
    #     # This test case checks that a user validates a transaction appropriately
    #     self.assertEqual(res["validationRequired"], True)
    #     self.assertEqual(self.rave.Card.validate(res["flwRef"], "12345")["error"], False)
    #     with self.assertRaises(TransactionValidationError):
    #         self.rave.Card.validate("FLW-MOCK-5a039c016e64da9b226c2562dcd76756", "12345") # a wrong otp to ensure TransactionValidationError is raised anytime a wrong otp is passed

    #     verify_res = self.rave.Card.verify(res["txRef"])
    #     self.assertEqual(verify_res["transactionComplete"], True)
    #     with self.assertRaises(TransactionVerificationError):
    #         self.rave.Card.verify("MC-8883838388881") # a wrong txRef to ensure TransactionVerificationError is raised anytime a wrong transaction reference is passed

    # def test_mobile_money_gh(self):
    #     res = self.rave.GhMobile.charge(self.ghDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["status"])
    #     self.assertEqual(res["error"], False)
    #     self.assertEqual(res["status"], "success")
    
    # def test_saved_card(self):
    #     res = self.rave.Card.charge(self.saved_card_details, chargeWithToken=True)
    #     self.assertIsNotNone(res["status"])
    #     self.assertEqual(res["status"], 'success')

    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.Card.charge(self.faulty_saved_card_details, chargeWithToken=True)
        
    #     self.assertEqual(self.rave.Card.verify(res["txRef"])["transactionComplete"], True)
    #     with self.assertRaises(TransactionVerificationError):
    #         self.rave.Card.verify("MC-8883838388881") # a wrong txRef to ensure TransactionVerificationError is raised anytime a wrong transaction reference is passed

    # def test_preauth(self):
    #     res = self.rave.Preauth.charge(self.preauthDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["status"])
    #     self.assertEqual(res["error"], False)
    #     self.assertEqual(res["status"], "success")

    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.Preauth.charge(self.faulty_preauthDetails) 

    #     with self.assertRaises(CardChargeError):
    #         self.rave.Preauth.charge(self.faulty_preauthDetails_2) 

    #     # capture
    #     res = self.rave.Preauth.capture(res["flwRef"])
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["status"])
    #     self.assertEqual(res["error"], False)
    #     self.assertEqual(res["status"], "success")



    # def test_transfer(self):
    #     #initiation - single transfer
    #     res = self.rave.Transfer.initiate(self.transferDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["data"]["is_approved"])
    #     self.assertEqual(res["data"]["is_approved"], 1)
    #     self.assertEqual(res["error"], False)

    #     # with self.assertRaises(InitiateTransferError):
    #     #     self.rave.Transfer.initiate(self.faulty_transferDetails)
        
    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.Transfer.initiate(self.faulty_transferDetails)
        
    #     #initiation - bulk transfer
    #     res = self.rave.Transfer.bulk(self.bulk_transferDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["status"])
    #     self.assertEqual(res["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     with self.assertRaises(InitiateTransferError):
    #         self.rave.Transfer.bulk(self.faulty_bulk_transferDetails)
        
    #     #fetch
    #     res = self.rave.Transfer.fetch("MC-1539086007702")
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #all transfers
    #     res = self.rave.Transfer.allTransfers()
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #get fee
    #     res = self.rave.Transfer.getFee('NGN')
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #get balance
    #     res = self.rave.Transfer.getBalance('NGN')
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)


    # def test_payment_plan(self):
    #     #create plan
    #     res = self.rave.PaymentPlan.createPlan(self.planDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["data"]["status"])
    #     self.assertIsNotNone(res["data"]["plan_token"])
    #     self.assertEqual(res["error"], False)

    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.PaymentPlan.createPlan(self.faulty_planDetails)

        
    #     #fetch
    #     res = self.rave.PaymentPlan.fetchPlan(898)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #all plans
    #     res = self.rave.PaymentPlan.allPlans()
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #cancel plan
    #     res = self.rave.PaymentPlan.cancelPlan(898)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    # def test_subaccount(self):
    #     #create plan
    #     res = self.rave.SubAccount.createSubaccount(self.subaccountDetails)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["data"]['subaccount_id'])

    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.SubAccount.createSubaccount(self.faulty_subaccountDetails_1)

    #     with self.assertRaises(SubaccountCreationError):
    #         self.rave.SubAccount.createSubaccount(self.faulty_subaccountDetails_2)

        
    #     #fetch
    #     res = self.rave.SubAccount.fetchSubaccount('RS_BF94DDF6AA2AB40BE874EA32DBD4DAA1')
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    #     #all plans
    #     res = self.rave.SubAccount.allSubaccounts()
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["returnedData"]["status"])
    #     self.assertEqual(res["returnedData"]["status"], "success")
    #     self.assertEqual(res["error"], False)

    # def test_ugmobile(self):
    #     #charge
    #     res = self.rave.UGMobile.charge(self.ugDetails)
    #     print(res)

    # def test_bills_payment(self):
    #     #single airtime purchase
    #     res = self.rave.Bills.create(self.bills_payment_details_1)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["data"]["Status"])
    #     self.assertEqual(res["error"], False)
    #     self.assertEqual(res["data"]["Status"], "success")
    #     with self.assertRaises(IncompletePaymentDetailsError):
    #         self.rave.Bills.create(self.faulty_bills_payment_details_1)

    #     #bulk airtime purchase
    #     res = self.rave.Bills.create(self.bills_payment_details_2)
    #     self.assertIsNotNone(res["error"])
    #     self.assertIsNotNone(res["data"]["Status"])
    #     self.assertEqual(res["error"], False)
    #     self.assertEqual(res["data"]["Status"], "success")

    # def test_virtual_card(self):
    #     res = self.rave.VirtualCard.create(self.virtual_card_details)
    #     print(res)

    def test_francophone_charge(self):
        res = self.rave.Francophone.charge(self.francophone_mobile_charge_details)
        self.assertIsNotNone(res["error"])
        self.assertEqual(res["error"], False)
        with self.assertRaises(IncompletePaymentDetailsError):
            self.rave.Francophone.charge(self.faulty_francophone_mobile_charge_details)

    
        

        
if __name__ == '__main__':
    unittest.main()