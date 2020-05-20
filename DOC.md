# Documentation
- [Modules](#modules)
- [Routes](#routes)

## Modules 
#### modulelift.client
- validate_user(self, user_id)

#### modulelift.client.league(self, league_id, region)
- get_server(self)
- queue_allowed(self)
- details(self)
- update(self, args: dict)

##### match(self, match_id=None)

---

```python
create(self, players: dict, maps: dict, team_names: dict)
```

**Parameters**
```
- Players: dict, required.
    - options: dict, required.
        - type: str, required.
            - random, selects captains randomly based off the list of players.
            - elo, selects captains depending off highest elo.
            - given, selects captain depending off given indexes in param.
        - param: dict, only required if type is `given`.
            - capt_1: int, index of player in list.
            - capt_2: int, index of player in list.
        - selection: str, only required if players aren't assigned teams. Expects string containing only A & B what tells the system the order of selections. The string must be the same length of the players given ignoring the captain.
        - assiged_teams: bool, telling the system if the teams are pre-assigned.
        - record_statistics: bool, if we should record statistics or not.
    - list: dict, expects key to be user ID & value to being the team (1, 2 or None / Null for no team.)
- Maps: dict, required.
    - options: dict, required.
        - type: str, required.
            - veto, captains veto maps.
            - random, maps are randomly selected.
            - given, map is given (Uses 1st index of map list.)
    - list: list, required. List of valid map names e.g. de_mirage.
- team_names: dict, required.
    - team_1, required. Name of team 1 (max 20 characters.)
    - team_2, required. Name of team 2 (max 20 characters.)
```
**Response**
[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---

- get(self)
- clone(self)
- scoreboard(self)
- end(self)
- players(self) - being developed
- select_player(self, user_id: str) - being developed
- select_map(self, map_id: str) - being developed

##### list(self, limit: int, offset: int, desc: bool, search: str = "")
- matches(self)
- players(self)

##### player(self, user_id)
- get(self)
- reset(self)
- delete(self)

##### players(self, user_ids)
- fetch(self, include_stats=False)
- validate(self)

##### api_key(self)
- paths(self)
- generate(self, user_id, access_level: int, active: bool = True)
- interact(self, api_key)
    - validate(self)
    - edit(self, access_level: int, active: bool = True)
    - delete(self)
    - paths(self)

## Routes
Coming soon