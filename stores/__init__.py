import json
import requests

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List


class Game:
    """
    Data-value class for game objects
    """

    def __init__(self, title: str, link: str, store):

        self.title = title
        self.link  = link
        self.store = store

    def get_data(self) -> dict:
        """
        Combines all data and returns a JSON string
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


class Store(ABC):

    def __init__(self, name: str, url: str):

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
