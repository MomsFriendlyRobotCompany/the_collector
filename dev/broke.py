#!/usr/bin/env python3

import msgpack
from collections import namedtuple
from io import BytesIO


Test = namedtuple("Test", "x y")
Vector = namedtuple("Vector", "x y z")


def serialize(x):
    print('serialize', x)
    if type(x) in [Test]:
        return msgpack.ExtType(1, msgpack.packb((x.__class__.__name__,) + tuple(x[:]), default=serialize))
    if type(x) in [Vector]:
        return msgpack.ExtType(2, msgpack.packb((x.__class__.__name__,) + tuple(x[:]), default=serialize))
    return x


def deserialize(code, data):
    print('deserialize', code, data)
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)
        print('d', d)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return Test(Vector(*d[1]), Vector(*d[2]))
    if code == 2:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return globals()[d[0]](*d[1:])

    return msgpack.ExtType(code, data)


data = [Test(Vector(1,2,3), Vector(4,5,6)), Vector(1,2,3)]
buf = BytesIO()

packer = msgpack.Packer(default=serialize, use_bin_type=True, strict_types=True)
unpacker = msgpack.Unpacker(buf, ext_hook=deserialize, raw=False)

for d in data:
    buf.write(packer.pack(d))

buf.seek(0)
unpacked = []
for d in unpacker:
    unpacked.append(d)

print("*"*40)
print("\nAre they the same?", data == unpacked, '\n')
print("*"*40)

print(data)
print('-'*40)
print(unpacked)
