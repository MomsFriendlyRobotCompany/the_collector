#!/usr/bin/env python3
from __future__ import print_function
from the_collector.bagit import BagReader, BagWriter


d = {'a': 1, 'b': 2}
bag = BagWriter()

for _ in range(100):
    bag.push(d)

bag.write('bob.bag')  # .bag is automagically appended if not present

bag = BagReader()
data = bag.read('bob.bag')

for msg in data:
    ans = 'GOOD'
    if d == msg:
        print('.', end='')
    else:
        ans = 'ERROR'
        print("data is different")
        print("original:", d)
        print("read in from file:", msg)
print('\nResult:', ans)
