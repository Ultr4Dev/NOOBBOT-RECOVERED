import discord
from discord.ext import commands
import time
from .. import functions as f

class pingcmd(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def ping(self, ctx):

        msg = await ctx.send('pinging.')
        time1 = time.time()
        await msg.edit(content="pinging..")
        time2 = time.time()
        await msg.edit(content="pinging...")
        time3 = time.time()
        apilatency = (time2 - time1) if (time3 - time2) > (time2-time1) else (time3- time2)
        embed = discord.Embed(
            title=f'{self.client.user.name} latency',
            description="Latency",
            color=0x00FFFF)
        embed.add_field(name="🤖BOT Latency", value=f"{str(round(apilatency * 1000))}ms", inline=False)

        embed.add_field(name="🔗API Latency", value=f"{str(round(self.client.latency * 1000))}ms", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(pingcmd(bot))
