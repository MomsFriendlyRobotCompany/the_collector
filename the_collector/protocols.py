##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import pickle
import simplejson as json
import io    # gzip to string
import gzip  # compression
import attr


@attr.s(slots=True)
class Pickle:
    # def __init__(self):
    #     self.proto = "pickle"
    proto = attr.ib(init=False, default="pickle")

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
