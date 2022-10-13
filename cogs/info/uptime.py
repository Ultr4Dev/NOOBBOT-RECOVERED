import discord
from discord.ext import commands
import time, datetime
from .. import functions as f

class uptimecmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ut"])
    async def uptime(self, ctx):
      current_time = datetime.datetime.utcnow()
      difference = int(round(current_time.timestamp() - self.bot.starttime.timestamp()))
      text = str(datetime.timedelta(seconds=difference))
      embed = discord.Embed(colour=0x00ff00)
      embed.add_field(name="Uptime:", value=text)
      embed.set_footer(text=f"nb!uptime | {ctx.message.author}")
      embed.timestamp = datetime.datetime.utcnow()
      await f.send_safe(ctx, ctx.channel, embed=embed)

#ultra broke it :facepalm:

def setup(bot):
    bot.add_cog(uptimecmd(bot))
