import discord, humanize, random, time, datetime, typing
from discord.ext import commands
from itertools import cycle
from operator import itemgetter
from .. import functions as f
from datetime import timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

class info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    def member_ui(self, member):
        embed = discord.Embed(
            title=f"{member}",
            description=f"Information about {member.name}",
            color=member.colour
        )
        embed.add_field(name="💳ID",
                        value=member.id)
        if member.display_name == member.name:
            embed.add_field(name="Nickname",
                            value="No nickname")
        else:
            embed.add_field(name="Nickname",
                            value=member.display_name)

        embed.set_thumbnail(url=member.avatar_url)

        if member.bot:
            embed.add_field(name="User is",
                            value="🤖Bot",
                            inline=False)

        else:
            embed.add_field(name="User is",
                            value="🙎Human",
                            inline=False)
        created_at = humanize.naturaltime(utc_to_local(datetime.datetime.utcnow())-utc_to_local(member.created_at))
        joined_at = humanize.naturaltime(utc_to_local(datetime.datetime.utcnow())-utc_to_local(member.joined_at))
        embed.add_field(
            name=":cake: Created",
            value=created_at,
            inline=False
        )

        embed.add_field(
            name=":calendar_spiral: Joined",
            value=joined_at,
            inline=False
        )

        return embed

    def user_ui(self, user):
        embed = discord.Embed(
            title=f"{user}",
            description=f"Information about {user.name}"
        )
        embed.add_field(name="💳ID",
                        value=user.id)

        embed.set_thumbnail(url=user.avatar_url)

        if user.bot:
            embed.add_field(name="User is",
                            value="🤖Bot",
                            inline=False)

        else:
            embed.add_field(name="User is",
                            value="🙎Human",
                            inline=False)
        created_at = humanize.naturaltime(utc_to_local(datetime.datetime.utcnow())-utc_to_local(user.created_at))
        embed.add_field(
            name=":cake: Created",
            value=created_at,
            inline=False
        )

        return embed

    @commands.command(aliases=["user-info", "userinfo", "ui", "uinfo", "u-info", "useri", "user-i"])
    async def user_info(self, ctx, member: typing.Union[discord.Member, int, str] = None):
        '''
        Command for info about a user.
        No extra permissions requierd.
        '''

        if member is None:
            return await ctx.send(embed=self.member_ui(ctx.author))

        if isinstance(member, discord.Member):
            return await ctx.send(embed=self.member_ui(member))

        if isinstance(member, int):
            return await ctx.send(embed=self.user_ui(await self.client.fetch_user(member)))


    @commands.command(aliases=["server-info", "serverinfo", "si", "sinfo", "s-info", "serveri", "server-i"])
    async def server_info(self, ctx, guild_id=None):
        guild = self.client.get_guild(guild_id) if guild_id is not None and f.is_bot_owner(ctx.author, self.client) else ctx.guild
        embed = discord.Embed(
            title=f"Information about {guild.name}",
            description="",
            color=0xcccc00
        )
        created_at = created_at = humanize.naturaltime(datetime.datetime.now()-guild.created_at)
        embed.add_field(name="❯ General info",
                        value=f":credit_card: ID: **{guild.id}**\n"
                              f":crown: Owner: **{guild.owner}**({guild.owner.mention})\n"
                              f":earth_americas: Region: **{guild.region}**\n"
                              f":clock: Created **{created_at}**",
                        inline=False)
        embed.add_field(name="❯ Channels",
                        value=f":speech_balloon: Text channels: **{len(guild.text_channels)}**\n"
                              f":loud_sound: Voice channels: **{len(guild.channels) - len(guild.categories) - len(guild.text_channels)}**",
                        inline=False)

        bots = 0
        for member in guild.members:
            if member.bot:
                bots += 1

        if guild.get_member(self.client.user.id).guild_permissions.ban_members:
            posible = True
            baned_members = []
            bans = await guild.bans()
            for member in bans:
                baned_members.append(member)
        else:
            baned_members = "f,"
            posible = False

        embed.add_field(name="❯ Members",
                        value=f":slight_smile: Members: **{len(guild.members)}**\n"
                              f"<:Bot:708465415805730826> Bots: **{bots}**\n"
                              f":man_pouting: Humans: **{len(guild.members) - bots}**\n"
                              f"<a:verification:712313395277332502> Verification level: **{None}**\n"
                              f"<:banhammer:709089870534017176> Bans: **{len(baned_members) if posible else 'not available'}**",
                        inline=False)

        roleused = {}
        for role in guild.roles:
            roleused[int(role.id)] = {"Number": 0, "ID": role.id}

        for member in guild.members:
            for role in member.roles:
                roleused[int(role.id)]["Number"] += 1

            # make a list with all users
            listan = []
            for _ , value in roleused.items():
                listan.append([value["Number"], value["ID"]])

            # sort the list
            listan = sorted(listan, key=itemgetter(0))
            listan = listan[::-1]

        embed.add_field(name="❯ Roles",
                        value=f"<a:gears:708464511648006144> Roles: **{len(guild.roles)}**\n"
                        f":arrow_double_up: Highest role: {guild.roles[len(guild.roles)-1].mention}\n"
                        f":arrow_double_down: Lowest role: {guild.roles[1].mention}\n"
                        f"Most used role: {guild.get_role(listan[1][1]).mention}[{listan[1][0]}]",
                        inline=False)

        embed.add_field(name="❯ Nitro",
                        value=f"<a:nitro:708431418551959605> Nitrobosts: **{guild.premium_subscription_count}**\n"
                              f"<a:nitroboosting:708430623215190077> Nitro lvl: **{guild.premium_tier}**")
        embed.set_thumbnail(url=guild.icon_url)

        await f.send_safe(ctx, ctx.channel, embed=embed)

    @commands.command(aliases=["d"])
    async def decode(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("You need to specify the text to be decoded!")
        else:
            for msg in f.split(f"{arg}\n{discord.utils.escape_mentions(discord.utils.escape_markdown(arg))}"):
                await ctx.send(msg)


def setup(bot):
    bot.add_cog(info(bot))
