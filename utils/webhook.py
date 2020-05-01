from discord import Webhook, AsyncWebhookAdapter


class WebhookSend:
    def __init__(self, aiohttp_session):
        self.aiohttp_session = aiohttp_session

    async def send(self, url, **kwargs):
        webhook = Webhook.from_url(
            url,
            adapter=AsyncWebhookAdapter(self.aiohttp_session)
        )

        await webhook.send(**kwargs)
