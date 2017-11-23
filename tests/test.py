from __future__ import print_function, division
from the_collector import BagWriter, BagReader
from the_collector import CircularBuffer
import os
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
	except:
		assert False, 'Could not write bag file'

	# data is a hash
	# each key has an array: [data_point, time_stamp]
	reader = BagReader()
	reader.use_compression = compress
	data = reader.load(filename)

	# for i in range(run_len):
	# 	assert data['data'][i][0] == i, 'Data is different'
	#
	# 	f = data['camera'][i][0]
	# 	print(f)
	# 	# print('size', f.shape, image_size, i)
	# 	assert f.shape == image_size, 'Image sizes are different'
	# 	assert f.shape == save_img[i].shape, 'Image sizes are different 2'
	# 	assert np.array_equal(save_img[i], f), 'Images are different'

	for i, (d, ts) in enumerate(data['data']):
		assert i == d, 'Data is different'


	os.remove(filename)


def test_write_load():
	# rw(True)
	rw(False)


# def test_circularBuff():
# 	cb_len = 10
# 	cb = CircularBuffer(cb_len)
# 	assert len(cb._data) == cb_len
#
# 	# should push 0 - 99
# 	for i in range(100):
# 		cb.push(i)
#
# 	# buffer should only have 90-99 in it since it is only 10 in length
# 	data = cb.get_all()
#
# 	for i, p in enumerate(range(90, 100)):
# 		assert data[i] == p
