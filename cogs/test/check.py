import aiohttp
from discord.ext import commands, tasks
import json
import cogs.functions as f


class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def testcheck(self, ctx, args=""):
        response = await f.gbcheck(ctx)
        await ctx.channel.send(response)


def setup(bot):
    bot.add_cog(modulename(bot))
