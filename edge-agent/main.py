import logging
import time

from collectors.system_collectors import SystemCollector
from config.logging_config import configure_logging
from config.settings import load_settings
from services.metric_service import MetricService
from services.nifi_client import NifiClient

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    settings = load_settings()

    collector = SystemCollector(settings.device_id)
    nifi_client = NifiClient(
        base_url=settings.nifi_base_url,
        ingest_path=settings.nifi_ingest_path,
        timeout_seconds=settings.nifi_timeout_seconds,
        verify_ssl=settings.nifi_verify_ssl,
        max_retries=settings.max_retries,
        retry_backoff_seconds=settings.retry_backoff_seconds,
    )
    service = MetricService(collector=collector, nifi_client=nifi_client)

    logger.info("Edge Agent started")

    while True:
        payload = service.collect_and_send()
        logger.info("Payload emitted: %s", payload)
        time.sleep(settings.collection_interval_seconds)


if __name__ == "__main__":
    main()

