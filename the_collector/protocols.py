from enum import Enum
import pickle

try:
    import simplejson as json
except ImportError:
    import json

try:
    import msgpack
except ImportError:
    class msgpack(object):
        def __init__(self):
            raise Exception("WARNING: msgpack not found")
        def pack(self, data): return None
        def unpack(self): return None




Protocols = Enum('Protocols', 'json pickle msgpack')

class Base(object):
    proto = None

class Pickle(Base):
    def __init__(self):
        self.proto = "pickle"

    def pack(self, data):
        return pickle.dumps(data)

    def unpack(self, data):
        return pickle.loads(data)


class Json(object):
    def __init__(self, compress=False):
        if compress:
            self.proto = "json-gz"
        else:
            self.proto = "json"

    def pack(self, data):
        return json.dumps(data)

    def unpack(self):
        return json.loads(data)


class MsgPack(object):
    def __init__(self):
        self.proto = "msgpack"
        pack = None
        self.p = msgpack.Packer(default=pack, use_bin_type=True, strict_types=True)

    def pack(self, data):
        return None

    def unpack(self):
        return None
