import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands, tasks
from .. import functions as f

class fake(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["fs", "fakesend", "fake-send"])
    async def fake_send(self, ctx, faked: discord.User, *, message):
      if f.is_bot_owner(ctx.author, self.client):
          webhook_found = False
          webhook_token = None
          webhook_id = None
          webhook_url = None
          for webhook in await ctx.channel.webhooks():
              if not webhook.token is None:
                  webhook_found = True
                  webhook_token = webhook.token
                  webhook_id = webhook.id
                  webhook_url = webhook.url

          if not webhook_found:
              if ctx.guild.me.permissions_in(ctx.channel).manage_webhooks:
                  webhook_found = True
                  webhook = await ctx.channel.create_webhook(name="NoobBot webhook")
                  webhook_token = webhook.token
                  webhook_id = webhook.id
                  webhook_url = webhook.url

          if webhook_found:
              try:
                  await ctx.message.delete()
              except:
                  pass
              webhook = Webhook.partial(webhook_id, webhook_token, adapter=RequestsWebhookAdapter())
              webhook.send(message, avatar_url=faked.avatar_url, username=faked.name)


def setup(bot):
    bot.add_cog(fake(bot))
