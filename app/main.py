import logging

from app.config import APP_NAME, LOG_LEVEL, MY_API_KEY


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("%s started.", APP_NAME)

    if MY_API_KEY:
        logger.info("API key loaded successfully.")
    else:
        logger.warning("API key not found.")


if __name__ == "__main__":
    main()