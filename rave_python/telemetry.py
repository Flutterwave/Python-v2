"""Telemetry module for sending SDK usage events to the SigNoz ingestion service."""
# ruff: noqa: ERA001

import os
import threading
import time
from typing import Any

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError, RequestException, Timeout

INGESTION_URL = "https://signozservice-prod.f4b-flutterwave.com/events"
API_KEY = os.environ.get("SIGNOZ_API_KEY", "IuUnO5cwI6Ta1JO/LEFUsMyz1AH3FNzW")

# logger = logging.getLogger("rave_python.telemetry")

_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}


class TelemetryBase:
    """Fire-and-forget HTTP client for sending telemetry events."""

    def __init__(self, endpoint: str = INGESTION_URL) -> None:  # noqa: D107
        self.endpoint = endpoint

    def _construct(self, name: str, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": name,
            "data": data,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        }

    def emit(self, name: str, data: dict[str, Any]) -> None:
        """Dispatch an event to the ingestion service on a daemon thread."""
        payload = self._construct(name, data)
        thread = threading.Thread(target=self._post, args=(payload,), daemon=True)
        thread.start()

    def post_sync(self, name: str, data: dict[str, Any]) -> dict[str, Any]:
        """POST an event synchronously and return the parsed response body.

        Used when the caller needs the response value — e.g. resolving app_id
        from the app.created event. Returns an empty dict on any failure so
        callers can treat a missing key as a non-fatal miss.
        """
        payload = self._construct(name, data)
        # event_name = payload.get("name", "unknown")
        # logger.debug(
        #     "[telemetry] sending %s | payload: %s",
        #     event_name,
        #     payload,  # ← add this line
        # )
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=_HEADERS,
                timeout=5,
            )
            response.raise_for_status()
        except HTTPError:
            # logger.warning(
            #     "[telemetry] HTTP error sending %s | status: %s | response: %s",
            #     event_name,
            #     e.response.status_code if e.response is not None else "unknown",
            #     e.response.text if e.response is not None else "",
            # )
            pass
        except Timeout:
            # logger.warning(
            #     "[telemetry] timeout sending %s",
            #     event_name,
            # )
            pass
        except RequestsConnectionError:
            # logger.warning(
            #     "[telemetry] connection error sending %s | reason: %s",
            #     event_name,
            #     str(e),
            # )
            pass
        except RequestException:
            # logger.warning(
            #     "[telemetry] unexpected error sending %s | error: %s",
            #     event_name,
            #     str(e),
            # )
            pass
        else:
            data = response.json()
            # logger.debug(
            #     "[telemetry] event sent: %s | status: %s | response: %s",
            #     event_name,
            #     response.status_code,
            #     data,
            # )
            return data  # type: ignore[return-value]  # noqa: RET504
        return {}

    def _post(self, payload: dict[str, Any]) -> None:
        # event_name = payload.get("name", "unknown")
        # logger.debug(
        #     "[telemetry] sending %s | payload: %s",
        #     event_name,
        #     payload,
        # )
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=_HEADERS,
                timeout=5,
            )
            response.raise_for_status()
            # logger.debug(
            #     "[telemetry] event sent: %s | status: %s | response: %s",
            #     event_name,
            #     response.status_code,
            #     response.text,
            # )
        except HTTPError:
            # logger.warning(
            #     "[telemetry] HTTP error sending %s | status: %s | response: %s",
            #     event_name,
            #     e.response.status_code if e.response is not None else "unknown",
            #     e.response.text if e.response is not None else "",
            # )
            pass
        except Timeout:
            # logger.warning(
            #     "[telemetry] timeout sending %s",
            #     event_name,
            # )
            pass
        except RequestsConnectionError:
            # logger.warning(
            #     "[telemetry] connection error sending %s | reason: %s",
            #     event_name,
            #     str(e),
            # )
            pass
        except RequestException:
            # logger.warning(
            #     "[telemetry] unexpected error sending %s | error: %s",
            #     event_name,
            #     str(e),
            # )
            pass


telemetry = TelemetryBase()
