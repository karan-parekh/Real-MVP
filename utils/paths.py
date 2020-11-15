import os

from os.path import join
from inspect import getsourcefile


CURRENT_PATH = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))


def app_path(path=''):
    app_path_ = os.path.realpath("{}/{}".format(CURRENT_PATH, "../"))

    if not path:
        return app_path_

    return os.path.realpath("{}/{}".format(app_path_, path))


def get_storage_path(file: str=''):

    storage = app_path('storage')

    return join(storage, file)


def get_games_path(file=''):

    games = get_storage_path('games')

    return join(games, file)


def get_template_path():

    return get_games_path('template.json')


def get_data_path(file=''):

    data = get_storage_path('data')

    return join(data, file)


def get_tmp_path(file: str=''):

    tmp = app_path('tmp')

    return join(tmp, file)


def get_stamp_file():

    return get_tmp_path('.stamp')


if __name__ == '__main__':

    print(app_path())

    print(get_stamp_file())
