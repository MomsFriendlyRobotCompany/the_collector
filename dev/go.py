#!/usr/bin/env python2

from __future__ import print_function, division
from the_collector.bagit import BagWriter, BagReader
from pygecko.transport.messages import serialize, deserialize, Pose, Vector, Quaternion
import msgpack

filename = 's.bag'
save = {
    'test': [],
    'bob': []
}
bag = BagWriter(filename, buffer_size=10, pack=serialize)

for i in range(20):
    d = Pose(Vector(1, 1, 1), Quaternion(1, 1, 1, 1))
    bag.push('test', d)
    bag.push('bob', i)

    save['test'].append(d)
    save['bob'].append(i)

bag.close()

bag = BagReader(unpack=deserialize)
load = bag.read(filename)

print("*"*40)
print('\nAre they the same?', save == load, '\n')
print("*"*40)

print('-'*40)
print(save)
print('-'*40)
print(load)
