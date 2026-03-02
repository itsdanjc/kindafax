import logging
import sys
import platform
import time
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

#Define here so we can use in methods
logger: logging.Logger
config: Config
args:  ArgumentParser


def run() -> int:
    try:
        match args.command:     #type: ignore
            case "auth":
                pass

            case _:
                sys.exit(0)

    except KeyboardInterrupt:
        logger.debug("Exiting (Received signal from user)")
        return 0

    except SystemExit as e:
        logger.debug("Exiting")
        return e.code

    except Exception as e:
        #Ensure any unhandled exceptions are logged.
        logger.exception(
            "Unhandled %s(\"%s\")",
            e.__class__.__name__,
            "\", \"".join(e.args),
            exc_info=e
        )

        if args.log: #type: ignore
            print(
                f"\nUnhandled {e.__class__.__name__}:",
                ", ".join(e.args),
                "(See log for details)",
                file=sys.stderr
            )

        logger.debug("Exiting (Unhandled Exception)")
        return 1

    logger.debug("Exiting")
    return 0


def init_cli() -> ArgumentParser:
    """
    Initialize the CLI
    """

    cli = ArgumentParser(prog="kindafax", description=PROG_DESC)
    add_cli_commands(cli)

    cli.add_argument(
        "--version", action="store_true",
        help="display version info, then exit"
    )

    log_opts = cli.add_argument_group("options for logging")
    log_opts.add_argument(
        "-v", "--verbose", action="store_true",
        help="show more information in logs"
    )
    log_opts.add_argument(
        "--log", action="store_true",
        help="log to file, instead of stdout (useful when running headless)"
    )
    log_opts.add_argument(
        "--no-ansi", action="store_true",
        help="remove all styling in log (default when \"--log\" is enabled)"
    )

    return cli


def add_cli_commands(parser: ArgumentParser) -> None:
    """
    Add commands to CLI
    :param parser:
    """

    cmds = parser.add_subparsers(dest="command", required=False)

    cmds.add_parser("auth")


def init_log(verbose: bool, file: Optional[Path]) -> None:
    """
    Initialize the logger.
    :param verbose: Whether to enable verbose logging
    :param file: Optional path to log file directory
    """
    global logger

    logger = get_set_logger("client")

    logger.addHandler(
        get_handlers(file, not args.no_ansi) #type: ignore
    )

    logger.setLevel(
        get_level(verbose)
    )


def init_config() -> None:
    """
    Wrapper for ``config.load()``.
    :return:
    """
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


def main() -> int:
    """
    Entrypoint for KindaFax client
    :return: Exit code
    """
    global args
    arg_parser = init_cli()
    args = arg_parser.parse_args(sys.argv[1::])

    if args.version:
        print(
            f"\n{VERSION_INFO}\n{VERSION_INFO_VERBOSE}\n",
            file=sys.stdout
        )
        return 0  # Version info already displayed, just exit.

    print(f"\n{VERSION_INFO}\n\n", file=sys.stdout, end="")

    global config
    config = Config("client")

    # Configure Log
    log_file: Optional[Path] = None

    if args.log:
        log_file = config.dirs.site_log_path
        print(f"Log at {log_file}", file=sys.stdout)

    init_log(args.verbose, log_file)

    # Get Config
    init_config()

    return run()

if __name__ == '__main__':
    main()
