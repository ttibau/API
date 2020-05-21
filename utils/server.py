import aiodactyl
import aiopes
import aiodathost

import sys

from settings import Config

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

        if Config.server["pterodactyl"]["enabled"]:
            pterodactyl = aiodactyl.client(
                api_key=Config.server["key"],
                route=Config.server["pterodactyl"]["route"],
                session=AIOHTTP.ClientSession
            )

            return pterodactyl.client

        elif Config.server["pes"]["enabled"]:
            pes = aiopes.client(
                api_key=Config.server["key"],
                session=AIOHTTP.ClientSession
            )

            return pes.server

        elif Config.server["dathost"]["enabled"]:
            if "/" not in Config.server["key"]:
                sys.exit("Dathost key isn't formatted correctly.")

            username, password = Config.server["key"].split("/")

            dathost = aiodathost.client(
                username=username,
                password=password,
                session=AIOHTTP.ClientSession
            )

            return dathost.server
        else:
            sys.exit("No server provider given.")
