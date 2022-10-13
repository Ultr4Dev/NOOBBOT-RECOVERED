import discord, inspect
from discord.ext import commands, tasks
from .. import functions as f

class src(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command(aliases=["src"])
    @commands.is_owner()
    async def source(self, ctx, command_name: str):
        '''
        Owner command for showing command code

        examples:
        ,src poll
        - show the source code for poll command
        '''

        command = self.client.get_command(command_name)
        # getting command object

        if command is None:
            # command was not found

            await ctx.send(f"No command by name ´{command_name}´ was found!")
            #sending return message

            return

        # if command was found
        source_lines, _ = inspect.getsourcelines(command.callback)
        source_lines = ''.join(source_lines)

        for msg in f.split(source_lines, end="```", start="```py\n", spliter="\n"):
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(src(bot))
