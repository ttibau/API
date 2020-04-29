from utils.response import response
from utils.queue.queue import Queue

from models.match import MatchModel
from models.scoreboard import ScoreboardModel

from starlette.background import BackgroundTask


class Match(object):
    def __init__(self, current_league, match_id):
        self.current_league = current_league
        self.match_id = match_id

    def clear_cache(self, server_id=None):
        """ Clears cached data for current league out of memeory. """

        in_memory_cache = self.current_league.obj.in_memory_cache

        if server_id in in_memory_cache.temp_server_blacklist:
            in_memory_cache.temp_server_blacklist.remove(server_id)

        if in_memory_cache.started_queues.get(self.current_league.league_id):
            if in_memory_cache.started_queues[self.current_league.league_id] \
                 == 1:
                in_memory_cache.started_queues.pop(
                    self.current_league.league_id
                )
            else:
                in_memory_cache.started_queues[self.current_league.league_id] \
                    -= 1

    async def create(self, players: dict, maps: dict, team_names: dict):
        """ Creates match.
                - players
                    {
                        "options": {
                            "type": "random"
                                    / "elo"
                                    / "given",
                            "param": None
                                    / ASC OR DESC
                                    / {"capt_1": index, "capt_2": index}
                            "selection": "ABBAABBA" / "ABBABABA" / "ABABABAB",
                            "assiged_teams": True / False,
                            "record_statistics": True / False,
                        },
                        "list": {
                            "user_id": None / 1 / 2
                        },
                    }
                - maps
                    {
                        "options": {
                            "type": "veto" / "random" / "vote" / "given",
                            "selection": "ABBAABBA" / "ABBABABA" / "ABABABAB",
                        },
                        "list": [list of full map names],
                    }
                - team_names
                    {
                        "team_1": "Max 13 characters",
                        "team_2": "",
                    }
        """

        queue_allowed = await self.current_league.queue_allowed()
        if not queue_allowed.error:
            in_memory_cache = self.current_league.obj.in_memory_cache

            # Once this queue is inserted into the database or it fails
            # -1 is removed from in_memory_cache.started_queues for this
            # league ID.
            if in_memory_cache.started_queues.get(
                    self.current_league.league_id):
                in_memory_cache.started_queues[self.current_league.league_id] \
                     += 1
            else:
                in_memory_cache.started_queues[self.current_league.league_id] \
                     = 1

            if "options" not in players or type(players["options"]) != dict \
                or "type" not in players["options"] \
                    or "list" not in players \
                    or type(players["list"]) != dict \
                    or "assiged_teams" not in players["options"] \
                    or "selection" not in players["options"] \
                    or "record_statistics" not in players["options"]:
                self.clear_cache()

                return response(error="Players payload formatted incorrectly")

            if len(maps) < 1 or "options" not in maps \
                or type(maps["options"]) != dict\
                    or "type" not in maps["options"] \
                    or "selection" not in maps["options"] \
                    or "list" not in maps \
                    or type(maps["list"]) != list:
                self.clear_cache()

                return response(error="Maps payload formatted incorrectly")

            if players["options"]["selection"] not in \
                self.current_league.obj.config.pug["selection_types"] \
                or maps["options"]["selection"] not in \
                    self.current_league.obj.config.pug["selection_types"]:
                self.clear_cache()

                return response(error="Invaild selection type")

            len_players = len(players["list"])
            if (len_players % 2) == 1 or len_players < 2 and len_players > 10:
                self.clear_cache()

                return response(error="Odd amout of players or\
                                         players is above 2 or below 10")

            if not team_names.get("team_1") or not team_names.get("team_2") \
                or type(team_names["team_1"]) != str\
                    or type(team_names["team_2"]) != str:
                self.clear_cache()

                return response(error="Invalid team names")

            available_server = await self.current_league.get_server()
            if available_server.error:
                self.clear_cache()

                return available_server

            in_memory_cache.temp_server_blacklist.append(available_server.data)

            queue = Queue(players=players,
                          maps=maps,
                          team_names=team_names,
                          server_id=available_server.data,
                          obj=self)

            # Ensures valid user IDs are given
            # If errors returns response return with
            # data of incorrect user ids.
            players_obj = self.current_league.players(
                user_ids=queue.players_list
            )

            players_validate = await players_obj.validate()
            if players_validate.error:
                self.clear_cache(server_id=available_server.data)

                return players_validate

            if players["options"]["type"] == "random":
                assign_random = queue.captain.random()

                # If none isn't returned
                # something has errored.
                if assign_random:
                    self.clear_cache(server_id=available_server.data)

                    return assign_random

            elif players["options"]["type"] == "elo" or\
                    players["options"]["type"] == "given":
                if not players["options"].get("param"):
                    self.clear_cache(server_id=available_server.data)

                    return response(
                        error="Param is required for type {}".format(
                            players["options"]["type"],
                        ))

                if players["options"]["type"] == "elo":
                    players_elo = await players_obj.fetch(include_stats=True)

                    if not players_elo.error:
                        assign_elo = queue.captain.elo(players_elo)
                        if assign_elo:
                            self.clear_cache(server_id=available_server.data)

                            return assign_elo
                    else:
                        self.clear_cache(server_id=available_server.data)

                        return response(error="""Something went
                                                 wrong during elo fetch""")
                else:
                    if type(players["options"]["param"]) != dict\
                        or not players["options"]["param"].get("capt_1") \
                        or not players["options"]["param"].get("capt_2") \
                        or type(players["options"]["param"]["capt_1"]) != int \
                            or type(players["options"]["param"]["capt_2"]) \
                            != int:
                        self.clear_cache(server_id=available_server.data)

                        return response(error="""Param payload
                                                 formatted incorrectly""")

                    if players["options"]["param"]["capt_1"] \
                        > len_players - 1 \
                        or players["options"]["param"]["capt_2"] \
                            > len_players - 1:

                        self.clear_cache(server_id=available_server.data)

                        return response(error="Index is not within range")

                    assign_given = queue.captain.given()
                    if assign_given:
                        self.clear_cache(server_id=available_server.data)

                        return assign_given
            else:
                self.clear_cache(server_id=available_server.data)

                return response(error="{} isn't a valid player type".format(
                    players["options"]["type"]
                ))

            if maps["options"]["type"] == "given":
                queue.map.given()
            elif maps["options"]["type"] == "random":
                queue.map.random()
            elif maps["options"]["type"] == "vote":
                queue.map.vote()
            elif maps["options"]["type"] == "veto":
                queue.map.veto()
            else:
                self.clear_cache(server_id=available_server.data)

                return response(error="{} isn't a valid map type".format(
                    maps["options"]["type"]
                ))

            # Creating match from given data.
            queue_create = await queue.create()

            self.clear_cache(server_id=available_server.data)

            if queue_create.error:
                return queue_create

            server_task = BackgroundTask(
                self.current_league.obj.server(
                    server_id=available_server.data
                ).start
            )

            return response(backgroud=server_task, data=queue_create.data)
        else:
            return response(error="Over queue limit")

    async def get(self):
        """ Gets base details about the match. """

        query = """SELECT match_id, server_id, map_order, player_order, timestamp, status,
                          map, team_1_name, team_2_name,
                          team_1_score, team_2_score,
                          team_1_side, team_2_side, record_statistics
                   FROM scoreboard_total
                   WHERE match_id = :match_id
                         AND league_id = :league_id AND region = :region"""
        values = {
            "match_id": self.match_id,
            "league_id": self.current_league.league_id,
            "region": self.current_league.region,
        }

        row = await self.current_league.obj.database.fetch_one(
            query=query,
            values=values
        )

        if row:
            return response(data=MatchModel(row).full)
        else:
            return response(error="No match with that ID")

    async def scoreboard(self):
        """ Match scoreboard. """

        match = await self.get()
        if match.error:
            return match

        # Don't need to validate region or league
        # because self.get() will fail if isn't
        # valid already.
        query = """SELECT sb.user_id, sb.captain, sb.team, sb.alive,
                          sb.ping, sb.kills, sb.headshots, sb.assists,
                          sb.deaths, sb.shots_fired, sb.shots_hit, sb.mvps,
                          sb.score, sb.disconnected,
                          users.discord_id, users.name, users.pfp,
                          users.steam_id, users.joined
                   FROM scoreboard AS sb
                        LEFT JOIN users
                            ON users.user_id = sb.user_id
                   WHERE sb.match_id = :match_id"""

        values = {"match_id": self.match_id, }

        players = await self.current_league.obj.database.fetch_all(
            query=query,
            values=values
        )

        return response(data=ScoreboardModel(
            match_data=match.data,
            players=players
        ).full)

    async def end(self):
        """ Ends given match. """

        match = self.get()
        if match.error:
            return match

        values = {"match_id": self.match_id, }

        query = """UPDATE scoreboard_total SET status = 0
                   WHERE match_id = :match_id"""
        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

        # We just delete map pool for the given match.
        query = "DELETE FROM map_pool WHERE match_id = :match_id"
        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

        server_task = BackgroundTask(
            self.current_league.obj.server(
                server_id=match.data["server_id"]
            ).stop)

        return response(data=match.data, backgroud=server_task)

    async def players(self):
        """ List players for given match. """
        pass

    async def select_player(self, user_id: str):
        pass

    async def select_map(self, map_id: str):
        pass
