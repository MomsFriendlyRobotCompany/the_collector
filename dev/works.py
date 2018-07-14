#!/usr/bin/env python3

import msgpack
from collections import namedtuple


Test = namedtuple("Test", "x")
Vector = namedtuple("Vector", "x y z")


def serialize(x):
    print('serialize', x)
    if type(x) in [Test, Vector]:
        return msgpack.ExtType(1, msgpack.packb((x.__class__.__name__,) + tuple(x[:]), default=serialize))
    return x


def deserialize(code, data):
    print('deserialize', code, data)
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return globals()[d[0]](*d[1:])
        
    return msgpack.ExtType(code, data)


data = [Test(1), Test(2),]

packed = msgpack.packb(data, default=serialize, use_bin_type=True, strict_types=True)
unpacked = msgpack.unpackb(packed, ext_hook=deserialize, raw=False)

print("*"*40)
print("\nAre they the same?", data == unpacked, '\n')
print("*"*40)

print(data)
print('-'*40)
print(unpacked)
