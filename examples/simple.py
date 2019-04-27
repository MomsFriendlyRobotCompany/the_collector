#!/usr/bin/env python3
from __future__ import print_function
from the_collector.BagReader import BagReader2
from the_collector.BagWriter import BagWriter2
from the_collector.protocols import Json, MsgPack, Pickle



d = {'a': 1, 'b': 2}
bag = BagWriter2(Pickle)

for _ in range(100):
    bag.push('test', d)
    bag.push('bob', d)
    bag.push('tom', d)

fname = bag.write('bob', timestamp=False)  # .bag is automagically appended if not present

print(">> created:", fname)

bag = BagReader2()
data = bag.read(fname)

for key, val in data.items():
    print("[{}]=================".format(key))
    print("  {}".format(val))

#
# for key in data.keys():
#     for msg in data[key]:
#         ans = 'GOOD'
#         if d == msg:
#             print('.', end='')
#         else:
#             ans = 'ERROR'
#             print("data is different")
#             print("original:", d)
#             print("read in from file:", msg)
#     print('\n{} data is {}'.format(key, ans))
