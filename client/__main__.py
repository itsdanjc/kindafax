import sys
import platform
from typing import Final
from common.config import Config
from common import __version__ as common_version
from .__init__ import __version__
from tomllib import TOMLDecodeError
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

def init_cli() -> ArgumentParser:
    cli = ArgumentParser(prog="kindafax", description=PROG_DESC)
    cli.add_argument("--version", action="store_true", help="display version info, then exit")
    cli.add_argument("-v", "--verbose", action="store_true", help="show more info in logs")

    return cli

def main() -> int:
    arg_parser = init_cli()
    args = arg_parser.parse_args(sys.argv[1::])

    print(VERSION_INFO)

    if args.version:
        print(VERSION_INFO_VERBOSE)
        return 0 # Version info already displayed, just exit.

    if args.verbose:
        print("Verbose mode enabled.")

    while True:
        pass

    # print(VERSION_INFO)
    # config = Config("client")
    # print(config.config_file_path)
    #
    # try:
    #     config.load()
    # except TOMLDecodeError as e:
    #     errs = ", ".join(e.args)
    #     print(f"Config {config.config_file_path} contains the following errors: {errs}")
    #     return 1
    # except ValueError:
    #     print(f"Config at {config.config_file_path} is empty. See the documentation on how to configure.")
    #     return 1
    # return 0

if __name__ == '__main__':
    main()