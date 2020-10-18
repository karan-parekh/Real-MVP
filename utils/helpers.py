from typing import List

import discord
from loguru import logger


def read_newline_sep_file(filename) -> list:
    """Returns a list of values separated by new lines in the file """

    with open(filename, 'r') as file:
        values = []

        for line in file.readlines():
            values.append(line.strip('\n\r'))

    return values


def read_file(path: str) -> str:
    """
    Reads text from file and returns string
    """

    with open(path, 'r') as file:

        return file.read()


def write_to_file(path: str, data: str):
    """
    Writes the data to file
    """

    with open(path, 'w') as file:

        file.write(data)


async def post_to_discord(games: List[dict], title: str, ctx=None, channel=None):

    if not any([ctx, channel]):

        logger.error("Expected at least 'ctx' or 'client' object")

        raise NoConnectionElement("Expected at least 'ctx' or 'client' object")

    embed = discord.Embed(title=title)

    for game in games:

        embed.add_field(
            name=game['title'],
            value="is free on [{}]({})".format(game['store'], game['link']),
            inline=False
        )

    if ctx:
        await ctx.send(embed=embed)
        return

    if channel:
        await channel.send(embed=embed)


class NoConnectionElement(Exception):
    """Raised when no context or channel object was found"""
