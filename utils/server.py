import aiodactyl
import aiopes
import aiodathost

import sys

from settings import Config as config


class Server:
    def __init__(self, obj):
        """ Working out what server provider we are using.

            For safetly reason only use identical
            functions what all given wrappers provide.

            Before adding any new functionality, look over
                https://github.com/WardPearce/aiodactyl
                https://github.com/WardPearce/aiopes
                https://github.com/WardPearce/aiodathost
            and see if all those APIs support it.
        """

        if config.server["pterodactyl"]["enabled"]:
            pterodactyl = aiodactyl.client(
                api_key=config.server["key"],
                route=config.server["pterodactyl"]["route"],
                session=obj.sessions.aiohttp
            )

            obj.server = pterodactyl.client

        elif config.server["pes"]["enabled"]:
            pes = aiopes.client(
                api_key=config.server["key"],
                session=obj.sessions.aiohttp
            )

            obj.server = pes.server

        elif config.server["dathost"]["enabled"]:
            if "/" not in config.server["key"]:
                sys.exit("Dathost key isn't formatted correctly.")

            username, password = config.server["key"].split("/")

            dathost = aiodathost.client(
                username=username,
                password=password,
                session=obj.sessions.aiohttp
            )

            obj.server = dathost.server
        else:
            sys.exit("No server provider given.")
