#!/usr/bin/env python3
from __future__ import print_function
from the_collector import BagIt
from the_collector import Json, MsgPack, Pickle
import json


d = {'a': 1, 'b': 2}

bag = BagIt(Json)
# bag = BagIt(Pickle)
# bag = BagIt(MsgPack)

for i in range(10):
    bag.push('test', d)
    bag.push('bob', d)
    bag.push('tom', ('a', i,))

fname = bag.write('bob', timestamp=False)

print(">> created:", fname)

data = bag.read(fname)
print(data)

# with open(fname, 'rb') as fd:
#     data = json.load(fd)
#
# for key, val in data.items():
#     print("{}[{}]".format(key, len(val)))
#     for v in val:
#         print("{}".format(v), end=' ')
#     print(' ')
