#!/usr/bin/env python3
from collections import namedtuple
import msgpack
import time
from array import array

Test = namedtuple("Test", "x")

def serialize(x):
    print('serialize', x)
    if x.__class__.__name__ in ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar', 'IMU']:
        return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=serialize, strict_types=True))
        # return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=serialize))
    return x


# def ext_unpack(code, data):
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

save = []
packer = msgpack.Packer(default=serialize, use_bin_type=True)
fd = open('test.bag', 'wb')

tmp = []
for i in range(20):
    d = tuple(range(5))  # this has to be a tuple, because use_list=False below
    d += (time.time(),)
    tmp.append(d)
    save.append(d)

    # tmp.append(array('d', [1.2, 3.4]))

    d = Test(i)
    tmp.append(d)
    save.append(d)
    if len(tmp) >= 10:
        print('>> flushing buffer')
        for t in tmp:
            fd.write(packer.pack(t))
        tmp = []
fd.close()


fd = open('test.bag', 'rb')
unpacker = msgpack.Unpacker(fd, raw=False)

load = []
for o in unpacker:
    # print(o)
    load.append(o)

print("Is it the same?", load == save)

print('-'*40)
print(save)
print('-'*40)
print(load)
