import discord, traceback, copy
from discord.ext import commands, tasks
from .. import functions as f

class poll():

    def __init__(self, client, question, author, uppvote="<a:Tick_Yes:778551286840688651>", downvote="<a:Tick_No:778551399675199509>"):
        self.client = client
        self.message = None
        self.id = None
        self.channel = None
        self.uppvotes = 0
        self.downvotes = 0
        self.uppvote = uppvote
        self.downvote = downvote
        self.question = question[:1].upper() + question[1:] + "?" if not question.endswith("?") else ""

        self.author = author
        self.embed = embed = discord.Embed(
            title=f"{self.author.name}'s poll",
            description=self.question,
            color=0x44e0e3
        )

    async def status(self):

        reactions = self.message.reactions

        for reaction in reactions:

            if str(reaction.emoji) in [self.uppvote, self.downvote]:
                users = await reaction.users().flatten()

                if str(reaction.emoji) == self.uppvote:
                    uppvotes = 0

                    for user in users:
                        if not user.bot:
                            uppvotes += 1


                if str(reaction.emoji) == self.downvote:
                    downvotes = 0

                    for user in users:
                        if not user.bot:
                            downvotes += 1


        if uppvotes > downvotes:
            return "👍 - Positive"

        if uppvotes < downvotes:
            return "👎 - Negative"

        return "🤷‍♂️ - Equal"



    async def initiate(self, location):
        '''
        Send the poll message.
        '''

        embed = copy.copy(self.embed)
        embed.add_field(name="Status", value="Preparing...")
        # creating embed

        message = await location.send(embed=embed)
        await message.add_reaction(self.uppvote)
        await message.add_reaction(self.downvote)
        # sending message and adding reactions

        embed = copy.copy(self.embed)
        embed.add_field(name="Status", value="🤷‍♂️ - Equal")
        # creating new embed

        await message.edit(embed=embed)
        # editing message

        self.message = message
        self.id = message.id
        self.channel = message.channel

    async def update(self):

        self.message = await self.channel.fetch_message(self.id)

        status = await self.status()
        # current message status

        embed = copy.copy(self.embed)
        embed.add_field(name="Status", value=status)
        # making embed

        await self.message.edit(embed = embed)
        # edit message




class pollcmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.polls = []
        self.update = []

    def get_poll(self, id):

        for poll in self.polls:
            if poll.id == id:
                return poll

        return None

    @commands.command(name="poll")
    async def _poll(self, ctx, *, question: str = None):
        global poll
        '''
        A common fun command. Used to ask a yes or no question with reactions.

        examples:
        ,poll Is this a good command?
         - the bot will send a embed contaning the question and add two rections for yes and no.
        '''

        if question is None:
            if f.ba(ctx.guild.id):
                await ctx.send("You didn't ask a question, why?")

        new_poll = poll(self.client, question, ctx.author)
        await new_poll.initiate(ctx.channel)
        # making poll and initiating poll message

        self.polls.append(new_poll)
        # adding poll to poll list

        await ctx.message.delete()


    @tasks.loop(seconds=1)
    async def poll_update(self):
        '''
        Task for updating polls
        '''



        for poll in self.update:
            await poll.update()

        self.update = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''
        will be called each time the bot detects a reaction.
        if the reaction was on a poll message we will set that message as "active" telling the task it has to be updated
        '''

        poll = self.get_poll(payload.message_id)

        if poll is not None:
            if not self.client.get_user(payload.user_id).bot:
                if poll not in self.update:
                    self.update.append(poll)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        '''
        will be called each time the bot detects a reaction removed.
        if the reaction was on a poll message we will set that message as "active" telling the task it has to be updated
        '''

        poll = self.get_poll(payload.message_id)

        if poll is not None:
            if poll not in self.update:
                self.update.append(poll)

    def start(self):
        self.poll_update.start()


def setup(bot):
    obj = pollcmd(bot)
    obj.start()
    bot.add_cog(obj)
