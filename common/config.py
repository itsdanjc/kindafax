from platformdirs import PlatformDirs
from pathlib import Path
from typing import Final, Any, Optional, Type
import tomllib

CONFIG_FILE: Final[str] = "config.toml"
APP_NAME: Final[str] = "kindafax"
APP_AUTHOR: Final[str] = "KindaFax"

class Config:
    """
    Represents a config file.

    This object should be instantiated per module.

    The configuration file is stored in the following locations:
        - **On Windows:**     `C:/ProgramData/KindaFax/kindafax/<module>/config.toml`
        - **On Linux:**       `/etc/xdg/kindafax/<module>/config.toml`
        - **On MacOS:**       `/Library/Application Support/kindafax/<module>/config.toml`
        - **On Android**      `/data/data/<pkg>/shared_prefs/kindafax/<module>/config.toml`

    :ivar location: Path to the config file.
    :ivar dirs: PlatformDirs instance storing common filesystem paths.
    """
    location: Final[Path]
    __config_dict: dict[str, Any] = dict()

    def __init__(self, module: str):
        self.dirs = PlatformDirs(
            APP_NAME,
            APP_AUTHOR,
            module,
            ensure_exists=True
        )

        self.location = self.dirs.site_config_path.joinpath(
            CONFIG_FILE
        )

    def __contains__(self, item) -> bool:
        return item in self.__config_dict

    def __getitem__(self, item) -> Any:
        return self.__config_dict[item]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__config_dict[key] = value

    def set(self, **kwargs) -> None:
        """
        Update the config with the key/value pairs from kwargs,
        overwriting existing keys.

        :raises ValueError: No arguments where given.
        :param kwargs:
        :return: None
        """
        self.__config_dict.update(kwargs)

    def get(
            self, key: str,
            default: Optional[Any] = None,
            ensure_type: Optional[Type] = None
    ) -> Any:
        """
        Get the value with key in the config file.

        :raises KeyError: Key not found.
        :raises TypeError: Invalid value type.
        :param key: Lookup key.
        :param default: Return this value, instead of raising `KeyError`.
        :param ensure_type: Raise an exception if the value is not this type.
        """
        return_value: Any
        return_value: Type[Any]

        if key in self:
            return_value = self[key]
            return_type = type(return_value)

            if ensure_type and return_type != ensure_type:
                raise TypeError(
                    f"Failed type validation for \"{key}\": "
                    f"Expected {ensure_type.__name__}, got {return_type.__name__}."
                )

            return return_value

        if default is not None:
            return default

        raise KeyError(f"Config contains no key \"{key}\"")

    def load(self) -> None:
        """
        Get config from config file.

        Creates empty file when config file does not exist.

        Raises exception if empty config.

        :raises tomllib.TOMLDecodeError: The config file contains errors.
        :raises ValueError: The config file was empty.
        :return:
        """
        exists = self.location.exists()
        is_file = self.location.is_file()

        if not (exists and is_file):
            self.location.touch()
            raise ValueError("Config files cannot be empty.")

        config: dict
        with open(self.location, "rb") as f:
            config = tomllib.load(f)

            if not config:
                raise ValueError("Config files cannot be empty.")

        self.set(**config)
