class Config:
    debug = True

    timestamp = "%d %B %Y @ %I:%M %p"

    database = {
        "username": "modulelift",
        "password": "Y2ZRSsje9qZHsxDu",
        "servername": "localhost",
        "port": 3306,
        "dbname": "modulelift",
    }

    auth_bypass = [
        "/api/version/"
    ]

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
            # SHOULD ALWAYS BE LOWER CASE.
            "nz": [
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
            # key shouldn't change.
            "pfps": "pfps/{}",
            "demos": "demos/{}",
        }
    }
