import os

import pytest  # type:ignore
from dotenv import load_dotenv

from rave_python.rave_payment import Payment

load_dotenv()


@pytest.fixture(scope="session")  # type:ignore
def public_key() -> str:
    key = os.getenv("PUBLIC_KEY")
    assert key is not None, "Missing PUBLIC_KEY"
    return key


@pytest.fixture(scope="session")  # type:ignore
def secret_key() -> str:
    key = os.getenv("SECRET_KEY")
    assert key is not None, "Missing SECRET_KEY"
    return key


@pytest.fixture  # type:ignore
def payment_client(public_key: str, secret_key: str) -> Payment:
    return Payment(
        publicKey=public_key,
        secretKey=secret_key,
        production=False,
        usingEnv=True,
    )
