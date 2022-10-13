import discord
from discord.ext import commands, tasks
from .. import functions


class error_msg(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild_settings = {}
        self.db = client.db


    @commands.command(aliases=["error", "error_msg", "set_error", "e_msg"])
    async def set_error_msg(self, ctx, type = None, value = None):
        pass

def setup(bot):
    bot.add_cog(error_msg(bot))
