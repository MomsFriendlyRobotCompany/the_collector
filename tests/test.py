# this can be run with:
#
# nosetests -vs test.py  note: this uses default python version
# python2 `which nosetests` -vs test.py
# python3 `which nosetests` -vs test.py

from __future__ import print_function, division
from the_collector.bagit import BagWriter, BagReader
from the_collector.circular_buffer import CircularBuffer
import os
import time


def test_rw():
    filename = 'bob.bag'

    d = {'a': 1, 'b': 2}
    data = []
    bag = BagWriter()

    for _ in range(100):
        d['stamp'] = time.time()
        data.append(d)

    for msg in data:
        bag.push(msg)

    bag.write(filename)  # .bag is automagically appended if not present

    bag = BagReader()
    data_in = bag.read(filename)

    assert data == data_in

    # to see output: nosetests -vs test.py
    print("{} is {:.1f} kB".format(filename, os.path.getsize(filename)/1000))

    # clean up and delete file
    os.remove(filename)


def test_circularBuff():
    cb_len = 10
    cb = CircularBuffer(cb_len)
    assert len(cb._data) == cb_len

    # should push 0 - 99
    for i in range(100):
        cb.push(i)

    # buffer should only have 90-99 in it since it is only 10 in length
    data = cb.get_all()

    assert len(data) == 10

    for i, p in enumerate(range(90, 100)):
        assert data[i] == p
