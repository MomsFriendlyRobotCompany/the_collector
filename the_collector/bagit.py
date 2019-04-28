from the_collector.protocols import Pickle, MsgPack, Json
import datetime


class BagIt(object):
    """
    """
    protocols = {
        'json': Json,
        'pickle': Pickle,
        'msgpack': MsgPack
    }

    def __init__(self, packer):
        """
        filename: either a string containing the desired file name (note that
          .bag is appended) OR a file-like object from io.Bytes or something
        buffer_size: number of Bytes, default 10MB
        """
        self.buffer = {}
        self.packer = packer()
        print(">> ", self.packer.proto)

    def __del__(self):
        # self.write()  # this kills me on BytesIO, it closes the buffer
        pass

    def fill(self, data):
        """
        Clears buffer and fills it data (dictionary)
        """
        self.buffer = {}
        print(".fill() ----------------------------")
        for key, val in data.items():
            print("- {}: {}".format(key, len(val)))
            for v in val:
                self.push(key, v)

    def push(self, key, msg):
        """
        Push another message and a key into the buffer. Once the buffer limit
        is reached it is written to a file.
        """
        if key not in self.buffer.keys():
            self.buffer[key] = []

        self.buffer[key].append(msg)

    def write(self, filename='data', timestamp=True):
        if len(self.buffer) == 0:
            return None

        if timestamp:
            dt = str(datetime.datetime.now()).replace(' ', '-')
            filename = "{}.{}.{}.bag".format(filename, dt, self.packer.proto)
        else:
            filename = "{}.{}.bag".format(filename, self.packer.proto)

        print("***", filename)
        print(self.packer)
        print(self.buffer)

        with open(filename, 'wb') as fd:
            d = self.packer.pack(self.buffer)
            print("-"*40)
            print(d)
            print("-"*40)
            fd.write(d)

        self.buffer = {}

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
        # packer = None
        for p in t:
            if p in ['msgpack', 'pickle', 'json']:
                # packer = self.protocols[p]()
                print(">> Reading[{}]: {}".format(p, filename))
                if p == self.packer.proto:
                    return self.packer.unpack(filename)
                else:
                    return self.readOther(filename, p)

        # if packer is None:
        raise Exception("Couldn't determine protocol of file:", filename)

        # return self.packer.unpack(filename)

    def readOther(self, filename, proto):
        """
        Given a filename, it opens it and read all data into memory and return
        Inputs:
          filename - name of file
          proto - protocol name: msgpack, json, pickle
        Return:
          dict() with keys for each recorded data stream and a list/tuple of
          data points
        """
        # t = filename.split('.')
        # packer = None
        # for p in t:
        #     if p in ['msgpack', 'pickle', 'json']:
        #         packer = self.protocols[p]()
        #         print(">> Reading[{}]: {}".format(p, filename))
        #         break
        packer = self.protocols[proto]()

        return packer.unpack(filename)
