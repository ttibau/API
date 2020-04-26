import aiodactyl
import aiopes
import aiodathost

import sys

class Server(object):
    def __init__(self, obj):
        """ Working out what server provider we are using.
            
            For safetly reason only use identical functions what all given wrappers provide. 

            Before adding any new functionality, look over 
            https://github.com/WardPearce/aiodactyl
            https://github.com/WardPearce/aiopes
            https://github.com/WardPearce/aiodathost
            and see if all those APIs support it.
        """

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