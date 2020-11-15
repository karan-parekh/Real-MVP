import discord

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

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(title="Commands")

        commands_ = {
            "free": "Lists all free games from all sources",
            "store": "Lists all free games for a store: <name>",
            "sources": "List all supported sources",
            "sub": "Subscribes to free games updates",
            "unsub": "Un-subscribes to free games updates"
        }

        for name, help_ in commands_.items():

            embed.add_field(
                name=name,
                value=help_,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def stores(self, ctx):

        embed = discord.Embed(title="Supported sources")

        embed.add_field(
            name='PlayStation Store',
            value='code: psn'
        )

        await ctx.send(embed=embed)

    @commands.command(help="Lists all free games from all sources")
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
