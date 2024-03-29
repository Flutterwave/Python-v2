import unittest
from rave_python import Rave, RaveExceptions, Misc
from rave_python.rave_exceptions import *
from dotenv import load_dotenv
import os

load_dotenv()

# This class tests card and account payment options on Rave. It uses mock data
class TestRavePaymentOptions(unittest.TestCase):
    def setUp(self):
        self.rave = Rave(
            os.getenv("PUBLIC_KEY"),
            os.getenv("RAVE_SECRET_KEY"),
            production=False,
            usingEnv=True)

    # def test_card_charge(self):
    #     # sample data
    #     card_details = {
    #         "cardno": "5531886652142950",
    #         "cvv": "564",
    #         "expirymonth": "09",
    #         "expiryyear": "22",
    #         "currency": "NGN",
    #         "amount": "100",
    #         "email": "user@example.com",
    #         "phonenumber": "08100000000",
    #         "firstname": "Test",
    #         "lastname": "User",
    #         "txRef": "mocked_test"
    #     }

    #     faulty_card_details = {
    #         "cardno": "5399838383838381",
    #         "cvv": "470",
    #         "expirymonth": "10",
    #         "currency": "NGN",
    #         "expiryyear": "22",
    #         "phonenumber": "08100000000",
    #         "firstname": "Test",
    #         "lastname": "User",
    #     }

    #     mocked_card_data_1 = {
    #         'validationRequired': True,
    #         'suggestedAuth': 'PIN',
    #         'flwRef': None, 
    #         'authUrl': None, 
    #         'error': False, 
    #         'txRef': 'mocked_test'
    #     }

    #     # 1. Test case 1: successful charge initiation - should return suggested auth
    #     response = self.rave.Card.charge(card_details)
    #     self.assertEqual(response['status'], 'success')

    #     # 2. Test case 2: failed charge initiation - should return IncompletePaymentDetailsError
    #     # 3. Test case 3: successful card charge - should return 200, response.data to include []
    #     # 4. Test case 4: successful charge validation - should return 200, response.data to include []
    #     # 5. Test case 5: successful transaction verification -  should return 200, response.data to include []

    # def test_eNaira(self):
    #     enaira_request = {
    #         "amount": 30,
    #         "PBFPubKey": os.getenv("PUBLIC_KEY"),
    #         "currency": "NGN",
    #         "email": "user@example.com",
    #         "meta": [{"metaname": "test", "metavalue": "12383"}],
    #         "ip": "123.0.1.3",
    #         "firstname": "Flutterwave",
    #         "lastname": "Tester",
    #         "is_token": False
    #     }

    #     #Test case 1: successful charge attempt
    #     response = self.rave.Enaira.charge(enaira_request)
    #     self.assertEqual(response['error'], False)
        


if __name__ == '__main__':
    unittest.main()
