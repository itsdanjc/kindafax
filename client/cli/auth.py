from client.pipe import DiscordAPI, DISCORD_HOST
from client.pipe.auth import AuthServer
from common.log import get_set_logger
from common.config import Config
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import BadRequest
import sys
import logging
import webbrowser

logger = get_set_logger("client")
api = DiscordAPI(DISCORD_HOST, 11)

# Disable log used by werkzeug
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.disabled = True

DISCORD_CLIENT_ID = "1483875791329693767"
HTML_TEMPLATE = (
    "<html>"
    "<body>"
    "{body} You may now close this window."
    "</body>"
    "</html>"
)

def callback(request: Request) -> Response:
    if not request.args:
        return Response(status=400)

    state = request.args.get("state", "")
    args = request.args.to_dict(False)

    if not (state and state == api.auth.get_set_state("base_authentication")):
        raise BadRequest("Could not login, please try again later.")

    if "error" in args:
        raise BadRequest(
            ", ".join(args.get("error_description", []))
        )

    code = request.args.get("code")

    logger.debug(code)

    message = HTML_TEMPLATE.format(
        body="Successfully logged in with Discord."
    )
    return Response(message, mimetype="text/html")


def auth(config: Config) -> None:
    client_id: str

    try:
        client_id = config.get("CLIENT_ID", ensure_type=str, default=DISCORD_CLIENT_ID)

    except KeyError as err:
        logger.error(err)
        raise SystemExit(1)

    except TypeError as err:
        logger.error(err)
        raise SystemExit(1)

    with AuthServer(callback, "/", ["GET"]) as server:
        auth_url = api.auth.get_base_authentication(
            client_id, f"http://{server.host}:{server.port}{server.path}"
        )

        logger.debug(f"Starting http server on port %d", server.port)
        server.start()


        logger.info("Attempting to open %s...", auth_url.join())

        browser = webbrowser.get()
        if not browser.open_new(auth_url.join()):
            logger.error("Could not open browser", auth_url.join())
            sys.exit(1)

        logger.info(f"Server waiting for response")
        server.block_until_request()
