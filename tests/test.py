from the_collector.bagit import BagWriter, BagReader
import os
import numpy as np


def rw(compress):
	run_len = 100
	filename = 'test.json'
	depth = 3
	row = 400
	col = 500
	image_size = (row, col, depth)

	bag = BagWriter()
	bag.open(['data', 'camera'])
	bag.stringify('camera')
	bag.use_compression = compress

	for i in range(run_len):
		# read and get imu data: data = imu.read()
		bag.push('data', i)

		frame = np.random.randint(0, 255, image_size)
		bag.push('camera', frame)

	try:
		bag.write(filename)
	except:
		assert False

	# data is a hash
	# each key has an array: [data_point, time_stamp]
	reader = BagReader()
	reader.use_compression = compress
	data = reader.load(filename)

	for i in range(run_len):
		assert data['data'][i][0] == i

		f = data['camera'][i][0]
		print('size', f.shape, image_size, i)
		assert f.shape == image_size

	os.remove(filename)


def test_write_load():
	rw(True)
	rw(False)
