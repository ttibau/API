class Config(object):
    debug = True

    database = {
        "username": "",
        "password": "",
        "servername": "",
        "port": 3306,
        "dbname": "",
    }

    auth_bypass = [
        "/api/version/"
    ]

    # Anyone with access to this key
    # can bypass all authorization.
    # Should be something generated like "import secrets; print(secrets.token_urlsafe(48))"
    master_key = ""

    cache = {
        "max_age": 60,
        "max_amount": 50,
    }

    proxyio = {
        "key": "",
    }

    pterodactyl = {
        "key": "",
        "route": "",

        # Cached on boot and on change.
        "regions": {}
    }

    pug = {
        # Caches selection ID types on boot.
        "selection_types": {
            "ABBAABBA": None,
            "ABBABABA": None,
            "ABABABAB": None,
        },
    }