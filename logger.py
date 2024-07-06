from loguru import logger
import os



def configure_logger() -> None:
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logger.add(
        "logs/logs.log",
        format='{time} - {level} - {message}',
        rotation="10 MB",
        retention="10 days",
        compression="zip"
    )