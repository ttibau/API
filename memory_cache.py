class InMemoryCache:
    api_key = []
    api_key_requests = {}

    started_queues = {}
    temp_server_blacklist = []
