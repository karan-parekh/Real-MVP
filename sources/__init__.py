import json
import requests

from enum import Enum
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from loguru import logger
from typing import List


class Platform(Enum):

    PC       = 'pc'
    PS4      = 'ps4'
    PS5      = 'ps5'
    STADIA   = 'stadia'
    XBOX     = 'xb'
    XBOX_360 = 'x360'
    XBOX_ONE = 'xb1'
    XBOXS_S  = 'xbs'
    XBOXS_X  = 'xbx'

    @classmethod
    def all(cls) -> list:

        return list(set(map(lambda c: c.value, cls)))


class Service(Enum):

    SELF      = 'self',   []
    STEAM     = 'steam',  [Platform.PC.value]
    EPIC      = 'epic',   [Platform.PC.value]
    HUMBLE    = 'humble', [Platform.PC.value]
    PRIME     = 'prime',  [Platform.PC.value]
    INDIEGALA = 'indie',  [Platform.PC.value]
    ITCH      = 'itch',   [Platform.PC.value]
    PS_NOW    = 'psn',    [Platform.PC.value]
    PS_PLUS   = 'ps+',    [Platform.PS4.value, Platform.PS5.value]
    STADIA    = 'stadia', [Platform.STADIA.value]
    MICROSOFT = 'ms',     [Platform.XBOX.value, Platform.XBOX_360.value, Platform.XBOX_ONE.value,
                           Platform.XBOXS_S.value, Platform.XBOXS_X.value]

    def __new__(cls, value, platforms):

        member           = object.__new__(cls)
        member._value_   = value
        member.platforms = platforms

        return member

    @classmethod
    def all(cls) -> list:
        return list(set(map(lambda c: str(c.value), cls)))


@logger.catch()
class Game:
    """
    Data-value class for game objects
    """

    def __init__(self, title: str, link: str, store):

        self.title = self._remove_ascii(title)
        self.link  = link
        self.store = store

    def get_data(self) -> dict:
        """
        Combines all data and returns a JSON compatible dict
        """

        data = {
            'title': self.get_title(),
            'link' : self.get_link(),
            'store': self.get_store_name()
        }

        return data

    def get_json_data(self) -> str:

        return json.dumps(self.get_data())

    def get_title(self) -> str:

        return self.title

    def get_link(self) -> str:

        return self.link

    def get_store_name(self):

        return self.store.get_name()

    @staticmethod
    def _remove_ascii(text: str):

        return text.encode('ascii', 'ignore').decode()


class Store(ABC):

    def __init__(self, name: Service, url: str):

        self.name = name
        self.url  = url

    @abstractmethod
    def get_free_games(self) -> List[Game]:
        """
        Gets free games from the store
        """

    @staticmethod
    def get_soup(url: str):
        """
        Gets a BeautifulSoup object for the store URL
        """
        response = requests.get(url)

        return BeautifulSoup(response.content, "html.parser")

    def get_name(self):

        return self.name
