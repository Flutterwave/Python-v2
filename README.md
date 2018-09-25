# Python_Rave

## Introduction
This is a Python wrapper around the [API](https://flutterwavedevelopers.readme.io/v2.0/reference) for [Rave by Flutterwave](https://rave.flutterwave.com).
#### Payment types implemented:
* Card Payments
* Bank Account Payments
* Ghana Mobile Money Payments
* Mpesa
* USSD Payments
## Installation
To install, run

``` pip install python_rave```

Note: This is currently under active development
## Import Package
The base class for this package is 'Rave'. To use this class, add:

``` from python_rave import Rave ```

## Initialization

#### To instantiate in sandbox:
To use Rave, instantiate the Rave class with your public key. We recommend that you store your secret key in an environment variable named, ```RAVE_SECRET_KEY```. Instantiating your rave object is therefore as simple as:

``` rave = Rave("YOUR_PUBLIC_KEY")```

####  To instantiate without environment variables (Sandbox):
If you choose not to store your secret key in an environment variable, we do provide a ```usingEnv``` flag which can be set to ```False```, but please be warned, do not use this package without environment variables in production

``` rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv = False) ```


#### To instantiate in production:
To initialize in production, simply set the ```production``` flag to ```True```. It is highly discouraged but if you choose to not use environment variables, you can do so in the same way mentioned above.

``` rave = Rave("YOUR_PUBLIC_KEY", production=True)```

# Rave Objects
This is the documentation for all of the components of python_rave


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

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the Misc library (add link).


A sample call is:

``` res = rave.Account.charge(payload) ```

#### Returns

This call returns a dictionary. A sample response is:

 ```{'error': False, 'validationRequired': True, 'txRef': 'MC-1530899106006', 'flwRef': 'ACHG-1530899109682', 'authUrl': None} ```

 This call raises an ```AccountChargeError``` if there was a problem processing your transaction. The ```AccountChargeError``` contains some information about your transaction. You can handle this as such:

```
try: 
    #Your charge call
except RaveExceptions.AccountChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': 'MC-1530897824739', 'flwRef': None, 'errMsg': 'Sorry, that account number is invalid, please check and try again'}```

<br>

### ```.validate(txRef)```

After a successful charge, most times you will be asked to verify with OTP. To check if this is required, check the ```validationRequired``` key in the ```res``` of the charge call.

In the case that an ```authUrl``` is returned from your charge call, you may skip the validation step and simply pass your authUrl to the end-user. 

```authUrl = res['authUrl'] ```

To validate, you need to pass the ```flwRef``` from the ```res``` of the charge call as well as the OTP.

A sample validate call is: 

```res2 = rave.Account.validate(res["flwRef"], "12345")```


#### Returns

This call returns a dictionary containing the ```txRef```, ```flwRef``` among others if successful.

This call raises a ```TransactionValidationError``` if the OTP is not correct or there was a problem processing your request. 

To handle this, write:

```
try:
    # Your charge call
except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': 'MC-1530899869968', 'flwRef': 'ACHG-1530899873118', 'errMsg': 'Pending OTP validation'}```



<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

``` res = rave.Account.verify(data["txRef"]) ```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.



<br>

### Complete account flow

```
from python_rave import Rave, RaveExceptions, Misc
rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)
# account payload
payload = {
  "accountbank": "232",# get the bank code from the bank list endpoint.
  "accountnumber": "0061333471",
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
        rave.Account.validate(res["flwRef"], "1234")

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
## ```rave.Card```
This is used to facilitate card transactions.

**Functions included:**

* ```.charge```

* ```.validate```

* ```.verify```

* ```.getTypeOfArgsRequired```

* ```.updatePayload```

<br>

### ```.charge(payload)```
This is called to start a card transaction. The payload should be a dictionary containing card information. It should have the parameters:

* ```cardno```,

* ```cvv```, 

* ```expirymonth```, 

* ```expiryyear```, 

* ```amount```, 

* ```email```, 

* ```phonenumber```,

* ```firstname```, 

* ```lastname```, 

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the Misc library (add link).


A sample call is:

``` res = rave.Card.charge(payload) ```

#### Returns

This call returns a dictionary. A sample response is:

 ```{'error': False, 'validationRequired': True, 'txRef': 'MC-1530899106006', 'flwRef': 'ACHG-1530899109682', 'suggestedAuth': None} ```

 This call raises an ```CardChargeError``` if there was a problem processing your transaction. The ```CardChargeError``` contains some information about your transaction. You can handle this as such:

```
try: 
    #Your charge call
except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': 'MC-1530897824739', 'flwRef': None, 'errMsg': 'Sorry, that card number is invalid, please check and try again'}```

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

```res2 = rave.Card.validate(res["flwRef"], "12345")```

#### Returns

This call returns a dictionary containing the ```txRef```, ```flwRef``` among others if successful.

This call raises a ```TransactionValidationError``` if the OTP is not correct or there was a problem processing your request. 

To handle this, write:

```
try:
    # Your charge call
except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])
```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': None, 'flwRef': 'FLW-MOCK-a7911408bd7f55f89f0211819d6fd370', 'errMsg': 'otp is required'}```

<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

``` res = rave.Card.verify(data["txRef"]) ```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

### Complete card charge flow

```

from python_rave import Rave
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
## ```rave.Mpesa```
This is used to facilitate Mpesa transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start an Mpesa transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```account```, 

* ```email```, 

* ```phonenumber```, 

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the Misc library (add link).


A sample call is:

``` res = rave.Mpesa.charge(payload) ```

#### Returns

This call returns a dictionary. A sample response is:

 ```{'error': False, 'validationRequired': True, 'txRef': 'MC-1530910216380', 'flwRef': 'N/A'} ```

 This call raises an ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': 'MC-1530910109929', 'flwRef': None, 'errMsg': 'email is required'}```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

``` res = rave.Mpesa.verify(data["txRef"]) ```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

<br>

### Complete Mpesa charge flow

```
from python_rave import Rave, RaveExceptions, Misc
rave = Rave("ENTIRE_YOUR_PUBLIC_KEY", "ENTIRE_YOUR_SECRET_KEY", usingEnv = False)

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

## ```rave.GhMobile```
This is used to facilitate Ghana mobile money transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start an Ghana mobile money transaction. The payload should be a dictionary containing account information. It should have the parameters:

* ```amount```,

* ```email```, 

* ```phonenumber```,

* ```network```,

* ```IP```,

* ```redirect_url```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the Misc library (add link).


A sample call is:

``` res = rave.GhMobile.charge(payload) ```

#### Returns

This call returns a dictionary. A sample response is:

 ```{'error': False, 'validationRequired': True, 'txRef': 'MC-1530910216380', 'flwRef': 'N/A'} ```

 This call raises an ```TransactionChargeError``` if there was a problem processing your transaction. The ```TransactionChargeError``` contains some information about your transaction. You can handle this as such:

```
try: 
    #Your charge call
except RaveExceptions.TransactionChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

```

A sample ``` e.err ``` contains:

```{'error': True, 'txRef': 'MC-1530911537060', 'flwRef': None, 'errMsg': None}```


<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```res``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

``` res = rave.GhMobile.verify(data["txRef"]) ```

#### Returns

This call returns a dict with ```txRef```, ```flwRef``` and ```transactionComplete``` which indicates whether the transaction was completed successfully. 

If your call could not be completed successfully, a ```TransactionVerificationError``` is raised.

<br>

### Complete GhMobile charge flow

```
from python_rave import Rave, RaveExceptions, Misc
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
## ```rave.Ussd```
This is used to facilitate USSD transactions.

**Functions included:**

* ```.charge```


* ```.verify```

<br>

### ```.charge(payload)```
This is called to start a USSD transaction. The payload should be a dictionary containing payment information. It should have the parameters:

* ```accountbank```,

* ```accountnumber```, 

* ```amount```, 

* ```email```,

* ```phonenumber```,

* ```IP```

Optionally, you can add a custom transaction reference using the ```txRef``` parameter. Note that if you do not specify one, it would be automatically generated. We do provide a function for generating transaction references in the Misc library (add link).


A sample call is:

``` furtherActionRequired, action = rave.Ussd.charge(payload) ```

#### Returns

This call returns two responses. The first variable indicates whether further action is required to complete the transaction. The second variable is what was returned from the server on the call.

<br>

### ```.verify(txRef)```

You can call this to check if your transaction was completed successfully. You have to pass the transaction reference generated at the point of charging. This is the ```txRef``` in the ```action``` parameter returned any of the calls (```charge``` or ```validate```). 

A sample verify call is:

``` success, data = rave.Ussd.verify(data["txRef"]) ```

<br>

### Complete USSD charge flow

```
from python_rave import Rave, RaveExceptions, Misc
rave = Rave("YOUR_PUBLIC KEY", "YOUR_SECRET_KEY", production=True, usingEnv = False)

zenithPayload = {
  "accountbank": "057",
  "accountnumber": "0691008392",#collect the customers account number for Zenith
  "currency": "NGN",
  "country": "NG",
  "amount": "10",
  "email": "desola.ade1@gmail.com",
  "phonenumber": "0902620185", 
  "IP": "355426087298442",
}

furtherActionNeeded, action = rave.Ussd.charge(zenithPayload)
if furtherActionNeeded:
  completed = False
  while not completed:
    try:
      completed = rave.Ussd.verify(zenithPayload["txRef"])
    except RaveExceptions.TransactionVerificationError:
      print(action)
    
success, data = rave.Ussd.verify(zenithPayload["txRef"])
print(success)

```

<br><br>
## ```rave.Preauth```
This is used to facilitate preauthorized card transactions. This inherits the Card class so any task you can do on Card, you can do with preauth.

**Functions included:**

* ```.charge```

* ```.validate```

* ```.verify```

* ```.getTypeOfArgsRequired```

* ```.updatePayload```

<br>



### ```.capture(flwRef)```

This is used to capture the funds held in the account. Similar to the validate call, it requires you to pass the ```flwRef```. The flwRef can be gotten from the by searching for the ```flwRef``` in the ```action``` (second returned variable) of the initial charge call.


A sample capture call is:

``` rave.Preauth.capture(data["flwRef"])```

<br>

### ```.void(flwRef)```

This is used to void a preauth transaction. Similar to the validate call, it requires you to pass the ```flwRef```. The flwRef can be gotten from the by searching for the ```flwRef``` in the ```action``` (second returned variable) of the initial charge call.


A sample capture call is:

```rave.Preauth.void(data["flwRef"]) ```

<br>

### ```.refund(flwRef)```

This is used to refund a preauth transaction. Similar to the validate call, it requires you to pass the ```flwRef```. The flwRef can be gotten from the by searching for the ```flwRef``` in the ```action``` (second returned variable) of the initial charge call.


A sample capture call is:

```rave.Preauth.refund(data["flwRef"]) ```

<br>


### Complete preauth charge flow

```
from python_rave import Rave
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv = False)

# Payload with pin
payload = {
  "cardno": "4751763236699647",
  "cvv": "890",
  "expirymonth": "09",
  "expiryyear": "21",
  "amount": "10",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
  "IP": "355426087298442",
}

try:
    res = rave.Preauth.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
        res = rave.Preauth.charge(payload)

    if res["validationRequired"]:
        rave.Preauth.validate(res["flwRef"], "12345")

    res = rave.Preauth.capture(res["flwRef"])
    res = rave.Preauth.verify(res["txRef"])
    print(res["transactionComplete"])

except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])


```

## ```rave.Transfer```

This is used to initiate and manage payouts


**Functions included:**

* ```.initiate```

* ```.bulk```

* ```.fetch```

* ```.getFee```

* ```.getBalance```

<br>

### Complete transfer flow

```
from python_rave import Rave, RaveExceptions
try:
    rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

    res = rave.Transfer.initiate({
    "account_bank": "044",
    "account_number": "0690000044",
    "amount": 500,
    "narration": "New transfer",
    "currency": "NGN",
    })

    res2 = rave.Transfer.bulk({
        "title": "test",
        "bulk_data":[
        ]
    })
    print(res)
    rave.Transfer.getBalance()

except RaveExceptions.IncompletePaymentDetailsError as e:
    print(e)

except RaveExceptions.InitiateTransferError as e:
    print(e.err)

except RaveExceptions.TransferFetchError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)


```