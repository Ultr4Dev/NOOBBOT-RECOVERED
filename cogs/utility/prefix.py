import discord, time
from discord.ext import commands, tasks
from .. import functions as f



class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["prefixes"])
    async def prefix(self, ctx, *, new_prefix=None):
        '''
        manage server prefixes

        examples:
        nb!prefix
         - shows the current prefix

        nb!prefix !
         - sets server prefix to !
        '''

        old_prefix = await f.get_prefixes(self.client, ctx.guild)
        if new_prefix is None:

            return await ctx.send(f"My prefix here is `{old_prefix}`")

        if not ctx.author.guild_permissions.manage_guild:
            return await ctx.send(f"{ctx.author.mention}, you are missing `Manage Guild` permission")

        if len(new_prefix) > 100:
            return await ctx.send(f"A prefix canot be longer than 100")

        if new_prefix == ",":
            self.client.cache["prefixes"].pop(ctx.guild.id)
            await self.client.db.execute(f"DELETE FROM prefixes WHERE guild_id={ctx.guild.id}")
            return await ctx.send("Prefex updated to default")

        if old_prefix != ",":
            # if old prefix was not default, update current row
            self.client.cache["prefixes"][ctx.guild.id] = new_prefix
            query = "UPDATE prefixes SET prefix = $1 WHERE guild_id=$2"
            await self.client.db.execute(query, new_prefix, ctx.guild.id)

        else:
            # if old prefix was default, insert a new row
            self.client.cache["prefixes"][ctx.guild.id] = new_prefix
            query = "INSERT INTO prefixes (guild_id, prefix) VALUES ($1, $2)"
            await self.client.db.execute(query, ctx.guild.id, new_prefix)

        return await ctx.send(f"Prefix updated to `{discord.utils.escape_markdown(new_prefix)}`")




def setup(bot):
    bot.add_cog(prefix(bot))
