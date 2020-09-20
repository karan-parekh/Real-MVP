
from discord.ext import commands


class Discord:

    def __init__(self, token: str):

        self.token  = token
        self.client = commands.Bot(command_prefix='.')

    def post(self, message):
        """
        Posts the message on discord
        """

    def run_client(self):

        self.client.run(self.token)

    async def on_ready(self):
        pass
