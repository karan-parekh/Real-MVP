import json

from datetime import datetime, timedelta
from loguru import logger
from typing import List, Optional

from modules.discord import DiscordModule as Discord
from stores import Game
from stores.psn import PSN
from utils.helpers import read_file
from utils.paths import get_storage_path, get_tmp_path, get_data_path


class Gamer:

    INTERVAL = 24  # in hours

    def __init__(self):

        self.stores = [PSN]
        self.now    = datetime.now()

    def run(self):

        logger.info("Gamer initiated")

        if not self._is_time():
            logger.info("Interval has not passed. Returning")
            return

        games = self._get_games()

        self._backup_data()
        self._update_data(games)
        self._post_to_discord()
        self._update_stamp(self.now)

    def _post_to_discord(self):
        """
        Posts the data to discord channel
        """
        logger.info("Posting to Discord")

        games = self._find_new_games()

        if not games:
            logger.info("No new games found. Returning")
            return

    # Todo: Use Discord module to post ot Discord

    def _find_new_games(self) -> Optional[List[dict]]:
        """
        Checks for difference between old and new data
        to find new games
        """
        logger.info("Check for difference in old and new data")

        old_games = set(self._get_games_from_data('old.json'))
        new_games = set(self._get_games_from_data('new.json'))

        diff = new_games.difference(old_games)

        if diff:
            return list(diff)

    @staticmethod
    def _get_games_from_data(filename: str) -> List[dict]:
        """
        Gets the list of games from the JSON data
        """

        with open(get_data_path(filename), 'r') as file:

            data = json.load(file)

        return data['games']

    def _update_stamp(self, stamp: datetime=None):
        """
        Updates the timestamp
        """
        logger.info("Updating time stamp to: {}".format(stamp))

    def _update_data(self, games: List[Game]):
        """
        Updates the new.json in storage
        """

        logger.info("Updating new data")

        data = {
            'meta': {
                'run'   : str(self.now),
                'stores': []
            },
            'games': []
        }

        for game in games:

            data['meta']['stores'].append(game.get_store_name())
            data['games'].append(game.get_data())

    def _backup_data(self):
        """
        Moves current data to old.json
        """

        logger.info("Backing up current data")

        with open(get_storage_path('new.json'), 'r') as file:

            data = json.load(file)

        with open(get_storage_path('old.json'), 'w') as file:

            json.dump(data, file)

    def _get_games(self) -> List[Game]:
        """
        Gets all free games from stores
        """
        logger.info("Getting games")

        games = []

        for store in self.stores:

            store = store()

            logger.info("Running for store: {}".format(store.get_name()))

            games.extend(store.get_free_games())

        return games

    def _is_time(self) -> bool:
        """
        Checks if its past interval
        """

        date_str = read_file(get_tmp_path('.stamp'))

        year, month, day = list(map(int, date_str.split('-')))

        last_run = datetime(year, month, day)

        diff = self.now - last_run

        logger.info("Time Interval: {}".format(diff))

        if diff > timedelta(hours=self.INTERVAL):
            return True

        return False


if __name__ == '__main__':

    Gamer().run()


