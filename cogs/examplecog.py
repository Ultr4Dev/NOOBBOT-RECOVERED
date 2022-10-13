import discord
from discord.ext import commands, tasks
from .. import functions as f

class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(bot):
    bot.add_cog(modulename(bot))
