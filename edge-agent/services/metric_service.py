import logging
from models.metric import Metric

logger = logging.getLogger(__name__)


class MetricService:
    def __init__(self, collector, nifi_client) -> None:
        self._collector = collector
        self._nifi_client = nifi_client

    def collect_and_send(self) -> dict:
        metric = self._collector.collect()

        if not self._validate(metric):
            logger.error("Collected metric is invalid: %s", metric)
            raise ValueError("Invalid metric")
        dict_metric=metric.to_dict()
        self._nifi_client.post_metric(dict_metric)
        logger.info("metric sent for device_id=%s", metric.device_id)
        return metric
   

    def _validate( self,metric: Metric) -> bool:
     return (
        bool(metric.device_id)
        and 0 <= metric.cpu_percent <= 100
        and 0 <= metric.ram_percent <= 100
        )


    