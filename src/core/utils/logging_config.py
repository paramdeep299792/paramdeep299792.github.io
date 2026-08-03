import logging
from logging import FileHandler, LogRecord
from typing import Optional
from zoneinfo import ZoneInfo
from datetime import datetime
from pathlib import Path
from typing import Union

class TimeZoneFormatter(logging.Formatter):
    """
    A logging formatter that converts log record timestamps to a specific timezone.

    This class overrides the default `formatTime` method to ensure all log
    timestamps are consistently displayed in the 'Asia/Kolkata' timezone,
    regardless of the server's local time settings.
    """
    def formatTime(self, record: LogRecord, datefmt: Optional[str] = None) -> str:
        """
        Formats the log record's creation time in the 'Asia/Kolkata' timezone.

        Args:
            record: The log record to be formatted.
            datefmt: The format string for the date/time. If None, a default
                     format is used.

        Returns:
            The formatted time string.
        """
        dt = datetime.fromtimestamp(record.created, tz=ZoneInfo('Asia/Kolkata'))
        if datefmt:
            return dt.strftime(datefmt)
        return super().formatTime(record, datefmt)
                                      
def setup_logging(log_file: Union[str, Path], reset_log: bool = False) -> None:
    """
    Configures the root logger for the application.

    This function sets up a root logger with two handlers:
    1. A FileHandler that writes logs to the specified `log_file`.
    2. A StreamHandler that prints logs to the console.

    Both handlers use the `TimeZoneFormatter` to ensure timestamps are displayed
    in the target timezone (e.g., 'Asia/Kolkata' IST) with a GMT offset.

    Args:
        log_file (Union[str, Path]): The destination path for the log file.
        reset_log (bool, optional): If True, overwrites the existing log file (mode 'w'). 
            If False, appends to the existing file (mode 'a'). Defaults to False.

    Returns:
        None
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.INFO)
    log_message_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_time_format = '%Y-%m-%d %H:%M:%S (GMT%z)'
    formatter = TimeZoneFormatter(
        fmt=log_message_format,
        datefmt=date_time_format
    )
    file_mode = 'w' if reset_log else 'a'
    file_handler = FileHandler(log_file, mode=file_mode)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)