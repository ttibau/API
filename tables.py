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

'''
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
'''

# TEMP NON ORM
# API tables
sqlalchemy.Table(
    "api_keys",
    metadata,
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("users.user_id")
    ),
    sqlalchemy.Column(
        "key",
        sqlalchemy.String(length=36),
        primary_key=True
    ),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
    sqlalchemy.Column(
        "access_level",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "active",
        sqlalchemy.Boolean
    ),
)

sqlalchemy.Table(
    "api_paths",
    metadata,
    sqlalchemy.Column(
        "path_id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    ),
    sqlalchemy.Column(
        "path",
        sqlalchemy.String(length=64)
    ),
)

sqlalchemy.Table(
    "api_permissions",
    metadata,
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
    sqlalchemy.Column(
        "path_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("api_paths.path_id")
    ),
    sqlalchemy.Column(
        "access_level",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "method",
        sqlalchemy.String(length=10),
    ),
)

sqlalchemy.Table(
    "elo_settings",
    metadata,
    sqlalchemy.Column(
        "elo_id",
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    ),
    sqlalchemy.Column(
        "kill",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "death",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "round_won",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "round_lost",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "match_won",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "match_lost",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "assist",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "mate_blined",
        sqlalchemy.Float
    ),
    sqlalchemy.Column(
        "mate_killed",
        sqlalchemy.Float
    ),
)

# Basic league info
# knife_round
# 0 - Disabled
# 1 - Enabled

# pause
# If no time given in seconds its disabled.

# warmup_commands_only
# Commands can only be used during warmup.

# captain_choice_time
# Max amount of time for a captain choice.

# surrender
# If teams are allowed to surrender.
sqlalchemy.Table(
    "league_info",
    metadata,
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        primary_key=True
    ),
    sqlalchemy.Column(
        "league_name",
        sqlalchemy.String(length=32)
    ),
    sqlalchemy.Column(
        "league_website",
        sqlalchemy.String(length=255)
    ),
    sqlalchemy.Column(
        "websocket_endpoint",
        sqlalchemy.String(length=255),
        nullable=True,
    ),
    sqlalchemy.Column(
        "discord_webhook",
        sqlalchemy.String(length=255),
        nullable=True,
    ),
    sqlalchemy.Column(
        "queue_limit",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "discord_prefix",
        sqlalchemy.String(length=3)
    ),
    sqlalchemy.Column(
        "sm_message_prefix",
        sqlalchemy.String(length=24)
    ),
    sqlalchemy.Column(
        "knife_round",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "pause",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "surrender",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "warmup_commands_only",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "captain_choice_time",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "elo_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("elo_settings.elo_id")
    ),
)

# Queue Channels
# queue_type
# 0 - bot interface
# 1 - website interface
sqlalchemy.Table(
    "league_queues",
    metadata,
    sqlalchemy.Column(
        "channel_id",
        sqlalchemy.BigInteger,
        primary_key=True
    ),
    sqlalchemy.Column(
        "guild_id",
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("league_discords.guild_id")
    ),
    sqlalchemy.Column(
        "queue_size",
        sqlalchemy.Integer
    ),
)

# Admins & Owners
# Access Levels
# 0 = Owner
# 1 = Admin
# 2 = Moderator
# 3 = Anti cheat reviewer
# 4 = Demo reviewer
# 5 = Sepecator
sqlalchemy.Table(
    "league_admins",
    metadata,
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("users.user_id")
    ),
    sqlalchemy.Column(
        "access_level",
        sqlalchemy.Integer
    ),
)

# User account details
sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.String(length=36),
        primary_key=True
    ),
    sqlalchemy.Column(
        "steam_id",
        sqlalchemy.String(length=64),
        primary_key=True,
        nullable=True
    ),
    sqlalchemy.Column(
        "discord_id",
        sqlalchemy.BigInteger,
        primary_key=True,
        nullable=True
    ),
    sqlalchemy.Column(
        "name",
        sqlalchemy.String(length=36)
    ),
    sqlalchemy.Column(
        "joined",
        sqlalchemy.types.TIMESTAMP,
        server_default=sqlalchemy.text("CURRENT_TIMESTAMP()")
    ),
    sqlalchemy.Column(
        "ip_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("ip_details.ip_id")
    ),
)

# Region table
sqlalchemy.Table(
    "regions",
    metadata,
    sqlalchemy.Column(
        "region",
        sqlalchemy.String(length=4),
        primary_key=True
    ),
)

# League Discords
sqlalchemy.Table(
    "league_discords",
    metadata,
    sqlalchemy.Column(
        "guild_id",
        sqlalchemy.BigInteger,
        primary_key=True
    ),
    sqlalchemy.Column(
        "region",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("regions.region")
    ),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
)

# IP details / Proxy caching
sqlalchemy.Table(
    "ip_details",
    metadata,
    sqlalchemy.Column(
        "ip_id",
        sqlalchemy.String(length=36),
        primary_key=True
    ),
    sqlalchemy.Column(
        "ip",
        sqlalchemy.String(length=39)
    ),
    sqlalchemy.Column(
        "region",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("regions.region")
    ),
    sqlalchemy.Column(
        "proxy",
        sqlalchemy.Boolean
    ),
    sqlalchemy.Column(
        "provider",
        sqlalchemy.String(length=124)
    ),
    sqlalchemy.Column(
        "city",
        sqlalchemy.String(length=64)
    ),
    sqlalchemy.Column(
        "country",
        sqlalchemy.String(length=64)
    ),
)

# Scoreboard
# Status codes
# 0 - Finished
# 1 - Live
# 2 - Map selection
# 3 - Player selection
sqlalchemy.Table(
    "scoreboard_total",
    metadata,
    sqlalchemy.Column(
        "match_id",
        sqlalchemy.String(length=36),
        primary_key=True
    ),
    sqlalchemy.Column(
        "server_id",
        sqlalchemy.String(length=36)
    ),
    sqlalchemy.Column(
        "map_order",
        sqlalchemy.String(length=20),
        nullable=True
    ),
    sqlalchemy.Column(
        "player_order",
        sqlalchemy.String(length=20),
        nullable=True
    ),
    sqlalchemy.Column(
        "timestamp",
        sqlalchemy.types.TIMESTAMP,
        server_default=sqlalchemy.text("CURRENT_TIMESTAMP()")
    ),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "map",
        sqlalchemy.String(length=24), server_default="NULL"
    ),
    sqlalchemy.Column(
        "region",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("regions.region")
    ),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
    sqlalchemy.Column(
        "team_1_name",
        sqlalchemy.String(length=64)
    ),
    sqlalchemy.Column(
        "team_2_name",
        sqlalchemy.String(length=64)
    ),
    sqlalchemy.Column(
        "team_1_score",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "team_2_score",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "team_1_side",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "team_2_side",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "record_statistics",
        sqlalchemy.Boolean,
        server_default="1"
    ),
)

# Team Codes
# 0 Teamless
# 1 = CT
# 2 = T
sqlalchemy.Table(
    "scoreboard",
    metadata,
    sqlalchemy.Column(
        "match_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("scoreboard_total.match_id")
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("users.user_id")
    ),
    sqlalchemy.Column(
        "captain",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "team",
        sqlalchemy.Integer
    ),
    sqlalchemy.Column(
        "alive",
        sqlalchemy.Integer,
        server_default="1"
    ),
    sqlalchemy.Column(
        "ping",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "kills",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "headshots",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "assists",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "deaths",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "shots_fired",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "shots_hit",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "mvps",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "score",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "disconnected",
        sqlalchemy.Boolean,
        server_default="0"
    ),
)

# Match Map Pool
# Data is delete from here once match has ended.
sqlalchemy.Table(
    "map_pool",
    metadata,
    sqlalchemy.Column(
        "match_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("scoreboard_total.match_id")
    ),
    sqlalchemy.Column(
        "map",
        sqlalchemy.String(length=24)
    ),
)

# Statistics
# user_id isn't unique here,
# different regions have different stats.
sqlalchemy.Table(
    "statistics",
    metadata,
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.String(length=36),
        sqlalchemy.ForeignKey("users.user_id")
    ),
    sqlalchemy.Column(
        "league_id",
        sqlalchemy.String(length=4),
        sqlalchemy.ForeignKey("league_info.league_id")
    ),
    sqlalchemy.Column(
        "region",
        sqlalchemy.String(length=4), sqlalchemy.ForeignKey("regions.region")
    ),
    sqlalchemy.Column(
        "last_connected",
        sqlalchemy.types.TIMESTAMP,
        server_default=sqlalchemy.text("""CURRENT_TIMESTAMP()
                                            ON UPDATE CURRENT_TIMESTAMP()""")
    ),
    sqlalchemy.Column(
        "total_time",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "elo",
        sqlalchemy.Float,
        server_default="0"
    ),
    sqlalchemy.Column(
        "kills",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "deaths",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "assists",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "shots",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "hits",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "damage",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "headshots",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "rounds_won",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "rounds_lost",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "wins",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "ties",
        sqlalchemy.Integer,
        server_default="0"
    ),
    sqlalchemy.Column(
        "loses",
        sqlalchemy.Integer,
        server_default="0"
    ),
)
# TEMP NON ORM END


class Tables:
    def __init__(self, obj):
        """ Ensures all the tables have been built correctly. """

        '''
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
        '''

        engine = sqlalchemy.create_engine(
            str(
                database_url.replace(driver="pymysql")
            ) + "?charset=utf8mb4"
        )

        metadata.create_all(engine)

        obj.database = database

        '''
        for table in tables:
            setattr(self, table.__name__, table)
        '''
