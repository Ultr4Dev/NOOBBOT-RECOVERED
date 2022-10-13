import discord, datetime
from discord.ext import commands, tasks
from .. import functions as f


class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and message.author.id != self.client.user.id:
            channel = self.client.get_channel(729757009360060417)

            embed = discord.Embed(title="", description=message.content)
            embed.set_author(name=message.author, url=message.author.avatar_url)
            embed.set_footer(text=f"ID: {message.author.id}")
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.command()
    async def dm(self, ctx, author: discord.User=None, *, message="Nothing to worry here just a stupid dev ;)"):
        if f.is_bot_owner(ctx.author, self.client):
            author = author or ctx.author
            try:
                await author.send(message)
            except:
                await ctx.message.add_reaction("\U0000274e")
            else:
                await ctx.message.add_reaction("\U00002705")

def setup(bot):
    bot.add_cog(modulename(bot))
