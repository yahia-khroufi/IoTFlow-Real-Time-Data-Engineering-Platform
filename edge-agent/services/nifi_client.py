import logging
import time

import requests

logger = logging.getLogger(__name__)


class NifiClient:
    def __init__(
        self,
        base_url: str,
        ingest_path: str,
        timeout_seconds: int,
        verify_ssl: bool,
        max_retries: int,
        retry_backoff_seconds: float,
    ) -> None:
        self._url = f"{base_url}{ingest_path}"
        self._timeout_seconds = timeout_seconds
        self._verify_ssl = verify_ssl
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds

    def post_metric(self, payload: dict) -> None:
        headers = {"Content-Type": "application/json"}
        last_error = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = requests.post(
                    self._url,
                    json=payload,
                    headers=headers,
                    timeout=self._timeout_seconds,
                    verify=self._verify_ssl,
                  )
        
                if 200 <= response.status_code < 300:
                    logger.info("Metric posted to NiFi successfully")
                    return
                response.raise_for_status()

            except requests.RequestException as err:
                last_error = err
                logger.warning(
                    "NiFi POST attempt %s/%s failed: %s",
                    attempt,
                    self._max_retries,
                    err,
                )
                if attempt < self._max_retries:
                    time.sleep(self._retry_backoff_seconds * attempt)

        raise RuntimeError(f"Failed to POST metric to NiFi after retries: {last_error}")