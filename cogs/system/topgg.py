from discord.ext import commands

import dbl


class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcxNDgwMjI3NTcyNTM0NDgzOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTk1ODc4Mzk2fQ.N0OxvFLFwCnu9b-UnFG1f81ve-isPJEpnfwP9iJNdAE' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='https://canary.discord.com/api/webhooks/766775343888859146/LsIh6M0C5y98GihMF_M92KFrynQfQX4cvwBbVFDaE2biI825zUBUUOIgOfOZvvvFRQ3F', webhook_auth='password', webhook_port=5000)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        self.bot.console_webhook.send(f"Received a upvote:\n{data}")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        self.bot.console_webhook.send(f"Received a test upvote:\n{data}")


def setup(bot):
    bot.add_cog(TopGG(bot))
