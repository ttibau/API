from starlette.applications import Starlette

import uvicorn

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

ml = modulelift.client()


app = Starlette(
    debug=Config.debug,
    routes=ml.routes.list,
    middleware=ml.middlewares.list,
    exception_handlers=ml.routes.exception_handlers,
    on_startup=[ml.startup],
    on_shutdown=[ml.shutdown],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8888)
