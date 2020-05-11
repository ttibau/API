from utils.response import Response

from modules.league.match import Match
from modules.league.player import Player
from modules.league.players import Players
from modules.league.list_info import List
from modules.league.api_key import ApiKey

from settings import Config


class League:
    def __init__(self, obj, league_id, region=None):
        self.obj = obj
        self.league_id = league_id
        self.region = region

    @property
    def api_key(self):
        """ Object used for interacting
            with api keys.
        """

        return ApiKey(current_league=self)

    def match(self, match_id=None):
        """ Match Object.
            If no match_id passed random UUID4 will be generated and used
            for create function.
        """

        return Match(current_league=self, match_id=match_id)

    def list(self, limit: int, offset: int, desc: bool, search: str = ""):
        """ List Object.
                - limit.
                - offset.
                - desc.
                - search.
        """

        return List(current_league=self, limit=limit, offset=offset,
                    search=search, desc=desc)

    def player(self, user_id):
        """ Player Object. """

        return Player(current_league=self, user_id=user_id)

    def players(self, user_ids):
        """ Players Object. """

        return Players(current_league=self, user_ids=user_ids)

    async def get_server(self):
        """ Finds a available server for the currnet league. """

        if not Config.server["regions"].get(self.region):
            return Response(error="No server IDs for that region")

        region_servers = list(
            Config.server["regions"][self.region]
        )
        region_servers_remove = region_servers.remove

        query = """SELECT server_id
                   FROM scoreboard_total
                   WHERE server_id IN :server_ids AND status != 0"""
        values = {"server_ids": region_servers}

        # Removing any server ID being used in an active match.
        async for row in self.obj.database.iterate(query=query, values=values):
            region_servers_remove(row["server_id"])

        # Removing any server IDs from our temp blacklist.
        for server_id in self.obj.in_memory_cache.temp_server_blacklist:
            if server_id in region_servers:
                region_servers_remove(server_id)

        if len(region_servers) > 0:
            return Response(data=region_servers[0])
        else:
            return Response(error="No available servers")

    async def queue_allowed(self):
        """ Checks if over the active queue limit. """

        query = """SELECT COUNT(score.status) AS active_queues,
                          IFNULL(info.queue_limit, 0) AS queue_limit
                   FROM league_info AS info
                    LEFT JOIN scoreboard_total AS score
                        ON score.league_id = info.league_id
                           AND score.status != 0
                   WHERE info.league_id = :league_id"""
        row = await self.obj.database.fetch_one(
            query=query,
            values={"league_id": self.league_id, }
        )

        if row:
            # Ensures users can't create another
            # queue when another queue is being created
            # what would put them over the queue limit.
            if self.obj.in_memory_cache.started_queues.get(self.league_id):
                active_queues = row["active_queues"] \
                     + self.obj.in_memory_cache.started_queues[self.league_id]
            else:
                active_queues = row["active_queues"]

            return Response(data=row["queue_limit"] > active_queues)
        else:
            return Response(error=True)

    async def details(self):
        """ Gets basic details of league. """

        row = await self.obj.database.fetch_one(
            query="""SELECT league_name, league_website, discord_webhook,
                            websocket_endpoint, queue_limit,
                            league_id, discord_prefix,
                            sm_message_prefix, knife_round,
                            pause, surrender,
                            warmup_commands_only, captain_choice_time
                     FROM league_info WHERE league_id = :league_id""",
            values={"league_id": self.league_id, })

        if row:
            formatted_row = {**row}

            if formatted_row["pause"] == 0:
                formatted_row["pause"] = False

            formatted_row["surrender"] = formatted_row["surrender"] == 1
            formatted_row["warmup_commands_only"] = \
                formatted_row["warmup_commands_only"] == 1
            formatted_row["knife_round"] = formatted_row["knife_round"] == 1

            return Response(data=formatted_row)

        return Response(error="No such league")

    async def update(self, args: dict):
        """ Updates details of league. """

        if len(args) > 0:
            query = "UPDATE league_info SET "
            values = {"league_id": self.league_id}

            for key, item in args.items():
                if type(item) == bool:
                    if item:
                        item = 1
                    else:
                        item = 0

                values[key] = item

                # Don't worry this isn't
                # injecting any values.
                query += "{}={},".format(key, ":"+key)

            query = query[:-1]
            query += " WHERE league_id = :league_id"

            await self.obj.database.execute(query=query, values=values)

            return Response(data=args)

        return Response(error="No arguments")
