import discord
from discord.ext import commands, tasks
from .. import functions as f

class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.client.get_channel(payload.channel_id)

        try:
            msg = await channel.fetch_message(payload.message_id)
        except:
            pass
        else:
            await self.client.process_commands(msg)

def setup(bot):
    bot.add_cog(modulename(bot))
