from databases import Database, DatabaseURL

from settings import Config
from tables import Tables

from routes.router import Routes
from middlewares.middlewares import Middlewares

from utils.memory_cache import InMemoryCache
from utils.sessions import Sessions
from utils.api import Api
from utils.server import Server

from modules.league import League

class client:
    config = Config

    database_url = DatabaseURL("mysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(config.database["username"], 
                                                                               config.database["password"], 
                                                                               config.database["servername"], 
                                                                               config.database["port"], 
                                                                               config.database["dbname"]))

    database = Database(database_url)

    in_memory_cache = InMemoryCache
    sessions = Sessions

    def __init__(self):
        """ This client assumes the developer has taken the initiative to correctly initialize the needed sessions. """

        self.routes = Routes(obj=self)
        self.middlewares = Middlewares(obj=self)
        self.api = Api(obj=self)
        self.tables = Tables(obj=self)

    def server_init(self):
        """ Should be ran within context of the loop after the aiohttp session is created. """

        self.server = Server(obj=self).client

    def league(self, league_id, region):
        return League(obj=self, league_id=league_id, region=region)