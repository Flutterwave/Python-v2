# ruff: noqa: ERA001
"""Identity resolution for the Flutterwave SDK."""

import json
import logging
import os
import re
from pathlib import Path
from threading import Lock

import requests

from rave_python import __version__
from rave_python.telemetry import telemetry

logger = logging.getLogger("rave_python.identity")


class AppIdentityClient:
    """Read-only identity resolver.

    Resolution order:
    1. In-memory cache (_app_id already set on this singleton instance)
    2. Disk cache (FLW_SDK_STATE_PATH, default /tmp/flw_sdk.json)
    3. Flutterwave mercinfo endpoint
    4. Telemetry ingestion service (app.created) — fallback if mercinfo fails

    Does NOT register or mutate identity beyond caching the resolved app_id.
    """

    _instance: "AppIdentityClient | None" = None
    _lock = Lock()

    MERCINFO_ENDPOINT = "https://api.ravepay.co/flwv3-pug/getpaidx/api/mercinfo"

    def __new__(cls, public_key: str):  # noqa: ANN204, ARG004
        """Return the singleton instance, creating it if necessary."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance  # type: ignore[return-value]

    def __init__(self, public_key: str) -> None:  # noqa: D107
        if hasattr(self, "_initialized"):
            return

        self.public_key = public_key
        self.storage_path = Path(os.getenv("FLW_SDK_STATE_PATH", "/tmp/flw_sdk.json"))  # noqa: S108
        self._app_id: str | None = None
        self._initialized = True

    def get_app_id(self) -> str:
        """Return the resolved app_id, fetching and caching it if not yet known."""
        if self._app_id:
            return self._app_id

        self._app_id = self._load_or_fetch()
        return self._app_id

    def _sanitise_app_id(self, value: str) -> str:
        """Convert a raw identifier to a safe slug for the ingestion service."""
        slugified = value.strip().replace(" ", "_")
        return re.sub(r"[^a-zA-Z0-9_\-]", "_", slugified).strip("_")

    def _load_or_fetch(self) -> str:
        cached = self._read_from_disk()
        if cached:
            # logger.debug("[identity] app_id loaded from disk cache")
            self._app_id = cached
            return cached

        app_id = self._resolve_app_id()
        self._write_to_disk(app_id)
        return app_id

    def _resolve_app_id(self) -> str:
        """Try mercinfo first; fall back to the telemetry app.created endpoint."""
        try:
            app_id = self._fetch_from_mercinfo()
        except Exception as e:  # noqa: BLE001
            logger.warning(
                "[identity] mercinfo failed (%s), falling back to telemetry endpoint",
                str(e),
            )
        else:
            # logger.debug("[identity] app_id resolved from mercinfo")
            return app_id

        return self._fetch_from_telemetry()

    def _fetch_from_mercinfo(self) -> str:
        """Fetch app_id from the Rave mercinfo endpoint using the public key."""
        response = requests.get(
            self.MERCINFO_ENDPOINT,
            params={"PBFPubKey": self.public_key},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        app_id = data.get("mn")
        if not app_id:
            msg = "app_id not found in mercinfo response"
            raise ValueError(msg)

        return self._sanitise_app_id(str(app_id))

    def _fetch_from_telemetry(self) -> str:
        """Register the integration via app.created and return the app_id.

        This is the fallback path when mercinfo is unavailable. The telemetry
        endpoint returns an app_id in the response body which is used as the
        integration identifier for all subsequent telemetry events.
        """
        # logger.debug(
        #     "[identity] sending app.created to telemetry endpoint for public_key: %s",
        #     self.public_key[:20] + "...",
        # )

        response = telemetry.post_sync(
            "app.created",
            {
                "client_id": None,
                "public_key": self.public_key,
                "library": "python",
                "library_version": __version__,
            },
        )

        app_id = response.get("app_id")
        if not app_id:
            msg = (
                "app_id not returned from telemetry endpoint. "
                "Check SIGNOZ_API_KEY and ingestion service availability."
            )
            raise RuntimeError(msg)

        # logger.debug("[identity] app_id resolved from telemetry endpoint: %s", app_id)
        return self._sanitise_app_id(str(app_id))

    def _read_from_disk(self) -> str | None:
        if not self.storage_path.exists():
            return None

        try:
            with self.storage_path.open() as f:
                return json.load(f).get("app_id")
        except Exception:  # noqa: BLE001
            return None

    def _write_to_disk(self, app_id: str) -> None:
        try:
            with self.storage_path.open("w") as f:
                json.dump({"app_id": app_id}, f)
        except Exception as e:  # noqa: BLE001
            logger.warning("[identity] failed to write app_id to disk: %s", str(e))
