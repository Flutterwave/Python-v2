# Upgrading to v1.5.0

## Requirements

| Requirement | v1.4.x | v1.5.0 |
|---|---|---|
| Python | >=2.7 | **>=3.10** |
| `pycryptodome` | any | >=3.10.0 |
| `requests` | any | >=2.20.0 |

---

## Before you upgrade

### 1. Check your Python version

```bash
python --version
```

If you are on Python 3.9 or below, upgrade Python before upgrading this SDK.


### 2. Clear the identity disk cache

If you have previously run the SDK, delete the cached identity file to allow the new telemetry
system to initialise cleanly:

```bash
rm /tmp/flw_sdk.json
```

If you set a custom path via `FLW_SDK_STATE_PATH`, delete that file instead.

---

## Migration guide

### Initialisation — no change required

```python
# This still works exactly as before
from rave_python import Rave

rave = Rave("YOUR_PUBLIC_KEY", production=False)
```

```python
# Or without environment variables
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv=False)
```

### Card charge flow — no change required

The charge and validate steps are unchanged:

```python
from rave_python import Rave, Misc
from rave_python.rave_exceptions import CardChargeError, TransactionValidationError, TransactionVerificationError

rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv=False)

payload = {
    "cardno": "5531886652142950",
    "cvv": "564",
    "expirymonth": "09",
    "expiryyear": "32",
    "amount": "100",
    "email": "user@example.com",
    "phonenumber": "08000000000",
    "firstname": "Flutterwave",
    "lastname": "Developer",
    "IP": "355426087298442",
    "currency": "NGN",
    "country": "NG",
}

try:
    res = rave.Card.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address={
                "billingzip": "07205",
                "billingcity": "Hillside",
                "billingaddress": "470 Mundet PI",
                "billingstate": "NJ",
                "billingcountry": "US",
            })
        res = rave.Card.charge(payload)

    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "12345")

    res = rave.Card.verify(res["txRef"])
    print(res["transactionComplete"])  # True for a successful transaction

except CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except TransactionValidationError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])
```

### Verify response — field names updated

If your code reads fields from the `rave.Card.verify()` response dict, update the field names
you reference:

```python
res = rave.Card.verify(txRef)

# v1.4.x — these field names may return None in v1.5.0
old_currency = res.get("currency")       # was from response field "currency"
old_chargecode = res.get("chargecode")   # was from response field "chargecode"

# v1.5.0 — same keys in the response dict, now correctly populated
currency = res["currency"]               # now from "transaction_currency"
chargecode = res["chargecode"]           # now from "flwMeta.chargeResponse"
transaction_complete = res["transactionComplete"]  # now correctly True/False
```

The keys in the returned dict are unchanged — `currency`, `chargecode`, `transactionComplete`
etc. are the same. What changed is that they are now correctly populated from the right fields
in the Flutterwave API response. Code that only checks `res["transactionComplete"]` requires
no changes.

New fields available in the verify response that were not present before:

```python
res = rave.Card.verify(txRef)

appfee = res["appfee"]          # transaction fee charged by Flutterwave
vbvcode = res["vbvcode"]        # VBV/3DS response code
status = res["status"]          # outer API response status ("success")
```

### Other payment methods — no change required

Mobile money, bank transfer, USSD, and all other payment methods work exactly as before.
The same verify response field improvements apply to all of them through the base class.

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes (if `usingEnv=True`) | — | Your Flutterwave secret key |
| `FLW_SDK_STATE_PATH` | No | `/tmp/flw_sdk.json` | Path for the identity disk cache |

---