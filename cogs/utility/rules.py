import discord, asyncio, typing
from discord.ext import commands, tasks
from .. import functions as f

class Rule():
    def __init__(self, client, rule):
        self.id = rule["rule_id"]
        self.guild = client.get_guild(rule["guild_id"])
        self.channel = client.get_channel(rule["channel_id"])
        self.text = rule["rule"]

class Rules(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def rules(self, ctx):
        '''
        Custom server rules.
        makes it easier for server moderators to have server rules and edit them without the original author having to be online.

        Can only be used toghether with subcommands at the moment.
        '''

        if not ctx.invoked_subcommand:
            # if the command was runned without a subcommand, send error message
            await ctx.send(f"This command only does something when invoked with a subcommand!\n`{'`|`'.join([cmd.name for cmd in ctx.command.commands])}`")

    async def is_locked(self, channel:discord.TextChannel):
        return await self.client.db.fetchrow("SELECT * FROM locked_rules WHERE channel_id=$1", channel.id)

    async def db_update(self, channel, rules):
        '''
        resetting all rules for the database
        '''

        await self.client.db.execute(f"DELETE FROM rules WHERE channel_id={channel.id}")
        # removing the previous rules

        for rule in rules:
            # looping through all rules

            rule.id = rules.index(rule)+1
            await self.client.db.execute(f"INSERT INTO rules (guild_id, channel_id, rule_id, rule) VALUES ($1, $2, $3, $4)", rule.guild.id, rule.channel.id, rule.id, rule.text)
            # fixing rule id and inserting to database

    def make_rule(self, rule):
        lines = rule.text.split("\n")
        return "\n> ".join(lines)


    def make_rules(self, rules):
        modifyed_rules = []
        for rule in rules:
            modifyed_rules.append(f"> **#{rules.index(rule)+1}**\n> " + self.make_rule(rule))

        return modifyed_rules

    def get_messages(self, rules):
        '''
        A function for getting the number of messages requierd as well as the content of each message
        '''

        rules = self.make_rules(rules)
        messages = []
        message = ""

        for rule in rules:
            if len(message + f"{rule}\n\n") < 2000:
                message += f"{rule}\n\n"

            else:
                messages.append(message)
                message = f"{rule}\n\n"

        messages.append(message)

        return messages



    async def distibute(self, channel, rules):
        '''
        checking and creating messages requierd for rules to be made
        '''
        message_ids = await self.client.db.fetch(f"SELECT message_id FROM rule_messages WHERE channel_id={channel.id}")
        messages = []
        for message_id in message_ids:
            try:
                messages.append(await channel.fetch_message(message_id["message_id"]))
            except:
                pass

        rule_messages = self.get_messages(rules)

        while len(rule_messages) > len(messages):
            message = await channel.send("prepearing...")
            await self.client.db.execute("INSERT INTO rule_messages (message_id, channel_id) VALUES ($1, $2)", message.id, channel.id)
            messages.append(message)

        while len(rule_messages) < len(messages):
            await messages[len(messages)-1].delete()
            await self.client.db.execute("DELETE FROM rule_messages WHERE message_id=$1", messages[len(messages)-1].id)
            messages.pop(len(messages)-1)

        for rule in rule_messages:
            message = messages[rule_messages.index(rule)]

            await message.edit(content=rule)



    @rules.command()
    async def add(self, ctx, channel: discord.TextChannel, *, args:str):
        '''
        Adding a rule to the server rule list.
        Requiers manage guild permission by default.
        '''

        if await self.is_locked(channel):
            return await ctx.send(f"{channel.mention} has been locked by the server owner!")

        Rules = await self.client.db.fetch("SELECT * FROM rules WHERE channel_id=$1", channel.id)
        # the rules fetched from database
        ArgList = args.split(" ")
        # a list of all the arguments passed
        RuleId = len(Rules)+1
        # the id of the new rule
        RuleText = " ".join(ArgList)
        # the text in the new rule
        RuleList = []
        # the list of all the rules


        if ArgList[0].isdigit():
            # if first wod in arguments is a intiger, it will be used as rule_id
            RuleText = " ".join(ArgList[1:])
            RuleId = int(ArgList[0])


        for rule in Rules:
            # looping through rules and making a class instance
            RuleList.append(Rule(self.client, dict(rule)))

        rule = {"rule_id": RuleId, "guild_id": ctx.guild.id, "channel_id": channel.id, "rule": RuleText}
        RuleList.insert(RuleId-1, Rule(self.client, rule))


        await self.distibute(channel, RuleList)
        await self.db_update(channel, RuleList)

        await ctx.send(f"Rule {RuleId} created.")
        await ctx.message.add_reaction("<:Yes:778530101179973632>")

    @rules.command()
    async def remove(self, ctx, channel: discord.TextChannel, rule_id:int):
        '''
        Removing a rule from servers custom rules
        requiers manage guild by default
        '''

        if await self.is_locked(channel):
            return await ctx.send(f"{channel.mention} has been locked by the server owner!")

        rules = await self.client.db.fetch("SELECT * FROM rules WHERE channel_id=$1", channel.id)
        rulelist = []

        if rule_id > len(rules):
            await ctx.message.add_reaction("<:No:778530212790927370>")
            return await ctx.send("That rule does not exist.")

        if rule_id < 1:
            await ctx.message.add_reaction("<:No:778530212790927370>")
            return await ctx.send("1 is the lowest possible rule id.")

        for rule in rules:
            # looping through rules and making a class instance
            rulelist.append(Rule(self.client, dict(rule)))

        rulelist.pop(rule_id-1)

        await self.distibute(channel, rulelist)
        await self.db_update(channel, rulelist)
        # edit messages and update database

        await ctx.send(f"Rule {rule_id} removed.")
        await ctx.message.add_reaction("<:Yes:778530101179973632>")
        # sending success message

    @rules.command()
    async def edit(self, ctx, channel: discord.TextChannel, rule_id:int, *, ruletext:str):
        '''
        Adding a rule to the server rule list.
        Requiers manage guild permission by default.
        '''


        if await self.is_locked(channel):
            return await ctx.send(f"{channel.mention} has been locked by the server owner!")

        Rules = await self.client.db.fetch("SELECT * FROM rules WHERE channel_id=$1", channel.id)
        # the rules fetched from database
        RuleList = []
        # the list of all the rules

        if rule_id > len(Rules):
            # if rule id is to big, send error message and react with no emoji
            await ctx.message.add_reaction("<:No:778530212790927370>")
            return await ctx.send("That rule does not exist.")

        if rule_id < 1:
            # if rule id is to low, send error message and react with no emoji
            await ctx.message.add_reaction("<:No:778530212790927370>")
            return await ctx.send("1 is the lowest possible rule id.")

        for rule in Rules:
            # looping through rules and making a class instance
            RuleList.append(Rule(self.client, dict(rule)))

        rule = {"rule_id": rule_id, "guild_id": ctx.guild.id, "channel_id": channel.id, "rule": ruletext}
        RuleList[rule_id-1] = Rule(self.client, rule)
        # adding rule to rule list


        await self.distibute(channel, RuleList)
        await self.db_update(channel, RuleList)
        # editing messages and saving to database

        await ctx.send(f"Rule {rule_id} edited.")
        await ctx.message.add_reaction("<:Yes:778530101179973632>")
        # sending success message

    @rules.command(aliases=["l"])
    async def lock(self, ctx, channel: discord.TextChannel):
        if not f.is_bot_owner(ctx.author, self.client) and not ctx.guild.owner == ctx.author:
            return await ctx.send("This command can only be run by the server owner!")

        if await self.is_locked(channel):
            return await ctx.send(f"This channel is alredy locked. Use `{await f.get_prefix(ctx.guild, self.client)}rules unlock #{channel.name}` to unlock it.")
        await self.client.db.execute("INSERT INTO locked_rules (channel_id) VALUES ($1)", channel.id)
        return await ctx.send(f"{channel.mention} has been locked. This means rules can't be edited added or reomved by anyone.")

    @rules.command(aliases=["ul"])
    async def unlock(self, ctx, channel: discord.TextChannel):
        if not f.is_bot_owner(ctx.author, self.client) and not ctx.guild.owner == ctx.author:
            return await ctx.send("This command an onl be runned by the server owner!")

        if not await self.is_locked(channel):
            return await ctx.send(f"This channel is not locked. Use `{await f.get_prefix(ctx.guild, self.client)}rules lock #{channel.name}` to lock it.")
        await self.client.db.execute("DELETE FROM locked_rules WHERE channel_id=$1", channel.id)
        return await ctx.send(f"{channel.mention} has been unlocked. This means rules can be edited added or reomved.")











def setup(bot):
    bot.add_cog(Rules(bot))
