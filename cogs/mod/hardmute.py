import discord, typing
from discord.ext import commands, tasks
import mysql.connector  # importing mysql
from .. import functions


# mysql

db = mysql.connector.connect(
    host="medin.nu",
    user="wbpqxeqo_ultra",
    passwd="YQ!8N*Y.B{yf",
    database="wbpqxeqo_noob"
)  # conecting to database

mycursor = db.cursor()  # mysql cursor object

class hardmute(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hardmutes = {}
        self.only_me_channelses = {}
        self.online = False

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            guild_info = await collection_hardmutes.find_one({"_id": guild.id})
            if guild_info is None:
                post = {"_id": guild.id, "hardmuted members": []}
                self.hardmutes[guild.id] = []
                await collection_hardmutes.insert_one(post)

            else:
                self.hardmutes[guild.id] = guild_info["hardmuted members"]
        self.online = True
        print("all guilds saved")

    @commands.command()
    async def hardmute(self, ctx, member: typing.Union[discord.Member, str], reason=None):
        if ctx.author.guild_permissions.manage_guild or await is_bot_owner(ctx.author):
            if isinstance(member, discord.Member):
                if not await is_bot_owner(member) or await is_bot_owner(ctx.author):
                    if member.id in self.hardmutes[ctx.guild.id]:
                        await send_safe(ctx, ctx.channel, f"`{member}` is already hardmuted.")

                    else:
                        self.hardmutes[ctx.guild.id].append(member.id)
                        await collection_hardmutes.update_one({"_id": ctx.guild.id}, {"$set": {"hardmuted members": self.hardmutes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, f"`{member}` is now hardmuted.")

                else:
                    await send_safe(ctx, ctx.channel, "Nope")

            else:
                await send_safe(ctx, ctx.channel, f"`{member}` is not a valid member.")

    @commands.command()
    async def unhardmute(self, ctx, member: typing.Union[discord.Member, str], reason=None):
        if ctx.author.guild_permissions.manage_guild or await is_bot_owner(ctx.author):
            if isinstance(member, discord.Member):
                if member.id in self.hardmutes[ctx.guild.id]:
                    self.hardmutes[ctx.guild.id].pop(self.hardmutes[ctx.guild.id].index(member.id))
                    await collection_hardmutes.update_one({"_id": ctx.guild.id}, {"$set": {"hardmuted members": self.hardmutes[ctx.guild.id]}})
                    await send_safe(ctx, ctx.channel, f"`{member}` is now unhardmuted.")

                else:
                    await send_safe(ctx, ctx.channel, f"`{member}` is not hardmuted.")

            else:
                await send_safe(ctx, ctx.channel, f"`{member}` is not a valid member.")

    @commands.command(aliases=["only-me"])
    async def only_me(self, ctx):
        if ctx.author.permissions_in(ctx.channel).manage_guild or await is_bot_owner(ctx.author):
            if not ctx.channel.id in self.only_me_channelses:
                await send_safe(ctx, ctx.channel, "Use the command again to stop this sesion.")
                self.only_me_channelses[ctx.channel.id] = ctx.author.id

            else:
                if self.only_me_channelses[ctx.channel.id] == ctx.author.id:
                    self.only_me_channelses.pop(ctx.channel.id)
                    await send_safe(ctx, ctx.channel, "👍")

    @commands.command()
    async def force_end(self, ctx):
        if await is_bot_owner(ctx.author):
            if not ctx.channel.id in self.only_me_channelses:
                self.only_me_channelses.pop(ctx.channel.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.online:
            if message.guild is not None:
                if message.author.id in self.hardmutes[message.guild.id]:
                    try:
                        await message.delete()
                    except:
                        pass

                elif message.channel.id in self.only_me_channelses:
                    if not self.only_me_channelses[message.channel.id] == message.author.id and not message.author.id == 714802275725344838:
                        try:
                            await message.delete()
                        except:
                            pass

def setup(bot):
    bot.add_cog(hardmute(bot))
