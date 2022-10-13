import discord
from discord.ext import commands, tasks
import mysql.connector  # importing mysql
from .. import functions as f

class suggestion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["suggestion"])
    async def suggest(self, ctx, *, suggestion:str = None):
      if suggestion is None:
        await f.send_safe(ctx, ctx.channel, "Failed to procced command due to missing argument (`suggestion`)")

      else:
        channel = self.client.get_channel(719604835938205746)
        await ctx.message.delete()

        #making embed
        embed = discord.Embed(
          title="Suggestion",
          description = suggestion,
          colour=ctx.author.colour
        )
        embed.add_field(name="author", value=f"{ctx.author} ({ctx.author.id})")
        embed.add_field(name="server", value=f"{ctx.guild.name} ({ctx.guild.id})")
        embed.set_image(url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await channel.send(embed=embed)
        await ctx.author.send("suggestion noted")

def setup(bot):
    bot.add_cog(suggestion(bot))
