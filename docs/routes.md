


## Match
Manage matches with match route

### New Match
`POST /api/match/`

### Parameters

**Player Parameters:**
| Name    | Type   | Required | Description                                                                                                                                                                                          |
|---------|--------|----------|--------------------------|
| options | Dictionary |    Yes   | The players match config |                                                                                                                                                                                              |
| type    | String |    Yes   | The match type: <br> - **random**: select captains randomly based on the list of players. <br>- **elo**: selects captains depending off highest elo. <br>- **given**: selects captain depending off given indexes in param.          | 
|    param     |    Dictionary|     Only is required if  type is **given**     |          Gives the capt_1 and capt_2 index in a list           |      
|    selection|       String     |  Only required if  players aren't assigned teams      | Expects string containing only A & B what tells the system the order of selections. The string must be the same length of the players given ignoring the captain    |  
| assigned_teams  | Boolean  | No   | Telling the system if the teams are pre assigned  |     
auto_balance | Boolean | No |  System will auto balance teams based off elo, **can't be used if assigned_teams is true**  |                
| record_statistics | Boolean | No | If we should record statistics or not  |
| list | Dictionary | Yes | Expects keys to be user ID & value to being the team (1, 2 or None / Null for no team) |                                                                                          

**Maps Parameters:**
| Name 	| Type 	| Required 	| Description 	|
|---------|--------|----------|--------------------------|
| options 	|  Dictionary	| Yes	| The maps match config 	|
| type 	|  String 	| Yes 	|  The map selection type: <br> - **veto:** captains veto maps <br> - **random:** maps are randomly selected <br> - **given:** map is given (Uses 1st index of map list)	|
| list 	|  List | Yes 	| Listof valid map names e.g. **de_mirage** 	|

**Team Names Parameters:**
| Name 	| Type 	| Required 	| Description 	|
|---------|--------|----------|--------------------------|
| team_1 	|  Dictionary	|  Yes	| Name of team 1 (max 20 characters.)	|
| team_2 	|  Dictionary	|  Yes	| Name of team 2 (max 20 characters.)	|


```javascript
{
	Players: {
		options: {
			type: 'given', // 
			param: {
				capt_1: 0,
				capt_2: 1
			},
			assigned_teams: true, 
			record_statistcs: true 
		},
		list: [
			{ '5d3e0a22-38cd-4509-a698-42398a6c6632': 1 },
			{ 'dd9d827a-d324-43f0-bb56-d0446dad9cea': 1 },
			{ '49bc2ff3-49ec-430d-b27f-6c2b088d92f3': 1 },
			{ 'f26cc486-3ea2-4b9b-8d86-172c3328aed7': 1 },
			{ '5d3e0a22-38cd-4509-a698-42398a6c6632': 1 },
			{ 'dd9d827a-d324-43f0-bb56-d0446dad9cea': 2 },
			{ '49bc2ff3-49ec-430d-b27f-6c2b088d92f3': 2 },
			{ 'f26cc486-3ea2-4b9b-8d86-172c3328aed7': 2 },
			{ '49bc2ff3-49ec-430d-b27f-6c2b088d92f3': 2 },
			{ 'f26cc486-3ea2-4b9b-8d86-172c3328aed7': 2 }
		]
	},
	Maps: {
		options: {
			type: 'veto',
		},
		list: [
			'de_mirage', 
			'de_overpass',
			'de_dust2', 
			'de_inferno'
		]
	},
	team_names: {
		team_1: 'team_TibauTV',
		team_2: 'team_Ward'
	}
}
```


### Response
- **userId** - Identifier for the user

### Errors
- **ErrorCode1** - Caused by missing identifier
- **ErrorCode2** - Username was not given
- **ErrorCode3** - Server exploded

### Example Request
`GET /account/1692/profile`

```javascript
{
	username: "NewUsername",
	email: "Email@Email.com"
}
```

### Example Response
`200 OK`

```javascript
{
	userId: 1692
}
```

## List

### Get Players List:
`GET /api/list/players/`

#### Parameters:
`None`

#### Response: 

``` javascript
[
	{
		name: "John Doe", 
		user_id: '5d3e0a22-38cd-4509-a698-42398a6c6632',
		steam_id: '[STEAM_0:0:88691122]',
		discord_id: '123123123123', 
		pfp: 'https://example.com/users/uuid4.png',
		joined: '1528797322',
		statistics: {
			kills: 8,
			deaths: 1,
			assists: 4,
			shots: 140,
			hits: 331,
			damage: 1076,
			headshots: 3,
			rounds_won: 6,
			rounds_lost: 3,
			wins: 1, 
			ties: 0,
			loses: 1
		},
		ranking: {
			elo: 1762
		}
	}, 
	{
		name: "John Doe", 
		user_id: '5d3e0a22-38cd-4509-a698-42398a6c6632',
		steam_id: '[STEAM_0:0:88691122]',
		discord_id: '123123123123', 
		pfp: 'https://example.com/users/uuid4.png',
		joined: '1528797322',
		statistics: {
			kills: 8,
			deaths: 1,
			assists: 4,
			shots: 140,
			hits: 331,
			damage: 1076,
			headshots: 3,
			rounds_won: 6,
			rounds_lost: 3,
			wins: 1, 
			ties: 0,
			loses: 1
		},
		ranking: {
			elo: 1762
		}
	},
	{
		name: "John Doe", 
		user_id: '5d3e0a22-38cd-4509-a698-42398a6c6632',
		steam_id: '[STEAM_0:0:88691122]',
		discord_id: '123123123123', 
		pfp: 'https://example.com/users/uuid4.png',
		joined: '1528797322',
		statistics: {
			kills: 8,
			deaths: 1,
			assists: 4,
			shots: 140,
			hits: 331,
			damage: 1076,
			headshots: 3,
			rounds_won: 6,
			rounds_lost: 3,
			wins: 1, 
			ties: 0,
			loses: 1
		},
		ranking: {
			elo: 1762
		}
	}
]
```
