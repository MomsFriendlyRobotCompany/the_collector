##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################


import msgpack

class MsgPack:
    def __init__(self, pack=None, unpack=None):
        self.proto = "msgpack"
        self.pack_hook = pack
        self.unpack_hook = unpack
        # if pack:
        #     self.p = msgpack.Packer(default=pack, use_bin_type=True, strict_types=True)
        # else:
        #     self.p = msgpack.Packer(use_bin_type=True, strict_types=True)

        # if unpack:
        #     unpacker = msgpack.Unpacker(fd, ext_hook=self.unpack, raw=False)
        # else:
        #     unpacker = msgpack.Unpacker(fd, raw=False)

    def pack(self, data):
        return msgpack.packb(data, use_bin_type=True)
        # return msgpack.packb(data, use_bin_type=True, strict_types=True)

    def unpack(self, filename):
        # return msgpack.unpackb(data, use_list=False, raw=False)
        with open(filename, 'rb') as fd:
            # data = json.load(fd)
            data = msgpack.unpack(fd, use_list=False, raw=False)

        # The original arrays were turned into tuples
        for key, val in data.items():
            data[key] = list(data[key])

        return data
