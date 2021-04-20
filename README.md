<p align="center">
    <img title="Flutterwave" height="200" src="https://flutterwave.com/images/logo-colored.svg" width="50%"/>
</p>

# Rave Python Library.
![Upload Python Package](https://github.com/Flutterwave/rave-python/workflows/Upload%20Python%20Package/badge.svg)
![PyPI](https://img.shields.io/pypi/v/rave_python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/rave_python)
![PyPI - License](https://img.shields.io/pypi/l/rave_python)


## Introduction
This is a Python wrapper around the [API](https://flutterwavedevelopers.readme.io/v2.0/reference) for [Rave by Flutterwave](https://rave.flutterwave.com).

#### Payment types implemented:
* Card Payments
* Bank Account Payments
* Ghana Mobile Money Payments
* Mpesa Payments
* Rwanda Mobile Money Payments
* Uganda Mobile Money Payments
* Zambia Mobile Money Payments
* Mobile Money Payments for Francophone countries
* Subaccounts
* Transfer
* Subscription (Recurring Payments)
* Bills payment
* Payment Plan
* USSD Payments (Still in Beta Mode)

#### Other features include:
* Preauthorization charges
* Refunds
* Transaction Verification
* Transfer Recipients
* Virtual Cards
* Virtual Accounts

## Installation
To install, run

```sh
pip install rave_python
```

Note: This is currently under active development
## Import Package
The base class for this package is 'Rave'. To use this class, add:

```py
from rave_python import Rave
```

## Initialization

#### To instantiate in sandbox:
To use Rave, instantiate the Rave class with your public key. We recommend that you store your secret key in an environment variable named, ```RAVE_SECRET_KEY```. Instantiating your rave object is therefore as simple as:

```py
rave = Rave("YOUR_PUBLIC_KEY")
```

####  To instantiate without environment variables (Sandbox):
If you choose not to store your secret key in an environment variable, we do provide a ```usingEnv``` flag which can be set to ```False```, but please be warned, do not use this package without environment variables in production

```py
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv = False)
```


#### To instantiate in production:
To initialize in production, simply set the ```production``` flag to ```True```. It is highly discouraged but if you choose to not use environment variables, you can do so in the same way mentioned above.

```py
rave = Rave("YOUR_PUBLIC_KEY", production=True)
```

# Rave Objects
This is the documentation for all of the components of rave_python

## ```rave.Card```
This is used to facilitate card transactions.

**Functions included:**

* ```.charge```

* ```.validate```

* ```.verify```

* ```.refund```

* ```.getTypeOfArgsRequired```

* ```.updatePayload```

<br>

### ```.charge(payload)```
This is called to start a card transaction. The payload should be a dictionary containing card information. It should have the parameters:

* ```cardno```,

* ```cvv```, 

* ```currency```, 

* ```country```, 

* ```expirymonth```, 

* ```expiryyear```, 

* ```amount```, 

* ```email```, 

* ```phonenumber```,

* ```firstname```, 

* ```lastname```, 

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.Card.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
 {'validationRequired': True, 'suggestedAuth': u'PIN', 'flwRef': None, 'authUrl': None, 'error': False, 'txRef': 'MC-1538095398058'}
 ```

This call raises a ```CardChargeError``` if there was a problem processing your transaction. The ```CardChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530897824739', 'flwRef': None, 'errMsg': 'Sorry, that card number is invalid, please check and try again'}
```


<br>

### ```rave.Misc.updatePayload(authMethod, payload, arg)```

Depending on the suggestedAuth from the charge call, you may need to update the payload with a pin or address. To know which type of authentication you would require, simply call ```rave.Card.getTypeOfArgsRequired(suggestedAuth)```. This returns either ```pin``` or ```address```. 

In the case of ```pin```, you are required to call ```rave.Card.updatePayload(suggestedAuth, payload, pin="THE_CUSTOMER_PIN")```. 

In the case of ```address```, you are required to call ```rave.Card.updatePayload(suggestedAuth, payload, address={ THE_ADDRESS_DICTIONARY })```

A typical address dictionary includes the following parameters:

```billingzip```, 

```billingcity```,

```billingaddress```, 
 
```billingstate```,
 
```billingcountry```

**Note:**
```suggestedAuth``` is the suggestedAuth returned from the initial charge call and ```payload``` is the original payload

<br>

### ```.validate(txRef)```

After a successful charge, most times you will be asked to verify with OTP. To check if this is required, check the ```validationRequired``` key in the ```res``` of the charge call.

To validate, you need to pass the ```flwRef``` from the ```res``` of the charge call as well as the OTP.

A sample validate call is: 

```py
res2 = rave.Card.validate(res["flwRef"], "12345")
```

#### Returns

This call returns a dictionary containing the ```txRef```, ```flwRef``` among others if successful. 

This call raises a ```TransactionValidationError``` if the OTP is not correct or there was a problem processing your request. 

To handle this, write:

```py
try:
    # Your charge call
except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': None, 'flwRef': 'FLW-MOCK-a7911408bd7f55f89f0211819d6fd370', 'errMsg': 'otp is required'}
```

<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Card.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

Sample
```py
{'flwRef': None, 'cardToken': u'flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k', 'chargedAmount': 100, 'amount': 100, 'transactionComplete': True, 'error': False, 'txRef': u'MC-1538095718251'}
```

> Please note that after charging a card successfully on rave, if you wish to save the card for further charges, in your verify payment response you will find an object: `"cardtoken": "flw-t0-f6f915f53a094671d98560272572993e-m03k"`.  This is the token you will use for card tokenization. Details are provided below.

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

<br>

### ```.charge(payload_for_saved_card, chargeWithToken=True)```
This is called to start a card transaction with a card that has been saved. The payload should be a dictionary containing card information. It should have the parameters:

* ```token```,

* ```country```, 

* ```amount```, 

* ```email```, 

* ```firstname```, 

* ```lastname```, 

* ```IP```,

* ```txRef```, 

* ```currency```

#### NB: email must be the same as before the card was saved
Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).

A sample call is:

```py
res = rave.Card.charge(payload_for_saved_card, chargeWithToken=True)
```

#### Returns

This call returns a dictionary. A sample response is:

 ```py
 {'status': u'success', 'validationRequired': False, 'suggestedAuth': None, 'flwRef': u'FLW-M03K-cdb24d740fb18c242dd277fb1f74d399', 'authUrl': None, 'error': False, 'txRef': 'MC-7666-YU'}
 ```

 This call raises a ```CardChargeError``` if a wrong token or email is passed or if there was a problem processing your transaction. The ```CardChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

This call also raises an ```IncompletePaymentDetailsError``` if any of the required parameters are missing. The ```IncompletePaymentDetailsError``` contains information about which parameter was not included in the payload. You can handle this such as:

```py
try:
    #Your charge call
except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e.err["errMsg"])
```

Once this is done, call ```rave.Card.verify``` passing in the ```txRef``` returned in the response to verify the payment. Sample response:

```py
{'flwRef': None, 'cardToken': u'flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k', 'chargedAmount': 1000, 'amount': 1000, 'transactionComplete': True, 'error': False, 'txRef': 'MC-7666-YU'}
```

```rave.Card.verify``` raises a ```TransactionVerificationError``` if an invalid ```txRef``` is supplied. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```
#### NB: when charging saved cards, you do not need to call rave.card.Validate()


### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Card.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36071, 'AccountId': 49278, 'TransactionId': 1664979, 'FlwRef': 'FLW-MOCK-62986ef948d6dd127102cdb58813d216', 'walletId': 50309, 'AmountRefunded': '5000', 'status': 'completed', 'destination': 'payment_source', 'meta': '{"source":"ledgerbalance","uniquereference":"62472228710"}', 'updatedAt': '2021-01-23T01:27:11.969Z', 'createdAt': '2021-01-23T01:27:08.672Z'})
```


### Complete card charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv = False)

# Payload with pin
payload = {
  "cardno": "5438898014560229",
  "cvv": "890",
  "expirymonth": "09",
  "expiryyear": "19",
  "amount": "10",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
  "IP": "355426087298442",
}

try:
    res = rave.Card.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
        res = rave.Card.charge(payload)

    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "")

    res = rave.Card.verify(res["txRef"])
    print(res["transactionComplete"])

except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
```

<br><br>
## ```rave.Account```
This is used to facilitate account transactions.

**Functions included:**

* ```.charge```

* ```.validate```

* ```.verify```

<br>

### ```.charge(payload)```
This is called to start an account transaction. The payload should be a dictionary containing card information. It should have the parameters:

* ```accountbank```, 

* ```accountnumber```, 

* ```amount```, 

* ```email```, 

* ```phonenumber```, 

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.Account.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
 {'error': False, 'validationRequired': True, 'txRef': 'MC-1530899106006', 'flwRef': 'ACHG-1530899109682', 'authUrl': None}
```

 This call raises an ```AccountChargeError``` if there was a problem processing your transaction. The ```AccountChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.AccountChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530897824739', 'flwRef': None, 'errMsg': 'Sorry, that account number is invalid, please check and try again'}
```

<br>

### ```.validate(txRef)```

After a successful charge, most times you will be asked to verify with OTP. To check if this is required, check the ```validationRequired``` key in the ```res``` of the charge call.

In the case that an ```authUrl``` is returned from your charge call, you may skip the validation step and simply pass your authUrl to the end-user. 

```py
authUrl = res['authUrl']
```

To validate, you need to pass the ```flwRef``` from the ```res``` of the charge call as well as the OTP.

A sample validate call is: 

```py
res2 = rave.Account.validate(res["flwRef"], "12345")
```


#### Returns

This call returns a dictionary containing the ```txRef```, ```flwRef``` among others if successful.

This call raises a ```TransactionValidationError``` if the OTP is not correct or there was a problem processing your request. 

To handle this, write:

```py
try:
    # Your charge call
except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530899869968', 'flwRef': 'ACHG-1530899873118', 'errMsg': 'Pending OTP validation'}
```



<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Account.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

Sample

```py
{'status': u'success', 'vbvcode': u'N/A', 'chargedamount': 500, 'vbvmessage': u'N/A', 'error': False, 'flwRef': u'ACHG-1538093023787', 'currency': u'NGN', 'amount': 500, 'transactionComplete': True, 'acctmessage': u'Approved Or Completed Successfully', 'chargecode': u'00', 'txRef': u'MC-1538093008498'}
```

If your call could not be completed successfully or if a wrong ```txRef``` is passed, a ```TransactionVerificationError``` is raised. You can handle that as such
```py
try: 
    #Your charge call
except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Account.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36070, 'AccountId': 49278, 'TransactionId': 1664654, 'FlwRef': '9792859961', 'walletId': 71139, 'AmountRefunded': '1500', 'status': 'pending-momo', 'destination': 'mobilemoney', 'meta': '{"source":"ledgerbalance","disburse_ref":"CC-REFD-31101658361-9792859961","disburse_status":"pending"}', 'updatedAt': '2021-01-23T01:17:43.665Z', 'createdAt': '2021-01-23T01:17:38.327Z'})
```


<br>

### Complete account flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)
# account payload
payload = {
  "accountbank": "044",  # get the bank code from the bank list endpoint.
  "accountnumber": "0690000031",
  "currency": "NGN",
  "country": "NG",
  "amount": "100",
  "email": "test@test.com",
  "phonenumber": "0902620185",
  "IP": "355426087298442",
}

try:
    res = rave.Account.charge(payload)
    if res["authUrl"]:
        print(res["authUrl"])

    elif res["validationRequired"]:
        rave.Account.validate(res["flwRef"], "12345")

    res = rave.Account.verify(res["txRef"])
    print(res)

except RaveExceptions.AccountChargeError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
```
<br><br>

## ```rave.GhMobile```
This is used to facilitate Ghanaian mobile money transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start a Ghana mobile money transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```amount```,

* ```email```, 

* ```phonenumber```,

* ```network```,

* ```IP```,

* ```redirect_url```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.GhMobile.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "Momo initiated",
    "data": {
        "code": "02",
        "status": "pending",
        "ts": 1591798138846,
        "link": "https://ravemodal-dev.herokuapp.com/captcha/verify/123:49fa60c0db04f0017d717a0a662194cd"
    }
}
```


In order to complete the charge, kindly redirect users to the link returned as `data.link` from the charge response.

 This call raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530911537060', 'flwRef': None, 'errMsg': None}
```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.GhMobile.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.GhMobile.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36070, 'AccountId': 49278, 'TransactionId': 1664654, 'FlwRef': '9792859961', 'walletId': 71139, 'AmountRefunded': '1500', 'status': 'pending-momo', 'destination': 'mobilemoney', 'meta': '{"source":"ledgerbalance","disburse_ref":"CC-REFD-31101658361-9792859961","disburse_status":"pending"}', 'updatedAt': '2021-01-23T01:17:43.665Z', 'createdAt': '2021-01-23T01:17:38.327Z'})
```

<br>

### Complete GhMobile charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "",
  "phonenumber": "054709929220",
  "network": "MTN",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
  "IP":""
}

try:
  res = rave.GhMobile.charge(payload)
  res = rave.GhMobile.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
```

<br><br>

## ```rave.Mpesa```
This is used to facilitate Mpesa transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start an Mpesa transaction. The payload should be a dictionary containing payment information. It should have the parameters:

* ```amount```, 

* ```email```, 

* ```phonenumber```, 

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.Mpesa.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'validationRequired': True, 'txRef': 'MC-1530910216380', 'flwRef': 'N/A'}
```

 This call raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530910109929', 'flwRef': None, 'errMsg': 'email is required'}
```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Mpesa.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.


### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Mpesa.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36070, 'AccountId': 49278, 'TransactionId': 1664654, 'FlwRef': '9792859961', 'walletId': 71139, 'AmountRefunded': '1500', 'status': 'pending-momo', 'destination': 'mobilemoney', 'meta': '{"source":"ledgerbalance","disburse_ref":"CC-REFD-31101658361-9792859961","disburse_status":"pending"}', 'updatedAt': '2021-01-23T01:17:43.665Z', 'createdAt': '2021-01-23T01:17:38.327Z'})
```

<br>

### Complete Mpesa charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# mobile payload
payload = {
    "amount": "100",
    "phonenumber": "0926420185",
    "email": "user@exampe.com",
    "IP": "40.14.290",
    "narration": "funds payment",
}

try:
    res = rave.Mpesa.charge(payload)
    res = rave.Mpesa.verify(res["txRef"])
    print(res)

except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
```

<br><br>

## ```rave.UGMobile```
This is used to facilitate Uganda mobile money transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start a Ugandan mobile money transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```amount```,

* ```email```, 

* ```phonenumber```,

* ```IP```,

* ```redirect_url```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.UGMobile.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "Momo initiated",
    "data": {
        "code": "02",
        "status": "pending",
        "ts": 1591798138846,
        "link": "https://ravemodal-dev.herokuapp.com/captcha/verify/123:49fa60c0db04f0017d717a0a662194cd"
    }
}
```


In order to complete the charge, kindly redirect users to the link returned as `data.link` from the charge response.

 This call raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530911537060', 'flwRef': None, 'errMsg': None}
```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.UGMobile.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.


### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.UGMobile.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36070, 'AccountId': 49278, 'TransactionId': 1664654, 'FlwRef': '9792859961', 'walletId': 71139, 'AmountRefunded': '1500', 'status': 'pending-momo', 'destination': 'mobilemoney', 'meta': '{"source":"ledgerbalance","disburse_ref":"CC-REFD-31101658361-9792859961","disburse_status":"pending"}', 'updatedAt': '2021-01-23T01:17:43.665Z', 'createdAt': '2021-01-23T01:17:38.327Z'})
```

<br>

### Complete UGMobile charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "",
  "phonenumber": "xxxxxxxx",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
  "IP":""
}

try:
  res = rave.UGMobile.charge(payload)
  res = rave.UGMobile.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
```

<br><br>

## ```rave.ZBMobile```
This is used to facilitate Zambian mobile money transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start a Zambian mobile money transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```amount```,

* ```email```, 

* ```phonenumber```,

* ```IP```,

* ```redirect_url```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.ZBMobile.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "Momo initiated",
    "data": {
        "code": "02",
        "status": "pending",
        "ts": 1591798138846,
        "link": "https://ravemodal-dev.herokuapp.com/captcha/verify/123:49fa60c0db04f0017d717a0a662194cd"
    }
}
```

In order to complete the charge, kindly redirect users to the link returned as `data.link` from the charge response.

 This call raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530911537060', 'flwRef': None, 'errMsg': None}
```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.ZBMobile.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.


### ```.refund(flwRef, amount)```

You can call this to refund a full or partial amount of a transaction that was completed successfully. You have to pass the flw reference generated at the point of verifing the transaction. This is the ```flwRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.ZBMobile.refund(data["flwRef"], amount)
```

#### Returns

This call returns a dict with ```status```, ```AmountRefunded```, ```disburse_ref``` and ```disburse_status``` which indicates whether the transaction was completed successfully. 

Sample
```py
(True, {'settlement_id': 'NEW', 'id': 36070, 'AccountId': 49278, 'TransactionId': 1664654, 'FlwRef': '9792859961', 'walletId': 71139, 'AmountRefunded': '1500', 'status': 'pending-momo', 'destination': 'mobilemoney', 'meta': '{"source":"ledgerbalance","disburse_ref":"CC-REFD-31101658361-9792859961","disburse_status":"pending"}', 'updatedAt': '2021-01-23T01:17:43.665Z', 'createdAt': '2021-01-23T01:17:38.327Z'})
```


<br>

### Complete ZBMobile charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "",
  "phonenumber": "xxxxxxxx",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
  "IP":""
}

try:
  res = rave.ZBMobile.charge(payload)
  res = rave.ZBMobile.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
```

<br><br>

## ```rave.Francophone```
This is used to facilitate mobile money transactions in Ivory Coast, Senegal and Mali.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start a francophone mobile money transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```amount```,

* ```email```, 

* ```phonenumber```,

* ```IP```,

* ```redirect_url```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the [Misc library](https://github.com/Flutterwave/rave-python/blob/master/rave_python/rave_misc.py).


A sample call is:

```py
res = rave.Francophone.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'validationRequired': True, 'txRef': 'MC-1566482674756', 'flwRef': None, 'suggestedAuth': None, 'redirectUrl': 'https://flutterwaveprodv2.com/flwcinetpay/paymentServlet?reference=FLW186321566482674310'}
```
 
 The call returns redirect Url ```'redirectUrl':'https://redirecturl.com'``` for the authentication of the transaction. It raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```py
{'error': True, 'txRef': 'MC-1530911537060', 'flwRef': None, 'errMsg': None}
```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

```py
res = rave.Francophone.verify(data["txRef"])
```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

<br>

### Complete Francophone mobile money charge flow

```py
from rave_python import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# mobile payload
payload = {
  "amount": "50",
  "email": "",
  "phonenumber": "054709929220",
  "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
  "IP":""
}

try:
  res = rave.Francophone.charge(payload)
  print(res)
  res = rave.Francophone.verify(res["txRef"])
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])
```

<br><br>

## ```rave.Preauth```
This is used to facilitate preauthorized card transactions. This inherits the Card class so any task you can do on Card, you can do with preauth.

**Functions included:**

* ```.charge```

* ```.capture```

* ```.validate```

* ```.verify```

* ```.refund```

* ```.void```


<br>

**
In order to ```preauthorize``` a card, you must have:
    1. charged the card initially using ```rave.Card.charge(payload)```
    2. saved the ```token``` returned to you for that card. A ```token``` looks like this ```flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k```
**

### ```.charge(cardDetails, chargeWithToken=True, hasFailed=False)```

This is used to preauthorize a specific amount to be paid by a customer.

**Note:** > it takes the same parameters as Card charge. However, the cardDetails object differs. See below for an example

Once preauthorized successfully, you can then ```capture``` that ```held``` amount at a later time or date

A sample charge call is:

```py
payload = {
    "token":"flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k",
    "country":"NG",
    "amount":1000,
    "email":"user@gmail.com",
    "firstname":"temi",
    "lastname":"Oyekole",
    "IP":"190.233.222.1",
    "txRef":"MC-7666-YU",
    "currency":"NGN"
rave.Preauth.charge(payload)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'status': 'success', 'validationRequired': False, 'txRef': 'MC-7666-YU', 'flwRef': 'FLW-PREAUTH-M03K-7d01799093ee2db9d8136cf042dc8c37', 'suggestedAuth': None, 'authUrl': None}
```

 This call raises a ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```


<br>


### ```.capture(flwRef)```

This is used to capture the funds held in the account. Similar to the validate call, it requires you to pass the ```flwRef``` of the transaction.

>Please **NOTE** that the ```flwRef``` must be gotten from the response of the initial charge i.e after calling ```rave.Preauth.charge(payload)```


A sample capture call is:

```py
rave.Preauth.capture(data["flwRef"])
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'status': 'success', 'message': 'Capture complete', 'validationRequired': False, 'txRef': 'MC-7666-YU', 'flwRef': 'FLW-PREAUTH-M03K-0bce8fe1c3561e17e026ddfbbea37fdb'}
```

 This call raises a ```PreauthCaptureError``` if there was a problem processing your transaction. The ```PreauthCaptureError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PreauthCaptureError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

<br>

### ```.void(flwRef)```

This is used to void a preauth transaction. Similar to the validate call, it requires you to pass the ```flwRef```. 

>Please **NOTE** that the ```flwRef``` must be gotten from the response of the initial charge i.e after calling ```rave.Preauth.charge(payload)```



A sample void call is:

```py
rave.Preauth.void(data["flwRef"])
```

<br>

### ```.refund(flwRef)```

This is used to refund a preauth transaction. Similar to the validate call, it requires you to pass the ```flwRef```. 

>Please **NOTE** that the ```flwRef``` must be gotten from the response of the initial charge i.e after calling ```rave.Preauth.charge(payload)```



A sample void call is:

```py
rave.Preauth.refund(data["flwRef"])
```


### ```.verify(txRef)```

**See rave.Card.verify above**

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'transactionComplete': True, 'txRef': 'MC-7666-YU', 'flwRef': None, 'amount': 1000, 'chargedAmount': 1000, 'cardToken': 'flw-t1nf-5b0f12d565cd961f73c51370b1340f1f-m03k'}
```

 This call raises a ```TransactionVerificationError``` if there was a problem processing your transaction. The ```TransactionVerificationError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

<br>


### Complete preauth charge flow

```py
from rave_python import Rave, Misc, RaveExceptions
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# Payload with pin
payload = {
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

try:
    res = rave.Preauth.charge(payload)
    res = rave.Preauth.capture(res["flwRef"])
    res = rave.Preauth.verify(res["txRef"])
    print(res)

except RaveExceptions.TransactionChargeError as e:
    print(e)
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.PreauthCaptureError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
```

<br>

## ```rave.SubAccount```

This is used to initiate and manage payouts


**Functions included:**

* ```.create```

* ```.all```

* ```.fetch```

* ```.edit```

* ```.cancel```

<br>

### ```.create(accountDetails)```

This allows you to create a subaccount plan. It requires a dict ```accountDetails``` containing ```account_bank```, ```account_number```, ```business_name```, ```business_email```, ```business_contact```, ```business_contact_mobile```, ```business_mobile```.
 
>account_bank: This is the sub-accounts bank ISO code, use the [List of Banks for Transfer](https://developer.flutterwave.com/reference#list-of-banks-for-transfer) endpoint to retrieve a list of bank codes.

>account_number: This is the customer's account number

>business_name: This is the sub-account business name.

>business_email: This is the sub-account business email.

>business_contact: This is the contact person for the sub-account e.g. Richard Hendrix

>business_contact_mobile: Business contact number.

>business_mobile: Primary business contact number.

>split_type: This can be set as   ```percentage``` or ```flat``` when set as percentage it means you want to take a percentage fee on all transactions, and vice versa for flat this means you want to take a flat fee on every transaction.

>split_value: This can be a ```percentage``` value or ```flat``` value depending on what was set on ```split_type```

More information can be found [here](https://developer.flutterwave.com/v2.0/reference#create-subaccount)


A sample create call is:

```py
 res = rave.SubAccount.create({
	"account_bank": "044",
	"account_number": "0690000031",
	"business_name": "Jake Stores",
	"business_email": "kwakj@services.com",
	"business_contact": "Amy Parkers",
	"business_contact_mobile": "09083772",
	"business_mobile": "0188883882",
    "split_type": "flat",
    "split_value": 3000
	"meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
})
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'id': 114, 'data': {'id': 114, 'account_number': '0690000032', 'account_bank': '044', 'business_name': 'Jake Stores', 'fullname': 'Pastor Bright', 'date_created': '2018-10-09T10:43:02.000Z', 'meta': [{'metaname': 'MarketplaceID', 'metavalue': 'ggs-920900'}], 'split_ratio': 1, 'split_type': 'flat', 'split_value': 3000, 'subaccount_id': 'RS_8279B1518A139DD3238328747F322418', 'bank_name': 'ACCESS BANK NIGERIA'}}
```

 This call raises a ```.SubaccountCreationError``` if there was a problem processing your transaction. The ```.SubaccountCreationError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions..SubaccountCreationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.all()```

This allows you retrieve all subaccounts 

A sample all Subaccounts call is:

```py
res2 = rave.SubAccount.all()
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'SUBACCOUNTS', 'data': {'page_info': {'total': 3, 'current_page': 1, 'total_pages': 1}, 'subaccounts': [{'id': 114, 'account_number': '0690000032', 'account_bank': '044', 'business_name': 'Jake Stores', 'fullname': 'Pastor Bright', 'date_created': '2018-10-09T10:43:02.000Z', 'meta': [{'metaname': 'MarketplaceID', 'metavalue': 'ggs-920900'}], 'split_ratio': 1, 'split_type': 'flat', 'split_value': 3000, 'subaccount_id': 'RS_8279B1518A139DD3238328747F322418', 'bank_name': 'ACCESS BANK NIGERIA'}, {'id': 107, 'account_number': '0690000031', 'account_bank': '044', 'business_name': 'Jake Stores', 'fullname': 'Forrest Green', 'date_created': '2018-10-05T18:30:09.000Z', 'meta': [{'metaname': 'MarketplaceID', 'metavalue': 'ggs-920900'}], 'split_ratio': 1, 'split_type': 'flat', 'split_value': 100, 'subaccount_id': 'RS_41FFE616A1FA7EA56C85E57F593056F7', 'bank_name': 'ACCESS BANK NIGERIA'}]}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.fetch(subaccount_id)```

This allows you fetch a subaccount. You may or may not pass in a ```subaccount_id```. If you do not pass in a ```subaccount_id``` all subacocunts will be returned.

>subaccount_id: This is the payment plan ID. It can be gotten from the response returned from creating a plan or from the Rave Dashboard


A sample fetch Subaccount call is:

```py
res2 = rave.SubAccount.fetch(900)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'SUBACCOUNT', 'data': {'id': 106, 'account_number': '0690000035', 'account_bank': '044', 'business_name': 'JK Services', 'fullname': 'Peter Crouch', 'date_created': '2018-10-05T18:24:21.000Z', 'meta': [{'metaname': 'MarketplaceID', 'metavalue': 'ggs-920900'}], 'split_ratio': 1, 'split_type': 'flat', 'split_value': 100, 'subaccount_id': 'RS_0A6C260E1A70934DE6EF2F8CEE46BBB3', 'bank_name': 'ACCESS BANK NIGERIA'}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### Complete SubAccount flow

```py
from rave_python import Rave, Misc, RaveExceptions
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_PRIVATE_KEY", usingEnv = False)
try:
   
    res = rave.SubAccount.create({
	"account_bank": "044",
	"account_number": "0690000032",
	"business_name": "Jake Stores",
	"business_email": "jdhhd@services.com",
	"business_contact": "Amy Parkers",
	"business_contact_mobile": "09083772",
	"business_mobile": "0188883882",
    "split_type": "flat",
    "split_value": 3000,
	"meta": [{"metaname": "MarketplaceID", "metavalue": "ggs-920900"}]
    })
    res = rave.SubAccount.fetch('RS_0A6C260E1A70934DE6EF2F8CEE46BBB3')
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.PlanStatusError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
```

<br>

## ```rave.Transfer```

This is used to initiate and manage payouts


**Functions included:**

* ```.initiate```

* ```.bulk```

* ```.fetch```

* ```.all```

* ```.getFee```

* ```.getBalance```

*```.retryTransfer```

*```fetchRetries```

<br>

### ```.initiate(transferDetails)```

This initiates a transfer to a customer's account. When a transfer is initiated, it comes with a status NEW this means the transfer has been queued for processing.

**Please note that you must pass ```beneficiary_name``` as part of the initiate call. Else an error will be thrown.**
>Also, if you are doing international transfers, you must pass a meta parameter as part of your payload as shown below:

```py
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
```

A sample initiate call is:

```py
res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    "beneficiary_name": "Kwame Adew"
    })
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'id': 2671, 'data': {'id': 2671, 'account_number': '0690000044', 'bank_code': '044', 'fullname': 'Mercedes Daniel', 'date_created': '2018-10-09T08:37:20.000Z', 'currency': 'NGN', 'amount': 500, 'fee': 45, 'status': 'NEW', 'reference': 'MC-1539074239367', 'meta': None, 'narration': 'New transfer', 'complete_message': '', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ACCESS BANK NIGERIA'}}
```

 This call raises an ```IncompletePaymentDetailsError``` if there was a problem processing your transaction. The ```IncompletePaymentDetailsError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.bulk(bulkDetails)```

This initiates a bulk transfer to the customers specified in the ```bulkDetails``` object. When a transfer is initiated, it comes with a status NEW this means the transfer has been queued for processing.

A sample bulk call is:

```py
res2 = rave.Transfer.bulk({
    "title":"May Staff Salary",
    "bulk_data":[
        {
            "Ban":"044",
            "Account Number": "0690000032",
            "Amount":500,
            "Currency":"NGN",
            "Narration":"Bulk transfer 1",
            "reference": "mk-82973029"
        },
        {
            "Bank":"044",
            "Account Number": "0690000034",
            "Amount":500,
            "Currency":"NGN",
            "Narration":"Bulk transfer 2",
            "reference": "mk-283874750"
        }
    ]
})
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'status': 'success', 'message': 'BULK-TRANSFER-CREATED', 'id': 499, 'data': {'id': 499, 'date_created': '2018-10-09T09:13:54.000Z', 'approver': 'N/A'}}
```

 This call raises an ```InitiateTransferError``` if there was a problem processing your transaction. The ```InitiateTransferError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.InitiateTransferError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.fetch(reference=None)```

This allows you retrieve a single transfer. You may or may not pass in a ```reference```. If you do not pass in a reference, all transfers that have been processed will be returned.

A sample fetch call is:

```py
res2 = rave.Transfer.fetch("mk-82973029")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'QUERIED-TRANSFERS', 'data': {'page_info': {'total': 0, 'current_page': 0, 'total_pages': 0}, 'transfers': []}}}
```

 This call raises a ```TransferFetchError``` if there was a problem processing your transaction. The ```TransferFetchError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransferFetchError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.all()```

This allows you retrieve all transfers. 

A sample all Transfers call is:

```py
res2 = rave.Transfer.all("")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'QUERIED-TRANSFERS', 'data': {'page_info': {'total': 19, 'current_page': 1, 'total_pages': 2}, 'transfers': [{'id': 2676, 'account_number': '0690000044', 'bank_code': '044', 'fullname': 'Mercedes Daniel', 'date_created': '2018-10-09T09:37:12.000Z', 'currency': 'NGN', 'debit_currency': None, 'amount': 500, 'fee': 45, 'status': 'PENDING', 'reference': 'MC-1539077832148', 'meta': None, 'narration': 'New transfer', 'approver': None, 'complete_message': '', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ACCESS BANK NIGERIA'}, {'id': 2673, 'account_number': '0690000044', 'bank_code': '044', 'fullname': 'Mercedes Daniel', 'date_created': '2018-10-09T09:31:37.000Z', 'currency': 'NGN', 'debit_currency': None, 'amount': 500, 'fee': 45, 'status': 'FAILED', 'reference': 'MC-1539077498173', 'meta': None, 'narration': 'New transfer', 'approver': None, 'complete_message': 'DISBURSE FAILED: Insufficient funds', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ACCESS BANK NIGERIA'}, {'id': 2672, 'account_number': '0690000034', 'bank_code': '044', 'fullname': 'Ade Bond', 'date_created': '2018-10-09T09:13:56.000Z', 'currency': 'NGN', 'debit_currency': None, 'amount': 500, 'fee': 45, 'status': 'FAILED', 'reference': None, 'meta': None, 'narration': 'Bulk transfer 2', 'approver': None, 'complete_message': 'DISBURSE FAILED: Insufficient funds', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ACCESS BANK NIGERIA'}]}}}
```

 This call raises a ```TransferFetchError``` if there was a problem processing your transaction. The ```TransferFetchError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.TransferFetchError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.getFee(currency)```

This allows you get transfer rates for all Rave supported currencies. You may or may not pass in a ```currency```. If you do not pass in a ```currency```, all Rave supported currencies transfer rates will be returned.

A sample getFee call is:

```py
res2 = rave.Transfer.getFee("EUR")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'TRANSFER-FEES', 'data': [{'id': 6, 'fee_type': 'value', 'currency': 'EUR', 'fee': 35, 'createdAt': None, 'updatedAt': None, 'deletedAt': None, 'AccountId': 1}]}}
```

 ### ```.getBalance(currency)```

This allows you get your balance in a specified. You may or may not pass in a ```currency```. If you do not pass in a ```currency```, your balance will be returned in the currency specified in your rave account

A sample fetch call is:

```py
res2 = rave.Transfer.Balance("EUR")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'WALLET-BALANCE', 'data': {'Id': 27122, 'ShortName': 'EUR', 'WalletNumber': '3855000502677', 'AvailableBalance': 0, 'LedgerBalance': 0}}}
```


### ```.retryTransfer(transfer_id)```

This allows you to retry a previously failed transfer attempt. You are expected to pass the id for the failed transfer into this call (ids can be gotten in data object from the initial transfer response)

A sample fetch call is:

```py
res2 = rave.retryTransfer.Balance("169680")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'Transfer retry attempt queued.', 'data': {'id': 169681, 'account_number': '0690000044', 'bank_code': '044', 'fullname': 'Mercedes Daniel', 'date_created': '2021-02-19T15:56:57.000Z', 'currency': 'NGN', 'amount': 500, 'fee': 10.75, 'status': 'NEW', 'reference': 'SampleTransfer4_PMCK_ST_FDU_1_RETRY_1', 'meta': None, 'narration': 'Test_Transfer_for_new_features', 'complete_message': '', 'requires_approval': 0, 'is_approved': 1, 'bank_name': 'ACCESS BANK NIGERIA'}}}
```

<br>

### ```.fetchRetries(transfer_id)```

This allows you to get all retry attempts for all previously failed transfer attempts.

A sample fetch call is:

```py
res2 = rave.fetchRetries.Balance("169680")
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'Transfer retry attempts retrieved.', 'data': [{'id': 169681, 'account_number': '0690000044', 'bank_code': '044', 'bank_name': 'ACCESS BANK NIGERIA', 'fullname': 'Mercedes Daniel', 'currency': 'NGN', 'debit_currency': None, 'amount': 500, 'fee': 10.75, 'status': 'FAILED', 'reference': 'SampleTransfer4_PMCK_ST_FDU_1_RETRY_1', 'narration': 'Test_Transfer_for_new_features', 'complete_message': 'DISBURSE FAILED: Transfer failed. Please contact support', 'meta': None, 'requires_approval': 0, 'is_approved': 1, 'date_created': '2021-02-19T15:56:57.000Z'}]}}
```


### Complete transfer flow

```py
from rave_python import Rave, RaveExceptions
try:
    rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

    res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    "beneficiary_name": "Kwame Adew"
    })

    res2 = rave.Transfer.bulk({
        "title": "test",
        "bulk_data":[
        ]
    })
    print(res)

    balanceres = rave.Transfer.getBalance("NGN")
    print(balanceres)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
```

<br>

## ```rave.Subscriptions```

This is used to initiate and manage Subscriptions


**Functions included:**

* ```.all```

* ```.fetch```

* ```.cancel```

* ```.activate```


### ```.all()```

This allows you retrieve all subscriptions 

A sample all subscriptions call is:

```py
res2 = rave.Subscriptions.all()
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'SUBSCRIPTIONS-FETCHED', 'data': {'page_info': {'total': 0, 'current_page': 0, 'total_pages': 0}, 'plansubscriptions': []}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.fetch(subscription_id, subscription_email)```

This allows you fetch a subscription. You may or may not pass in a ```subscription_id``` or ```subscription_email```. If you do not pass in a ```subscription_id``` or ```subscription_email``` all subscriptions will be returned.

>subscription_id: This is the subscription ID.

>subscription_email: This is the subscription email.


A sample fetch subscription call is:

```py
res2 = rave.Subscriptions.fetchSubscription(900)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'SUBSCRIPTIONS-FETCHED', 'data': {'page_info': {'total': 0, 'current_page': 0, 'total_pages': 0}, 'plansubscriptions': []}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.cancelSubscription(subscription_id)```

This allows you cancel a subscription.

>subscription_id: This is the subscription ID. It can be gotten from the Rave Dashboard


A sample cancel subscription call is:

```py
res2 = rave.Subscriptions.cancel(900)
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```


### ```.activate(subscription_id)```

This allows you activate a subscription.

>subscription_id: This is the subscription ID. It can be gotten from the Rave Dashboard


A sample activate subscription call is:

```py
res2 = rave.Subscriptions.activate(900)
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### Complete Subscriptions flow

```py
from rave_python import Rave, Misc, RaveExceptions
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_PRIVATE_KEY", usingEnv = False)
try:
   
    res = rave.Subscriptions.all()
    res = rave.Subscriptions.fetch(880)
    res = rave.Subscriptions.cancel(880)
    print(res)

except RaveExceptions.PlanStatusError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
```

<br>

## ```rave.PaymentPlan```

This is used to initiate and manage payment plans


**Functions included:**

* ```.create```

* ```.all```

* ```.fetch```

* ```.cancelPlan```

* ```.edit```

<br>

### ```.create(planDetails)```

This allows a customer to create a payment plan. It requires a dict ```planDetails``` containing ```amount```, ```name```, ```interval```, ```duration```. 
>amount: this is the amount for the plan

>name: This is what would appear on the subscription reminder email

>interval: This are the charge intervals possible values are:
```
daily;
weekly;
monthly;
yearly;
quarterly;
bi-anually;
every 2 days;
every 90 days;
every 5 weeks;
every 12 months;
every 6 years;
every x y (where x is a number and y is the period e.g. every 5 months)
```

>duration: This is the frequency, it is numeric, e.g. if set to 5 and intervals is set to monthly you would be charged 5 months, and then the subscription stops.

More information can be found [here](https://developer.flutterwave.com/v2.0/reference#create-payment-plan)


**If duration is not passed, any subscribed customer will be charged indefinitely**


A sample create call is:

```py
 res = rave.PaymentPlan.create({
    "amount": 1,
    "duration": 5,
    "name": "Ultimate Play",
    "interval": "5"
 })
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'id': 890, 'data': {'id': 890, 'name': 'Ultimate Play', 'amount': 1, 'interval': 'dai', 'duration': 5, 'status': 'active', 'currency': 'NGN', 'plan_token': 'rpp_af8ea4d5d785d08f47d8', 'date_created': '2018-10-09T10:03:00.000Z'}}
```

 This call raises an ```IncompletePaymentDetailsError``` if there was a problem processing your transaction. The ```IncompletePaymentDetailsError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.all()```

This allows you retrieve all payment plans. 

A sample all plans call is:

```py
res2 = rave.Transfer.all()
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'QUERIED-PAYMENTPLANS', 'data': {'page_info': {'total': 12, 'current_page': 1, 'total_pages': 2}, 'paymentplans': [{'id': 890, 'name': 'Ultimate Play', 'amount': 1, 'interval': 'dai', 'duration': 5, 'status': 'active', 'currency': 'NGN', 'plan_token': 'rpp_af8ea4d5d785d08f47d8', 'date_created': '2018-10-09T10:03:00.000Z'}, {'id': 885, 'name': 'N/A', 'amount': 0, 'interval': 'daily', 'duration': 0, 'status': 'cancelled', 'currency': 'NGN', 'plan_token': 'rpp_19c8a7af7a06351fd78b', 'date_created': '2018-10-05T17:16:15.000Z'}]}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.fetch(plan_id, plan_name)```

This allows you fetch a payment plan. You may or may not pass in a ```plan_id``` or ```plan_name```. If you do not pass in a ```plan_id``` or ```plan_name```, all payment plans will be returned.

>plan_id: This is the payment plan ID. It can be gotten from the response returned from creating a plan or from the Rave Dashboard

>plan_name: This is the payment plan name. It can be gotten from the response returned from creating a plan or from the Rave Dashboard

A sample fetch plan call is:

```py
res2 = rave.Transfer.fetch(900)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'QUERIED-PAYMENTPLANS', 'data': {'page_info': {'total': 1, 'current_page': 1, 'total_pages': 1}, 'paymentplans': [{'id': 890, 'name': 'Ultimate Play', 'amount': 1, 'interval': 'dai', 'duration': 5, 'status': 'active', 'currency': 'NGN', 'plan_token': 'rpp_af8ea4d5d785d08f47d8', 'date_created': '2018-10-09T10:03:00.000Z'}]}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.cancelPlan(plan_id)```

This allows you cancel a payment plan. It requires that you pass in an ```plan_id```.

>plan_id: This is the payment plan ID. It can be gotten from the response returned from creating a plan or from the Rave Dashboard

A sample cancelPlan call is:

```py
res2 = rave.Transfer.cancelPlan(900)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'PLAN-CANCELED', 'data': {'id': 890, 'name': 'Ultimate Play', 'uuid': 'rpp_af8ea4d5d785d08f47d8', 'status': 'cancelled', 'start': None, 'stop': None, 'initial_charge_amount': None, 'currency': 'NGN', 'amount': 1, 'duration': 5, 'interval': 'dai', 'createdAt': '2018-10-09T10:03:00.000Z', 'updatedAt': '2018-10-09T10:17:14.000Z', 'deletedAt': None, 'AccountId': 5949, 'paymentpageId': None}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```


### ```.edit(plan_id, newData={})```

This allows you edit a payment plan. It requires that you pass in an ```plan_id```. If you do not pass in the ```newData``` dict containing the change you want to make to your plan, the plan stays the same.

>plan_id: This is the payment plan ID. It can be gotten from the response returned from creating a plan or from the Rave Dashboard

>newData: A ```dict``` that must contain one or both of: ```name```, ```status``` as properties. 
>```name``` specifies the new name for your payment plan.
>```status``` : possible values are ```active``` and ```cancelled```

A sample cancel plan call is:

```py
res = rave.PaymentPlan.editPlan(880, {
        "name": "Jack's Plan",
        "status": "active"
})
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{'error': False, 'returnedData': {'status': 'success', 'message': 'PLAN-EDITED', 'data': {'id': 880, 'name': "Jack's Plan", 'uuid': 'rpp_237e94690d8e7089c07b', 'status': 'active', 'start': None, 'stop': None, 'initial_charge_amount': None, 'currency': 'NGN', 'amount': 1, 'duration': 5, 'interval': 'dai', 'createdAt': '2018-10-05T17:13:16.000Z', 'updatedAt': '2018-10-09T10:25:25.000Z', 'deletedAt': None, 'AccountId': 5949, 'paymentpageId': None}}}
```

 This call raises a ```PlanStatusError``` if there was a problem processing your transaction. The ```PlanStatusError``` contains some information about your transaction. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.PlanStatusError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

<br>

### Complete PaymentPlan flow

```py
from rave_python import Rave, Misc, RaveExceptions
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_PRIVATE_KEY", usingEnv = False)
try:

    res = rave.PaymentPlan.create({
        "amount": 1,
        "duration": 5,
        "name": "Ultimate Plan",
        "interval": "dai"
    })
    
    res = rave.PaymentPlan.edit(880, {
        "name": "Jack's Plan",
        "status": "active"
    })
    print(res)

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
```

<br>

## ```rave.Ussd```

>**NOTE:** This payment option is still in beta mode.

<br>

## ```rave.VirtualAccount```

This is used to create virtual account for transfers.


**Functions included:**

* ```.create```

<br>

### ```.create(accountDetails)```

This allows a customer to create a virtual card. It requires a dict ```vcardDetails``` containing ```email```, ```seckey```, ```is_permanant```, ```frequency```, ```duration``` and  ```narration```.

A sample Create call is:

```py
 res = rave.VirtualAccount.create({
	"email": "user@example.com",
	"seckey": "FLWSECK-****************************-X",
	"is_permanent": true
})
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "BANKTRANSFERS-ACCOUNTNUMBER-CREATED",
    "data": {
        "response_code": "02",
        "response_message": "Transaction in progress",
        "flw_reference": "FLW-89298329b9794587807aa775cda5db9f",
        "accountnumber": "1357960669",
        "accountstatus": "ACTIVE",
        "frequency": "N/A",
        "bankname": "Highstreet MFB",
        "created_on": "2019-08-20 12:18:46",
        "expiry_date": "N/A",
        "note": "Please make a bank transfer to Raver",
        "amount": null
    }
}
```

 This call raises an ```IncompleteAccountDetailsError``` if there was a problem creating your virtual account. The ```IncompleteCardDetailsError``` contains some information about your virtual account. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.IncompleteAccountDetailsError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

<br>

## ```rave.VirtualCard```

This is used to create virtual cards and carry out other virtual card operations.


**Functions included:**

* ```.create```

* ```.all```

* ```.get```

* ```.cancel```

* ```.freeze```

* ```.unfreeze```

* ```.fund```

* ```.withdraw```
<br>

### ```.create(vcardDetails)```

This allows a customer to create a virtual card. It requires a dict ```vcardDetails``` containing ```currency```, ```amount```, ```billing name```, ```billing address```, ```billing city```, ```billing state```, ```billing postal code```, ```billing country```

A sample Create call is:

```py
 res = rave.VirtualCard.create({
    "currency": "NGN",
    "amount": "100",
    "billing_name": "Corvus james",
    "billing_address": "8, Providence Street",
    "billing_city": "Lekki",
    "billing_state": "Lagos",
    "billing_postal_code": "100001",
    "billing_country": "NG",
 })
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{"status": "success", "message": "Card created successfully", "data": {"id": "c3ff3ac4-784b-4d07-9fc7-b5b9cde75752", "AccountId": 507, "amount": "100.00", "currency": "NGN", "card_hash": "c3ff3ac4-784b-4d07-9fc7-b5b9cde75752", "cardpan": "5563389915692128", "maskedpan": "556338*******2128", "city": "Lekki", "state": "Lagos", "address_1": "8, Providence Street", "address_2": null, "zip_code": "100001", "cvv": "408", "expiration": "2022-01", "send_to": null, "bin_check_name": null, "card_type": "mastercard", "name_on_card": "Corvus james", "date_created": "2019-01-30T16:45:45.550663+00:00", "is_active": true}}
```

 This call raises an ```IncompleteCardDetailsError``` if there was a problem creating your card. The ```IncompleteCardDetailsError``` contains some information about the error encountered in creating your card. You can handle this as such:

```py
try: 
    #Your charge call
except RaveExceptions.IncompleteCardDetailsError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

### ```.all()```

This allows a the user to query all cards 

A sample Create call is:

```py
res = rave.VirtualCard.all()
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "SUCCESSFUL",
    "data": [
        {
            "id": "660bae3b-333c-410f-b283-2d181587247f",
            "AccountId": 507,
            "amount": "1.00",
            "currency": "USD",
            "card_hash": "660bae3b-333c-410f-b283-2d181587247f",
            "cardpan": "5563384241646062",
            "maskedpan": "556338*******6062",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "480",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "ruby cupp",
            "date_created": "2019-01-26T04:00:10.263Z",
            "is_active": true
        },
        {
            "id": "6b7daf10-ade2-4633-a2ab-ea5495bb0ce2",
            "AccountId": 507,
            "amount": "10.00",
            "currency": "USD",
            "card_hash": "6b7daf10-ade2-4633-a2ab-ea5495bb0ce2",
            "cardpan": "5563387512530188",
            "maskedpan": "556338*******0188",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "248",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "Paige graffunder",
            "date_created": "2019-01-27T10:52:31.65Z",
            "is_active": true
        },
        {
            "id": "f32a2067-1b5e-419f-ae5c-69f968ee85db",
            "AccountId": 507,
            "amount": "1.00",
            "currency": "USD",
            "card_hash": "f32a2067-1b5e-419f-ae5c-69f968ee85db",
            "cardpan": "5563387304903023",
            "maskedpan": "556338*******3023",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "994",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "Donna Gaydosh",
            "date_created": "2019-01-27T11:10:29.333Z",
            "is_active": true
        },
        {
            "id": "3ff39cd4-4451-403d-874a-f90fa67fd1b8",
            "AccountId": 507,
            "amount": "1.00",
            "currency": "USD",
            "card_hash": "3ff39cd4-4451-403d-874a-f90fa67fd1b8",
            "cardpan": "5563380574586529",
            "maskedpan": "556338*******6529",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "950",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "Stephanie elmer",
            "date_created": "2019-01-27T11:12:26.68Z",
            "is_active": true
        },
        {
            "id": "cabbea77-9040-47b4-ac05-b7d1d804173b",
            "AccountId": 507,
            "amount": "1.00",
            "currency": "USD",
            "card_hash": "cabbea77-9040-47b4-ac05-b7d1d804173b",
            "cardpan": "5563388312887679",
            "maskedpan": "556338*******7679",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "147",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "Jack Ma",
            "date_created": "2019-01-27T15:20:20.52Z",
            "is_active": true
        },
        {
            "id": "c3ff3ac4-784b-4d07-9fc7-b5b9cde75752",
            "AccountId": 507,
            "amount": "12.00",
            "currency": "USD",
            "card_hash": "c3ff3ac4-784b-4d07-9fc7-b5b9cde75752",
            "cardpan": "5563389915692128",
            "maskedpan": "556338*******2128",
            "city": "Hillside",
            "state": "New jersey",
            "address_1": "471 mundet pl",
            "address_2": null,
            "zip_code": "07205",
            "cvv": "408",
            "expiration": "2022-01",
            "send_to": null,
            "bin_check_name": null,
            "card_type": "mastercard",
            "name_on_card": "Jamiu Ganiu",
            "date_created": "2019-01-30T16:45:47.233Z",
            "is_active": true
        }
    ]
}
```

### ```.get()```

This allows a the user to query the details of a card with a given id. 

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.get(card_id)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "status": "success",
    "message": "SUCCESSFUL",
    "data": {
        "id": "660bae3b-333c-410f-b283-2d181587247f",
        "AccountId": 507,
        "amount": "21.00",
        "currency": "USD",
        "card_hash": "660bae3b-333c-410f-b283-2d181587247f",
        "cardpan": "5563384241646062",
        "maskedpan": "556338*******6062",
        "city": "Hillside",
        "state": null,
        "address_1": "471 mundet pl",
        "address_2": null,
        "zip_code": "07205",
        "cvv": "480",
        "expiration": "2022-01",
        "send_to": null,
        "bin_check_name": null,
        "card_type": "mastercard",
        "name_on_card": null,
        "date_created": "2019-01-30T17:01:47.0972087+00:00",
        "is_active": true
    }
}
```

### ```.cancel()```

This allows a the user to terminate the use of a card with a given id permanently. This cancellation results in the permanent deletion of the card. 

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.cancel(card_id)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
  "Status": "success",
  "Message": "Card terminated successfully",
  "Reference": null
}
```

### ```.freeze()```

This allows a the user to terminate the use of a card with a given id temporarily. This cancellation results in the temporary suspension of the card 

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.freeze(card_id)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
  "Status": "success",
  "Message": "Card freeze successful",
  "Reference": null
}
```

### ```.unfreeze()```

This allows a the user to resume the use of a temporarily suspended or frozen card with a given id. 

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.unfreeze(card_id)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
  "Status": "success",
  "Message": "Card unfreeze successful",
  "Reference": null
}
```

### ```.fund()```

This allows a the user to add funds to a card with a given id. the `card_id`, `currency` and `amount` are passed into the `.fundCard()` method.

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.fund(card_id, "NGN", 2000)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "Status": "success",
    "Message": "Card was funded successfully",
    "Reference": null
}
```

### ```.withdraw()```

This allows a the user to withdraw funds from a card with a given id. the `card id` and `amount` are passed into the `.Withdraw()` method.

A sample Create call is:

```py
card_id = "660bae3b-333c-410f-b283-2d181587247f"
res = rave.VirtualCard.withdraw(card_id, 1000)
print(res)
```

#### Returns

This call returns a dictionary. A sample response is:

```py
{
    "Status": "success",
    "Message": "Withdrawal successful",
    "Reference": null
}
```
<br>

## Run Tests

All of the SDK's tests are written with Python's ```unittest``` module. The tests currently test:
```rave.Account```
```rave.Card```
```rave.Transfer```
```rave.Preauth```
```rave.Subaccount```
```rave.Subscriptions```
```rave.Paymentplan```

They can be run like so:

```sh
python test.py
```

>**NOTE:** If the test fails for creating a subaccount, just change the ```account_number``` ```account_bank```  and ```businesss_email``` to something different

>**NOTE:** The test may fail for account validation - ``` Pending OTP validation``` depending on whether the service is down or not
<br>

## Support
For further assistance in using the SDK, you can contact the Developers on [Slack](https://join.slack.com/t/flutterwavedevelopers/shared_invite/enQtNTk3MjgxMjU3ODI5LWFkMjBkYTc0ZGJhM2Q5MTY3YjFkYzAyYmM1ZDZjZjUwMjE4YTc2NjQ1ZGM5ZWE4NDUxMzc4MmExYmI1Yjg5ZWU) and [Email](mailto:developers@flutterwavego.com). You can get more information about the amazing features here [here](https://developer.flutterwave.com/reference#introduction).
