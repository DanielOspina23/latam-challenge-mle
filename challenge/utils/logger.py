import logging

from google.cloud import logging_v2 as cloud_logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler


def get_logger():
    client = cloud_logging.Client()
    handler = CloudLoggingHandler(client)

    logger = logging.getLogger("flight-delay")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
