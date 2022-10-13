import discord
from typing import Union
from discord.ext import commands, tasks
from .. import functions as f

class bancmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check_roles(self, guild, user1, user2):
        '''
        function for checking who has the highest role of two users

        if user1 has the highest role, return will be True
        else False
        '''

        return guild.roles.index(user1.top_role) > guild.roles.index(user2.top_role)

    def ban_check(self, ctx, member):
        '''
        checking atributes and permissions for ban command
        '''

        if not ctx.author.guild_permissions.ban_members and not f.is_bot_owner(ctx.author, self.client):
            return "You are missing a requierd permission (`Ban Members`)."

        if not ctx.guild.me.guild_permissions.ban_members:
            return "I am missing requierd permission (`Ban Members`)."

        if isinstance(member, str):
            return "Unknown member"

        if member is None:
            return "No member was specifyed."

        if isinstance(member, discord.Member) or isinstance(member, discord.User):
            # bot owner check can only be done if it is a user or member

            if f.is_bot_owner(member, self.client):
                return "Thats one of my devs, and im sadly not alowed to ban them."

        if isinstance(member, discord.Member):
            # these checks can only be done if it is a member

            if ctx.guild.owner == member:
                return "Thats the server owner..."

            if not self.check_roles(ctx.guild, ctx.author, member) and not f.is_bot_owner(ctx.author, self.client):
                return "You must be higher than the person you want to ban."

            if not self.check_roles(ctx.guild, ctx.guild.me, member):
                return "This person has a higher role than me."



    @commands.command()
    async def ban(self, ctx, member: Union[discord.Member, discord.User, int, str]=None, *, reason: str="No reason specifyed"):
        '''
        Ban

        Used to ban a member from the guild

        snyntax:
        ,ban <member> [reason]

        examples:
        ,ban @ultra#6969 he is dumb
         - bans ultra with reason "he is dumb"
        '''

        check_result = self.ban_check(ctx, member)
        # checking if the command is called with valid permissions and arguments

        if check_result is not None:
            #if the command was called invalid, add cross reaction and send return message
            await ctx.message.add_reaction("\U0000274c")
            return await ctx.send(check_result)

        if isinstance(member, discord.Member):
            await ctx.guild.ban(member, reason=f"Action done by {ctx.author} (ID: {ctx.author.id}) with reason: {reason}")
            await ctx.send(f"**{member}** was banned")
            await ctx.message.add_reaction("\U00002705")
            return

        # banning user by id
        member = await self.client.fetch_user(member)
        # fetching user

        await ctx.guild.ban(member, reason=f"Action done by {ctx.author} (ID: {ctx.author.id}) with reason: {reason}")
        # banning

        await ctx.send(f"**{member}** was banned")
        await ctx.message.add_reaction("\U00002705")
        #response




def setup(bot):
    bot.add_cog(bancmd(bot))
