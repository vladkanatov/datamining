from loguru import logger
import sys
def configure_logger() -> None:
    logger.remove()
    logger.add(sink='logs/logs.log',
               format="{time} {level} {message}",
               level='INFO',
               retention="10 days",
               rotation="10 MB")
    
    logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")

    logger.info("Logger configured")