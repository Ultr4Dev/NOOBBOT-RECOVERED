import discord, datetime
import time as pythontime
from datetime import timedelta
from discord.ext import commands, tasks
import praw, random
import asyncio
import mysql.connector  # importing mysql
from .. import functions

# Reddit data
reddit = praw.Reddit(client_id="7WnQ89ny0avsUg",
                     client_secret="ITmA0Bkd7JIV-e6VyjCIUEpsie4",
                     password="Noob-Bot-Password123",
                     user_agent="Noob-Bot-Discord",
                     username="Noob-Bot-Discord")
memeupdate = False
memename = []
memelist = []
sub = []

#class
class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.auto_memes = {}

    #task for updating meme list
    @tasks.loop(seconds = 10)
    async def memelistupdate(self):

        #list of subredits to chose from
        choice = random.choice(['memes'])
        subreddit = reddit.subreddit(choice)
        sub.insert(0, choice)

        hot_python = subreddit.hot(limit = 100)
        memeupdate = True
        memelist.clear()
        memename.clear()
        for x in hot_python:
            if (str(x.url)).endswith('.jpg') or (str(x.url)).endswith('.png') or (str(x.url)).endswith('.jpeg'):
                memelist.append(x.url)
                memename.append(x.title)
        memeupdate = False

    #task for checking and sendning auto memes
    @tasks.loop(seconds=1)
    async def auto_meme_check(self):
        try:
            for guild in self.client.guilds:
                auto_memes = self.auto_memes[guild.id]
                for auto_meme in auto_memes:
                    if int(auto_meme["last"]) + int(auto_meme["duration"]) < pythontime.time() and auto_meme["active"]:
                        if memeupdate is True:
                            await asyncio.sleep(0.2)
                        memeurl = random.choice(memelist)
                        ind = memelist.index(memeurl)
                        title = memename[ind]
                        memeembed = discord.Embed(
                            title = f'{title}',
                            colour = discord.Color.red()
                        )
                        memeembed.set_footer(text = f"r/{sub[0]}")
                        memeembed.timestamp = datetime.datetime.utcnow()
                        memeembed.set_image(url=memeurl)

                        channel = self.client.get_channel(auto_meme["channel"])
                        if channel is None:
                            auto_memes.pop(auto_memes.index(auto_meme))
                            self.auto_memes[guild.id] = auto_memes
                            await collection_auto_memes.update_one({"_id": guild.id}, {"$set": {"auto memes": auto_memes}})
                        else:
                            try:
                                await channel.send(embed=memeembed)
                                auto_meme["last"] = pythontime.time()

                                await collection_auto_memes.update_one({"_id": guild.id}, {"$set": {"auto memes": auto_memes}})
                            except:
                                pass
        except Exception as e:
            embed = discord.Embed(title="Auto_meme check error", description=e)
            channel = self.client.get_channel(719594549109850204)
            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):



        for guild in self.client.guilds:
            guild_info = await collection_auto_memes.find_one({"_id": guild.id})

            if guild_info is None:
                post = {"_id":guild.id, "auto memes": []}
                await collection_auto_memes.insert_one(post)
                self.auto_memes[guild.id] = []

            else:
                self.auto_memes[guild.id] = guild_info["auto memes"]

        self.memelistupdate.start()
        self.auto_meme_check.start()




    @commands.command()
    async def meme(self, ctx):
        if memeupdate is True:
            await asyncio.sleep(0.2)
        memeurl = random.choice(memelist)
        ind = memelist.index(memeurl)
        title = memename[ind]
        memeembed = discord.Embed(
            title = f'{title}',
            colour = discord.Color.red()
        )
        memeembed.set_footer(text = f"r/{sub[0]}")
        memeembed.timestamp = datetime.datetime.utcnow()
        memeembed.set_image(url=memeurl)

        text_responses = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, f"Tierd of using the meme command everytime. Use `{ctx.prefix}auto_meme` to get automatic memes in your channel."]
        text_respons = random.choice(text_responses)
        await send_safe(ctx, ctx.channel, text_respons, embed=memeembed)

    @commands.command()
    async def auto_meme(self, ctx, arg="add", *, duration="1m"):
        if ctx.author.permissions_in(ctx.channel).manage_messages or await is_bot_owner(ctx.author):
            if arg == "add":
                words = duration.split(" ")
                #what to run
                run = True
                second = True
                minute = True
                hour = True
                day = True

                #total time
                total_seconds = 0
                total_time = timedelta(0)

                for word in words:
                    if run:
                        if word.endswith("s"):

                            if run and second:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time
                                    total_time += timedelta(seconds=time)
                                    second=False

                                else:
                                    run=False



                        elif word.endswith("m"):

                            if run and minute:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60
                                    total_time += timedelta(minutes=time)
                                    minute=False

                                else:
                                    run=False



                        elif word.endswith("h"):

                            if run and hour:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60*60
                                    total_time += timedelta(hours=time)
                                    hour=False

                                else:
                                    run=False


                        elif word.endswith("d"):

                            if run and day:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60*60*24
                                    total_time += timedelta(days=time)
                                    day=False

                                else:
                                    run=False

                auto_memes = self.auto_memes[ctx.guild.id]
                auto_meme_config = False
                for auto_meme in auto_memes:
                    if auto_meme["channel"] == ctx.channel.id:
                        auto_meme_config = True

                if total_seconds > 2:
                    if not auto_meme_config:
                        self.auto_memes[ctx.guild.id].append({"last":int(pythontime.time()), "duration": int(total_seconds), "channel":ctx.channel.id, "active":True})
                        await collection_auto_memes.update_one({"_id": ctx.guild.id}, {"$set": {"auto memes": self.auto_memes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, f"Auto meme duration set to: {total_time}")
                    else:
                        await send_safe(ctx, ctx.channel, f"This channel already has a auto meme configured. If it is not running use the command `{ctx.prefix}auto_meme unpaues` to enable it.")
                else:
                    await send_safe(ctx, ctx.channel, "No")

            if arg == "pause":
                auto_memes = self.auto_memes[ctx.guild.id]
                auto_meme_config = False
                for auto_meme in auto_memes:

                    if auto_meme["channel"] == ctx.channel.id:
                        auto_meme_config = True

                    if auto_meme_config:
                        auto_meme["active"] = False
                        self.auto_memes[ctx.guild.id] = auto_memes
                        await collection_auto_memes.update_one({"_id": ctx.guild.id}, {"$set": {"auto memes": self.auto_memes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, "This channel's auto meme has been paused")

            if arg == "unpause" or arg == "resume" or arg == "stop":
                auto_memes = self.auto_memes[ctx.guild.id]
                auto_meme_config = False
                for auto_meme in auto_memes:

                    if auto_meme["channel"] == ctx.channel.id:
                        auto_meme_config = True

                    if auto_meme_config:
                        auto_meme["active"] = True
                        self.auto_memes[ctx.guild.id] = auto_memes
                        await collection_auto_memes.update_one({"_id": ctx.guild.id}, {"$set": {"auto memes": self.auto_memes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, "This channel's auto meme has been unpaused")

            if arg == "remove":
                auto_memes = self.auto_memes[ctx.guild.id]
                auto_meme_config = False
                for auto_meme in auto_memes:

                    if auto_meme["channel"] == ctx.channel.id:
                        auto_meme_config = True

                    if auto_meme_config:
                        auto_memes.pop(auto_memes.index(auto_meme))
                        self.auto_memes[ctx.guild.id] = auto_memes
                        await collection_auto_memes.update_one({"_id": ctx.guild.id}, {"$set": {"auto memes": self.auto_memes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, "This channel's auto meme has been removed")

            if arg == "edit":
                words = duration.split(" ")
                #what to run
                run = True
                second = True
                minute = True
                hour = True
                day = True

                #total time
                total_seconds = 0
                total_time = timedelta(0)

                for word in words:
                    if run:
                        if word.endswith("s"):

                            if run and second:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time
                                    total_time += timedelta(seconds=time)
                                    second=False

                                else:
                                    run=False



                        elif word.endswith("m"):

                            if run and minute:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60
                                    total_time += timedelta(minutes=time)
                                    minute=False

                                else:
                                    run=False



                        elif word.endswith("h"):

                            if run and hour:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60*60
                                    total_time += timedelta(hours=time)
                                    hour=False

                                else:
                                    run=False


                        elif word.endswith("d"):

                            if run and day:
                                is_time = True

                                try:
                                    time = int(word[:-1])
                                except ValueError:
                                    is_time = False
                                    run = False

                                if is_time:
                                    total_seconds += time*60*60*24
                                    total_time += timedelta(days=time)
                                    day=False

                                else:
                                    run=False

                auto_memes = self.auto_memes[ctx.guild.id]
                auto_meme_config = False
                for auto_meme in auto_memes:
                    if auto_meme["channel"] == ctx.channel.id:
                        auto_meme_config = True

                if total_seconds > 2:
                    if auto_meme_config:
                        self.auto_memes[ctx.guild.id][self.auto_memes[ctx.guild.id].index(auto_meme)] = {"last":int(pythontime.time()), "duration": int(total_seconds), "channel":ctx.channel.id, "active":True}
                        await collection_auto_memes.update_one({"_id": ctx.guild.id}, {"$set": {"auto memes": self.auto_memes[ctx.guild.id]}})
                        await send_safe(ctx, ctx.channel, f"Auto meme duration set to: {total_time}")
                    else:
                        await send_safe(ctx, ctx.channel, f"This channel already has no auto meme configured.")
                else:
                    await send_safe(ctx, ctx.channel, "No")






def setup(bot):
    bot.add_cog(meme(bot))
