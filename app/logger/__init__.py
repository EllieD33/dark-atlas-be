from .config import configure_logging
import logging

configure_logging()

def get_logger(name: str):
    return logging.getLogger(name)