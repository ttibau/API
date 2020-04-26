import aiodactyl
import aiopes
import aiodathost

import sys

class Server(object):
    def __init__(self, obj):
        self.obj = obj

        if self.obj.config.server["pterodactyl"]["enabled"]:
            pterodactyl = aiodactyl.client(api_key=self.obj.config.server["key"], route=self.obj.config.server["route"], session=self.obj.session.aiohttp)

            self.client = pterodactyl.client

        elif self.obj.config.server["pes"]["enabled"]:
            pes = aiopes.client(api_key=self.obj.config.server["key"], session=self.obj.session.aiohttp)

            self.client = pes.server

        elif self.obj.config.server["dathost"]["enabled"]:
            if "/" not in self.obj.config.server["key"]:
                sys.exit("Dathost key isn't formatted correctly.")

            username, password = self.obj.config.server["key"].split("/")

            dathost = aiodathost.client(username=username, password=password, session=self.obj.session.aiohttp)

            self.client = dathost.server
        else:
            sys.exit("No server provider given.")