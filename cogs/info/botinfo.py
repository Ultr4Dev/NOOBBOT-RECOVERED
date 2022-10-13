import discord, datetime, platform, humanize
from discord.ext import commands
from .. import functions as f

class botinfocmd(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    def get_description(self):
        description = ""

        owners = ", ".join([str(self.client.get_user(id)) for id in self.client.owner_ids])
        description += f"\U0001f451 **Owners:\n**{owners}\n\n"
        # owners

        description += f"\U0001f4dc **Language:** Python ({platform.python_version()})\n"
        #language

        description += f"\U0001f4d8 **Library:** discord.py ({discord.__version__})\n\n\n"
        # library

        description += f"\U0001f3db **Guilds:** {len(self.client.guilds)}\n\n"
        # guilds

        text_channel = 0
        voice_channel = 0
        category = 0
        for channel in self.client.get_all_channels():
            if channel.type == discord.ChannelType.text:
                text_channel += 1

            if channel.type == discord.ChannelType.voice:
                voice_channel += 1

            if channel.type == discord.ChannelType.category:
                category += 1

        description += f"**Channels:** {text_channel+voice_channel+category}\n\
                        <:Text_Channel:778350926468743228> Text: {text_channel}\n\
                        <:Voice_Channel:778351389415440395> Voice: {voice_channel}\n\
                        Categories: {category}\n\n"
        # channels

        bots = 0
        humans = 0

        for user in self.client.users:
            if user.bot:
                bots += 1

            else:
                humans += 1

        description += f"**Users:** {len(self.client.users)}\n\
                        \U0001f64e Humans: {humans}\n\
                        \U0001f916 Bots: {bots}\n\n"
        # members and users

        difference = datetime.datetime.now() - self.client.starttime.timestamp()
        text = humanize.naturaltime(difference)

        description += f"**Uptime:** {text}\n"

        description += f"If you happend to like me, consider [inviting me]({self.client.invite}) and joining my [support server.]({self.client.server})"
        # invites
        return description

    @commands.command(name="bot_info", aliases=["bot-info", "botinfo", "bi", "binfo", "b-info", "boti", "bot-i"])
    async def _bot_info(self, ctx):
        '''
        Bot info

        Command for showing general info about the bot
        '''

        embed = discord.Embed(
            title=f"{self.client.user.name} Info",
            color=self.client.color
        )
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url, url=self.client.invite)
        embed.timestamp = datetime.datetime.utcnow()
        # making embed

        embed.description = self.get_description()

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(botinfocmd(bot))
