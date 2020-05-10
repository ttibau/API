from utils.response import response

from settings import Config as config


class Steam:
    base_url = "https://api.steampowered.com/"

    profile_url = base_url +\
        "ISteamUser/GetPlayerSummaries/v2/?key=" +\
        config.steam["key"] + "&steamids={}"

    def __init__(self, obj):
        self.obj = obj

    async def get_user(self, steam_id):
        """ Get's details from steam API about given steam ID. """

        async with self.obj.sessions.aiohttp.get(
                self.profile_url.format(steam_id)) as resp:
            if resp.status == 200:
                resp_json = await resp.json()

                if "response" in resp_json \
                        and "players" in resp_json["response"] \
                        and len(resp_json["response"]["players"]) == 1:
                    return response(data=resp_json["response"]["players"][0])

        return response(error="Invalid user or API key")
