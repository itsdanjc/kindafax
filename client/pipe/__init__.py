from http.client import HTTPSConnection
# from client.__main__ import __version__
from client.pipe.auth import AuthAPI
import json

DISCORD_HOST = "discord.com"
USER_AGENT = f"KindaFax Client (https://github.com/itsdanjc/kindafax, 0.0.0)"
HEADERS = {'User-Agent': USER_AGENT}


class DiscordAPI:
    user_agent: str = USER_AGENT

    def __init__(self, host: str, api_version: int):
        self.host = host
        self.url_prefix = f"/api/v{api_version}"
        self.api = HTTPSConnection(self.host)
        self.headers = HEADERS
        self.auth = AuthAPI(self.api, self.headers)

    def ping(self) -> dict:
        self.api.request("GET", self.url_prefix)
        req = self.api.getresponse()
        return json.loads(req.read())
