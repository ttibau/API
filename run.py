from starlette.applications import Starlette

import uvicorn
import sys

from settings import Config as config

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

ml = modulelift.client()

# Security checks.
if len(config.master_key) < 48 and not config.debug:
    sys.exit("Master key must be 48 characters or longer.")


async def startup_task():
    await ml.context_init()


async def shutdown_task():
    await ml.clean_up()


app = Starlette(
    debug=config.debug,
    routes=ml.routes.list,
    middleware=ml.middlewares.list,
    exception_handlers=ml.routes.exception_handlers,
    on_startup=[startup_task],
    on_shutdown=[shutdown_task],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888)
