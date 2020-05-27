import aiodactyl
import aiopes
import aiodathost

import sys

from settings import CONFIG

from aiohttp_session import AIOHTTP


class Server:
    def load(self):
        """ Working out what server provider we are using.

            For safety reason only use identical
            functions what all given wrappers provide.

            Before adding any new functionality, look over
                https://github.com/WardPearce/aiodactyl
                https://github.com/WardPearce/aiopes
                https://github.com/WardPearce/aiodathost
            and see if all those APIs support it.
        """

        if CONFIG.server["pterodactyl"]["enabled"]:
            pterodactyl = aiodactyl.client(
                api_key=CONFIG.server["key"],
                route=CONFIG.server["pterodactyl"]["route"],
                session=AIOHTTP.ClientSession
            )

            return pterodactyl.client

        elif CONFIG.server["pes"]["enabled"]:
            pes = aiopes.client(
                api_key=CONFIG.server["key"],
                session=AIOHTTP.ClientSession
            )

            return pes.server

        elif CONFIG.server["dathost"]["enabled"]:
            if "/" not in CONFIG.server["key"]:
                sys.exit("Dathost key isn't formatted correctly.")

            username, password = CONFIG.server["key"].split("/")

            dathost = aiodathost.client(
                username=username,
                password=password,
                session=AIOHTTP.ClientSession
            )

            return dathost.server
        else:
            sys.exit("No server provider given.")
