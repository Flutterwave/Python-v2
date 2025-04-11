# Standard library imports
import unittest, logging
from mock import Mock, patch
import os

# Third party imports
from dotenv import load_dotenv
from nose.tools import *

# Local imports
from rave_python import Rave, RaveExceptions, Misc
from rave_python.rave_exceptions import *

load_dotenv()


# This class tests card and account payment options on Rave. It uses mock data
class TestRavePaymentOptions(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        publicKey = os.getenv("PUBLIC_KEY")
        secretKey = os.getenv("SECRET_KEY")

        self.rave = Rave(
            publicKey,
            secretKey,
            production=False,
            usingEnv=True
        )

        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

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

    def test_apple_pay_successful_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock payload
            sample_payload = {
                "amount": 10,
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "currency": "USD",
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = apple_pay_response
        

            response = self.rave.ApplePay.charge(sample_payload)
            
            self.assertEqual(response['flwRef'], apple_pay_response['data']['flwRef'])
            self.assertIsNotNone(response['authurl'])

            # self.logger.debug("Mocked Response: %s", response)
        
    @raises(IncompletePaymentDetailsError)
    def test_apple_pay_failed_incomplete_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock incomplete payload (missing amount)
            sample_payload = {
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "currency": "USD",
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = apple_pay_response

            response = self.rave.ApplePay.charge(sample_payload)

    
    def test_fawry_pay_successful_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock payload
            sample_payload = {
                "amount": 10,
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester",
                "phonenumber": "233010521034"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = fawry_pay_response
        

            response = self.rave.FawryPay.charge(sample_payload)
            
            self.assertEqual(response['flwRef'], fawry_pay_response['data']['flwRef'])

            # self.logger.debug("Mocked Response: %s", response)
        
    @raises(IncompletePaymentDetailsError)
    def test_fawry_pay_failed_incomplete_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock incomplete payload (missing amount)
            sample_payload = {
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = fawry_pay_response

            response = self.rave.FawryPay.charge(sample_payload)

    
    def test_google_pay_successful_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock payload
            sample_payload = {
                "amount": 10,
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "currency": "USD",
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = google_pay_response
        

            response = self.rave.GooglePay.charge(sample_payload)
            
            self.assertEqual(response['flwRef'], google_pay_response['data']['flwRef'])
            self.assertIsNotNone(response['authurl'])

            # self.logger.debug("Mocked Response: %s", response)
        
    @raises(IncompletePaymentDetailsError)
    def test_google_pay_failed_incomplete_charge(self):
        with patch('rave_python.rave_payment.requests.post') as mock_post:
            
            # mock incomplete payload (missing amount)
            sample_payload = {
                "PBFPubKey": os.getenv("PUBLIC_KEY"),
                "currency": "USD",
                "email": "user@example.com",
                "meta": [{"metaname": "test", "metavalue": "12383"}],
                "ip": "123.0.1.3",
                "firstname": "Flutterwave",
                "lastname": "Tester"
            }

            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = google_pay_response

            response = self.rave.GooglePay.charge(sample_payload)


if __name__ == '__main__':
    unittest.main()
