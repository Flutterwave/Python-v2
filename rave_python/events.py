# ruff: noqa: D100, D101
from decimal import Decimal
from enum import Enum
from typing import TypedDict


class Env(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


class AppCreatedEvent(TypedDict):
    app_id: str
    client_id: str | None
    public_key: str | None
    library: str
    library_version: str


class RequestSentEvent(TypedDict):
    app_id: str
    environment: str
    api_version: str
    library_version: str
    method: str
    reference: str
    path: str


class AppTransactionEvent(TypedDict):
    app_id: str
    reference: str
    currency: str
    amount: Decimal
    fee: Decimal
    method: str


class AppErrorEvent(TypedDict):
    app_id: str
    library: str
    library_version: str
    environment: str
    error_code: str | None
    error_message: str
