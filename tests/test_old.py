from __future__ import print_function, division
from the_collector import BagWriter, BagReader
from the_collector import CircularBuffer
import os
import time
import numpy as np


def rw(compress):
    run_len = 10
    filename = 'test.json'
    depth = 3
    row = 400
    col = 500
    image_size = (row, col, depth)

    bag = BagWriter()
    bag.open(['data', 'camera'])
    bag.stringify('camera')
    bag.use_compression = compress

    save_img = []  # use this for comparing later

    for i in range(run_len):
        bag.push('data', i)

        # create image of random(0, 255) of size image_size
        frame = np.random.randint(0, 255, image_size)
        save_img.append(frame.copy())

        bag.push('camera', frame)

    try:
        bag.write(filename)
    except Exception as e:
        print(e)
        assert False, 'Could not write bag file'

    # data is a hash
    # each key has an array: [data_point, time_stamp]
    reader = BagReader()
    reader.use_compression = compress
    data = reader.load(filename)

    for i, (d, ts) in enumerate(data['data']):
        assert i == d, 'Data is different'

    assert len(save_img) == len(data['camera']), 'Different data lengths'

    for i, (f, ts) in enumerate(data['camera']):
        # print(f)
        # print(save_img[i])
        assert f.shape == image_size, 'Image sizes are different'
        assert f.shape == save_img[i].shape, 'Image sizes are different 2'

        # images are jpeg compress, so they won't match
        # assert np.array_equal(save_img[i], f), 'Images are different'

    os.remove(filename)
    time.sleep(1)


def test_write_load():
    rw(False)


def test_write_load_compressed():
    rw(True)


def test_size():
    bag = BagWriter()
    bag.open(['data', 'camera'])

    for i in range(10):
        bag.push('data', i)

    sz  = bag.size()

    assert sz['data'] == 10, 'Data size is wrong'
    assert sz['camera'] == 0, 'Camera size is wrong'


def test_circularBuff():
    cb_len = 10
    cb = CircularBuffer(cb_len)
    assert len(cb._data) == cb_len

    # should push 0 - 99
    for i in range(100):
        cb.push(i)

    # buffer should only have 90-99 in it since it is only 10 in length
    data = cb.get_all()

    for i, p in enumerate(range(90, 100)):
        assert data[i] == p
