import os

from loguru import logger
from tinydb import TinyDB, where
from tinydb.table import Table
from typing import List

from utils.paths import get_storage_path, get_games_path


class GamesRepository:
    """A TinyDB JSON database"""

    DB  = 'games'
    NEW = 'new'
    OLD = 'old'

    def __init__(self):

        self.db_path = None
        self._setup()

        self.db = TinyDB(self.db_path)

        self._create_tables()

    def get_new_games(self) -> List[dict]:

        return self._get_games(self.NEW)

    def get_old_games(self) -> List[dict]:

        return self._get_games(self.OLD)

    def replace_new_games(self, games: List[dict]):

        self._replace_games(self.NEW, games)

    def replace_old_games(self, games: List[dict]):

        self._replace_games(self.OLD, games)

    def find_by_platform(self, table_name: str, name: str) -> List[dict]:

        table = self.get_table(table_name)

        return table.search(where('platform') == name)

    def _get_games(self, table_name: str) -> List[dict]:

        table = self.get_table(table_name)

        return [game for game in table]

    def _replace_games(self, table_name: str, games: List[dict]):

        table = self.get_table(table_name)

        self._delete_table(table_name)
        self._create(table_name)

        for game in games:
            table.insert(game)

    def _setup(self):

        db_dir       = get_games_path()
        self.db_path = os.path.join(db_dir, "{}.json".format(self.DB))

        self._mkdir(db_dir)

    def _create_tables(self):

        self._create(self.OLD)
        self._create(self.NEW)

    def _delete_table(self, table_name: str):
        """Purges table in DB"""

        if table_name in self.db.tables():
            self.db.table(table_name).truncate()

    def get_table(self, table_name: str) -> TinyDB.table:

        if table_name not in self.db.tables():

            logger.error("No table name: {}".format(table_name))
            raise TableException("No table name: {}".format(table_name))

        return self.db.table(table_name)

    def _create(self, table_name: str) -> int:
        """Creates a table in DB"""

        if table_name not in self.db.tables():

            return self._touch_table(self.db.table(table_name))

    @staticmethod
    def _touch_table(table) -> int:
        """Inserts a dummy data in the table to make it readable"""

        return table.remove(doc_ids=[table.insert({})])

    @staticmethod
    def _mkdir(dir_path: str):
        """Creates a directory if one does not exist"""
        try:
            os.mkdir(dir_path)

        except FileExistsError:
            pass


class GamesRepoException(Exception):
    """Raised for any exceptions in GlowDB class"""


class TableException(GamesRepoException):
    """Raised for any exceptions in querying table"""
