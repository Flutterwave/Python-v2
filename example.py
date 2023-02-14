from rave_python import Rave, RaveExceptions, Misc
PublicKey = "FLWPUBK-45587fdb1c84335354ab0fa388b803d5-X"
SecretKey = "FLWSECK-2c9a2a781e56760b5d9c29c67ec22347-X"

rave = Rave(PublicKey, SecretKey, production=True, usingEnv=False)

accountDetails = {
    "email": "cornelius.ashley@outlook.com",
    "seckey": SecretKey,
    "is_permanent": True,
    "narration": "Yaovi Test",
    "bvn": "22169541783",
    "txRef": "sample1234"
}
print(rave.VirtualAccount.create(accountDetails))
