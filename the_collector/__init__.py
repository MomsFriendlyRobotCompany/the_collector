##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
from the_collector.circular_buffer import CircularBuffer
from the_collector.bagit import BagIt
from the_collector.protocols import Json, Pickle
from the_collector.data import Data
# from the_collector.utils import bag_info
# from colorama import Fore


try:
    import numpy as np
    from the_collector.extra_numpy import array_pack, array_unpack
except ImportError:
    pass

# try:
#     import msgpack
#     from the_collector.extra_msgpack import MsgPack
# except ImportError:
#     pass

try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

__license__ = "MIT"
__author__ = "Kevin J. Walchko"
__version__ = version("the_collector")
