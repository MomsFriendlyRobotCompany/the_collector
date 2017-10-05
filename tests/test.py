from the_collector.bagit import Bag
import os


def test_dummy():
	assert True


def test_write():
	filename = 'test.json'
	bag = Bag(filename, ['data'])

	for i in range(200):
		# read and get imu data: data = imu.read()
		bag.push('data', i)

	bag.close()

	# data is a hash
	# each key has an array: [data_point, time_stamp]
	data = bag.read()

	for i in range(200):
		# print(data['data'][i][0], i)
		assert data['data'][i][0] == i

	bag.close()

	os.remove(filename)
