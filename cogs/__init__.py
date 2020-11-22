
from typing import List

from database import GamesRepository
from sources.metacritic import MetaCritic


class MVP:
    """
    Interface for the bot and GameRepository
    """

    def __init__(self):

        self.sources = [MetaCritic]
        self.repo    = GamesRepository()

    def run(self):
        """
        Runs all sources and updates new games
        """

        for source in self.sources:
            source().run()

        self._update_diff()

    def get_latest_games(self) -> List[dict]:

        return [game for game in self.repo.get_diff() if game['available']]

    def find_by_service(self, code: str) -> List[dict]:

        return [game for game in self.repo.find_by_service(self.repo.NEW, code) if game['available']]

    def find_by_platform(self, code: str) -> List[dict]:

        return [game for game in self.repo.find_by_platform(self.repo.NEW, code) if game['available']]

    def _update_diff(self):

        old_games = self.repo.get_old_games()
        new_games = self.repo.get_new_games()

        diff = [game for game in new_games if game not in old_games]

        self.repo.replace_diff(diff)
