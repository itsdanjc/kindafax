import sys
from common.config import Config

def main():
    print("KindaFax Client")
    config = Config("client")

    try:
        config.load()
    except FileNotFoundError:
        print("Config file not found")
        return 1


    print(config.dirs.site_log_dir)
    return 0

if __name__ == '__main__':
    sys.exit(main())