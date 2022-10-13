import discord, random, time, datetime
from discord.ext import commands
from itertools import cycle
from .. import functions as f

class helpcmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_req_type(self, arg):
        '''
        A function that outputs one of Five values ("default", "module", "cmd", "alias", "none")
        '''

        helpdict = self.client.info["helpcmd"]

        if arg is None:
            # If arg is None, no arguments where specifyed and default help is requested

            return "default"


        elif arg in helpdict:
            # If arg is one of the key in helpdict, its a module and module helpcmd is requested

            return "module"


        else:
            # If none of previous where True it's ether a cmd, alias, nonexcisting request

            for name, module in helpdict.items():
                # looping throgh modules

                if arg in module["commands"]:
                    # checking if arg is in module commands

                    return "cmd"

        for name, module in helpdict.items():
            # looping throgh modules

            for name, command in module["commands"].items():
                # looping trogh module commands

                if arg in command["aliases"]:
                    # if arg in command aliases

                     return "alias"


        return "none"
        # returning request type

    def add_value(self, embed, name, values, countr=True):
        '''
        A function for adding a field to embeds with a formating

        args:
        embed - the embed the feild should be added to
        *requierd

        name - the name of the feild
        *requierd

        values - a list with all the values
        *requierd

        countr - if a number should be displayed that shows how many values there is
        '''

        if len(values) == 0:
            embed.add_field(
                name=f"{'[0] ' if countr else ''}**{name}**",
                value=f"No {name.lower()}",
                inline=False
            ) # adding feild without any values

        else:
            valstr = f"`{'` | `'.join(values)}`"
            # the feild value

            embed.add_field(
                name=f"{f'[{len(values)}] ' if countr else ''}**{name}**",
                value=valstr,
                inline=False
            ) # adding feild with values

        return embed

    def defult_help(self, prefix):
        '''
        A function for generating the default helpcmd embed.
        No arguments are requierd
        '''

        #declaring vars
        helpdict = self.client.info["helpcmd"]

        embed = discord.Embed( # the embed that will later be returned
            title = f"{self.client.user.name} Help menu",
            description = f"Thanks for inviting me! This servers prefix is: `{prefix}`\n"
                          f"Please report any glitches or bugs in our support server\n"
                          f"[support server]({self.client.server}) | [Invite me]({self.client.invite})",
            color = self.client.color
        )

        for name, module in helpdict.items():
            # looping trogh modules

            embed = self.add_value(embed, name, [name for name, _ in module["commands"].items()])

        #returning embed
        return embed

    def module_help(self, prefix, module):
        '''
        generating module helpcmd
        '''

        #declaring vars
        helpdict = self.client.info["helpcmd"]

        embed = discord.Embed(
            title = f"{module.title()} help page",
            description = helpdict[module]["description"],
            colour = self.client.color
        ) # making embed

        module = helpdict[module]

        for name, cmd in module["commands"].items():
            # looping throgh commands in module

            embed.add_field(
                name=name,
                value=f"`{prefix}{name}{cmd['syntax']}`",
                inline=False
            ) # adding command to embed

        return embed

    def cmd_help(self, prefix, cmd):
        '''
        generating command helpcmd
        '''

        #declaring vars
        helpdict = self.client.info["helpcmd"]

        for module in helpdict:
            # lopping throgh modules

            if cmd in helpdict[module]["commands"]:
                # if cmd is in modules

                command = helpdict[module]["commands"][cmd]

                description = f"`{prefix}{cmd} {command['syntax']}`\n{command['description']}"

                embed = discord.Embed(
                    title = f"{cmd.title()} help page",
                    description = description,
                    color = self.client.color
                ) # making embed

                self.add_value(embed, "Aliases", command["aliases"], countr=False)
                self.add_value(embed, "Subcommands", command["sub"], countr=False)

                examplestr = ""
                examples = command["examples"]

                for name, value in examples.items():
                    examplestr += f"`{prefix}{cmd}{f' {name}' if name != '' else ''}`- {value}\n"

                embed.add_field(name="Examples", value=examplestr)

        return embed

    def alias_help(self, prefix, alias):
        '''
        generating alias helpcmd
        '''

        #declaring vars
        helpdict = self.client.info["helpcmd"]

        for modulename, module in helpdict.items():
            # lopping throgh modules

            for cmdname, command in module["commands"].items():

                if alias in command["aliases"]:
                    # if cmd is in modules

                    description = f"`{prefix}{alias}{command['syntax']}`\n{command['description']}"

                    embed = discord.Embed(
                        title = f"{cmdname.title()} help page",
                        description = description,
                        color = self.client.color
                    ) # making embed

                    command["aliases"][command["aliases"].index(alias)] = cmdname
                    self.add_value(embed, "Aliases", command["aliases"], countr=False)
                    self.add_value(embed, "Subcommands", command["sub"], countr=False)
                    command["aliases"][command["aliases"].index(cmdname)] = alias
                    # adding subcmd and aliases

                    examplestr = ""
                    examples = command["examples"]

                    for name, value in examples.items():
                        examplestr += f"`{prefix}{alias}{f' {name}' if name != '' else ''}` - {value}\n"

                    embed.add_field(name="Examples", value=examplestr)

        return embed


    async def do_help(self, ctx, arg):
        '''
        Main function for the help command.
        This function requiers ctx and arg. arg can be None.
        '''

        #declaring variables
        helpdict = self.client.info["helpcmd"] # dictionary with help info
        help_type = self.get_req_type(arg) # what type the help request is
        content = None # the content that should be sent as normal message
        prefix = (await f.get_prefixes(self.client, ctx.guild))[0]

        if help_type == "default":
            # if default helpcmd was requested

            embed = self.defult_help(prefix)
            return await ctx.send(content, embed=embed)


        elif help_type == "module":
            # if a module help was requested

            modules = list(helpdict.keys())
            index = modules.index(arg)
            paginator = self.client.utils.paginator(self.client, ctx.author)

            for module in modules:
                embed = self.module_help(prefix, module)
                paginator.add_page(embed)

            await paginator.send(ctx.channel, index=index)



        elif help_type == "cmd":
            # if a command help was requested

            commands = []

            for value in helpdict.values():
                for key in value["commands"].keys():
                    commands.append(key)

            paginator = self.client.utils.paginator(self.client, ctx.author)
            index = commands.index(arg)

            for command in commands:
                embed = self.cmd_help(prefix, command)
                paginator.add_page(embed)

            await paginator.send(ctx.channel, index=index)



        elif help_type == "alias":
            # if a alias help was requested

            embed = self.alias_help(prefix, arg)
            return await ctx.send(content, embed=embed)



        elif help_type == "none":
            # if the request was invalid, send default help with modifyed message content

            embed = self.defult_help(prefix)
            content = f"{ctx.author.mention}, No command by name `{arg}` was found. Showing defult help instead."
            return await ctx.send(content, embed=embed)





    @commands.command(aliases=["h"])
    async def help(self, ctx, arg=None):
        '''
        A command to show help about all other commands.
        No extra permissions requierd.

        To add, edit or remove a command go to info.json under "helpcmd"

        examples:
        ,help
         - Show all commands and modules

        ,help utility
         - Show help about the utility module

        ,help prefix
         - Show help about the prefix command
        '''

        await self.do_help(ctx, arg)

def setup(bot):
    bot.add_cog(helpcmd(bot))
