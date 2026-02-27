import logging
import sys
from typing import Final, Optional, Union, TypeAlias
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOGGER_NAME_PREFIX: Final[str] = "kindafax"
LOGGER_NAME_SEPARATOR: Final[str] = "."
LOGGER_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
LOGGER_FILE_NAME: Final[str] = f"kindafax.log"

LogHandler: TypeAlias = Union[logging.StreamHandler, TimedRotatingFileHandler]

FORMAT_COLORED: Final[dict[int, str]] = {
    logging.DEBUG:
        "\033[36m%(asctime)s\033[0m  %(message)s",  # Cyan Timestamp. Uncolored Message.
    logging.INFO:
        "\033[36m%(asctime)s\033[0m  %(message)s",  # Same as debug
    logging.WARNING:
        "\033[36m%(asctime)s\033[33m  %(levelname)s: %(message)s\033[0m",  # Yellow Message
    logging.ERROR:
        "\033[36m%(asctime)s\033[31m  %(levelname)s: %(message)s\033[0m",  # Red Message
    logging.CRITICAL:
        "\033[36m%(asctime)s\033[31m  %(levelname)s: %(message)s\033[0m",  # Same as error
}

FORMAT: Final[dict[int, str]] = {
    logging.DEBUG:      "%(asctime)s  %(message)s",
    logging.INFO:       "%(asctime)s  %(message)s",
    logging.WARNING:    "%(asctime)s  %(levelname)s: %(message)s",
    logging.ERROR:      "%(asctime)s  %(levelname)s: %(message)s",
    logging.CRITICAL:   "%(asctime)s  %(levelname)s: %(message)s",
}

class LoggerFormat(logging.Formatter):
    def __init__(self, use_ansi: bool) -> None:
        super().__init__(datefmt=LOGGER_DATE_FORMAT)
        self._formatters: dict[int, logging.Formatter]

        if use_ansi:
            self._formatters = {
                level: logging.Formatter(fmt, LOGGER_DATE_FORMAT)
                for level, fmt in FORMAT_COLORED.items()
            }

        else:
            self._formatters = {
                level: logging.Formatter(fmt, LOGGER_DATE_FORMAT)
                for level, fmt in FORMAT.items()
            }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self._formatters.get(
            record.levelno,
            self._formatters[logging.INFO],
        )
        return formatter.format(record)


def get_set_logger(module: str) -> logging.Logger:
    """
    Return a logger for the given module name, creating it if necessary.
    """

    return logging.getLogger(
        f"{LOGGER_NAME_PREFIX}{LOGGER_NAME_SEPARATOR}{module}"
    )


def get_handlers(out: Optional[Path] = None) -> LogHandler:
    """
    Create a logger handler. Also define a formatter for messages.

    :param out: Optional path to log file. Otherwise, log to `stdout`.
    :return: `RotatingFileHandler` if logging to file, else `StreamHandler`
    """
    handler: LogHandler
    use_ansi: bool

    if out:
        use_ansi = False
        handler = TimedRotatingFileHandler(
            filename = out.joinpath(LOGGER_FILE_NAME),
            when = "midnight",
            backupCount = 5,
            encoding = "utf-8",
            utc = False,
        )
        handler.namer = lambda n: "{}{}".format(
            n.replace(".log", ""), ".log"
        )
    else:
        use_ansi = True
        handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(
        LoggerFormat(use_ansi)
    )
    return handler


def get_level(make_verbose: bool) -> int:
    """
    To keep consistent between modules,
    use this function to determine the logging level.

    :returns: `logging.DEBUG` if in verbose mode, else `logging.INFO`
    """

    if make_verbose:
        return logging.DEBUG
    return logging.INFO
