import uvicorn

from starlette.applications import Starlette

from routes.router import ROUTES, EXCEPTION_HANDLERS
from middlewares import MIDDLEWARES

from settings import Config

import modulelift

print("-"*62)

print(r"  __  __           _       _      _      _____ ______ _______ ")
print(r" |  \/  |         | |     | |    | |    |_   _|  ____|__   __|")
print(r" | \  / | ___   __| |_   _| | ___| |      | | | |__     | |   ")
print(r" | |\/| |/ _ \ / _` | | | | |/ _ \ |      | | |  __|    | |   ")
print(r" | |  | | (_) | (_| | |_| | |  __/ |____ _| |_| |       | |   ")
print(r" |_|  |_|\___/ \__,_|\__,_|_|\___|______|_____|_|       |_|   ")
print("\nCreated by the ModuleLFIT team.")
print("https://github.com/ModuleLIFT\n")

print("-"*62)

app = Starlette(
    debug=Config.debug,
    routes=ROUTES,
    middleware=MIDDLEWARES,
    exception_handlers=EXCEPTION_HANDLERS,
    on_startup=[modulelift.CLIENT.startup],
    on_shutdown=[modulelift.CLIENT.shutdown],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888)
