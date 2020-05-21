from utils.response import Response

from settings import Config

from aiohttp_session import AIOHTTP


class Steam:
    base_url = "https://api.steampowered.com/"

    profile_url = base_url +\
        "ISteamUser/GetPlayerSummaries/v2/?key=" +\
        Config.steam["key"] + "&steamids={}"

    async def get_user(self, steam_id):
        """ Gets details from steam API about given steam ID. """

        async with AIOHTTP.ClientSession.get(
                self.profile_url.format(steam_id)) as resp:
            if resp.status == 200:
                resp_json = await resp.json()

                if "response" in resp_json \
                        and "players" in resp_json["response"] \
                        and len(resp_json["response"]["players"]) == 1:
                    return Response(data=resp_json["response"]["players"][0])

        return Response(error="Invalid user or API key")
