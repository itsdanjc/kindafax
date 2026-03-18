from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

@dataclass
class URLType:
    scheme: str
    host: str
    path: str
    args: Optional[dict]
    anchor: Optional[str]

    def join(self):
        args_str: str = ""
        anchor_str: str = ""

        if self.args:
            args_str = f"?{urlencode(self.args)}"

        if self.anchor:
            anchor_str = f"#{self.anchor}"

        return (
            f"{self.scheme}"
            f"{self.host}"
            f"{self.path}"
            f"{args_str}"
            f"{anchor_str}"
        )

    def __str__(self):
        return self.join()
