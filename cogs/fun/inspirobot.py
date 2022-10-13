import discord
from discord.ext import commands, tasks
import aiohttp

# Asking inspirobot for a inspirational picture

class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def inspirobot(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://inspirobot.me/api?generate=true') as resp:
                await ctx.send(await resp.text())

def setup(bot):
    bot.add_cog(modulename(bot))
