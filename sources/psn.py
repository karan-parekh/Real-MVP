
from bs4 import BeautifulSoup
from typing import List

from . import Store, Game, Service


class PSN(Store):

    NAME         = Service.PS_NOW.value
    BASE_URL     = 'https://store.playstation.com'
    PS_PLUS_PATH = '/en-in/home/games/psplus'

    def __init__(self):

        super(PSN, self).__init__(self.NAME, self.BASE_URL)

    def get_free_games(self) -> List[Game]:

        container = self._get_container()
        game_objs = self._get_game_objects(container)
        meta      = self._get_meta(game_objs)

        games = []

        for title, link in meta.items():

            games.append(Game(title, link, self))

        return games

    def _get_meta(self, games: list) -> dict:
        """
        Gets the game names and links
        """

        names = {}

        for game in games:

            title = game.find('div', 'grid-cell__title').span.text
            path  = game.find('a', 'internal-app-link ember-view')['href']
            link  = self._build_url(path)

            names[title] = link

        return names

    @staticmethod
    def _get_game_objects(container: BeautifulSoup) -> list:
        """
        Gets free games from the container
        """

        free_games = []

        for game in container.find_all('div', 'grid-cell__body'):

            price = game.find('div', 'price-display__price--is-plus-upsell')

            if price and price.text.lower() == 'free':
                free_games.append(game)

        return free_games

    def _get_container(self) -> BeautifulSoup:
        """
        Gets the container containing free games
        """

        soup = self.get_soup(self._build_url(self.PS_PLUS_PATH))

        for container in soup.find_all('div', 'grid-cell-row'):

            name = container.find('span', 'grid-cell-row__container-name')

            if 'monthly games' in name.text.lower():
                return container

    def _build_url(self, path: str) -> str:
        """
        Appends path with the base URL
        """

        if not path.startswith("/"):

            return "{}/{}".format(self.BASE_URL, path)

        return "{}{}".format(self.BASE_URL, path)
