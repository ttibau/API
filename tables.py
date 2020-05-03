from databases import Database, DatabaseURL

from datetime import datetime

from settings import Config as config

from utils.misc import Misc

import sqlalchemy
import orm

database_url = DatabaseURL(
    "mysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
                                            config.database["username"],
                                            config.database["password"],
                                            config.database["servername"],
                                            config.database["port"],
                                            config.database["dbname"])
)

database = Database(database_url)

metadata = sqlalchemy.MetaData()


class EloSettings(orm.Model):
    __tablename__ = "elo_settings"
    __database__ = database
    __metadata__ = metadata

    elo_id = orm.String(
        primary_key=True,
        max_length=36,
        default=Misc.uuid4
    )
    kill = orm.Float(
        default=0.0
    )
    death = orm.Float(
        default=0.0
    )
    round_won = orm.Float(
        default=0.0
    )
    round_lost = orm.Float(
        default=0.0
    )
    match_won = orm.Float(
        default=0.0
    )
    match_lost = orm.Float(
        default=0.0
    )
    assist = orm.Float(
        default=0.0
    )
    mate_blined = orm.Float(
        default=0.0
    )
    mate_killed = orm.Float(
        default=0.0
    )


class LeagueInfo(orm.Model):
    __tablename__ = "league_info"
    __database__ = database
    __metadata__ = metadata

    league_id = orm.String(
        max_length=4,
        primary_key=True
    )
    league_name = orm.String(
        max_length=32
    )
    league_website = orm.String(
        max_length=255
    )
    websocket_endpoint = orm.String(
        max_length=255
    )
    queue_limit = orm.Integer()
    discord_prefix = orm.String(
        max_length=4
    )
    sm_message_prefix = orm.String(
        max_length=24
    )
    knife_route = orm.Boolean()
    pause = orm.Integer()
    surrender = orm.Integer()
    warmup_commands_only = orm.Boolean()
    captain_choice_time = orm.Integer()
    elo_id = orm.ForeignKey(
        EloSettings,
        allow_null=True
    )


class Regions(orm.Model):
    __tablename__ = "regions"
    __database__ = database
    __metadata__ = metadata

    region = orm.String(
        primary_key=True,
        max_length=4
    )


class LeagueDiscords(orm.Model):
    __tablename__ = "league_discords"
    __database__ = database
    __metadata__ = metadata

    guild_id = orm.Integer(
        primary_key=True
    )
    region = orm.ForeignKey(Regions)
    league_id = orm.ForeignKey(LeagueInfo)


class LeagueQueues(orm.Model):
    __tablename__ = "league_queues"
    __database__ = database
    __metadata__ = metadata

    channel_id = orm.Integer(
        primary_key=True
    )
    queue_size = orm.Integer()
    guild_id = orm.ForeignKey(LeagueDiscords)


class IpDetails(orm.Model):
    __tablename__ = "ip_details"
    __database__ = database
    __metadata__ = metadata

    ip_id = orm.String(
        primary_key=True,
        max_length=36,
        default=Misc.uuid4
    )
    ip = orm.String(
        max_length=39
    )
    region = orm.ForeignKey(Regions)
    proxy = orm.Boolean()
    provider = orm.String(
        max_length=124,
        allow_null=True
    )
    city = orm.String(
        max_length=64,
        allow_null=True
    )
    country = orm.String(
        max_length=64,
        allow_null=True
    )


class Users(orm.Model):
    __tablename__ = "users"
    __database__ = database
    __metadata__ = metadata

    user_id = orm.String(
        primary_key=True,
        max_length=36,
        default=Misc.uuid4
    )
    steam_id = orm.String(
        max_length=64,
        allow_null=True,
    )
    discord_id = orm.Integer(
        allow_null=True
    )
    name = orm.String(
         max_length=36
    )
    joined = orm.DateTime(
        default=datetime.now
    )
    ip_id = orm.ForeignKey(IpDetails)


class ScoreboardTotal(orm.Model):
    __tablename__ = "scoreboard_total"
    __database__ = database
    __metadata__ = metadata

    match_id = orm.String(
        primary_key=True,
        max_length=36,
        default=Misc.uuid4
    )
    server_id = orm.String(
        max_length=36
    )
    map_order = orm.String(
        max_length=14
    )
    player_order = orm.String(
        max_length=14
    )
    timestamp = orm.DateTime(
        default=datetime.now
    )
    status = orm.Integer()
    map = orm.String(
        max_length=24,
        allow_null=True
    )
    region = orm.ForeignKey(Regions)
    league_id = orm.ForeignKey(LeagueInfo)
    team_1_name = orm.String(
        max_length=32
    )
    team_2_name = orm.String(
        max_length=32
    )
    team_1_score = orm.Integer(
        default=0
    )
    team_2_score = orm.Integer(
        default=0
    )
    team_1_side = orm.Integer(
        allow_null=True
    )
    team_2_side = orm.Integer(
        allow_null=True
    )
    record_statistics = orm.Boolean()


# Team Codes
# 0 Teamless
# 1 = CT
# 2 = T
class Scoreboard(orm.Model):
    __tablename__ = "scoreboard"
    __database__ = database
    __metadata__ = metadata

    match_id = orm.ForeignKey(ScoreboardTotal)
    user_id = orm.ForeignKey(Users)
    captain = orm.Boolean(
        default=False
    )
    team = orm.Integer()
    alive = orm.Integer(
        default=1
    )
    ping = orm.Integer(
        default=0
    )
    kills = orm.Integer(
        default=0
    )
    headshots = orm.Integer(
        default=0
    )
    assists = orm.Integer(
        default=0
    )
    deaths = orm.Integer(
        default=0
    )
    shots_fired = orm.Integer(
        default=0
    )
    shots_hit = orm.Integer(
        default=0
    )
    mvps = orm.Integer(
        default=0
    )
    score = orm.Integer(
        default=0
    )
    disconnected = orm.Boolean(
        default=False
    )


# Match Map Pool
# Everything is this table is temp.
# It's deleted as used.
class MapPool(orm.Model):
    __tablename__ = "map_pool"
    __database__ = database
    __metadata__ = metadata

    match_id = orm.ForeignKey(ScoreboardTotal)
    map = orm.String(
        max_length=24
    )


class Statistics(orm.Model):
    __tablename__ = "statistics"
    __database__ = database
    __metadata__ = metadata

    user_id = orm.ForeignKey(Users)
    league_id = orm.ForeignKey(LeagueInfo)
    region = orm.ForeignKey(Regions)
    last_connected = orm.DateTime(
        default=sqlalchemy.text("""CURRENT_TIMESTAMP()
                                   ON UPDATE CURRENT_TIMESTAMP()""")
    )
    total_time = orm.Integer(
        default=0
    )
    elo = orm.Float(
        default=0.0
    )
    kills = orm.Integer(
        default=0
    )
    deaths = orm.Integer(
        default=0
    )
    assists = orm.Integer(
        default=0
    )
    shots = orm.Integer(
        default=0
    )
    hits = orm.Integer(
        default=0
    )
    damage = orm.Integer(
        default=0
    )
    headshots = orm.Integer(
        default=0
    )
    rounds_won = orm.Integer(
        default=0
    )
    rounds_lost = orm.Integer(
        default=0
    )
    wins = orm.Integer(
        default=0
    )
    ties = orm.Integer(
        default=0
    )
    loses = orm.Integer(
        default=0
    )


# Admins & Owners
# Access Levels
# 0 = Owner
# 1 = Admin
# 2 = Moderator
# 3 = Anti cheat reviewer
# 4 = Demo reviewer
# 5 = Sepecator
class LeagueAdmins(orm.Model):
    __tablename__ = "league_admins"
    __database__ = database
    __metadata__ = metadata

    league_id = orm.ForeignKey(LeagueInfo)
    user_id = orm.ForeignKey(Users)
    access_level = orm.Integer()


class ApiKeys(orm.Model):
    __tablename__ = "api_keys"
    __database__ = database
    __metadata__ = metadata

    key = orm.String(
        primary_key=True,
        max_length=24,
        default=Misc.api_key
    )
    access_level = orm.Integer()
    active = orm.Boolean()
    user_id = orm.ForeignKey(Users)
    league_id = orm.ForeignKey(LeagueInfo)


class ApiPaths(orm.Model):
    __tablename__ = "api_paths"
    __database__ = database
    __metadata__ = metadata

    path_id = orm.String(
        primary_key=True,
        max_length=36,
        default=Misc.uuid4
    )
    path = orm.String(
        max_length=64
    )


class ApiPerms(orm.Model):
    __tablename__ = "api_permissions"
    __database__ = database
    __metadata__ = metadata

    path_id = orm.ForeignKey(ApiPaths)
    league_id = orm.ForeignKey(LeagueInfo)
    method = orm.String(
        max_length=10
    )
    access_level = orm.Integer()


class Tables:
    def __init__(self, obj):
        """ Ensures all the tables have been built correctly. """

        tables = [
            Users,
            ApiPaths,
            ApiPerms,
            ApiKeys,
            IpDetails,
            Regions,
            EloSettings,
            LeagueInfo,
            LeagueDiscords,
            LeagueQueues,
            LeagueAdmins,
            ScoreboardTotal,
            Scoreboard,
            MapPool,
            Statistics,
        ]

        engine = sqlalchemy.create_engine(
            str(
                database_url.replace(driver="pymysql")
            ) + "?charset=utf8mb4"
        )

        metadata.create_all(engine)

        obj.database = database

        for table in tables:
            setattr(self, table.__name__, table)
