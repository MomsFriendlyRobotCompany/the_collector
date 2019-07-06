
from collections import namedtuple
import time


class Data(namedtuple('Data', 'data timestamp')):
    """
    Generic data container with a timestamp.
        data = tuple of data
        timestamp = from time.time(), where it is measured in seconds
    """
    __slots__ = ()

    def __new__(cls, d, ts=None):
        if ts:
            return cls.__bases__[0].__new__(cls, d, ts)
        else:
            return cls.__bases__[0].__new__(cls, d, time.time())
