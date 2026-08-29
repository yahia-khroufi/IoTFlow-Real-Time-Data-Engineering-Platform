from dataclasses import  dataclass, asdict
from datetime import datetime
from datetime import date

@dataclass
class Metric:
    device_id: str
    event_date: date
    event_time: datetime
    cpu_percent: float
    ram_percent: float
    temperature: float
    status: str


    def to_dict(self):
        return asdict(self)

