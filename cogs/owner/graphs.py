import discord
from discord.ext import commands, tasks
from .. import functions as f
import matplotlib.pyplot as plt
from collections import Counter
import io

class graphs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def usage(self , ctx):
        keys = list(dict(Counter(self.client.command_count).most_common()).keys())
        values = list(dict(Counter(self.client.command_count).most_common()).values())

        labels = keys
        sizes = values
        colors = None
        explode = ()
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels ,startangle=90 , colors = colors , textprops={'color':"w"}, radius=10, rotatelabels=True)
        ax1.axis('equal')

        buf = io.BytesIO()

        plt.savefig(buf, format="png" , transparent = True)
        buf.seek(0)
        await ctx.send(file = discord.File(buf , filename = "Graph.png"))
        plt.close()

def setup(bot):
    bot.add_cog(graphs(bot))
