
## Match
Manage matches with match route

### New Match
`POST /api/match/`

#### Parameters
- **players** - list of player in a match
- **maps** - list of maps in a match
- **team_names** - name of both teams in a match

| Name    | Type   | required | Description              | Example                                                                                                                                                                                      |
|---------|--------|----------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| options | Object |    yes   | The players match config |                                                                                                                                                                                              |
| type    | String |    yes   | The match type           | - **random**: select captains randomly based on the list of players. <br>- **elo**: selects captains depending off highest elo. <br>- **given**: selects captain depending off given indexes in param.   |
|         |        |          |                          |                                                                                                                                                                                              |
|         |        |          |                          |                                                                                                                                                                                              |                                                                                                                                                                                     |

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
