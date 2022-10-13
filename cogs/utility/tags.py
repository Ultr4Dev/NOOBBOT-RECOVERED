from ..utils import *

class tags():
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(tags(client))
