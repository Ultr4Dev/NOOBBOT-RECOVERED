import discord
from discord.ext import commands, tasks
from .. import functions as f


class guild_log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
            embed = discord.Embed(
                title="I joined a server :open_mouth:",
                description=guild.name,
                colour=0x00FF00
            )

            embed.set_thumbnail(url=guild.owner.avatar_url)
            embed.add_field(name="Member count", value=guild.member_count)
            embed.add_field(name="Owner", value=guild.owner)
            embed.set_image(url=guild.icon_url)
            embed.set_footer(text=f"Im curently in {len(self.client.guilds)}")
            await self.client.get_channel(self.client.info["console_channel"]).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
            embed = discord.Embed(
                title="I left a server :sob:",
                description=guild.name,
                colour=0xFF0000
            )

            embed.set_thumbnail(url=guild.owner.avatar_url)
            embed.add_field(name="Member count", value=guild.member_count)
            embed.add_field(name="Owner", value=guild.owner)
            embed.set_image(url=guild.icon_url)
            embed.set_footer(text=f"Im curently in {len(self.client.guilds)}")
            await self.client.get_channel(self.client.info["console_channel"]).send(embed=embed)

def setup(bot):
    bot.add_cog(guild_log(bot))
