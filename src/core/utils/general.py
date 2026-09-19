import logging
import traceback

from ..config import separator

logger = logging.getLogger(__name__)

def exception_handler(e: BaseException) -> None:
    logger.exception(separator)
    logger.exception(f"An unhandled exception \"{e}\" occurred. The program will now terminate.")
    traceback.print_exc()
    logger.info(separator)