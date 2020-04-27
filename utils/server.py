import aiodactyl
import aiopes
import aiodathost

import sys

class Server:
    def find_client(obj):
        """ Working out what server provider we are using.
            
            For safetly reason only use identical functions what all given wrappers provide. 

            Before adding any new functionality, look over 
                https://github.com/WardPearce/aiodactyl
                https://github.com/WardPearce/aiopes
                https://github.com/WardPearce/aiodathost
            and see if all those APIs support it.
        """

        if obj.config.server["pterodactyl"]["enabled"]:
            pterodactyl = aiodactyl.client(api_key=obj.config.server["key"], route=obj.config.server["pterodactyl"]["route"], 
                                           session=obj.sessions.aiohttp)

            return pterodactyl.client

        elif obj.config.server["pes"]["enabled"]:
            pes = aiopes.client(api_key=obj.config.server["key"], session=obj.sessions.aiohttp)

            return pes.server

        elif obj.config.server["dathost"]["enabled"]:
            if "/" not in obj.config.server["key"]:
                sys.exit("Dathost key isn't formatted correctly.")

            username, password = obj.config.server["key"].split("/")

            dathost = aiodathost.client(username=username, password=password, session=obj.sessions.aiohttp)

            return dathost.server
        else:
            sys.exit("No server provider given.")