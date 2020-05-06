class Config:
    # Human friendly address for the API.
    # must end in a slash.
    website = "http://localhost:8888/"

    debug = True

    timestamp = "%d %B %Y @ %I:%M %p"

    database = {
        "username": "modulelift",
        "password": "Y2ZRSsje9qZHsxDu",
        "servername": "localhost",
        "port": 3306,
        "dbname": "modulelift",
    }

    # Anyone with access to this key
    # can bypass all authorization.
    # Should be something generated like
    # "import secrets; print(secrets.token_urlsafe(48))"
    master_key = "placeholder"

    cache = {
        "max_age": 60,
        "max_amount": 50,
    }

    proxyio = {
        "key": "",
    }

    regions = {
        # Unique region code
        # and all iso codes what fall under it.
        "OCE": [
            "AU",
            "NZ",
        ],
    }

    server = {
        # pterodactyl application key, dathost key or pes key.
        # incase of dathost just do username/password
        "key": "",

        # https://pterodactyl.io/
        # self hosting using the pterodactyl control panel.
        "pterodactyl": {
            "enabled": True,

            # Route to your pterodactyl panel ending in
            # /api
            "route": "https://example.com/api",
        },

        # https://dathost.net/
        "dathost": {
            "enabled": False,
        },

        # https://www.pacifices.cloud/
        "pes": {
            "enabled": False,
        },

        # Cached on boot and on change.
        "regions": {
            # Region code for that server.
            # SHOULD ALWAYS BE lower case.
            "oce": [
                # Unique ID for server
                # given by host.
                "server_id"
            ],
        },
    }

    cdn = {
        # Link to CDN, ENDING IN A SLASH!!
        "link": "",
        # For b2 this should be the bucket ID.
        # For s3 this should be the bucket name.
        # Bucket needs to be public.
        "bucket": "",
        "b2": {
            "enabled": False,
            "application_key_id": "",
            "application_key": "",
        },
        "s3": {
            "enabled": True,
            "secret_access_key": "",
            "access_key_id": "",
            "region_name": "",
            "endpoint_url": "",
        },
        "paths": {
            # Folder to store under in the bucket
            # {} is where the filename will go.
            # key should NEVER change.
            "pfps": "pfps/{}",
            "demos": "demos/{}",
        }
    }

    steam = {
        "endpoint": "https://steamcommunity.com/",
    }

    login = {
        # If discord enabled
        # 1st time users ever log in
        # they will have to login with both
        # steam & discord, discord will be used
        # for caching name & pfp onto b2/s3.
        "discord": {
            "enabled": True,
            "endpoint": "",
            # Found at https://discordapp.com/developers/
            "client_id": "",
            "client_secret": "",
        },
        "steam": {
            "route": "steam/login",
            "return": "steam/validate",
        }
    }
