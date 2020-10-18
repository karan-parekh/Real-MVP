
from discord.guild import Guild
from discord.abc import GuildChannel
from discord.ext import commands
from main import Gamer
from typing import Optional

from utils.helpers import post_to_discord


class Commands(commands.Cog):

    FREE_GAMES_CHANNEL = 'free-games'

    def __init__(self, client):

        self.client = client

    @commands.command(help="Lists all free games from all stores")
    async def free(self, ctx):

        games = Gamer().get_games_from_data('new.json')

        if games:
            await post_to_discord(games, "Current Free Games", ctx)

    @commands.command(help="Lists all free games from a store")
    async def store(self, ctx, name: str):

        games = Gamer().get_games_from_data('new.json')

        store_games = [game for game in games if game['store'] == name]

        if not store_games:
            await post_to_discord([], "No games found for {}".format(name), ctx)
            return

        await post_to_discord(store_games, "Currently Free on {}".format(name), ctx)

    @commands.command(help="Subscribes to free games updates")
    async def sub(self, ctx):

        guild = ctx.message.guild

        if not self._get_free_channel(guild):

            await guild.create_text_channel(self.FREE_GAMES_CHANNEL)

    @commands.command(help="Un-subscribes to free games updates")
    async def unsub(self, ctx):

        guild   = ctx.message.guild
        channel = self._get_free_channel(guild)

        if channel:
            await channel.delete()

    def _get_free_channel(self, guild: Guild) -> Optional[GuildChannel]:

        for channel in guild.channels:

            if channel.name == self.FREE_GAMES_CHANNEL:

                return channel


def setup(client):

    client.add_cog(Commands(client))
