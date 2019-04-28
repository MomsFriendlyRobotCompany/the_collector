#!/usr/bin/env python
from the_collector import CircularBuffer
from collections import namedtuple
import msgpack
import os
import time
from io import BytesIO
from the_collector import BagIt
from the_collector import Json, MsgPack, Pickle
import json


def bagfile(kind):
    bag = BagIt(kind)

    copy = {
        'test': [],
        'bob': [],
        'tom': []
    }

    d = {'a': 1.2345678}
    tt = namedtuple('tt','a b c')  # this has issues

    for i in range(10):
        # t = tt('hello', i, 10*i)
        t = (1,-1,0.00001,100000,)
        bag.push('test', d)
        bag.push('bob', t)
        bag.push('tom', ('a', i,))

        copy['test'].append(d)
        copy['bob'].append(t)
        copy['tom'].append(('a', i,))

    fname = bag.write('bob', timestamp=False)

    # print(">> created:", fname)

    data = bag.read(fname)

    print(copy)
    print(data)

    assert data == copy


def test_json():
    bagfile(Json)


def test_msgpack():
    bagfile(MsgPack)


def test_pickle():
    bagfile(Pickle)

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
