from platformdirs import PlatformDirs
from pathlib import Path
from typing import Final, Any, Optional, Type
import tomllib

class Config:
    """
    Represents a config file.

    This object should be created for each module that uses it.

    The configuration file is stored in the following locations:
        - **On Windows:**     `C:/ProgramData/kindafax/kindafax-<module>/config.toml`
        - **On Linux:**       `/etc/xdg/kindafax-<module>/config.toml`
        - **On MacOS:**       `/Library/Application Support/kindafax-<module>/config.toml`
        - **On Android**      `/data/data/<pkg>/shared_prefs/kindafax-<module>/config.toml`
    """
    config_file: Final[str] = "config.toml"
    config_file_path: Final[Path]
    __config_dict: dict[str, Any] = dict()

    def __init__(self, module: str):
        self.dirs = PlatformDirs(f"kindafax-{module}", "kindafax")
        self.config_file_path = self.dirs.site_config_path.joinpath(
            self.config_file
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
        exists = self.config_file_path.exists()
        is_file = self.config_file_path.is_file()

        if not (exists and is_file):
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_file_path.touch()
            raise ValueError("Config files cannot be empty.")

        config: dict
        with open(self.config_file_path, "rb") as f:
            config = tomllib.load(f)
        self.set(**config)
