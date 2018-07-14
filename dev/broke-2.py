#!/usr/bin/env python3

import msgpack
from collections import namedtuple
from io import BytesIO
import time


Test = namedtuple("Test", "x y")
Vector = namedtuple("Vector", "x y z")


def mk(x):
    print('mk', x)
    if type(x) in [Test, Vector]:
        d = [msgpack.packb(x.__class__.__name__)]
        for i in x:
            d.append(msgpack.packb(i, default=mk, strict_types=True))
        return b''.join(d)


def process(x):
    print('process', x)
    if type(x) is Vector:
        return (x.__class__.__name__,) + x
    elif type(x) is Test:
        print(x)
        return (x.__class__.__name__,) + (process(x[0]),) + (process(x[1]),)
    else:
        return (x,)


def serialize(x):
    print('serialize', x)
    if type(x) in [Test, Vector]:
        msg = msgpack.ExtType(1, msgpack.packb(process(x)))
        print(msg)
        return msg
    # if type(x) in [Vector]:
    #     return msgpack.ExtType(2, msgpack.packb((x.__class__.__name__,) + x, default=serialize))
    return x

# def sserialize(x):
#     print('simple serialize', x)
#     if type(x) in [Test, Vector]:
#         return msgpack.ExtType(2, msgpack.packb((x.__class__.__name__,) + x, default=sserialize, strict_types=True))
#     return x



def deserialize(code, data):
    print('deserialize', code, data)
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)
        print('d', d)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        # return Test(Vector(*d[1]), Vector(*d[2]))
        # globals()[d[0]](*d[1:])
        if d[0] in ['Test']:
            vals = []
            for i in d[1:]:
                print(i)
                if len(i) > 1:
                    v = globals()[i[0]](*i[1:])
                else:
                    v = i[0]
                print(v)
                vals.append(v)
            return globals()[d[0]](*vals)
        else:
            return globals()[d[0]](*d[1:])
    # if code == 2:
    #     # you call this again to unpack and ext_hook for nested
    #     d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)
    #
    #     # print d[0]   # holds class name
    #     # print d[1:]  # holds data inorder
    #     # finds constructor in namespace and calls it
    #     return globals()[d[0]](*d[1:])

    return msgpack.ExtType(code, data)


data = [Test(Vector(1,2,3), Vector(4,5,6)), Vector(1,2,3), Test(Vector(1,2,3), 3), Test("hi how are you", 3)]
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
