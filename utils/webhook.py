from discord import Webhook, AsyncWebhookAdapter


class WebhookSend:
    def __init__(self, aiohttp_session):
        self.adapter = AsyncWebhookAdapter(aiohttp_session)

    async def send(self, url, **kwargs):
        webhook = Webhook.from_url(
            url,
            adapter=self.adapter
        )

        await webhook.send(**kwargs)
