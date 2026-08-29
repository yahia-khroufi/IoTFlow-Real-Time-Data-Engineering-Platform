import logging
import random
from datetime import datetime, timezone
from models.metric import Metric
import psutil

logger = logging.getLogger(__name__)


class SystemCollector:
    def __init__(self, device_id: str) -> None:
        self._device_id = device_id

    def collect(self) -> Metric:
        now = datetime.now(timezone.utc)
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent
        temperature = round(random.uniform(35.0, 70.0), 1)
        status = "WARNING" if cpu_percent > 90 or temperature > 65 else "OK"

        metric = Metric (
            device_id= self._device_id,
            event_date= now.date().isoformat(),
            event_time= now.isoformat(),
            cpu_percent= cpu_percent,
            ram_percent= ram_percent,
            temperature= temperature,
            status= status,) 
                
        logger.info("Collected metric for device_id=%s", self._device_id)
        return metric






