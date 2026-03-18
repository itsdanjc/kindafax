from typing import Final, List, Optional, Callable
from http.client import HTTPSConnection
from werkzeug.wrappers import Request, Response
from werkzeug.serving import make_server, BaseWSGIServer
from client.pipe.types import URLType
import threading
import secrets
import time

AUTH_SCOPES: Final[List[str]] = ["email"] # ["dm_channels.messages.read"]

class AuthAPI:
    def __init__(self, connection: HTTPSConnection, headers: dict):
        self.__state: str
        self.api = connection
        self.url_prefix = "/oauth2"
        self.headers = headers

    def get_set_state(self, func_name: str, recreate: Optional[bool] = False) -> str:
        if hasattr(self, f"__state_{func_name}") and not recreate:
            return getattr(self, f"__state_{func_name}")

        state = secrets.token_urlsafe(16)
        setattr(self, f"__state_{func_name}", state)
        return state

    def get_base_authentication(self, client_id: str, redirect_url: str) -> URLType:
        url_path: str = f"{self.url_prefix}/authorize"
        state = self.get_set_state("base_authentication")
        scopes = " ".join(AUTH_SCOPES)

        url_args = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_url,
            "scope": scopes,
            "state": state,
        }

        return URLType(
            scheme="https://",
            host=self.api.host,
            path=url_path,
            args=url_args,
            anchor=None
        )


class AuthServer:
    """

    """
    host: Final[str] = "127.0.0.1"
    port: Final[int] = 8000
    ok_to_exit: bool = False
    __server: BaseWSGIServer
    __thread: threading.Thread

    def __init__(
            self,
            callback: Callable[[Request], Response],
            path: str,
            allowed_methods: List[str],
    ):
        self.callback_func = callback
        self.path = path
        self.allowed_methods = allowed_methods

    @Request.application
    def callback(self, request: Request) -> Response:
        if request.method not in self.allowed_methods:
            return Response(status=405)

        if request.path != self.path:
            return Response(status=404)

        response = self.callback_func(request)
        self.ok_to_exit = True

        return response

    def __enter__(self):
        self.__server = make_server(
            self.host,
            self.port,
            self.callback
        )
        self.__thread = threading.Thread(
            target=self.__server.serve_forever
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ok_to_exit = True
        self.block_until_request()

    def start(self) -> None:
        self.__thread.start()

    def block_until_request(self) -> None:
        while not self.ok_to_exit:
            time.sleep(1)

        self.__server.shutdown()
        self.__thread.join()