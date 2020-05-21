from memory_cache import IN_MEMORY_CACHE


class QueueCache:
    server_id = None

    def __init__(self, league_id):
        """ Handles caching league active queues
            & blacked listed servers for edge cases. """

        # Once this queue is inserted into the database or it fails
        # -1 is removed from in_memory_cache.started_queues for this
        # league ID.
        if league_id in IN_MEMORY_CACHE.started_queues:
            IN_MEMORY_CACHE.started_queues[league_id] += 1
        else:
            IN_MEMORY_CACHE.started_queues[league_id] = 1

        self.league_id = league_id

    def server(self, server_id):
        """ Adds server ID to temp blacklist. """

        IN_MEMORY_CACHE.temp_server_blacklist.append(server_id)

        self.server_id = server_id

        return server_id

    def clear(self):
        """ Clears cached data for current league out of memory. """

        if self.server_id:
            if self.server_id in IN_MEMORY_CACHE.temp_server_blacklist:
                IN_MEMORY_CACHE.temp_server_blacklist.remove(self.server_id)

        if self.league_id in IN_MEMORY_CACHE.started_queues:
            if IN_MEMORY_CACHE.started_queues[self.league_id] == 1:
                IN_MEMORY_CACHE.started_queues.pop(
                    self.league_id
                )
            else:
                IN_MEMORY_CACHE.started_queues[self.league_id] -= 1
