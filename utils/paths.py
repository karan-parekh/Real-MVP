import os

from os.path import join


def get_app_path(path: str=''):

    cwd      = os.getcwd()
    app_path = cwd.rsplit(os.sep, 1)[0]

    return join(app_path, path)


def get_storage_path(file: str=''):

    storage = get_app_path('storage')

    return join(storage, file)


def get_data_path(file=''):

    data = get_storage_path('data')

    return join(data, file)


def get_tmp_path(file: str=''):

    tmp = get_app_path('tmp')

    return join(tmp, file)


def get_stamp_file():

    return get_tmp_path('.stamp')


if __name__ == '__main__':

    print(get_app_path())

    print(get_stamp_file())
