import discord, traceback
from discord.ext import commands, tasks
from .. import functions as f

class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def eval(self, ctx, *, evalthingy=None):
        if f.is_bot_owner(ctx.author, self.client):
            error = "no error"
            try:
                result = eval(evalthingy)
            except Exception as e:
                error = e

            if error == "no error":
                typet = str(type(result))

                embed = discord.Embed(title="Eval exicution", description=f"**input**\n```py\n{evalthingy}\n```")
                embed.add_field(name="Output", value=f"\n```css\n{result}\n```", inline=False)
                embed.add_field(name="Type", value=f"\n```fix\n{typet}\n```", inline=False)
                await f.send_safe(ctx, ctx.channel, embed=embed)

            else:
                # get data from exception
                etype = type(error)
                trace = error.__traceback__

                # 'traceback' is the stdlib module, `import traceback`.
                lines = traceback.format_exception(etype, error, trace)

                # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
                traceback_text = ''.join(lines)

                await f.send_safe(ctx, ctx.channel, f.split(traceback_text, start="```py\n", end="\n```"))
        else:

            await ctx.send("This command is only for bot owners")


def setup(bot):
    bot.add_cog(Eval(bot))
