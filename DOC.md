# Documentation
- [Modules](#modules)
- [Routes](#routes)

## Modules 
#### modulelift.client.user(self, user_id=None)
---
```python
user(self, user_id=None).exists(self)
```

**Parameters**
```
None
```
**Response**

Response object with data being a bool.

---
```python
user(self, user_id=None).external_exists(self, steam_id, discord_id)
```

**Parameters**
```
- steam_id, valid steamID64.
- discord_id, valid Discord snowflake ID.
```
**Response**

Response object with data being a bool.

---
```python
user(self, user_id=None).create(self, steam_id, ip=None, name=None, discord_id=None, pfp=None)
```

**Parameters**
```
- steam_id, valid steamID64.
- ip, optional, used for alt detection.
- name, optional, if not passed steam name will be used.
- discord_id, optional, valid Discord snowflake ID.
- pfp, optional, if not passed steam pfp will be used. Expects link to valid image format.
```
**Response**

[Minimal player model](https://github.com/ModuleLIFT/API/blob/master/models/player.py#L46) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
#### modulelift.client.league(self, league_id, region)

```python
league(self, league_id, region).get_server(self)
```

**Parameters**
```
None
```
**Response**

Response object with data being server ID.

---
```python
league(self, league_id, region).queue_allowed(self)
```

**Parameters**
```
None
```
**Response**

Response object with data telling us if the queue is allowed.

---
```python
league(self, league_id, region).details(self)
```

**Parameters**
```
None
```
**Response**

```python
{
    "league_name": str,
    "league_website": str,
    "discord_webhook": str,
    "websocket_endpoint": str,
    "queue_limit": int,
    "league_id": str,
    "discord_prefix": str,
    "sm_message_prefix": str,
    "knife_round": bool,
    "pause": bool or int,
    "surrender": bool,
    "warmup_commands_only": bool,
    "captain_choice_time": int,
}
```

---
```python
league(self, league_id, region).update(self, args: dict)
```

**Parameters**
```
- league_name, str.
- league_website, str.
- websocket_endpoint, str.
- discord_webhook, str.
- discord_prefix, str.
- sm_message_prefix, str.
- knife_round, str.
- pause, str.
- surrender, str.
- warmup_commands_only, str.
- captain_choice_time, str.
```
**Response**

Response object with whatever you passed to it.

---

##### match(self, match_id=None)

```python
match(self, match_id=None).create(self, players: dict, maps: dict, team_names: dict)
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
```python
match(self, match_id=None).get(self)
```

**Parameters**
```
None
```

**Response**

[Full match model](https://github.com/ModuleLIFT/API/blob/master/models/match.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
```py
match(self, match_id=None).clone(self)
```

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
```py
match(self, match_id=None).scoreboard(self)
```

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
```python
match(self, match_id=None).end(self)
```

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
```python
match(self, match_id=None).select.player(self, user_id: str)
```

**Parameters**
```
- user_id: str
    - Valid User ID.
```

**Response**

```python
{
    "completed": bool,
    "next_turn": str,
    "status": int,
}
```

---
```python
match(self, match_id=None).select.map(self, map_id: str)
```

**Parameters**
```
- map_id: str
    - Valid Map ID.
```

**Response**

```python
{
    "completed": bool,
    "next_turn": str,
    "status": int,
}
```

---
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