from github import Github
import discord, asyncio, os, sys
from discord.ext import commands, tasks
from .. import functions as f
'''
Not yet implemented
'''
# Declare the github token and select repo
g = Github("")
repo = g.get_repo("")


class modulename(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=["re"])
    @commands.is_owner()
    async def restart(self, ctx):
        pass

    @restart.command(aliases=["c"])
    async def cogs(self, ctx, *, cogs="all"):
        args = cogs.split(" ")
        if len(args) > 1:
            for cog in args:
                cogs = cog.strip("cogs.")
        else:
            cogs = cogs.strip("cogs.")

        # making embeds
        embed_1 = discord.Embed(
            title="Update source code confirmation",
            description="Are you sure that you want to restart my cogs?",
            color=self.client.color # preset color that matches the bot them
        ) # start embed

        embed_2 = discord.Embed(
            title="I'm alive",
            description = "YAY, i get to live another day!",
            color = 0x00FF00 # green
        ) # if user decided not to kill the bot

        embed_3 = discord.Embed(
            title="To slow",
            description = "YAY, i get to live another day!",
            color = 0x00FF00 # green
        ) # if user where to slow

        embed_4 = discord.Embed(
            title = "Updating source code for code 🔁",
            description = "Downloading latest files from github ⏬",
            color = self.client.color # preset color that matches the bot them
        ) # during github download

        embed_5 = discord.Embed(
            title = "Updating source code for cogs 🔁",
            description = "Restarting cogs...",
            color = self.client.color # red
        ) # when bot has been killed

        embed_6 = discord.Embed(
            title = "Updating source code for cogs 🔁",
            description = "Done!",
            color = 0x00FF00 # red
        ) # when bot has been killed

        #sending message
        msg = await ctx.send(embed=embed_1)

        # adding vote reactions for confermation
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")



        # check for checking that author and emoji is correct
        def check(r, a):
            return r.message.id == msg.id and a.id == ctx.author.id and str(r.emoji) in ["✅", "❎"]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)

        except asyncio.TimeoutError:
            await msg.edit(embed=embed_3)
            await ctx.send(f"{ctx.author.mention}, ⏱️ Time is up!")

        else:
            try:
                await msg.clear_reactions()
            except:
                pass
            if reaction.emoji == "❎":
                await msg.edit(embed=embed_2)

            else:
                await msg.edit(embed=embed_4)

                # os.system('git pull')

                await msg.edit(embed=embed_5)

                result = f.reload(self.client, cogs)

                if len(result["failed"]) > 0:
                    failed = ""
                    for key, value in result["failed"].items():
                        failed += f"`{key}`\n - {value}\n\n"

                    failed.strip("\n")

                    embed_6.add_field(name="Failed", value=failed, inline=False)

                success = ("\n".join(result["succes"]))
                if len(success) > 0:
                    embed_6.add_field(name="Successed", value=success)

                await msg.edit(embed=embed_6)

    @restart.command(name="bot", aliases=["b"])
    async def _bot(self, ctx, branch="master"):

        # making embeds
        embed_1 = discord.Embed(
            title="Update source code confirmation",
            description="Are you shure that you want to restart me?",
            color=self.client.color # preset color that matches the bot them
        ) # start embed

        embed_2 = discord.Embed(
            title="I'm alive",
            description = "YAY, i get to live another day!",
            color = 0x00FF00 # green
        ) # if user decided not to kill the bot

        embed_3 = discord.Embed(
            title="To slow",
            description = "YAY, i get to live another day!",
            color = 0x00FF00 # green
        ) # if user where to slow

        embed_4 = discord.Embed(
            title = "Updating source code 🔁",
            description = "Downloading latest files from github ⏬",
            color = self.client.color # preset color that matches the bot them
        ) # during github download

        embed_5 = discord.Embed(
            title = "Updating source code 🔁",
            description = "I had a stroke and died :(",
            color = 0xFF0000 # red
        ) # when bot has been killed

        #sending message
        msg = await ctx.send(embed=embed_1)

        # adding vote reactions for confermation
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")



        # check for checking that author and emoji is correct
        def check(r, a):
            return r.message.id == msg.id and a.id == ctx.author.id and str(r.emoji) in ["✅", "❎"]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)

        except asyncio.TimeoutError:
            await msg.edit(embed=embed_3)
            await ctx.send(f"{ctx.author.mention}, ⏱️ Time is up!")

        else:
            await msg.clear_reactions()
            if reaction.emoji == "❎":
                await msg.edit(embed=embed_2)

            else:
                await msg.edit(embed=embed_4)

                # os.system('git pull')

                await msg.edit(embed=embed_5)

                sys.exit()


def setup(bot):
    bot.add_cog(modulename(bot))
