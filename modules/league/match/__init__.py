from utils.response import Response
from utils.queue import Queue
from utils.misc import Misc

from models.match import MatchModel
from models.scoreboard import ScoreboardModel

from .select import Select

from starlette.background import BackgroundTasks

from sessions import SESSIONS

import discord


class Match:
    def __init__(self, current_league, match_id):
        self.current_league = current_league

        if match_id:
            self.match_id = match_id
        else:
            self.match_id = Misc.uuid4()

    @property
    def select(self):

        return Select(
            current_league=self.current_league,
            current_match=self
        )

    async def create(self, players: dict, maps: dict, team_names: dict):
        """ Creates match.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#createself-players-dict-maps-dict-team_names-dict
        """

        queue = Queue(
            current_league=self.current_league,
            current_match=self,
            players=players,
            maps=maps,
            team_names=team_names,
        )

        validation = await queue.validate()
        if validation.error:
            queue.cache.clear()
            return validation

        # Working out player selection type.
        if queue.player_type.random:
            assign_random = queue.captain.random()

            if assign_random.error:
                return assign_random

        elif queue.player_type.elo:
            assign_elo = await queue.captain.elo()

            if assign_elo.error:
                return assign_elo

        else:
            assign_given = queue.captain.given()
            if assign_given:
                return assign_given

        # Working out map selection type.
        if queue.map_type.given:
            queue.map.given()

        elif queue.map_type.random:
            queue.map.random()

        else:
            queue.map.veto()

        # Creating the match.
        return await queue.create()

    async def get(self):
        """ Gets base details about the match.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#getself
        """

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

        row = await SESSIONS.database.fetch_one(
            query=query,
            values=values
        )

        if row:
            return Response(data=MatchModel(row).full)
        else:
            return Response(error="No match with that ID")

    async def clone(self):
        """ Clones given match.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#cloneself
        """

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
        """ Match scoreboard.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#scoreboardself
        """

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

        players = await SESSIONS.database.fetch_all(
            query=query,
            values=values
        )

        return Response(data=ScoreboardModel(
            match_data=match.data,
            players=players
        ).full)

    async def end(self):
        """ Ends given match.
            https://github.com/ModuleLIFT/API/blob/master/docs/modules.md#endself
        """

        match = await self.scoreboard()
        if match.error:
            return match

        if match.data["status"] == 0:
            return Response(error="Match already ended")

        values = {"match_id": self.match_id, }

        query = """UPDATE scoreboard_total SET status = 0
                   WHERE match_id = :match_id"""
        await SESSIONS.database.execute(
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
                    SESSIONS.websocket.send,
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
                    SESSIONS.webhook.send,
                    url=league_details.data["discord_webhook"],
                    content=match_message,
                    embed=embed
                )

        background_tasks.add_task(
            SESSIONS.server(
                server_id=match.data["server_id"]
            ).stop
        )

        # Forcing status to be correct.
        match.data["status"] = 0

        return Response(data=match.data, background=background_tasks)
