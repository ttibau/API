# Documentation
- [Modules](#modules)
- [Routes](#routes)

## Modules 
#### modulelift.client
Expects ``server_init()`` to be called after aiohttp session has been passed within loop context.

#### modulelift.client.league(self, league_id, region)
- get_server(self)
- queue_allowed(self)
- details(self)
- update(self, args: dict)

###### match(self, match_id=None)
    - create(self, players: dict, maps: dict, team_names: dict)
    - get(self)
    - clone(self)
    - scoreboard(self)
    - end(self)
    - players(self) - being developed
    - select_player(self, user_id: str) - being developed
    - select_map(self, map_id: str) - being developed

###### list(self, limit: int, offset: int, desc: bool, search: str = "")
    - matches(self)
    - players(self)

###### player(self, user_id)
    - get(self)
    - reset(self)
    - delete(self)

###### players(self, user_ids)
    - fetch(self, include_stats=False)
    - validate(self)

## Routes
Coming soon