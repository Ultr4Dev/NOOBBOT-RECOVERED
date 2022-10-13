import discord
from discord.ext import commands

class UserData(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def add_member(self, member):
        member_in_db = await self.client.db.fetchrow(f"SELECT * FROM users WHERE user_id={member.id}")
        if member_in_db is None:
            await self.client.db.execute(f"INSERT INTO users (user_id, )")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

def setup(client):
    client.add_cog(UserData(client))
