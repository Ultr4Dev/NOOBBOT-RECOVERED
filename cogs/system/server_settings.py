import discord, asyncio
from discord.ext import commands, tasks
import time
from .. import functions



class settings(commands.Cog):
    def __init__(self, client, guild_settings):
        self.client = client
        self.active_changes = {}
        self.db = client.db

    '''
    @commands.command(aliases=["server_settings"])
    async def settings(self, ctx): # settings command

        if not ctx.channel.id in self.active_changes: #checking if channel aldery has a settings thing active

            #making initial embed
            embed = discord.Embed(title="Settings", description="**Step: 1**\nWhat do you want to change?\nReply with `command`|**More options comming soon!!!**\n**3** tries left!")
            embed.set_footer(text="Reply with `cancel` to stop.")

            if ctx.guild.me.permissions_in(ctx.channel).embed_links:

                #sending innitial embed
                bot_msg = await ctx.send(embed=embed)

                #saving data
                channel = ctx.channel
                self.active_changes[ctx.channel.id] = {"stage": "1", "info": {}, "tries": 3,}

                while channel.id in self.active_changes and self.active_changes[channel.id]["tries"] > 0:

                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

                    try:
                        msg = await self.client.wait_for("message", timeout=60.0, check=check)

                    except asyncio.TimeoutError:
                        if channel.id in self.active_changes:
                            await send_safe(ctx, channel, f"{ctx.author.mention}, ⏱️ Times up!")
                            self.active_changes.pop(channel.id)
                            embed = None
                            content = f"⏱️ Times up!"
                            break

                    else:
                        if msg.content.lower() == "cancel":
                            self.active_changes.pop(channel.id)
                            embed = discord.Embed(title="Process canceled!", description=f"The process has been canceled!", colour=0xFF0000)
                            content = ""

                        elif self.active_changes[channel.id]["stage"] == "1":
                            if msg.content.lower() == "command":
                                self.active_changes[channel.id]["stage"] = "command-1"
                                self.active_changes[channel.id]["tries"] = 3
                                content = ""
                                embed = discord.Embed(title="Settings", description=f"What command do you want to change?\nReply with `command name`\n**{self.active_changes[channel.id]['tries']}** tries left!")
                                embed.add_field(name="What to change?", value="command-1")
                                embed.add_field(name="what command?", value="--")
                                embed.add_field(name="what to change with command?", value="--")
                                embed.set_footer(text="Reply with `cancel` to stop.")

                            else:
                                #saving data
                                self.active_changes[channel.id]["tries"] -= 1


                                if self.active_changes[channel.id]["tries"] > 0:#checking if there is no more tries
                                    embed = discord.Embed(title="Settings", description=f"What do you want to change?\nReply with `command`\n**{self.active_changes[channel.id]['tries']}** tries left!")
                                    embed.set_footer(text="Reply with `cancel` to stop.")
                                    content = ""

                                else:
                                    embed = discord.Embed(title="Process canceled - No more tries", description=f"You where to bad answearing my questions! Use the command again to retry.", colour=0xFF0000)
                                    content = ""
                                    self.active_changes.pop(channel.id)
                                    await bot_msg.edit(content=content, embed=embed)
                                    break


                        elif self.active_changes[channel.id]["stage"] == "command-1":

                            #geting data from database
                            result = await collection_guild_settings.find_one({"_id": ctx.guild.id})
                            prefixes = result["prefixes"]

                            #adding mentions to prefix
                            prefixes.append(f"<@!{self.client.user.id}>")
                            prefixes.append(f"<@!{self.client.user.id}> ")
                            prefixes.append(f"")

                            #checking if message starts with prefix
                            command = False
                            command_prefix = None

                            for prefix in prefixes:
                                if msg.content.startswith(prefix):
                                    command = True
                                    command_prefix = prefix

                            #checking if user responded with actual command
                            if command:
                                if not self.client.get_command(msg.content[0+len(command_prefix):].split(" ")[0]) is None:
                                    command_name = self.client.get_command(msg.content[0+len(command_prefix):].split(" ")[0]).name
                                    self.active_changes[channel.id]["info"]["command name"] = command_name
                                    self.active_changes[channel.id]["stage"] = "command-2"
                                    self.active_changes[channel.id]["tries"] = 3
                                    content = ""
                                    embed = discord.Embed(title="Settings", description=f"What command do you want to change?\nReply with `blacklist`|`whitelist`|`{'enable' if command_name in self.guild_settings[ctx.guild.id]['command_permissions']['deactivated_commands'] else 'disable'}`|\n**{self.active_changes[channel.id]['tries']}** tries left!")
                                    embed.add_field(name="What to change?", value="command-1")
                                    embed.add_field(name="what command?", value=command_name)
                                    embed.add_field(name=f"what to change with {self.active_changes[channel.id]['info']['command name']}?", value="--")
                                    embed.set_footer(text="Reply with `cancel` to stop.")

                                else:
                                    self.active_changes[channel.id]["tries"] -= 1
                                    if self.active_changes[channel.id]["tries"] > 0:
                                        content = ""
                                        embed = discord.Embed(title="Settings", description=f"What command do you want to change?\nReply with `command name`\n**{self.active_changes[channel.id]['tries']}** tries left!")
                                        embed.add_field(name="What to change?", value="command-1")
                                        embed.add_field(name="what command?", value="--")
                                        embed.add_field(name="what to change with command?", value="--")
                                        embed.set_footer(text="Reply with `cancel` to stop.")

                                    else:
                                        embed = discord.Embed(title="Process canceled - No more tries", description=f"You where to bad answearing my questions! Use the command again to retry.", colour=0xFF0000)
                                        content = ""
                                        self.active_changes.pop(channel.id)
                                        await bot_msg.edit(content=content, embed=embed)
                                        break

                        elif self.active_changes[channel.id]["stage"] == "command-2":
                            pass







                    await bot_msg.edit(content=content, embed=embed)


            elif self.guild_settings[ctx.guild.id]["error messages"]["bot missing permissions"]:
                await send_safe(ctx, ctx.channel, "Failed to proceed command due to bot missing required permission (`Embed Links`)\nProcess automaticly stopped.")
    '''

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id in self.active_changes and not message.guild is None:
            guild = message.guild

            #getting database and converting it to list
            self.mycursor.execute(f"SELECT prefix FROM prefixes WHRERE serverid = {message.guild.id}")
            db.close()
            prefixes = [entry[0] for entry in self.mycursor]

            prefixes.append(f"<@!{self.client.user.id}>")
            prefixes.append(f"<@!{self.client.user.id}> ")

            command = False
            command_prefix = None

            for prefix in prefixes:
                if message.content.startswith(prefix):
                    command = True
                    command_prefix = prefix

            if command:
                command_name = self.client.get_command(message.content[0+len(command_prefix):].split(" ")[0])
                if command_name is None:
                    print("not a command")

                else:
                    if is_bot_owner(message.author):
                        await self.client.process_commands(message)

                    else:
                        command_name = command_name.name
                        whitelisted_channelses = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["wl c"]
                        blacklisted_channelses = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["bl c"]
                        whitelisted_roles = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["wl r"]
                        blacklisted_roles = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["bl r"]
                        whitelisted_users = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["wl u"]
                        blacklisted_users = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["bl u"]
                        global_whitelisted_users = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["whitelisted_users"]
                        global_blacklisted_users = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["blacklisted_users"]
                        disabled_commands = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["deactivated_commands"]
                        command_permissions = self.guild_settings[guild.id]["guild settings"]["command_permissions"]["commands"][command_name]["perm"]


                        channel_whtelisted = True
                        if not len(whitelisted_channelses) == 0:
                            if not message.channel.id in whitelisted_channelses:
                                channel_whtelisted = False
                        else:
                            if message.channel.id in blacklisted_channelses:
                                channel_whtelisted = False

                        role_whitelisted = True
                        for role in message.author.roles:
                            if role_whitelisted:
                                if not len(whitelisted_channelses) == 0:
                                    if not role.id in whitelisted_roles:
                                        role_whitelisted = False
                                else:
                                    if role.id in blacklisted_roles:
                                        role_whitelisted = False

                        user_whtelisted = True
                        if not len(whitelisted_users) == 0:
                            if not message.author.id in whitelisted_users:
                                user_whtelisted = False
                        else:
                            if message.author.id in blacklisted_users:
                                user_whtelisted = False



                        global_user_whtelisted = True
                        if not len(global_whitelisted_users) == 0:
                            if not message.author.id in global_whitelisted_users:
                                global_user_whtelisted = False
                        else:
                            if message.author.id in global_blacklisted_users:
                                global_user_whtelisted = False

                        command_enabled = True
                        if command_name in disabled_commands:
                            command_enabled = False

                        permissions_passed = True
                        for permission in command_permissions:
                            permission = permission.replace("manage_channel ", "manage_channels ")
                            if permission == "owner":
                                if not message.author.id == message.guild.owner.id:
                                    permissions_passed = False
                            else:
                                function = getattr(message.author.permissions_in(message.channel), permission)
                                permissions_passed = function

                        if command_enabled:
                            if global_user_whtelisted:
                                if user_whtelisted:
                                    if role_whitelisted:
                                        if channel_whtelisted:
                                            if permissions_passed:
                                                await self.client.process_commands(message)
                                            else:
                                                print("denyed perm")
                                        else:
                                            print("denyed channel")
                                    else:
                                        print("denyed role")
                                else:
                                    print("denyed user")
                            else:
                                print("denyed global user")





def setup(bot):
    '''
    1. Going through all guilds the bot is in
    2. making sure all of them are in the databse
    3. caching the database in memory
    '''

    guild_settings = {}
    new_guilds = 0

    guilds_in_db = non_await_guild_settings.find_one({"_id": "guilds"})
    guilds_in_db = guilds_in_db["saved guilds"]

    for guild in bot.guilds:
        if guild.id in guilds_in_db:
            guild_info = non_await_guild_settings.find_one({"_id": guild.id})
            guild_settings[guild.id] = guild_info

        else:
            try:
                try:
                    non_await_guild_settings.insert_one({"_id": guild.id, "guild settings": post_commands, "rules": {}})
                except:
                    print(f"Failed to add \"{guild.name}\" to database")
                else:
                    print(f"Added \"{guild.name}\" to database")
                guilds_in_db.append(guild.id)
                guild_settings[guild.id] = post_commands
                new_guilds += 1
            except Exception as e:
                print(e)

        print(f"{bot.guilds.index(guild) + 1} / {len(bot.guilds)} guilds saved")


    print(f"{len(bot.guilds)} guilds cached in local memory\n{new_guilds} new guilds")
    non_await_guild_settings.update_one({"_id": "guilds"}, {"$set": {"saved guilds": guilds_in_db}})

    bot.add_cog(settings(bot, guild_settings))
