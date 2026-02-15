# from http.client import HTTPSConnection
# import json
#
# DISCORD_HOST = "discord.com"
# USER_AGENT = "KindaFax Client (https://github.com/itsdanjc/kindafax, 0.0.0)"
# HEADERS = {'User-Agent': USER_AGENT}
#
#
# class DiscordAPI:
#     host: str = DISCORD_HOST
#     user_agent: str = USER_AGENT
#     url_prefix: str = "/api/v11"
#
#     def __init__(self):
#         self.api = HTTPSConnection(self.host)
#
#     def ping(self) -> dict:
#         self.api.request("GET", self.url_prefix)
#         req = self.api.getresponse()
#         return json.loads(req.read())
#
#
#
#
#     @property
#     def headers(self):
#         return HEADERS.copy()
#
#
# if __name__ == '__main__':
#     conn = DiscordAPI()
#
