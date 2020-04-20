from the_collector.circular_buffer import CircularBuffer
from the_collector.bagit import BagIt
from the_collector.protocols import Json, Pickle
from the_collector.data import Data

# try:
#     import msgpack
#     from the_collector.protocols import MsgPack
# except ImportError:
#     pass

try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

__license__ = "MIT"
__author__ = "Kevin J. Walchko"
__version__ = version("the_collector")
