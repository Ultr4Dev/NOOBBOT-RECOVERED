import discord
from discord.ext import commands, tasks
import aiohttp


class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roastme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.rappad.co/api/battles/random_insult') as resp:
                resp = await resp.json()
                await ctx.send(resp['insult'][:1].upper() + resp['insult'][1:].lower())

def setup(bot):
    bot.add_cog(modulename(bot))
