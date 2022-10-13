import discord
import typing
import datetime
import time, requests
from discord.ext import commands, tasks
import mysql.connector  # importing mysql
from .. import functions as f


# mysql

db = mysql.connector.connect(
    host="medin.nu",
    user="wbpqxeqo_ultra",
    passwd="YQ!8N*Y.B{yf",
    database="wbpqxeqo_noob"
)  # conecting to database

mycursor = db.cursor()  # mysql cursor object


class muteing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            guild_info = await collectionmod.find_one({"_id": guild.id})

            if guild_info is None:
                members_tempmute = {}
                members_mute = {}
                members_warnings = {}
                members_tempban = {}
                for member in guild.members:
                    if not member.bot:

                        members_tempmute[str(member.id)] = {
                            "id": member.id, "tempmuted": False, "end_time": None}
                        members_mute[str(member.id)] = {
                            "id": member.id, "muted": False}
                        members_tempban[str(member.id)] = {
                            "id": member.id, "tempbanned": False, "end_time": None}
                        members_warnings[str(member.id)] = {
                            "id": member.id, "warnings": []}

                post = {"_id": guild.id,
                        "muted role": None,
                        "auto mod actions": {},
                        "warnings removal": None,
                        "tempmute": members_tempmute,
                        "mutes": members_mute,
                        "warnings": members_warnings,
                        "tempban": members_tempban}

                await collectionmod.insert_one(post)
                print(f"Data for {guild.name} was added")

            else:
                for member in guild.members:
                    if member in guild_info["tempmute"]:
                        pass

                    else:
                        members_tempmute = guild_info["tempmute"]
                        members_mute = guild_info["mutes"]
                        members_warnings = guild_info["warnings"]
                        members_tempban = guild_info["tempban"]
                        for member in guild.members:
                            if not member.bot:

                                members_tempmute[str(member.id)] = {
                                    "id": member.id, "tempmuted": False, "end_time": None}
                                members_mute[str(member.id)] = {
                                    "id": member.id, "muted": False}
                                members_tempban[str(member.id)] = {
                                    "id": member.id, "tempbanned": False, "end_time": None}
                                members_warnings[str(member.id)] = {
                                    "id": member.id, "warnings": []}

                                await collectionmod.update_one({"_id": guild.id}, {"$set": {"tempmuted": members_tempmute, "mutes": members_mute, "warnings": members_warnings, "tempban": members_tempban}})

        print("muteing is done")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_info = await collectionmod.find_one({"_id": guild.id})

        if guild_info is None:
            members_tempmute = {}
            members_mute = {}
            members_warnings = {}
            members_tempban = {}
            for member in guild.members:
                if not member.bot:
                    members_tempmute[str(member.id)] = {
                        "id": member.id, "tempmuted": False, "end_time": None}
                    members_mute[str(member.id)] = {
                        "id": member.id, "muted": False}
                    members_tempban[str(member.id)] = {
                        "id": member.id, "tempbanned": False, "end_time": None}
                    members_warnings[str(member.id)] = {
                        "id": member.id, "warnings": []}

            post = {"_id": guild.id,
                    "muted role": None,
                    "auto mod actions": {},
                    "warnings removal": None,
                    "tempmute": members_tempmute,
                    "mutes": members_mute,
                    "warnings": members_warnings,
                    "tempban": members_tempban}

            await collectionmod.insert_one(post)
            print(f"Data for {guild.name} was added")

        else:

            guild = member.guild
            guild_info = await collectionmod.find_one({"_id": guild.id})
            if not str(member.id) in guild_info["tempmute"]:
                guild_info["muted role"] = None
                guild_info["auto mod actions"] = {}
                guild_info["warnings removal"] = None


                #editing data
                #tempmute
                guild_info["tempmute"][str(member.id)] = {
                    "id": member.id, "tempmuted": False, "end_time": None}

                #mute
                guild_info["mutes"][str(member.id)] = {
                    "id": member.id, "muted": False}

                #tempban
                guild_info["tempban"][str(member.id)] = {
                    "id": member.id, "tempbanned": False, "end_time": None}

                #warnings
                guild_info["warnings"][str(member.id)] = {
                    "id": member.id, "warnings": []}


                #saving data
                await collectionmod.update_one(
                    {"_id": guild.id}, {"$set": {"tempmute": guild_info["tempmute"]}})
                await collectionmod.update_one(
                    {"_id": guild.id}, {"$set": {"tempban": guild_info["tempban"]}})
                await collectionmod.update_one(
                    {"_id": guild.id}, {"$set": {"warnings": guild_info["warnings"]}})
                await collectionmod.update_one(
                    {"_id": guild.id}, {"$set": {"mutes": guild_info["mutes"]}})

            if guild_info["mutes"][str(member.id)]["muted"]:
                role = guild.get_role(guild_info["muted role"])

                if not role is None and guild.me.guild_permissions.manage_roles and guild.roles.index(role) < guild.roles.index(guild.me.top_role):
                    await member.add_roles(role)
                    try:
                        await member.send("Your muted role doesn't disappear because you leave and rejoin the server.")
                    except:
                        pass

    @commands.command(aliases=["smr", "setmutedrole", "set-muted-role"])
    async def set_muted_role(self, ctx, role: typing.Union[discord.Role, str] = None):
        if ctx.author.guild_permissions.manage_roles or f.is_bot_owner(ctx.author):
            if isinstance(role, str):
                await send_safe(ctx, ctx.channel, "Argument `Role` must be a role.")
            else:
                if role is None or ctx.guild.roles.index(role) < ctx.guild.roles.index(ctx.guild.me.top_role):
                    # geting old data
                    guild_info = await collectionmod.find_one({"_id": ctx.guild.id})
                    old_role = ctx.guild.get_role(guild_info["muted role"])

                    # saving data
                    await collectionmod.update_one({"_id": ctx.guild.id}, {
                                             "$set": {"muted role": role.id if isinstance(role, discord.Role) else None}})

                    # making embed
                    embed = discord.Embed(
                        title="Muted Role Set",
                        description="New muted role has been set",
                        colour=0x4287f5
                    )
                    embed.add_field(name="New role", value=role.name if isinstance(
                        role, discord.Role) else None)
                    embed.add_field(name="Old role", value=old_role.name if isinstance(
                        ctx.guild.get_role(guild_info["muted role"]), discord.Role) else None)

                    # sending embed
                    await send_safe(ctx, ctx.channel, embed=embed)

                else:
                    await send_safe(ctx, ctx.channel, f"`{role.name}` is above my top role ({ctx.guild.me.top_role.name}) so i can't use it.")

        else:
            await send_safe(ctx, ctx.channel, "You are missing requierd permission (`Manage Roles`)")

    @commands.command()
    async def mute(self, ctx, member: typing.Union[discord.Member, str] = None, *, reason="No reason specifyed"):
        # permission check
        if ctx.author.guild_permissions.manage_roles or is_bot_owner(ctx.author):
            # perm check passed

            # bot perm check
            if not ctx.guild.me.guild_permissions.manage_roles:

                await send_safe(ctx, ctx.channel, "Bot is missing required permission (`Manage Roles`)")

            else:
                if member is None:
                    await send_safe(ctx, ctx.channel, f"Failed to procced command due to missing arguments (`Member`)\nUse `{ctx.prefix}help mute` to se all required arguments.")

                else:
                    if isinstance(member, str):
                        await send_safe(ctx, ctx.channel, f"Argmuent `Member` must be a member.")

                    elif is_bot_owner(member) and not is_bot_owner(ctx.author):
                        await send_safe(ctx, ctx.channel, f"I'm not muting my devs and creators.")

                    else:
                        guild = ctx.guild
                        guild_info = await collectionmod.find_one(
                            {"_id": ctx.guild.id})
                        no_mutede_role_set = False
                        i_made_muted_role = False

                        if guild_info["muted role"] is None or str(type(guild.get_role(guild_info["muted role"]))) == "<class 'NoneType'>":
                            guild_info["muted role"] = None
                            no_mutede_role_set = True
                            for role in guild.roles:
                                if not role.permissions.send_messages and guild.roles.index(role) < guild.roles.index(guild.me.top_role) and guild_info["muted role"] is None:
                                    guild_info["muted role"] = role.id
                                    await collectionmod.update_one({"_id": ctx.guild.id}, {
                                                             "$set": {"muted role": role.id}})
                                    for channel in guild.text_channels:
                                        if guild.me.permissions_in(channel).manage_permissions:
                                            await channel.set_permissions(role, send_messages=False, reason="Fixing permissions for new muted role")

                            if guild_info["muted role"] is None:
                                i_made_muted_role = True
                                role = await guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, read_messages=True), reason="No muted role set")

                                # saving data
                                guild_info["muted role"] = role.id
                                await collectionmod.update_one({"_id": ctx.guild.id}, {
                                                         "$set": {"muted role": role.id}})

                                # uptading channel perms
                                for channel in guild.text_channels:
                                    if guild.me.permissions_in(channel).manage_permissions:
                                        await channel.set_permissions(role, send_messages=False, reason="Fixing permissions for new muted role")

                            await collectionmod.update_one({"_id": ctx.guild.id}, {
                                                     "$set": {"muted role": guild_info["muted role"]}})

                        if not guild.get_role(guild_info["muted role"]) in member.roles:


                            url = "http://dc.api.medin.nu/add/"

                            querystring = {"key":"20200924-41-QGBVFXMWKSZXD0EPTNAUC5R8AKI3","uid":member.id}

                            headers = {
                                'cache-control': "no-cache",
                                'postman-token': "204fd13a-181e-df63-02f4-e6ca71aabd77"
                                }

                            response = requests.request("GET", url, headers=headers, params=querystring)

                            print(response.text)

                            await member.add_roles(guild.get_role(guild_info["muted role"]), reason=reason)
                            guild_info["mutes"][str(member.id)]["muted"] = True
                            await collectionmod.update_one({"_id": ctx.guild.id}, {
                                                     "$set": {"mutes": guild_info["mutes"]}})

                            if not no_mutede_role_set and not i_made_muted_role:
                                await send_safe(ctx, ctx.channel, f"**{member}** was muted.")

                            elif no_mutede_role_set and not i_made_muted_role:
                                await send_safe(ctx, ctx.channel, f"**{member}** was muted.\nBecaus no muted role was set i choosed `{guild.get_role(guild_info['muted role']).name}` as the muted role. This can be changed by using `{ctx.prefix}set_muted_role <role>`.")

                            elif no_mutede_role_set and i_made_muted_role:
                                await send_safe(ctx, ctx.channel, f"**{member}** was muted.\nBecaus no muted role was set and i did not find any role suitable i made a new role called `Muted` wich is now the muted role. This can be changed by using `{ctx.prefix}set_muted_role <role>`.")

                        else:
                            if not no_mutede_role_set and not i_made_muted_role:
                                await send_safe(ctx, ctx.channel, f"**{member}** is already muted.")

                            elif no_mutede_role_set:
                                await send_safe(ctx, ctx.channel, f"**{member}** is already muted.\nBecaus no muted role was set i choosed `{guild.get_role(guild_info['muted role']).name}` as the muted role and {member} already had it. The muted role can be changed by using `{ctx.prefix}set_muted_role <role>`.")
        else:
            await send_safe(ctx, ctx.channel, "You are missing requierd permission (`Manage Roles`)")


def setup(bot):
    bot.add_cog(muteing(bot))
