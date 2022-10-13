import discord, traceback, json
from discord.ext import commands
import mysql.connector  # importing mysql
from .. import functions as f

class cmdlog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        '''
        This function calls whenever a command is runed.
        Here there will be adding one count to the command count and sending that a command was used in noob bot console channel.
        '''

        # saving command usage
        if ctx.command.qualified_name in self.client.command_count:
            # updating local counter
            self.client.info["command count"][ctx.command.qualified_name] += 1

            #updating json file
            self.client.utils.update_json()


        else:
            # updating local counter
            self.client.info["command count"][ctx.command.qualified_name] = 1

            #updating json file
            self.client.utils.update_json()



        # making info embed
        embed = discord.Embed(
            title="Command log",
            description=ctx.message.content
        )

        # adding fields
        embed.add_field(name="command", value=ctx.command.name)
        embed.add_field(name="author", value=ctx.author)
        embed.add_field(name="server", value=ctx.guild.name)
        embed.add_field(name="channel", value=f"{ctx.channel.name}\n({ctx.channel.mention}) [{ctx.channel.id}]")
        embed.add_field(name="message url", value=f"[Jump to message]({ctx.message.jump_url})")

        # setting thumbnail
        embed.set_thumbnail(url=ctx.author.avatar_url)

        # sending the message
        self.client.console_webhook.send(embed=embed, username="Command Compleatin Logger", avatar_url="https://cdn.discordapp.com/attachments/714797824386007070/773836247461658624/nb_command_completion.png")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            channel = self.client.get_channel(self.client.info["console_channel"])
            embed = discord.Embed(
                title="Error",
                description=str(ctx.message.content),
                colour=0xFF0000
            )
            embed.add_field(name="error msg", value=error)
            embed.add_field(name="author", value=ctx.author)
            embed.add_field(name="server", value=f"{ctx.guild.name} ({ctx.guild.id})")
            self.client.console_webhook.send(embed=embed, username="Command Failure Logger", avatar_url="https://cdn.discordapp.com/attachments/714797824386007070/773837178190954506/nb_command_failed.png")


            if f.is_bot_owner(ctx.author, self.client):

                # get data from exception
                etype = type(error)
                trace = error.__traceback__

                # 'traceback' is the stdlib module, `import traceback`.
                lines = traceback.format_exception(etype, error, trace)

                # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
                traceback_text = ''.join(lines)

                for msg in f.split(traceback_text, start="```py\n", end="\n```"):
                    await ctx.send(msg)

            raise error

def setup(bot):
    bot.add_cog(cmdlog(bot))
