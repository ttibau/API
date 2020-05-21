from discord import Webhook, AsyncWebhookAdapter

from aiohttp_session import AIOHTTP


class WebhookSend:
    def __init__(self):
        self.adapter = AsyncWebhookAdapter(AIOHTTP.ClientSession)

    async def send(self, url, **kwargs):
        webhook = Webhook.from_url(
            url,
            adapter=self.adapter
        )

        await webhook.send(**kwargs)
