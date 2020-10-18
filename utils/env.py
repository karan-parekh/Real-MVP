import re
import os
import dotenv

from utils.helpers import read_newline_sep_file


class Env:

    @staticmethod
    def _get_env_path():

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.pringle'))

        if not (os.path.exists(path) and os.path.getsize(path) > 0):
            raise Exception('Pringle file at path "%s" doesn\'t exists!' % path)

        return path

    def load(self):

        dotenv.load_dotenv(self._get_env_path(), override=True)

        return self

    @staticmethod
    def _get_all_names():

        lines = read_newline_sep_file(".pringle")
        names = []

        for line in lines:
            name = re.search("^\w+", line)

            if name:
                names.append(name.group(0))

        return names

    def validate(self):

        names = self._get_all_names()

        for name in names:

            value = self.get(name)

            if not value or value == "null":
                raise NameError('{} value is not set!'.format(name))

    @staticmethod
    def get(name, default=''):

        env_ = os.getenv(name, None)

        if not env_:
            return default

        return env_

    def is_staging(self):

        return True if self.get('APP_ENV') == 'staging' else False


def env(name, default=''):

    if not Env().get('APP_ENV'):
        Env().load().validate()

    return Env().get(name, default)


def is_staging():

    return Env().is_staging()
