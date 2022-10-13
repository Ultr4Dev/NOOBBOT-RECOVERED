import discord
from discord.ext import commands, tasks
import mysql.connector  # importing mysql
from .. import functions as f


class vr_chat(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.chats = {}
        self.authors = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if not message.author.bot or message.author.id == self.client.user.id:
                if message.guild is None:
                    if message.author.id in self.authors:
                        if message.content.startswith("end vr chat"):
                            self.chats.pop(self.authors[message.author.id])
                            self.authors.pop(message.author.id)
                            await message.author.send("Your vr chat has been ended")

                        else:
                            await self.client.get_channel(self.authors[message.author.id]).send(message.content)

                elif message.channel.id in self.chats:
                    embed = discord.Embed(title="", description=message.content)
                    embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                    await self.client.get_user(self.chats[message.channel.id]).send(embed=embed)
        except:
            pass


    @commands.command()
    async def setup_vr_chat(self, ctx, channel_id=""):
        if f.is_bot_owner(ctx.author, self.client):
            is_int = True
            try:
                int(channel_id)
            except:
                is_int = False
                await ctx.send("channel id can only be a intiger")

            if is_int:
                is_channel = True
                try:
                    channel = self.client.get_channel(int(channel_id))
                except:
                    is_channel = False
                    await ctx.send("No a valid channel id")

                if is_channel:
                    self.chats[channel.id] = ctx.author.id
                    self.authors[ctx.author.id] = channel.id
                    await ctx.author.send(f"You have ben linked to {channel.mention} ({channel.name})")

def setup(bot):
    bot.add_cog(vr_chat(bot))
