from utils.response import response


class MatchSelect(object):
    async def _update_player(self, user_id, team):
        """ Inserts player into team. """

        query = """UPDATE scoreboard SET team = :team
                   WHERE match_id = :match_id AND user_id = :user_id"""

        values = {
            "match_id": self.match_id,
            "user_id": user_id,
            "team": team,
        }

        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

    def _stage_letter_to_team(self, letter):
        if letter == "A":
            team = 1
        else:
            team = 2

        return team

    async def select_player(self, user_id: str):
        """ Selects player. """

        match_scoreboard = await self.scoreboard()
        if match_scoreboard.error:
            return match_scoreboard

        if match_scoreboard.data["status"] != 3:
            return response(error="This match isn't at player selection stage")

        if user_id not in match_scoreboard.data["players"]["unassigned"]:
            return response(error="Player isn't in unassigned")

        # Works out the current stage index.
        # Because the captains are already in the teams & we want the index
        # we subtract 2 to the total len for both teams.
        stage_index = len(match_scoreboard.data["players"]["team_1"]) \
            + len(match_scoreboard.data["players"]["team_2"]) - 2

        print(stage_index)

        stage_letter = match_scoreboard.data["player_order"][stage_index]

        print(stage_letter)

        return_data = {
            "completed": False,
            "next_turn": match_scoreboard.data["player_order"][
                stage_index + 1],
            "status": 3,
        }

        if len(match_scoreboard.data["players"]["unassigned"]) == 2:
            for unassigned_user_id in match_scoreboard.data["players"][
                    "unassigned"].keys():
                if unassigned_user_id == user_id:
                    current_stage = stage_letter
                else:
                    current_stage = return_data["next_turn"]

                team = self._stage_letter_to_team(current_stage)

                await self._update_player(unassigned_user_id, team)

            return_data["completed"] = True

            if not match_scoreboard.data["map"]:
                next_status = 2
            else:
                next_status = 1

            return_data["status"] = next_status

            query = """UPDATE scoreboard_total
                       SET status = :next_status
                       WHERE match_id = :match_id"""
            values = {"match_id": self.match_id, "next_status": next_status, }

            await self.current_league.obj.database.execute(
                query=query,
                values=values
            )
        else:
            team = self._stage_letter_to_team(stage_letter)

            await self._update_player(user_id, team)

        return response(data=return_data)

    async def select_map(self, map_id: str):
        """ Selects map. """

        match_scoreboard = await self.scoreboard()
        if match_scoreboard.error:
            return match_scoreboard

        if match_scoreboard.data["status"] != 2:
            return response(error="This match isn't at map selection stage")

        query = "SELECT map FROM map_pool WHERE match_id = :match_id"
        values = {"match_id": self.match_id, }

        maps = await self.current_league.obj.database.fetch_all(
            query=query,
            values=values
        )

        maps_len = len(maps)

        valid_map = False
        if maps_len > 2:
            for value in maps:
                if map_id == value["map"]:
                    valid_map = True
                    break
        else:
            selected_map = None
            for value in maps:
                if map_id == value["map"]:
                    valid_map = True
                else:
                    selected_map = value["map"]

        if not valid_map:
            return response(error="Invalid map")

        query = """DELETE FROM map_pool
                   WHERE map = :map AND match_id = :match_id"""
        values["map"] = map_id

        await self.current_league.obj.database.execute(
            query=query,
            values=values
        )

        next_stage_letter = match_scoreboard.data["map_order"][
            maps_len]

        return_data = {
            "completed": False,
            "next_turn": next_stage_letter,
            "status": 2,
        }

        if maps_len == 2:
            if len(match_scoreboard.data["players"]["unassigned"]) == 0:
                next_status = 1
            else:
                next_status = 3

            return_data["status"] = next_status
            return_data["completed"] = True

            query = """UPDATE scoreboard_total SET map = :map, status = :next_status
                       WHERE match_id = :match_id"""
            values = {"map": selected_map, "next_status": next_status}

            await self.current_league.obj.database.execute(
                query=query,
                values=values
            )

        return response(data=return_data)
