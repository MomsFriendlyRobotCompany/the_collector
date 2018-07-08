.. image:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/the-collector/master/pics/header.jpg
    :align: center
    :width: 300px
    :target: https://github.com/MomsFriendlyRobotCompany/the-collector

The Collector
=================


.. image:: https://img.shields.io/pypi/v/the-collector.svg
    :target: https://pypi.python.org/pypi/the-collector/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/l/the-collector.svg
    :target: https://pypi.python.org/pypi/the-collector/
    :alt: License
.. image:: https://travis-ci.org/MomsFriendlyRobotCompany/the-collector.svg?branch=master
    :target: https://travis-ci.org/MomsFriendlyRobotCompany/the-collector
.. image:: https://img.shields.io/pypi/pyversions/the-collector.svg
    :target:  https://pypi.python.org/pypi/the-collector
.. image:: https://img.shields.io/pypi/format/the-collector.svg
    :target:  https://pypi.python.org/pypi/the-collector



**This is still under heavy development**

The idea behind this a container that can store data and time tag the data when
it is captured. The main structure is a `dict` which has keys for each data
series stored.

Setup
--------

Install
~~~~~~~~~~~~~

The suggested way to install this is via the ``pip`` command as follows::

	pip install the_collector

Development
~~~~~~~~~~~~~

To submit git pulls, clone the repository and set it up as follows::

	git clone https://github.com/MomsFriendlyRobotCompany/the-collector
	cd the-collector
	pip install -r requirements
	pip install -e .

Usage
--------

In the code example below, sensor data is saved to a file. Specifically, it is saving:

- imu: accel, gyro, magnetometer
- camera: raspberry pi images.

Every time data is pushed into the Bag file, each data point is given a time stamp.
Thus, for the camera, the Bag (which is a dictionary) would have an array of:

.. code-block:: python

	bag['camera'] = [[frame0, stamp], [frame1, stamp], ... ]
	bag['imu'] = [[imu0, stamp], [imu1, stamp], ... ]

where ``stamp`` is a time stamp, ``frame`` is an image from from a camera, and imu
is an array of [accel, gyro, magnetometer] data. Now to save data to disk:

.. code-block:: python

	from the_collector.bagit import BagWriter
	import time

	# this file name gives a time/date when it was created
	# you don't have to do this, 'data.json' would work fine too
	filename = 'robot-{}.json'.format(time.ctime().replace(' ', '-'))

	# create the writer
	bag = BagWriter()
	bag.open(filename, ['imu', 'camera'])

	# camera images are binary arrays, we are going to base64 encode them
	# so we can store them in a json file nicely
	bag.stringify('camera')  # this can be a string or an array of keys

	try:
		while True:
			# read and get imu data, say: data = imu.read()
			# always push (key, data), push will add a timestamp
			bag.push('imu', data)

			# read camera, say: ret, frame = camera.read()
			bag.push('camera', frame)

	except KeyboardError:
		bag.write()  # actually writes the data to disk

To read data from a bag file:

.. code-block:: python

	from the_collector.bagit import BagReader

	reader = BagReader()
	data = reader.load('my_file.json')  # read in the file and conver to dict

	# now print everything out
	for key, value in data.items():
		print('-- {} -----------------'.format(key))
		for sample in value:
			point, timestamp = sample
			print(timestamp, point)
		print('')

Compression
~~~~~~~~~~~~~~

You can turn on or off compress to reduce file size. If you use the compression,
then it really **isn't a json file anymore**. Thus, other programs won't be able
to read it.

.. code-block:: python

	bag = BagWriter()           # or BagReader()
	bag.use_compression = True  # or False (default)

Examples
---------

See ``examples`` folder	examples how to capture images and record them.

Change Log
-------------

========== ======= =============================
2017-11-23 0.4.0   fixes, documentation, unit tests
2017-10-04 0.0.1   init
========== ======= =============================

Software License
------------------------

**The MIT License (MIT)**

Copyright (c) 2017 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
