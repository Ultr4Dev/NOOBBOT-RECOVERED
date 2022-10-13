import discord
from discord.ext import commands, tasks



class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def midget(self, ctx, args=""):
        await ctx.channel.send("YEET test")

def setup(bot):
    bot.add_cog(modulename(bot))
