from starlette.background import BackgroundTask

from utils.response import Response
from utils.misc import Misc

from sessions import SESSIONS

from .captain import Captain
from .map import Map

from .cache import QueueCache

import re


class PlayerTypes:
    random = False
    elo = False
    given = False


class MapTypes:
    given = False
    random = False
    veto = False


class Queue:
    captains = {"team_1": None, "team_2": None}

    players_formatted = []
    players_formatted_append = players_formatted.append

    players_list = []

    details = {
        "match_id": None,
        "server_id": None,
        "league_id": None,
        "region": None,
        "team_1_name": None,
        "team_2_name": None,
    }

    players_obj = None

    player_type = PlayerTypes()
    map_type = MapTypes()

    def __init__(self, current_league, current_match,
                 players, maps, team_names):
        """ Handles queue logic, expects league object. """

        self.current_league = current_league
        self.current_match = current_match

        self.players = players
        self.maps = maps
        self.team_names = team_names
        self.players_list = list(self.players["list"].keys())

        self.cache = QueueCache(current_league.league_id)

        self.captain = Captain(
            self.players_obj,
            self.players,
            self.captains,
            self.players_list
        )
        self.map = Map(self.details, self.maps)

    async def validate(self):
        """ Validates queue """

        # Validating if queue is allowed.
        queue_allowed = await self.current_league.queue_allowed()
        if queue_allowed.error:

            self.cache.clear()
            return Response(error="Over queue limit")

        # Validating player payload.
        if "options" not in self.players \
            or type(self.players["options"]) != dict \
            or "type" not in self.players["options"] \
                or "list" not in self.players \
                or type(self.players["list"]) != dict \
                or "assigned_teams" not in self.players["options"] \
                or "record_statistics" not in self.players["options"] \
                or "auto_balance" not in self.players["options"]:

            self.cache.clear()
            return Response(error="Players payload formatted incorrectly")

        if self.players["options"]["assigned_teams"] \
                and self.players["options"]["auto_balance"]:

            self.cache.clear()
            return Response(error="Team can't be assigned if auto balanced")

        # Validating maps playload.
        if len(self.maps) < 1\
            or "options" not in self.maps \
            or type(self.maps["options"]) != dict\
                or "type" not in self.maps["options"] \
                or "list" not in self.maps \
                or type(self.maps["list"]) != list:

            self.cache.clear()
            return Response(error="Maps payload formatted incorrectly")

        # Assign a var the length of players['list'].
        # this will be used for multiple checks.
        players_len = len(self.players["list"])

        # Validating selection & types for maps & players.
        if "selection" not in self.players["options"]\
                or "selection" not in self.maps["options"]:
            if not self.players["options"]["assigned_teams"]\
                or (self.maps["options"]["type"] != "random"
                    and self.maps["options"]["type"] != "given"):

                self.cache.clear()
                return Response(error="Selection type must be passed")
        else:
            # Validating Selection types.
            if len(self.maps["options"]["selection"]) \
                != len(self.maps["list"]) \
                or len(self.players["options"]["selection"]) \
                    != players_len - 2:

                self.cache.clear()
                return Response(error="Invalid selection type")

            self.maps["options"]["selection"] =\
                self.maps["options"]["selection"].upper()

            self.players["options"]["selection"] =\
                self.players["options"]["selection"].upper()

            # Validating selection type has only A or B
            if not re.match("^[AB]*$", self.maps["options"]["selection"]) \
                or not re.match("^[AB]*$",
                                self.players["options"]["selection"]):

                self.cache.clear()
                return Response(error="Only A & B are valid")

        # Validating player length.
        if (players_len % 2) == 1 or players_len < 2 and players_len > 10:

            self.cache.clear()
            return Response(error="Odd amount of players or " +
                            "players is above 2 or below 10")

        # Validating team name playload.
        if "team_1" not in self.team_names\
            or "team_2" not in self.team_names \
            or type(self.team_names["team_1"]) != str\
                or type(self.team_names["team_2"]) != str\
                or len(self.team_names["team_1"]) > 20\
                or len(self.team_names["team_2"]) > 20:

            self.cache.clear()
            return Response(error="Invalid team names")

        self.details["team_1_name"] = Misc.sanitation(
            self.team_names["team_1"]
        )
        self.details["team_2_name"] = Misc.sanitation(
            self.team_names["team_2"]
        )

        # Validating a server is available.
        available_server = await self.current_league.get_server()
        if available_server.error:

            self.cache.clear()
            return available_server

        # Caching the server into the temp blacklist.
        self.details["server_id"] = self.cache.server(available_server.data)

        self.players_obj = self.current_league.players(
            user_ids=self.players_list
        )

        # Validating player IDs are correct.
        players_validate = await self.players_obj.validate()
        if players_validate.error:

            self.cache.clear()
            return players_validate

        # Validating if option type is correct.
        if self.players["options"]["type"] == "random":
            self.player_type.random = True

        elif self.players["options"]["type"] == "given":
            # Validating if params payload.
            if "param" not in self.players["options"] or\
                type(self.players["options"]["param"]) != dict \
                or "capt_1" not in self.players["options"]["param"] \
                or "capt_2" not in self.players["options"]["param"] \
                or type(
                    self.players["options"]["param"]["capt_1"]
                    ) != int \
                    or type(
                        self.players["options"]["param"]["capt_2"]
                        ) != int:

                self.cache.clear()
                return Response(error="Param payload " +
                                "formatted incorrectly")

            if self.players["options"]["param"]["capt_1"] \
                > players_len - 1 \
                or self.players["options"]["param"]["capt_2"] \
                    > players_len - 1:

                self.cache.clear()
                return Response(error="Index is not within range")

            self.player_type.given = True

        elif self.players["options"]["type"] == "elo":
            self.player_type.elo = True

        else:

            self.cache.clear()
            return Response(error="{} isn't a valid player type".format(
                self.players["options"]["type"]
            ))

        # Validating map payload.
        if self.maps["options"]["type"] == "given":
            self.map_type.given = True
        elif self.maps["options"]["type"] == "random":
            self.map_type.random = True
        elif self.maps["options"]["type"] == "veto":
            self.map_type.random = True
        else:

            self.cache.clear()
            return Response(error="{} isn't a valid map type".format(
                self.maps["options"]["type"]
            ))

        return Response(data=True)

    def _assign(self, user_id, team, captain):
        """ Assigns player to tell. """

        self.players_formatted_append({
            "match_id": self.details["match_id"],
            "user_id": user_id,
            "captain": captain,
            "team": team,
        })

    async def _auto_balance(self):
        """ Assigns players to team based off elo. """

        player_elo = await self.players_obj.fetch(include_stats=True)
        if player_elo.error:
            return player_elo

        for index in range(0, len(player_elo.data)):
            current_player = player_elo.data[index]

            if current_player["user_id"] != self.captains["team_1"] \
                    or current_player["user_id"] != self.captains["team_2"]:

                if (index + 1) % 2 == 0:
                    print("assigning team 2")
                    self.players["list"][current_player["user_id"]] = 2
                else:
                    print("assigning team 1")
                    self.players["list"][current_player["user_id"]] = 1

    async def create(self):
        """ Assigns players & captains to given
            team & also inserts the data into the database.
        """

        self.details["match_id"] = self.current_match.match_id

        if self.map_type.random or \
           self.map_type.given:
            map_pool = None

            if self.players["options"]["assigned_teams"] \
                    or self.players["options"]["auto_balance"]:
                # Setting match as live
                self.details["player_order"] = None
                self.details["status"] = 1
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.players[
                    "options"]["selection"]
                self.details["status"] = 3
        else:
            map_pool = []
            map_pool_append = map_pool.append
            for map_name in self.maps["list"]:
                map_pool_append({
                    "map": map_name,
                    "match_id": self.details["match_id"],
                })

            if self.players["options"]["assigned_teams"] \
                    or self.players["options"]["auto_balance"]:
                # Setting match as map selection stage
                self.details["player_order"] = None
                self.details["status"] = 2
            else:
                # Setting match as player selection stage
                self.details["player_order"] = self.players[
                    "options"]["selection"]
                self.details["status"] = 3

        if self.players["options"]["record_statistics"]:
            self.details["record_statistics"] = 1
        else:
            self.details["record_statistics"] = 0

        if self.players["options"]["auto_balance"]:
            await self._auto_balance()

        team_1_count = 0
        team_2_count = 0
        for user_id, team in self.players["list"].items():
            if self.captains["team_1"] == user_id or \
                    self.captains["team_2"] == user_id:
                captain = 1

                if self.captains["team_1"] == user_id:
                    team = 1
                else:
                    team = 2
            else:
                captain = 0

            if team is None:
                team = 0
            elif team == 1:
                team_1_count += 1
            elif team == 2:
                team_2_count += 1
            else:
                self.cache.clear()

                return Response(error="{} isn't a valid team side".format(
                    team
                ))

            self._assign(user_id=user_id, team=team, captain=captain)

        if team_1_count != team_2_count:
            self.cache.clear()

            return Response(error="Team 1 & 2 should have a" +
                            " even amount of players")

        self.details["league_id"] = self.current_league.league_id
        self.details["region"] = self.current_league.region

        query = """INSERT INTO scoreboard_total (match_id, league_id,
                                                 status, server_id,
                                                 region, team_1_name,
                                                 team_2_name, map,
                                                 map_order,
                                                 player_order,
                                                 record_statistics)
                                        VALUES  (:match_id, :league_id,
                                                 :status, :server_id,
                                                 :region, :team_1_name,
                                                 :team_2_name, :map,
                                                 :map_order,
                                                 :player_order,
                                                 :record_statistics)"""
        await SESSIONS.database.execute(query=query, values=self.details)

        query = """INSERT INTO scoreboard (match_id, user_id, captain, team)
                   VALUES (:match_id, :user_id, :captain, :team)"""
        await SESSIONS.database.execute_many(
            query=query,
            values=self.players_formatted
        )

        if map_pool:
            # If map type is random or given we don't
            # need a map pool.
            query = """INSERT INTO map_pool (match_id, map)
                                     VALUES (:match_id, :map)"""
            await SESSIONS.database.execute_many(query=query, values=map_pool)

        server_task = BackgroundTask(
            SESSIONS.server(
                server_id=self.details["server_id"]
            ).start
        )

        return Response(
            background=server_task,
            data=(await self.current_match.scoreboard()).data
        )
