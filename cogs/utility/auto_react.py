from ..utils import *


class auto_react(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.last = time.time()

    @commands.Cog.listener("on_message")
    async def auto_react_check(self, message):
        if message.guild is None:
            return

        if message.channel.id in self.client.cache["auto_react"].keys():

            emojis = self.client.cache["auto_react"][message.channel.id]

            for emoji in emojis:
                await asyncio.sleep(self.last-time.time()+0.25)
                await message.add_reaction(emoji)
                self.last = time.time()

    @commands.group(aliases=["ar"])
    async def auto_react(self, ctx):
        '''
        Show all active auto reactions in this server
        '''
        pass

    def emoji_check(self, emoji):
        if isinstance(emoji, discord.Emoji):
            return True

        return str(emoji) in f.emojis.values()

    @auto_react.command(aliases=["a"])
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, channel:discord.TextChannel, emoji: typing.Union[discord.Emoji, str]):
        '''
        add a auto reaction to your server
        '''

        query = """
        INSERT INTO auto_react (channel_id, emoji)
        VALUES ($1, $2)
        """

        if channel.id in self.client.cache["auto_react"]:
            if len(self.client.cache["auto_react"][channel.id]) >= 5:
                return await ctx.send(f"Maximum number of reactions in {channel.mention} reached!")

        if not self.emoji_check(emoji):
            return await ctx.send("Invalid emoji!")

        if not ctx.guild.me.permissions_in(channel).add_reactions:
            # if the bot does not have necesary permissions
            return await ctx.send(f"I am missing requierd permission (`Add Reactions`) in {channel.mention}")

        if isinstance(emoji, discord.Emoji):
            if emoji.guild != ctx.guild and not ctx.guild.me.permissions_in(channel).use_external_emojis:
                return await ctx.send(f"I am missing requierd permission (`Use External Emojis`) in {channel.mention}")


        if channel.id in self.client.cache["auto_react"]:
            if str(emoji) in self.client.cache["auto_react"][channel.id]:
                return await ctx.send("This configuration alredy exist! Make sure i have `Add Reactions` and `Use External Emojis` if it does not work.")

        await self.client.db.execute(query, channel.id, str(emoji))

        if channel.id in self.client.cache["auto_react"]:
            self.client.cache["auto_react"][channel.id].append(str(emoji))
        else:
            self.client.cache["auto_react"][channel.id] = [str(emoji)]

        await ctx.send(f"I will now react with {str(emoji)} on every message in {channel.mention}")

    @auto_react.command(aliases=["r"])
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, channel:discord.TextChannel, emoji: typing.Union[discord.Emoji, str]=None):
        '''
        add a auto reaction to your server
        '''

        query = """
        DELETE FROM auto_react WHERE channel_id=$1 emoji=$2)
        """
        if emoji is None:
            await self.client.db.execute("DELETE FROM auto_react WHERE channel_id=$1", channel.id)
            return await ctx.send(f"All configurations in {channel.mention} has been removed!")

        if not self.emoji_check(emoji):
            return await ctx.send("Invalid emoji!")


        if channel.id in self.client.cache["auto_react"]:
            if channel.id in self.client.cache["auto_react"]:
                if not str(emoji) in self.client.cache["auto_react"][channel.id]:
                    return await ctx.send("This configuration does not exist!")

            else:
                return await ctx.send(f"{channel.mention} has no auto reactions!")

        await self.client.db.execute(query, channel.id, str(emoji))

        if len(self.client.cache["auto_react"][channel.id]) == 1:
            self.client.cache["auto_react"].pop(channel.id)

        else:
            self.client.cache["auto_react"][channel.id].pop(self.client.cache["auto_react"][channel.id].index(emoji)

        await ctx.send(f"I will no longer react with {str(emoji)} on messages in {channel.mention}")


def setup(bot):
    bot.add_cog(auto_react(bot))
