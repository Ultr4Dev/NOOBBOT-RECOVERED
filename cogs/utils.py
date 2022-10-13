import discord, time, json, datetime, os, asyncpg, asyncio, copy
from discord.ext import commands, tasks
from discord import Webhook, RequestsWebhookAdapter
import cogs.functions as f
import typing

class Utils():
    def __init__(self, client):
        self.client = client

    async def connect(self):
        print("connecting")
        db = await asyncpg.connect(user = self.client.external["db"]["user"],
                                          password = self.client.external["db"]["pass"],
                                          host = self.client.external["db"]["host"],
                                          port = self.client.external["db"]["port"],
                                          database="noobbot")
        print("connected")
        return db

    def update_json(self):
        file = open(self.client.path, "w")
        json.dump(self.client.info, file, indent=4)
        file.close()

    async def get_prefixes(self):
        resoponses = await self.client.db.fetch("SELECT * FROM prefixes")
        prefixes = {}
        for respons in resoponses:
            respons = dict(respons)
            prefixes[respons["guild_id"]] = respons["prefix"]

        return prefixes

    async def get_auto_react(self):
        resoponses = await self.client.db.fetch("SELECT * FROM auto_react")
        auto_react = {}
        for respons in resoponses:
            respons = dict(respons)
            if respons["channel_id"] in auto_react:
                auto_react[respons["channel_id"]].append(respons["emoji"])
            else:
                auto_react[respons["channel_id"]] = [respons["emoji"]]

        return auto_react

    async def recache(self):
        self.client.cache["prefixes"] = await self.get_prefixes()
        self.client.cache["auto_react"] = await self.get_auto_react()


class Paginator():
    def __init__(self, client: commands.AutoShardedBot, user: discord.User, remove_when_done: bool=False, timeout: int=120, remove_reactions: bool=True):
        self.client = client
        self.pages = []
        self.message = None
        self.page = None
        self.remove_reactions = remove_reactions
        self.remove_when_done = remove_when_done
        self.author = user
        self.timeout = timeout
        self.active = False
        self.preset = None

    def add_page(self, page, index: int=None):
        # add page to paginator

        if index is None:
            # if no index was specifyed, add page to end and return current page list

            self.pages.append(page)

        else:
            # if a index is specifyed
            if len(self.pages) > index:
                # if index is in pages, insert page
                self.pages.insert(index, page)

            else:
                #if index is outside pages, raise custom index error
                raise IndexError(f"Index {index} is out of range. Current list size is only {len(self.pages)}")

        return self.pages
        # return current page list

    def remove_page(self, index: int=0):
        # remove a page from paginator

        if len(self.pages) > index:
            # if index in current pages, remove page and return current page list

            self.pages.pop(index)
            return self.pages

        raise IndexError(f"Index {index} is out of range. Current list size is only {len(self.pages)}")
        # otherwise a error is raised

    def add_custom_footer(self, page: discord.Embed, text: str):
        # adding embed footer if no fo
        page = copy.copy(page)
        if page.footer.text != discord.Embed.Empty:
            return page

        else:

            page.set_footer(text=text, icon_url=page.footer.icon_url)
            return page

    async def edit(self):
        page = self.pages[self.page]

        if type(page) is discord.Embed:
            embed = self.add_custom_footer(page, f"Page {self.page+1}/{len(self.pages)}")
            await self.message.edit(embed=embed)

        else:
            await self.message.edit(content=page)


    def first(self):
        self.page = 0

    def preveous(self):
        if self.page <= 0:
            self.page = len(self.pages)-1

        else:
            self.page -= 1

    def stop(self):
        self.active = False

    def next(self):
        if self.page >= len(self.pages)-1:
            self.page = 0

        else:
            self.page += 1

    def last(self):
        self.page = len(self.pages) - 1

    def start(self):
        self.page = self.preset

    async def listener(self):
        def check(r, u):
            if u == self.author:
                if r.message == self.message:
                    emojis = ["\U000023ea", "\U000025c0", "\U000023f9", "\U000025b6", "\U000023e9"]
                    if self.preset is not None:
                        emojis.append("\U0001f501")
                    if r.emoji in emojis:
                        return True

            return False

        while self.active:

            try:
                r, u = await self.client.wait_for("reaction_add", check=check, timeout=self.timeout)
            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                if type(self.pages[self.page]) == discord.Embed:
                    embed = self.add_custom_footer(self.pages[self.page], f"Time is Up! - Page {self.page+1}/{len(self.pages)-1}")
                    await self.message.edit(embed=embed)
            else:
                if r.emoji in ["\U000023ea", "\U000025c0", "\U000025b6", "\U000023e9", "\U0001f501"]:
                    await self.message.remove_reaction(r, u)
                    if r.emoji == "\U000023ea":
                        self.first()

                    if r.emoji == "\U000025c0":
                        self.preveous()

                    if r.emoji == "\U000025b6":
                        self.next()

                    if r.emoji == "\U000023e9":
                        self.last()

                    if r.emoji == "\U0001f501":
                        self.start()

                    await self.edit()

                    continue

                else:
                    self.active = False
                    await self.message.delete()
                    return None





    async def send(self, channel: discord.TextChannel, index: int=None):
        if index is None:
            self.page = 0
        else:
            self.page = index
            self.preset = index
        if not len(self.pages) > self.page:
            raise IndexError(f"Index {self.page} is out of range. Current list size is only {len(self.pages)}")

        page = self.pages[self.page]

        if type(page) == discord.Embed:
            page = self.add_custom_footer(page, f"Page {index+1}/{len(self.pages)}")
            self.message = await channel.send(embed=page)

        else:
            self.message = await channel.send(page)

        if len(self.pages) > 1:
            await self.message.add_reaction("\U000023ea")
            await self.message.add_reaction("\U000025c0")
            await self.message.add_reaction("\U000023f9")
            await self.message.add_reaction("\U000025b6")
            await self.message.add_reaction("\U000023e9")
            if self.preset:
                await self.message.add_reaction("\U0001f501")
            self.active = True

            await self.listener()
        return None

def owner_only():
    def predicate(ctx):
        return ctx.author.id in [239719341958889473, 569915198974984202]

    return commands.check(predicate)
