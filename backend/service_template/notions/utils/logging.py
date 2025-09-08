import logging

from notions.config.settings import settings


def configure_logging() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

