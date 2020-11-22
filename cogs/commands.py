import discord

from discord.guild import Guild
from discord.abc import GuildChannel
from discord.ext import commands
from main import Gamer
from typing import Optional
from sources import Platform, Service

from utils.helpers import post_to_discord
from . import MVP


class Commands(commands.Cog):

    FREE_GAMES_CHANNEL = 'free-games'

    def __init__(self, client):

        self.client = client
        self.mvp    = MVP()

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(title="Commands")

        commands_ = {
            "free"     : "Lists all free games from all sources",
            "help"     : "Show this message",
            "stores"   : "List all supported stores",
            "store"    : "Lists all free games for a store: <name>",
            "platforms": "List all supported platforms",
            "platform" : "Lists all free games for a platform: <name>",
            "sub"      : "Subscribes to free games updates",
            "unsub"    : "Un-subscribes to free games updates"
        }

        for name, help_ in commands_.items():

            embed.add_field(
                name=name,
                value=help_,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(help="Lists all free games from all sources")
    async def free(self, ctx):

        games = self.mvp.get_latest_games()

        if games:
            await post_to_discord(games, "Current Free Games", ctx=ctx)

    @commands.command(help="Lists all free games from a store")
    async def store(self, ctx, name: str):

        games = Gamer().get_games_from_data('new.json')

        store_games = [game for game in games if game['store'] == name]

        if not store_games:
            await post_to_discord([], "No games found for {}".format(name), ctx=ctx)
            return

        await post_to_discord(store_games, "Currently Free on {}".format(name), ctx=ctx)

    @commands.command()
    async def platform(self, ctx, name: str):

        pass

    @commands.command()
    async def stores(self, ctx):

        embed = discord.Embed(title="Supported sources")

        for service in Service.ui_index():

            embed.add_field(
                name=service['name'],
                value="code: {}".format(service['code']),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def platforms(self, ctx):

        embed = discord.Embed(title="Supported platforms")

        for platform in Platform.ui_index():

            embed.add_field(
                name=platform['name'],
                value="code: {}".format(platform['code']),
                inline=False
            )

        await ctx.send(embed=embed)

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
