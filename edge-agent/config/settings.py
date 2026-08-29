import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    device_id: str
    collection_interval_seconds: int
    nifi_base_url: str
    nifi_ingest_path: str
    nifi_timeout_seconds: int
    nifi_verify_ssl: bool
    max_retries: int
    retry_backoff_seconds: float


def load_settings() -> Settings:
    device_id = os.getenv("DEVICE_ID")
    if not device_id:
        raise ValueError("Missing required env var: DEVICE_ID")

    nifi_base_url = os.getenv("NIFI_BASE_URL")
    if not nifi_base_url:
        raise ValueError("Missing required env var: NIFI_BASE_URL")

    return Settings(
        device_id=device_id,
        collection_interval_seconds=int(os.getenv("COLLECTION_INTERVAL_SECONDS", "5")),
        nifi_base_url=nifi_base_url.rstrip("/"),
        nifi_ingest_path=os.getenv("NIFI_INGEST_PATH", "/metrics"),
        nifi_timeout_seconds=int(os.getenv("NIFI_TIMEOUT_SECONDS", "5")),
        nifi_verify_ssl=_as_bool(os.getenv("NIFI_VERIFY_SSL", "false"), default=False),
        max_retries=int(os.getenv("EDGE_MAX_RETRIES", "3")),
        retry_backoff_seconds=float(os.getenv("EDGE_RETRY_BACKOFF_SECONDS", "1.5")),
    )

