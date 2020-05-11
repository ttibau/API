from utils.response import Response
from utils.queue import Queue
from utils.misc import Misc

from models.match import MatchModel
from models.scoreboard import ScoreboardModel

from modules.league.match.select import Select

from starlette.background import BackgroundTask, BackgroundTasks

import discord
import re


class Match:
    def __init__(self, current_league, match_id):
        self.current_league = current_league

        if match_id:
            self.match_id = match_id
        else:
            self.match_id = Misc.uuid4()

    def _clear_cache(self, server_id=None):
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

    @property
    def select(self):

        return Select(
            current_league=self.current_league,
            current_match=self
        )

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
                            "selection": "ABBAABBA"
                                          / "ABBABABA"
                                          / "ABABABAB"
                                          / None,
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
                            "selection": "ABBAABBA"
                                          / "ABBABABA"
                                          / "ABABABAB"
                                          / None,
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
                    or "record_statistics" not in players["options"]:
                self._clear_cache()

                return Response(error="Players payload formatted incorrectly")

            if len(maps) < 1 or "options" not in maps \
                or type(maps["options"]) != dict\
                    or "type" not in maps["options"] \
                    or "list" not in maps \
                    or type(maps["list"]) != list:
                self._clear_cache()

                return Response(error="Maps payload formatted incorrectly")

            len_players = len(players["list"])

            if "selection" not in players["options"]\
                    or "selection" not in maps["options"]:
                if not players["options"]["assiged_teams"]\
                    or (maps["options"]["type"] != "random"
                        and maps["options"]["type"] != "given"):
                    self._clear_cache()

                    return Response(error="Selection type must be passed")

            else:
                if len(maps["options"]["selection"]) \
                   != len(maps["list"]) \
                   or len(players["options"]["selection"]) \
                   != len_players - 2:
                    self._clear_cache()

                    return Response(error="Invaild selection type")

                maps["options"]["selection"] = maps["options"][
                    "selection"].upper()
                players["options"]["selection"] = players["options"][
                    "selection"].upper()

                if not re.match("^[AB]*$", maps["options"]["selection"]) \
                    or not re.match("^[AB]*$",
                                    players["options"]["selection"]):
                    self._clear_cache()

                    return Response(error="Only A & B are valid")

            if (len_players % 2) == 1 or len_players < 2 and len_players > 10:
                self._clear_cache()

                return Response(error="Odd amout of players or\
                                         players is above 2 or below 10")

            if not team_names.get("team_1") or not team_names.get("team_2") \
                or type(team_names["team_1"]) != str\
                    or type(team_names["team_2"]) != str:
                self._clear_cache()

                return Response(error="Invalid team names")

            available_server = await self.current_league.get_server()
            if available_server.error:
                self._clear_cache()

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
                self._clear_cache(server_id=available_server.data)

                return players_validate

            if players["options"]["type"] == "random":
                assign_random = queue.captain.random()

                # If none isn't returned
                # something has errored.
                if assign_random:
                    self._clear_cache(server_id=available_server.data)

                    return assign_random

            elif players["options"]["type"] == "elo" or\
                    players["options"]["type"] == "given":
                if not players["options"].get("param"):
                    self._clear_cache(server_id=available_server.data)

                    return Response(
                        error="Param is required for type {}".format(
                            players["options"]["type"],
                        ))

                if players["options"]["type"] == "elo":
                    players_elo = await players_obj.fetch(include_stats=True)

                    if not players_elo.error:
                        assign_elo = queue.captain.elo(players_elo)
                        if assign_elo:
                            self._clear_cache(server_id=available_server.data)

                            return assign_elo
                    else:
                        self._clear_cache(server_id=available_server.data)

                        return Response(error="""Something went
                                                 wrong during elo fetch""")
                else:
                    if type(players["options"]["param"]) != dict \
                        or "capt_1" not in players["options"]["param"] \
                        or "capt_2" not in players["options"]["param"] \
                        or type(players["options"]["param"]["capt_1"]) != int \
                            or type(players["options"]["param"]["capt_2"]) \
                            != int:
                        self._clear_cache(server_id=available_server.data)

                        return Response(error="Param payload\
                                               formatted incorrectly")

                    if players["options"]["param"]["capt_1"] \
                        > len_players - 1 \
                        or players["options"]["param"]["capt_2"] \
                            > len_players - 1:

                        self._clear_cache(server_id=available_server.data)

                        return Response(error="Index is not within range")

                    assign_given = queue.captain.given()
                    if assign_given:
                        self._clear_cache(server_id=available_server.data)

                        return assign_given
            else:
                self._clear_cache(server_id=available_server.data)

                return Response(error="{} isn't a valid player type".format(
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
                self._clear_cache(server_id=available_server.data)

                return Response(error="{} isn't a valid map type".format(
                    maps["options"]["type"]
                ))

            # Creating match from given data.
            queue_create = await queue.create()

            self._clear_cache(server_id=available_server.data)

            if queue_create.error:
                return queue_create

            server_task = BackgroundTask(
                self.current_league.obj.server(
                    server_id=available_server.data
                ).start
            )

            return Response(backgroud=server_task, data=queue_create.data)
        else:
            return Response(error="Over queue limit")

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
            return Response(data=MatchModel(row).full)
        else:
            return Response(error="No match with that ID")

    async def clone(self):
        """ Clones given match. """

        match_scoreboard = await self.scoreboard()
        if match_scoreboard.error:
            return match_scoreboard

        if match_scoreboard.data["status"] != 0:
            return Response(error="Active matches can't be cloned")

        match_data = {
            "players": {
                "options": {
                    "type": "given",
                    "param": {"capt_1": None, "capt_2": None},
                    "assiged_teams": True,
                    "record_statistics": match_scoreboard.
                    data["record_statistics"],
                },
                "list": {},
            },
            "maps": {
                "options": {
                    "type": "given",
                },
                "list": [
                    match_scoreboard.data["map"]
                ],
            },
            "team_names": {
                "team_1": match_scoreboard.data["team_1"]["name"],
                "team_2": match_scoreboard.data["team_2"]["name"],
            },
        }

        for user_id, user_data in match_scoreboard.data["players"][
                "team_1"].items():
            match_data["players"]["list"][user_id] = 1

            if user_data["captain"]:
                match_data["players"]["options"]["param"]["capt_1"] = \
                    list(match_data["players"]["list"]
                         .keys()).index(user_id)

        for user_id, user_data in match_scoreboard.data["players"][
                "team_2"].items():
            match_data["players"]["list"][user_id] = 2

            if user_data["captain"]:
                match_data["players"]["options"]["param"]["capt_2"] = \
                    list(match_data["players"]["list"]
                         .keys()).index(user_id)

        return await self.create(**match_data)

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
                          users.discord_id, users.name,
                          users.steam_id, users.joined,
                          users.file_type
                   FROM scoreboard AS sb
                        LEFT JOIN users
                            ON users.user_id = sb.user_id
                   WHERE sb.match_id = :match_id"""

        values = {"match_id": self.match_id, }

        players = await self.current_league.obj.database.fetch_all(
            query=query,
            values=values
        )

        return Response(data=ScoreboardModel(
            match_data=match.data,
            players=players
        ).full)

    async def end(self):
        """ Ends given match. """

        match = await self.scoreboard()
        if match.error:
            return match

        if match.data["status"] == 0:
            return Response(error="Match already ended")

        values = {"match_id": self.match_id, }

        query = """UPDATE scoreboard_total SET status = 0
                   WHERE match_id = :match_id"""
        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

        match.data["winner"] = Misc.determine_winner(
            match.data["team_1"],
            match.data["team_2"]
        )

        background_tasks = BackgroundTasks()

        league_details = await self.current_league.details()
        if not league_details.error:
            if league_details.data["websocket_endpoint"]:
                background_tasks.add_task(
                    self.current_league.obj.websocket.send,
                    uri=league_details.data["websocket_endpoint"],
                    data=match.data
                )

            if league_details.data["discord_webhook"]:
                embed = discord.Embed(
                    description="**Details:**\n\
                                Map: {}\nScore: {}\n\
                                    [Scoreboard]({})".format(
                                        match.data["map"],
                                        "{}:{}".format(
                                            match.data["team_1"]["score"],
                                            match.data["team_2"]["score"]
                                        ),
                                        "{}/scoreboard/{}".format(
                                            league_details.data[
                                                "league_website"],
                                            match.data["match_id"]
                                        )
                                    ))

                formatted_player_names = {
                    "team_1": "",
                    "team_2": "",
                }

                winner_mention = ""

                for index in formatted_player_names.keys():
                    for values in match.data["players"][index].values():
                        if index == match.data["winner"]:
                            winner_mention += "<@{}>".format(
                                values["discord_id"]
                            )

                        formatted_player_names[index] += "{}\n".format(
                            values["name"]
                        )

                embed.add_field(
                    name=match.data["team_1"]["name"],
                    value=formatted_player_names["team_1"],
                    inline=True
                )

                embed.add_field(
                    name=match.data["team_2"]["name"],
                    value=formatted_player_names["team_2"],
                    inline=True
                )

                if match.data["winner"] == "tie":
                    match_message = "Congratulations everyone for tying!"
                else:
                    match_message = "Congratulations {} for winning!".format(
                        winner_mention
                    )

                background_tasks.add_task(
                    self.current_league.obj.webhook.send,
                    url=league_details.data["discord_webhook"],
                    content=match_message,
                    embed=embed
                )

        background_tasks.add_task(
            self.current_league.obj.server(
                server_id=match.data["server_id"]
            ).stop
        )

        # Forcing status to be correct.
        match.data["status"] = 0

        return Response(data=match.data, backgroud=background_tasks)
