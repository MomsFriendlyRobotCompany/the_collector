# this can be run with:
#
# nosetests -vs test.py  note: this uses default python version
# python2 `which nosetests` -vs test.py
# python3 `which nosetests` -vs test.py

from __future__ import print_function, division
from the_collector import BagWriter, BagReader
from the_collector import CircularBuffer
from collections import namedtuple
import msgpack
import os
import time
from io import BytesIO

from the_collector.messages import serialize, deserialize
from the_collector.messages import Pose, Vector, Quaternion, IMU, Image


def rw(buffer_size, ts_stamp=False):
    filename = 'bob.bag'
    # filename = BytesIO()
    save = {'a': []}
    bag = BagWriter(filename, buffer_size=buffer_size)

    for i in range(20):
        d = {'one': 1, 'two': 2, 'stamp': time.time()}

        if ts_stamp:
            bag.push_stamp('a', d)
        else:
            bag.push('a', d)
        save['a'].append(d)

    bag.close()
    # filename.seek(0)

    bag = BagReader()
    data = bag.read(filename)

    # print(tuple(save['a'][0].keys()), tuple(data['a'][0].keys()))

    print(save)
    print('-'*40)
    print(data)

    assert type(data) == type(save)
    assert len(data['a']) == len(save['a'])
    assert tuple(save.keys()) == tuple(data.keys())

    if ts_stamp:
        # time stamp is added to the data: (data, time_stamp)
        for a, b in zip(save, data):
            assert a == b[0]
    else:
        assert tuple(save['a'][0].keys()) == tuple(data['a'][0].keys())  # push_stamp breaks this
        assert save == data

    # to see output: nosetests -vs test.py
    print("{} is {:.1f} kB".format(filename, os.path.getsize(filename)/1000))

    # clean up and delete file
    os.remove(filename)


def test_rw_large_buffer():
    rw(1000)


def test_rw_small_buffer():
    rw(10)


def test_rw_large_buffer_time_stamp():
    rw(1000, True)


def test_rw_small_buffer_time_stamp():
    rw(10, True)


def test_messages():
    filename = 's.bag'
    save = {
        'test': [],
        'bob': []
    }
    bag = BagWriter(filename, buffer_size=10, pack=serialize)

    for i in range(20):
        d = Pose(Vector(1, 1, 1), Quaternion(1, 1, 1, 1))
        bag.push('test', d)

        k = IMU(Vector(.1,.1,.1), Vector(.2,.2,.2), Vector(.3,.3,.3))
        bag.push('bob', k)

        save['test'].append(d)
        save['bob'].append(k)

    bag.close()

    bag = BagReader(unpack=deserialize)
    load = bag.read(filename)
    assert save == load
    # print("*"*40)
    # print('\nAre they the same?', save == load, '\n')
    # print("*"*40)
    #
    # print('-'*40)
    # print(save)
    # print('-'*40)
    # print(load)
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
