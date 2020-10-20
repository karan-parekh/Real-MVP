import os
import discord

from discord.ext import commands, tasks

from utils.env import env
from utils.helpers import post_to_discord
from main import Gamer
from loguru import logger


client = commands.Bot(command_prefix='gg ')

client.remove_command('help')


@client.command(help="Load a command")
async def load(ctx, extension):

    logger.info("Loading extension: {}".format(extension))
    client.load_extension("cogs.{}".format(extension))
    logger.info("Extension loaded successfully")


@client.command(help="Unload a command")
async def unload(ctx, extension):

    logger.info("Unloading extension: {}".format(extension))
    client.unload_extension("cogs.{}".format(extension))
    logger.info("Extension unloaded successfully")


@client.command(help="Reload a command")
async def reload(ctx, extension):

    logger.info("Reloading Extension: {}".format(extension))

    client.load_extension("cogs.{}".format(extension))
    client.unload_extension("cogs.{}".format(extension))

    logger.info("Extension reloaded successfully")


for file in os.listdir('./cogs'):

    if file.startswith("__"):
        continue

    if file.endswith('.py'):
        client.load_extension("cogs.{}".format(file[:-3]))


@client.event
async def on_ready():

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='gg'))

    logger.info("Bot is ready")

    check.start()


@tasks.loop(hours=24)
async def check():

    games = Gamer().run()

    if not games:
        return

    channels = client.get_all_channels()

    for channel in channels:

        if channel.name == 'free-games':

            await post_to_discord(games, "New Free Games", channel=channel)


if __name__ == "__main__":

    client.run(env('DISCORD_TOKEN'))
