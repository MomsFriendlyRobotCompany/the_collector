#!/usr/bin/env python
from the_collector import CircularBuffer
from collections import namedtuple
# import msgpack
import os
# import time
# from io import BytesIO
from the_collector import BagIt
from the_collector import Json, MsgPack, Pickle
import json
import msgpack
import pickle


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

    os.remove(fname)

    print(copy)
    print(data)

    assert data == copy


def bagfile_rw(kind):
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

    # data = bag.read(fname)
    if bag.packer.proto == 'json':
        print("<<< json >>>")
        with open(fname, 'rb') as fd:
            data = json.load(fd)

        for key, val in data.items():
            if isinstance(val[0], list):
                for i in range(len(val)):
                    data[key][i] = tuple(data[key][i])
    elif bag.packer.proto == 'pickle':
        print("<<< pickle >>>")
        with open(fname, 'rb') as fd:
            data = pickle.load(fd)
    elif bag.packer.proto == 'msgpack':
        print("<<< msgpack >>>")
        with open(fname, 'rb') as fd:
            data = msgpack.unpack(fd, use_list=False, raw=False)

        # The original arrays were turned into tuples
        for key, val in data.items():
            data[key] = list(data[key])
    else:
        assert False

    os.remove(fname)

    print("Copy\n", copy)
    print("Data\n", data)

    assert data == copy


def test_json():
    bagfile(Json)


def test_json_lib():
    bagfile_rw(Json)


def test_msgpack():
    bagfile(MsgPack)


def test_msgpack_lib():
    bagfile_rw(MsgPack)


def test_pickle():
    bagfile(Pickle)


def test_pickle_lib():
    bagfile_rw(Pickle)

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
