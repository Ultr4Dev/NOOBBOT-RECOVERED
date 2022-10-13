from .utils import *

class startup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.cache = {"prefixes": {}, "auto_react": {}}

        self.client.utils = Utils(self.client)
        self.client.utils.paginator = Paginator
        webhook_info = self.client.info["console_webhook"]
        self.client.console_webhook = Webhook.partial(webhook_info["id"], webhook_info["token"], adapter=RequestsWebhookAdapter())




    @commands.Cog.listener()
    async def on_ready(self):
        self.client.db = await self.client.utils.connect()
        await self.client.utils.recache()
        print("connected and cached")

def setup(client):
    print("starting")
    client.add_cog(startup(client))
