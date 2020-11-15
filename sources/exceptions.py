
class GamesDBException(Exception):
    """Raised for any exceptions in GlowDB class"""


class TableException(GamesDBException):
    """Raised for any exceptions in querying table"""


class NoDatabaseFound(GamesDBException):
    """Raised when required DB is not found or does not exist"""


class DataCorruptedError(GamesDBException):
    """Raised when the data in glow DB is corrupted"""


class CacheManagerException(Exception):
    """Raised for any exception in cache manager operations"""
