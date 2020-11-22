import random
from typing import List

import discord
from loguru import logger


def sterilize(text):

    return " ".join(text.split())


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


async def post_to_discord(games: List[dict], title: str, **kwargs):
    """
    Posts to discord

    :param games: games to be posted
    :param title: title for the post
    :param kwargs: kwargs must specify at least one of the following connectors
                   [ctx, channel, guild]
    """

    connectors = ['ctx', 'channel', 'guild']

    for key in connectors:

        connector = kwargs.get(key)

        if connector:
            break
    else:
        raise NoConnectorObject("Expected at least one connector object out of {}".format(connectors))

    embed = discord.Embed(title=title)

    for game in games:

        embed.add_field(
            name=game['title'],
            value="is free on [{}]({})".format(game['service'], game['link']),
            inline=False
        )

    if kwargs.get('guild'):

        for channel in connector.channels:

            if channel.name == 'free-games':
                await channel.send(embed=embed)

                return

    await connector.send(embed=embed)


def get_standard_headers():

    return {
        "Accept"                    : "*/*",
        "Accept-Encoding"           : "gzip, deflate, br",
        "Accept-Language"           : "en-US,en;q=0.9",
        "Cache-Control"             : "no-cache",
        "Pragma"                    : "no-cache",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent"                : random.choice(get_useragents())
    }


def get_useragents() -> list:
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/20090327 Galeon/2.0.7",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6a) Gecko/20031002 Firebird/0.7",
        "Mozilla/5.0 (iPhone; U; Linux i686; pt-br) AppleWebKit/532+ (KHTML, like Gecko) Version/3.0 Mobile/1A538b Safari/419.3 Midori/0.2.0",
        "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0"
    ]


class NoConnectorObject(Exception):
    """Raised when no context or channel object was found"""
