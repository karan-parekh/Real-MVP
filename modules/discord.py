
from pkg.discord import Discord


class DiscordModule:

    def __init__(self, token: str):

        self.token = token

    def post_games(self):
        """
        Posts the games in the new.json to the Discord channel
        """