from datetime import date, datetime


REQUIRED_FIELDS = {
    "device_id",
    "event_date",
    "event_time",
    "cpu_percent",
    "ram_percent",
    "temperature",
    "status",
}


class MetricContract:
    @staticmethod
    def validate(payload: dict) -> tuple[bool, str | None]:
        missing = [field for field in REQUIRED_FIELDS if field not in payload]
        if missing:
            return False, f"missing_fields:{','.join(sorted(missing))}"

        if not payload.get("device_id"):
            return False, "device_id_empty"

        cpu_percent = payload.get("cpu_percent")
        ram_percent = payload.get("ram_percent")

        if not isinstance(cpu_percent, (int, float)):
            return False, "cpu_not_numeric"
        if not isinstance(ram_percent, (int, float)):
            return False, "ram_not_numeric"

        if not (0 <= cpu_percent <= 100):
            return False, "cpu_out_of_range"
        if not (0 <= ram_percent <= 100):
            return False, "ram_out_of_range"

        try:
            MetricContract.parse_event_date(payload["event_date"])
        except ValueError:
            return False, "event_date_invalid"

        try:
            MetricContract.parse_event_time(payload["event_time"])
        except ValueError:
            return False, "event_time_invalid"

        return True, None

    @staticmethod
    def parse_event_date(value: str | date) -> date:
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        return date.fromisoformat(str(value))

    @staticmethod
    def parse_event_time(value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))

    