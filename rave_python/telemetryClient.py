# ruff: noqa: N999, D100, D101, D102, D107, ANN204
import threading
from decimal import Decimal
from typing import Any, ClassVar, cast
from urllib.parse import urlparse

from rave_python import __version__
from rave_python.events import (
    AppCreatedEvent,
    AppErrorEvent,
    AppTransactionEvent,
    Env,
    RequestSentEvent,
)
from rave_python.telemetry import telemetry


class TelemetryClient:
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _registered: ClassVar[bool] = False
    _logged_transactions: ClassVar[set[str]] = set()

    def __init__(self, app_id: str, environment: Env):
        self._app_id = app_id
        self._environment = environment

    def register_app(self, public_key: str) -> None:
        with self._lock:  # guard against race on first call
            if self._registered:
                return
            TelemetryClient._registered = True  # write to class, not instance

        event: AppCreatedEvent = {
            "app_id": self._app_id,
            "client_id": None,
            "public_key": public_key,
            "library": "python",
            "library_version": __version__,
        }

        telemetry.emit("app.created", cast("dict[str, Any]", event))

    def request_sent(
        self,
        url: str,
        method: str,
        reference: str,
        api_version: str,
        library_version: str = __version__,
    ) -> None:
        path = urlparse(url).path

        event: RequestSentEvent = {
            "app_id": self._app_id,
            "environment": self._environment.value,
            "api_version": api_version,
            "library_version": library_version,
            "method": method,
            "reference": reference,
            "path": path,
        }
        telemetry.emit("request.sent", cast("dict[str, Any]", event))

    def transaction(
        self,
        reference: str,
        currency: str,
        amount: Decimal,
        fee: Decimal,
        method: str,
    ) -> None:
        # Only fire in production
        if self._environment != Env.PRODUCTION:
            return

        if not reference or reference in self._logged_transactions:
            return

        event: AppTransactionEvent = {
            "app_id": self._app_id,
            "reference": reference,
            "currency": currency,
            "amount": amount,
            "fee": fee,
            "method": method,
        }

        self._logged_transactions.add(reference)
        telemetry.emit("app.transaction", cast("dict[str, Any]", event))

    def error(self, message: str, code: str | None = None) -> None:
        event: AppErrorEvent = {
            "app_id": self._app_id,
            "library": "python",
            "library_version": __version__,
            "environment": self._environment.value,
            "error_code": code,
            "error_message": message,
        }

        telemetry.emit("app.error", cast("dict[str, Any]", event))
