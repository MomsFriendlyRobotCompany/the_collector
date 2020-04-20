# from enum import Enum
import pickle
try:
    import simplejson as json
except ImportError:
    import json

import io    # gzip to string
import gzip  # compression
# try:
#     import msgpack
# except ImportError:
#     class msgpack(object):
#         def __init__(self):
#             raise Exception("WARNING: msgpack not found")
#         def packb(self, data): return None
#         def unpackb(self, data): return None


# Protocols = Enum('Protocols', 'json pickle msgpack')

# class Base(object):
#     proto = None


class Pickle:
    def __init__(self):
        self.proto = "pickle"

    def pack(self, data):
        return pickle.dumps(data)

    def unpack(self, filename):
        # return pickle.loads(data)
        with open(filename, 'rb') as fd:
            data = pickle.load(fd)
        return data


class Json:
    def __init__(self, compress=False, use_tuples=True):
        self.use_tuples = use_tuples
        self.compress(compress)

    def compress(self, compress):
        if compress:
            self.proto = "json-gz"
        else:
            self.proto = "json"

    def pack(self, data):
        if self.proto == "json-gz":
            # with gzip.open(filename, 'rb') as f:
            #     data = json.load(f)
            out = io.BytesIO()
            with gzip.GzipFile(fileobj=out, mode='wb') as fo:
                fo.write(json.dumps(data).encode("utf-8"))
            return out.getvalue()
        else:
            return json.dumps(data).encode("utf-8")

    def unpack(self, filename):
        if self.proto == "json-gz":
            with gzip.open(filename, 'rb') as fd:
                data = json.load(fd)
        else:
            with open(filename, 'rb') as fd:
                data = json.load(fd)

        if self.use_tuples:
            for key, val in data.items():
                if isinstance(val[0], list):
                    for i in range(len(val)):
                        data[key][i] = tuple(data[key][i])
        return data

    def packs(self, s):
        raise NotImplementedError("Json.unpacks()")

    def unpacks(self, s):
        raise NotImplementedError("Json.unpacks()")


# try:
#     import msgpack

#     class MsgPack:
#         def __init__(self, pack=None, unpack=None):
#             self.proto = "msgpack"
#             self.pack_hook = pack
#             self.unpack_hook = unpack
#             # if pack:
#             #     self.p = msgpack.Packer(default=pack, use_bin_type=True, strict_types=True)
#             # else:
#             #     self.p = msgpack.Packer(use_bin_type=True, strict_types=True)

#             # if unpack:
#             #     unpacker = msgpack.Unpacker(fd, ext_hook=self.unpack, raw=False)
#             # else:
#             #     unpacker = msgpack.Unpacker(fd, raw=False)

#         def pack(self, data):
#             return msgpack.packb(data, use_bin_type=True)
#             # return msgpack.packb(data, use_bin_type=True, strict_types=True)

#         def unpack(self, filename):
#             # return msgpack.unpackb(data, use_list=False, raw=False)
#             with open(filename, 'rb') as fd:
#                 # data = json.load(fd)
#                 data = msgpack.unpack(fd, use_list=False, raw=False)

#             # The original arrays were turned into tuples
#             for key, val in data.items():
#                 data[key] = list(data[key])

#             return data

# except ImportError:
#     class MsgPack(object):
#         def __init__(self):
#             raise Exception("WARNING: msgpack not found, install with `pip install msgpack`")

#         def pack(self, data):
#             return None

#         def unpack(self, filename):
#             return None
