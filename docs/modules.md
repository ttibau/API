### Notice
This API is only design to be used internally for the system, if you're looking at developing a system using ModuleLIFT check out the route documentation or check out [this wrapper](https://github.com/ModuleLIFT/aiomodulelift).

# Module's Documentation
- [User](#moduleliftclientuserself-user_idnone)
    - [exists(self)](#existsself)
    - [external_exists(self, steam_id, discord_id)](#external_existsself-steam_id-discord_id)
    - [create(self, steam_id, ip=None, name=None, discord_id=None, pfp=None)](#createself-steam_id-ipnone-namenone-discord_idnone-pfpnone)
- [League](#moduleliftclientleagueself-league_id-region)
    - [get_server(self)](#get_serverself)
    - [queue_allowed(self)](#queue_allowedself)
    - [details(self)](#detailsself)
    - [update(self, args: dict)](#updateself-args-dict)
    - [Match](#matchself-match_idnone)
        - [create(self, players: dict, maps: dict, team_names: dict)](#createself-players-dict-maps-dict-team_names-dict)
        - [get(self)](#getself)
        - [clone(self)](#cloneself)
        - [scoreboard(self)](#scoreboardself)
        - [end(self)](#endself)
        - Select
            - [player(self, user_id: str)](#selectplayerself-user_id-str)
            - [map(self, map_id: str)](#selectmapself-map_id-str)
    - [List](#listself-limit-int-offset-int-desc-bool-search-str--)
        - [matches(self)](#matchesself)
        - [players(self)](#playersself)
    - [Player](#playerself-user_id)
        - [get(self)](#getself-1)
        - [reset(self)](#resetself)
        - [delete(self)](#deleteself)
    - [Players](#playersself-user_ids)
        - [fetch(self, include_stats=False)](#fetchself-include_statsfalse)
        - [validate(self)](#validateself)
    - [API Key](#api_keyself)
        - [paths(self)](#pathsself)
        - [generate(self, user_id, access_level: int, active: bool = True)](#generateself-user_id-access_level-int-active-bool--true)
        - [Interact](#interactself-api_key)
            - [validate(self)](#validateself-1)
            - [edit(self, access_level: int, active: bool = True)](#editself-access_level-int-active-bool--true)
            - [delete(self)](#deleteself-1)
            - [paths(self)](#pathsself-1)

## modulelift.client.user(self, user_id=None)
##### exists(self)
```python
user(self, user_id=None).exists(self)
```
**Functionality**

Checks if the given ID exists outside of league context.

**Parameters**
```
None
```
**Response**

Response object with data being a bool.

---
##### external_exists(self, steam_id, discord_id)
```python
user(self, user_id=None).external_exists(self, steam_id, discord_id)
```
**Functionality**

Checks if external IDs exists / have been used by other users. Mainly for alt detection.

**Parameters**
```
- steam_id, valid steamID64.
- discord_id, valid Discord snowflake ID.
```
**Response**

Response object with data being a bool.

---
##### create(self, steam_id, ip=None, name=None, discord_id=None, pfp=None)
```python
user(self, user_id=None).create(self, steam_id, ip=None, name=None, discord_id=None, pfp=None)
```
**Functionality**

Attempts to create a user from the given information, if IP is passed alt detection will be done.

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
## modulelift.client.league(self, league_id, region)
##### get_server(self)
```python
league(self, league_id, region).get_server(self)
```
**Functionality**

Finds a free server for a match to use, takes memory cache into consideration.

**Parameters**
```
None
```
**Response**

Response object with data being server ID.

---
##### queue_allowed(self)
```python
league(self, league_id, region).queue_allowed(self)
```
**Functionality**

Checks if the current league is over the queue limit, takes memory cache into consideration.

**Parameters**
```
None
```
**Response**

Response object with data telling us if the queue is allowed.

---
##### details(self)
```python
league(self, league_id, region).details(self)
```

**Functionality**

Returns details about the current league.

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
##### update(self, args: dict)
```python
league(self, league_id, region).update(self, args: dict)
```
**Functionality**

Updates details about the league.

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

### match(self, match_id=None)
##### create(self, players: dict, maps: dict, team_names: dict)
```python
match(self, match_id=None).create(self, players: dict, maps: dict, team_names: dict)
```
**Functionality**

Attempts to create a match off the given data. If successful it sets the match_id to the match ID it just created.

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
        - assigned_teams: bool, telling the system if the teams are pre-assigned.
        - auto_balance: bool, system will auto balance teams based off elo, can't be used if assigned_teams is true.
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
##### get(self)
```python
match(self, match_id=None).get(self)
```
**Functionality**

Gets base details about current match.

**Parameters**
```
None
```

**Response**

[Full match model](https://github.com/ModuleLIFT/API/blob/master/models/match.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### clone(self)
```py
match(self, match_id=None).clone(self)
```
**Functionality**

Attempts to clone match from current ID, returns the same data as if to create a match.

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### scoreboard(self)
```py
match(self, match_id=None).scoreboard(self)
```

**Functionality**

Gets scoreboard data for match.

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### end(self)
```python
match(self, match_id=None).end(self)
```
**Functionality**

Ends the current match.

If discord webhook is configured for the current league it attempts to send a fancy embed about the match.

If websocket is configured for the current league it attempts to send the match data to it.

**Parameters**
```
None
```

**Response**

[Full scoreboard model](https://github.com/ModuleLIFT/API/blob/master/models/scoreboard.py#L15) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### select.player(self, user_id: str)
```python
match(self, match_id=None).select.player(self, user_id: str)
```
**Functionality**

Selects player for team depending off captain turn.

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
##### select.map(self, map_id: str)
```python
match(self, match_id=None).select.map(self, map_id: str)
```
**Functionality**

Veto's map depending off captain turn.

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
### list(self, limit: int, offset: int, desc: bool, search: str = "")
##### matches(self)
```python
list(self, limit: int, offset: int, desc: bool, search: str = "").matches(self)
```
**Functionality**

Pulls matches what match ;) given parameters.

**Parameters**
```
None
```

**Response**

[Full match model](https://github.com/ModuleLIFT/API/blob/master/models/match.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### players(self)
```python
list(self, limit: int, offset: int, desc: bool, players: str = "").players(self)
```

**Functionality**

Pulls players what match given parameters.

**Parameters**
```
None
```

**Response**

[Full player model](https://github.com/ModuleLIFT/API/blob/master/models/player.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---

### player(self, user_id)
##### get(self)
```python
player(self, user_id).get(self)
```
**Functionality**

Gets full details about that player for the current league.

**Parameters**
```
None
```

**Response**

[Full player model](https://github.com/ModuleLIFT/API/blob/master/models/player.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### reset(self)
```python
player(self, user_id).reset(self)
```
**Functionality**

Resets the stats for the given player for the given league.

**Parameters**
```
None
```

**Response**

Bool inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### delete(self)
```python
player(self, user_id).delete(self)
```

**Functionality**

Deletes given player for the current league.

**Parameters**
```
None
```

**Response**

Bool inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---

### players(self, user_ids)
##### fetch(self, include_stats=False)
```python
players(self, user_ids).fetch(self, include_stats=False)
```
**Functionality**

Pulls details about list of IDs given.

**Parameters**
```
- include_stats, If we should include player stats.
```

**Response**

If include_stats equals true
[Full player model](https://github.com/ModuleLIFT/API/blob/master/models/player.py#L9) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

Otherwise
[Minimal player model](https://github.com/ModuleLIFT/API/blob/master/models/player.py#L46) inside the [response object](https://github.com/ModuleLIFT/API/blob/master/utils/response.py).

---
##### validate(self)
```python
players(self, user_ids).validate(self)
```
**Functionality**

Validates if given IDs are valid and returns invalid IDs. 

**Parameters**
```
None
```

**Response**

Returns bool if valid.
Any IDs returned in data when response errors are invalid IDs.

---

### api_key(self)
##### paths(self)
```python
api_key(self).paths(self)
```

**Functionality**

Lists all paths the league can access.

**Parameters**
```
None
```

**Response**

List

---
##### generate(self, user_id, access_level: int, active: bool = True)
```python
api_key(self).generate(self, user_id, access_level: int, active: bool = True)
```
**Functionality**

Generates a new api key for a user ID.

**Parameters**
```
- user_id, valid user ID.
- access_level, access level to grand this user.
- active, if the key should be active or not.
```

**Response**

```python
{
    "key": str,
}
```

---
#### interact(self, api_key)
##### validate(self)
```python
interact(self, api_key).validate(self)
```
**Functionality**

Validates given API Key.

**Parameters**
```
None
```

**Response**

Bool

---
##### edit(self, access_level: int, active: bool = True)
```python
interact(self, api_key).edit(self, access_level: int, active: bool = True)
```
**Functionality**

Edits given API Key.

**Parameters**
```
- access_level, New access level.
- active, If key should be active.
```

**Response**

Bool

---
##### delete(self)
```python
interact(self, api_key).delete(self)
```
**Functionality**

Deletes current API Key.

**Parameters**
```
None
```

**Response**

Bool

---
##### paths(self)
```python
interact(self, api_key).paths(self)
```
**Functionality**

Lists paths this key can access.

**Parameters**
```
None
```

**Response**

List

---