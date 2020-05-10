from utils.response import response


class Proxy:
    def __init__(self, obj, ip):
        self.obj = obj
        self.values = {"ip": ip, }

    async def alt_detection(self):
        """ Does a couple checks to ensure the given IP isn't a alt. """

        exists = await self.exists()
        if exists.data:
            return response(data=True)

        ip_details = await self.get()
        if ip_details.error:
            return ip_details

        if ip_details.data["proxy"]:
            return response(data=True)

        return response(data=False)

    async def exists(self):
        """ Checks if IP already exists in our cache. """

        query = """SELECT COUNT(*) FROM ip_details
                   WHERE ip = :ip"""

        count = await self.obj.database.fetch_val(
            query=query,
            values=self.values,
        )

        return response(data=bool(count))

    async def get(self):
        """ Get's details about IP from proxycheck.io or cache. """

        query = """SELECT ip, proxy, provider, city, country
                   FROM ip_details WHERE ip = :ip"""

        row = await self.obj.database.fetch_one(
            query=query,
            values=self.values
        )

        if row:
            row_formatted = {**row}
            row_formatted["proxy"] == 1

            return response(data=row_formatted)

        ip_details = await self.obj.sessions.proxy.get(
            ip=self.values["ip"],
            flags={"asn": True, "vpn": True, }
        )

        if not ip_details or "proxy" not in ip_details:
            return response(error="Invalid proxy request")

        values = {
            "ip": self.values["ip"],
            "proxy": int(ip_details["proxy"]),
        }

        if "provider" in ip_details:
            values["provider"] = ip_details["provider"]
        else:
            values["provider"] = None

        if "city" in ip_details:
            values["city"] = ip_details["city"]
        else:
            values["city"] = None

        if "country" in ip_details:
            values["country"] = ip_details["country"]
        else:
            values["country"] = None

        query = """INSERT INTO ip_details (
                        ip,
                        proxy,
                        provider,
                        city,
                        country
                   )
                   VALUES (
                        :ip,
                        :proxy,
                        :provider,
                        :city,
                        :country
                   )"""
        await self.obj.database.execute(query=query, values=values)

        values["proxy"] = bool(values["proxy"])
        return response(data=values)
