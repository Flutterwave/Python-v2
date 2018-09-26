import unittest
from python_rave import Rave, RaveExceptions, Misc
from python_rave.rave_exceptions import RaveError, IncompletePaymentDetailsError, AccountChargeError,TransactionVerificationError, TransactionValidationError, ServerError, CardChargeError
from test_data import TestData
data = TestData()

class TestRavePaymentOptions(unittest.TestCase):
    def setUp(self):
        self.account_details = {
            "accountbank":"044",
            "accountnumber":"0690000031",
            "amount":"500",
            "country":"NG",
            "email":"varisiv@gmail.com",
            "phonenumber":"08031142735",
            "IP":"127.0.0.1"
        }
        self.faulty_account_details = {
            "accountbank":"044",
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
            "expiryyear": "22",
            "phonenumber": "0902620185",
            "firstname": "temi",
            "lastname": "desola",
            "IP": "355426087298442",
        }

        self.rave = Rave("FLWPUBK-ba0a57153f497c03bf34a9e296aa9439-X", "FLWSECK-327b3874ca8e75640a1198a1b75c0b0b-X", usingEnv = False)

    def test_account(self):
        # This test case checks that on initiating a payment, the user is requested to validate the payment
        res = self.rave.Account.charge(self.account_details)
        self.assertEqual(res["validationRequired"], True)
        with self.assertRaises(AccountChargeError):
            self.rave.Account.charge(self.faulty_account_details) 

        # This test case checks that a user validates a transaction appropriately
        self.assertEqual(self.rave.Account.validate(res["flwRef"], "12345")["error"], False)
        with self.assertRaises(TransactionValidationError):
            self.rave.Account.validate(res["flwRef"], "123") # a wrong otp to ensure TransactionValidationError is raised anytime a wrong otp is passed

        self.assertEqual(self.rave.Account.verify(res["txRef"])["transactionComplete"], True)
        with self.assertRaises(TransactionVerificationError):
            self.rave.Account.verify("MC-8883838388881") # a wrong txRef to ensure TransactionVerificationError is raised anytime a wrong transaction reference is passed
        
    def test_card(self):
        
        res = self.rave.Card.charge(self.card_details)
        self.assertIsNotNone(res["suggestedAuth"])
        with self.assertRaises(IncompletePaymentDetailsError):
            self.rave.Card.charge(self.faulty_card_details)

        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])
        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], self.card_details, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], self.card_details, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})

        res = self.rave.Card.charge(self.card_details)
        # This test case checks that a user validates a transaction appropriately
        self.assertEqual(res["validationRequired"], True)
        self.assertEqual(self.rave.Card.validate(res["flwRef"], "12345")["error"], False)
        with self.assertRaises(TransactionValidationError):
            self.rave.Card.validate("FLW-MOCK-5a039c016e64da9b226c2562dcd76756", "12345") # a wrong otp to ensure TransactionValidationError is raised anytime a wrong otp is passed

        
        self.assertEqual(self.rave.Card.verify(res["txRef"])["transactionComplete"], True)
        with self.assertRaises(TransactionVerificationError):
            self.rave.Card.verify("MC-8883838388881") # a wrong txRef to ensure TransactionVerificationError is raised anytime a wrong transaction reference is passed

        
if __name__ == '__main__':
    unittest.main()