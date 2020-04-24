from starlette.applications import Starlette

import uvicorn
import asyncio
import aiohttp
import aiodactyl

from aioproxyio import proxy_io

import modulelift

ml = modulelift.client()

async def startup_task():
    print("-"*62)
    
    print("  __  __           _       _      _      _____ ______ _______ ")
    print(" |  \/  |         | |     | |    | |    |_   _|  ____|__   __|")
    print(" | \  / | ___   __| |_   _| | ___| |      | | | |__     | |   ")
    print(" | |\/| |/ _ \ / _` | | | | |/ _ \ |      | | |  __|    | |   ")
    print(" | |  | | (_) | (_| | |_| | |  __/ |____ _| |_| |       | |   ")
    print(" |_|  |_|\___/ \__,_|\__,_|_|\___|______|_____|_|       |_|   ")
    print("\nCreated by the ModuleLFIT team.")
    print("https://github.com/ModuleLIFT\n")

    print("-"*62)

    ml.sessions.aiohttp = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    ml.sessions.proxy = proxy_io(api_key=ml.config.proxyio["key"], session=ml.sessions.aiohttp)
    ml.sessions.dactyl = aiodactyl.client(api_key=ml.config.pterodactyl["key"], route=ml.config.pterodactyl["route"],
                                          session=ml.sessions.aiohttp)
    await ml.database.connect()

async def shutdown_task():
    await ml.sessions.aiohttp.close()
    await ml.database.disconnect()

app = Starlette(
    debug=ml.config.debug,
    routes=ml.routes.list,
    middleware=ml.middlewares.list,
    exception_handlers=ml.routes.exception_handlers,
    on_startup=[startup_task],
    on_shutdown=[shutdown_task],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)