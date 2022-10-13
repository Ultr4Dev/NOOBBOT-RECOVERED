import discord, asyncio, datetime
from discord.ext import commands
from .. import functions as f
import time

class purge(commands.Cog):
    def __init__(self, client):
        self.client = client



    def values(self, guild, arg):

        '''
        Function for generating tuple with member, limit and text
        '''

        # variables that will be returned
        member = None
        limit = None
        text = None

        # arguments in list
        args = arg.split(" ")

        member = f.get_member(guild, args[0])
        # getting member from custom function



        if member is None:
            # if member is None

            if args[0].isdigit():
                # if first argument in a number

                limit = args[0]
                # setting limit to argument 1

            if len(args) > 1:
                # if there is more than 1 argument

                member = f.get_member(guild, args[1])
                # getting member from custom function

        else:
            # if member was succesfully found

            if len(args) > 1:
                # if there is more than 1 argument

                if args[1].isdigit():
                    # if second argument is a number

                    limit = args[1]
                    # setting limit to argument 2

        if limit is None and member is None:
            # if both limit and member was not found. set text to alla arguments
            text = arg

        if limit is None and member is not None:
            # if only limit was None. set text to all arguments except first

            if len(args) > 1:
                # if there is more than 1 argument

                text = "" # the text variable
                for arg in args[1:]:
                    # looping throgh arguments

                    text += f"{arg} "
                    # argument added to text

                text = text.strip(" ")
                # removing extra space from text


        if limit is not None and member is None:
            # if only member was None. set text to all arguments except first

            if len(args) > 1:
                # if there is more than 1 argument

                text = ""# the text variable
                for arg in args[1:]:
                    # looping throgh arguments

                    text += f" {arg}"
                    # argument added to text

                text = text.strip(" ")
                # removing extra space from text

        if limit is not None and member is not None:
            # if nether member and limit was None. set text to all arguments except first and second

            if len(args) > 2:
                # if there is more than 2 argument

                text = ""# the text variable
                for arg in args[2:]:
                    # looping throgh arguments

                    text += f" {arg}"
                    # argument added to text

                text = text.strip(" ")
                # removing extra space in the begining and end from text


        #returning result
        limit = 1000 if limit == None else int(limit)
        print(f"({limit}, {member}, {text})")
        return (limit, member, text)


    async def purgeing(self, ctx, arg):

        '''
        This function actualy purges
        '''


        if arg is None:

            # if argument is None. Request value

            if not f.is_bot_owner(ctx.author, self.client):
                await ctx.send("Please specify the amount of messages to be deleted or some other arguments!")

            else:

                try:
                    # trying to purge
                    msg = await ctx.channel.purge(limit=1000, after=datetime.datetime.utcnow()-datetime.timedelta(days=14))
                    await ctx.send(f"`{len(msg)-1}` messages", delete_after=3)

                except:
                    #if purging failed, do nothing
                    pass

        else:

            t2 = time.time()
            (limit, member, text) = self.values(ctx.guild, arg)
            print(f"getting values took: {time.time()-t2}")


            limit = int(limit)
            ctx.countr = 1 if member is None else 0

            def check(m):
                return_msg = True

                if text is not None:
                    return_msg = text.lower() in m.content.lower()

                if member is not None and return_msg is True:
                    return_msg = m.author.id == member.id

                if ctx.countr >= limit:
                    return_msg = False

                if m.id == ctx.message.id:
                    return_msg = True

                return return_msg



            try:
                t3 = time.time()
                msg = await ctx.channel.purge(limit=limit + 1, check=check, after=datetime.datetime.utcnow()-datetime.timedelta(days=14))
                await ctx.send(f"`{len(msg)-1}` messages", delete_after=1)
                print(f"Main purge took {time.time()-t3}")

            except:
                pass



    def purge_permission_check(self, channel: discord.TextChannel=None):
        '''
        A function for checking if bot has necesary permissions in the channel to purge in
        '''

        # making sure channel is not None and right type
        if channel is None or not isinstance(channel, discord.TextChannel):

            #raise syntax error
            raise SyntaxError("Channel must be discord.TextChannel")

        else:
            # returns True or False if bot has manage permission
            return channel.guild.me.permissions_in(channel).manage_messages



    async def do_purge(self, ctx, args):
        '''
        Main function for the purge command
        '''

        if not self.purge_permission_check(channel = ctx.channel):
            # missing permissions

            #checking if message should be sent
            if f.bmp(ctx.guild.id):

                #sending message
                await f.send_safe(ctx, ctx.channel, ":warning: Failed to proceed command due to missing permissions (`manage messages`) :warning:")

        else:
            t = time.time()
            await self.purgeing(ctx, args)
            print(f"total time:{time.time()-t}")


    @commands.command(aliases=["p", "delete", "del"])
    async def purge(self, ctx, *, args = None):

        '''
        A command for deleting multiple messages on one channel

        examples:
        nb!purge 10
         - delete 10 messages in the channel the command is called in

        nb!purge 10 @ultra#6969
         - delete 10 message from ultra in the channel the command was called in

        nb!purge 10 text
         - delte 10 messages that contains "text" in the channel the command was called in

        nb!purge
         - delete all messages in the channel the command was called in

        '''

        if ctx.author.permissions_in(ctx.channel).manage_messages:
            await self.do_purge(ctx, args)


def setup(bot):
    bot.add_cog(purge(bot))
