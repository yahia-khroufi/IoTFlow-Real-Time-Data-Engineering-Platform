import logging
import os
from logging.handlers import RotatingFileHandler


def logging_config()->None:
    os.mkdirs("logd",exist_ok=True)

    formater=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
    root=logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()

    stream_handlers=logging.StreamHandler()
    stream_handlers.setFormatter("formater")

    app_logs=RotatingFileHandler(
        "logs/consumer.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    root.addHandler(stream_handlers)
    root.addHandler(app_logs)