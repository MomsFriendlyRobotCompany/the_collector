##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# from the_collector.circular_buffer import CircularBuffer
# from the_collector.bagit import BagIt
# from the_collector.protocols import Pickle
# from the_collector.protocols import Json
# from the_collector.data import Data
# from the_collector.utils import bag_info
# from colorama import Fore
from .ver_2.collector import Collector
from .ver_2.collector import nuke


# try:
#     import numpy as np
#     from the_collector.extra_numpy import array_pack, array_unpack
# except ImportError:
#     pass

from importlib.metadata import version # type: ignore

__license__ = "MIT"
__author__ = "Kevin J. Walchko"
__version__ = version("the_collector")
