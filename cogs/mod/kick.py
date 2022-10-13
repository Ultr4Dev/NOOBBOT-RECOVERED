import discord
from typing import Optional
from discord.ext import commands, tasks
from .. import functions as f

class kickcmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check_roles(self, guild, user1, user2):
        '''
        function for checking who has the highest role of two users

        if user1 has the highest role, return will be True
        else False
        '''

        return guild.roles.index(user1.top_role) > guild.roles.index(user2.top_role)

    def kick_check(self, ctx, member):
        '''
        checking atributes and permissions for kick command
        '''

        if not ctx.author.guild_permissions.kick_members and not f.is_bot_owner(ctx.author, self.client):
            return "You are missing a requierd permission (`kick Members`)."

        if not ctx.guild.me.guild_permissions.kick_members:
            return "I am missing requierd permission (`kick Members`)."

        if member is None:
            return "No member was specifyed."

        if ctx.guild.owner == member:
            return "Thats the server owner..."

        if f.is_bot_owner(member, self.client):
            return "Thats one of my devs, and im sadly not alowed to kick them."

        if not self.check_roles(ctx.guild, ctx.author, member) and not f.is_bot_owner(ctx.author, self.client):
            return "You must be higher than the person you want to kick."

        if not self.check_roles(ctx.guild, ctx.guild.me, member):
            return "This person has a higher role than me."



    @commands.command()
    async def kick(self, ctx, member: Optional[discord.Member], *, reason="No reason specifyed"):
        '''
        kick

        Used to kick a member from the guild

        snyntax:
        ,kick <member> [reason]

        examples:
        ,kick @ultra#6969 he is dumb
         - kick ultra with reason "he is dumb"
        '''

        check_result = self.kick_check(ctx, member)
        # checking if the command is called with valid permissions and arguments

        if check_result is not None:
            #if the command was called invalid, add cross reaction and send return message
            return await ctx.send(check_result)
            await ctx.message.add_reaction("\U0000274c")

        await member.kick(reason=f"Action done by {ctx.author} (ID: {ctx.author.id}) with reason: {reason}")
        await ctx.send(f"**{member}** was kickned")
        await ctx.message.add_reaction("\U00002705")




def setup(bot):
    bot.add_cog(kickcmd(bot))
