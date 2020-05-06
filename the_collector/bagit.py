##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
from the_collector.protocols import Pickle, Json
import datetime
from collections import defaultdict


class BagIt(object):
    """
    """
    __slots__ = ('buffer', 'packer')

    def __init__(self, packer):
        """
        filename: either a string containing the desired file name (note that
          .bag is appended) OR a file-like object from io.Bytes or something
        buffer_size: number of Bytes, default 10MB
        """
        # self.buffer = {}
        self.buffer = defaultdict(list)
        self.packer = packer()
        # print(">> ", self.packer.proto)

    def __del__(self):
        # self.write()  # this kills me on BytesIO, it closes the buffer
        pass

    def info(self):
        print('Bag keys:')
        print('-'*50)
        for k in self.buffer.keys():
            print(f'  {k:>10}: {len(self.buffer[k]):<7}')

    def fill(self, data):
        """
        Clears buffer and fills it data (dictionary)
        """
        if not isinstance(data, dict):
            raise Exception(f"data is not a dict, it is: {type(data)}")

        self.buffer.clear()
        print(".fill() ----------------------------")
        for key, val in data.items():
            print("- {key}: {len(val)}")
            for v in val:
                self.push(key, v)

    def push(self, key, msg):
        """
        Push another message and a key into the buffer. Once the buffer limit
        is reached it is written to a file.
        """
        # if key not in self.buffer.keys():
        #     self.buffer[key] = []

        self.buffer[key].append(msg)

    def write(self, filename='data', timestamp=True):
        if len(self.buffer) == 0:
            return None

        if timestamp:
            dt = str(datetime.datetime.now()).replace(' ', '-')
            filename = f"{filename}.{dt}.{self.packer.proto}.bag"
        else:
            filename = f"{filename}.{self.packer.proto}.bag"

        with open(filename, 'wb') as fd:
            d = self.packer.pack(self.buffer)
            fd.write(d)

        # self.buffer = {}
        self.buffer.clear()

        return filename

    def read(self, filename):
        """
        Given a filename, it opens it and read all data into memory and return
        Inputs:
          filename - name of file
        Return:
          dict() with keys for each recorded data stream and a list/tuple of
          data points
        """
        t = filename.split('.')
        p = t[-2]

        if p in ['msgpack', 'pickle', 'json', "json-gz"]:
            print(f">> Reading[{p}]: {filename}")
            if p != self.packer.proto:
                raise Exception(f"File is {p} protocol, this Bagit is {self.packer.proto}")

            return self.packer.unpack(filename)
        else:
            raise Exception("Couldn't determine protocol of file:", filename)

        # return self.packer.unpack(filename)
