import discord
from discord.ext import commands, tasks
from .. import functions as f
from typing import Union

class unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    def find_user(self, guild: discord.Guild, user, bans):

        for entry in bans:
            member = entry.user

            if isinstance(user, int):
                if str(member.id) == str(user):
                    return member

            if str(member) == str(user):
                return member

            if str(member.name) == str(user):
                return member

            if str(user) in str(member):
                return member

        return None

    def unban_check(self, ctx, member, bans):
        '''
        checking atributes and permissions for ban command
        '''

        if not ctx.author.guild_permissions.ban_members and not f.is_bot_owner(ctx.author, self.client):
            return "You are missing a requierd permission (`Ban Members`)."

        if not ctx.guild.me.guild_permissions.ban_members:
            return "I am missing requierd permission (`Ban Members`)."

        if member is None:
            return "No member was specifyed."

        if (self.find_user(ctx.guild, member, bans)) is None:
            return "User was not found"

        return None

    @commands.command()
    async def unban(self, ctx, user: Union[discord.User, int, str]=None, reason: str="No reason specifyed"):
        '''
        unban

        unban a banned user

        syntax:
        ,unban <member> [reason]

        examples:
        ,unban @ultra#6969 im sry lmao
         - unbans ultra with reason: im sry lmao
        '''

        bans = await ctx.guild.bans()

        check_result = self.unban_check(ctx, user, bans)
        if check_result is not None:
            await ctx.send(check_result)
            await ctx.message.add_reaction("\U0000274c")
            return

        user = self.find_user(ctx.guild, user, bans)

        await ctx.guild.unban(user, reason=f"Action done by {ctx.author} (ID: {ctx.author.id}) with reason: {reason}")
        await ctx.send(f"**{user}** was unbanned.")
        await ctx.message.add_reaction("\U00002705")


def setup(bot):
    bot.add_cog(unban(bot))
