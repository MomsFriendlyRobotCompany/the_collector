##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
from __future__ import print_function, division
import time
import os
import msgpack


class BagReadError(Exception):
    pass


class BagReader(object):
    """
    """
    def __init__(self, unpack=None):
        self.ext_unpack = unpack

    def read(self, filename):
        """
        Given a filename, it opens it and read all data into memory and return
        Inputs:
          filename - name of file
        Return:
          dict() with keys for each recorded data stream and a list/tuple of
          data points
        """
        data = {}
        # check to see if this is a file-like object
        # if (hasattr(filename, 'read') and hasattr(filename, 'write')):
        #     fd = filename
        # else:
        fd = open(filename, 'rb')

        if self.ext_unpack:
            # print('unpacker')
            unpacker = msgpack.Unpacker(fd, ext_hook=self.ext_unpack, raw=False)
        else:
            unpacker = msgpack.Unpacker(fd, raw=False)

        for o in unpacker:
            key = o[0]
            value = o[1]
            if key not in data:
                data[key] = []
            data[key].append(value)

        return data
