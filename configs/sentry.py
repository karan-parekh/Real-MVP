import sentry_sdk

from utils.env import env

DEBUG = False


def capture_exception(ex: Exception):

    sentry_sdk.init(env('SENTRY_DSN'), release=env('APP_VERSION'))

    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', DEBUG)

    return sentry_sdk.capture_exception(ex)


def capture_message(message: str):

    sentry_sdk.init(env('SENTRY_DSN'), release=env('APP_VERSION'))

    with sentry_sdk.push_scope() as scope:  
        scope.set_extra('debug', DEBUG)

    return sentry_sdk.capture_message(message)
