import logging
import sys
import platform
from pathlib import Path
from typing import Final, Optional
from common.config import Config
from common.log import get_set_logger, get_handlers, get_level
from common import __version__ as common_version
from tomllib import TOMLDecodeError
from .__init__ import __version__
from argparse import ArgumentParser


PROG_NAME: Final[str] = f"KindaFax Client"
PROG_DESC: Final[str] = f"The client for KindaFax, A fax-like messaging system, using receipt printers."
VERSION_INFO: Final[str] = f"{PROG_NAME} {__version__}"
VERSION_INFO_VERBOSE: Final[str] = (
    "   {common_label}{common_version}\n"
    "   {py_label}{python} ({python_implementation})\n"
    "   {os_label}{os} {os_release} (Build {os_build})"
).format(
    common_label="Common".ljust(10),
    py_label="Python".ljust(10),
    os_label="OS".ljust(10),
    common_version=common_version,
    python=platform.python_version(),
    python_implementation=platform.python_implementation(),
    os=platform.system(),
    os_release=platform.release(),
    os_build=platform.version(),
)

logger: logging.Logger #Define here so we can use in methods

def init_cli() -> ArgumentParser:
    cli = ArgumentParser(prog="kindafax", description=PROG_DESC)
    cli.add_argument("--version", action="store_true", help="display version info, then exit")
    cli.add_argument("-v", "--verbose", action="store_true", help="show more info in logs")
    cli.add_argument("-l", "--log-file", action="store_true", help="log to a file, instead of stdout")

    return cli

def init_log(verbose: bool, file: Optional[Path]) -> None:
    global logger

    logger = get_set_logger("client")
    logger.addHandler( get_handlers(file) )
    logger.setLevel( get_level(verbose) )

def init_config() -> Config:
    config = Config("client")

    try:
        config.load()
    except TOMLDecodeError as e:
        logger.error(
            "%s in %s",
            "".join(e.args),
            config.location
        )

    except ValueError as e:
        logger.error(
            "Config file is empty, see %s",
            "https://kindafax.itsdanjc.com/docs/client/configuration.html"
        )

    return config

def main() -> int:
    arg_parser = init_cli()
    args = arg_parser.parse_args(sys.argv[1::])

    if args.version:
        print(
            f"\n{VERSION_INFO}\n{VERSION_INFO_VERBOSE}\n",
            file=sys.stdout
        )
        return 0 # Version info already displayed, just exit.

    print(f"\n{VERSION_INFO}\n\n", file=sys.stdout, end="")

    # Configure Log
    log_file: Optional[Path] = None

    if args.log_file:
        # log_file = config.dirs.site_log_path
        print(f"Log at {log_file}", file=sys.stdout)

    init_log(args.verbose, log_file)


    # Get Config
    config = init_config()

    input("\nPress any key to exit") # No event loop yet. Just exit after input.
    return 0

if __name__ == '__main__':
    main()