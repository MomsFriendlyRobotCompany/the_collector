#!/usr/bin/env python

from __future__ import print_function, division
import cv2
import time
import numpy as np
import os
import simplejson as json
import base64
import gzip  # compression


"""
encode:
img_str = cv2.imencode('.jpg', img)[1].tostring()

decode:
nparr = np.fromstring(STRING_FROM_DATABASE, np.uint8)
img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

unicode errors with above

jpeg = = cv2.imencode('.jpg', img)[1]
img_str = base64.b64encode(jpeg)

now to reverse:

ii = base64.b64decode(img_str)
ii = np.fromstring(ii, dtype=np.uint8)
ii = cv2.imdecode(ii, self.depth)

"""


class Base(object):
	"""
	"""
	encode = '.jpg'
	use_compression = True

	def decodeB64(self, b64, depth):
		"""base64 to OpenCV"""
		ii = base64.b64decode(b64)
		ii = np.fromstring(ii, dtype=np.uint8)
		img = cv2.imdecode(ii, depth)
		return img

	def encodeB64(self, img):
		"""OpenCV to base64"""
		ret, jpeg = cv2.imencode(self.encode, img)
		if not ret:
			print('<<<< error >>>>>>')
		# jpeg = img.tobytes()
		b64 = base64.b64encode(jpeg)
		return b64


class BagReader(Base):
	"""
	"""
	def load(self, filename):
		try:
			if self.use_compression:
				with gzip.open(filename, 'r') as f:
					data = json.load(f)
			else:
				with open(filename, 'r') as f:
					data = json.load(f)

			for key in data['b64keys']:
				tmp = []
				for b64, datestamp in data[key]:
					img = self.decodeB64(b64, 1)  # not sure depth is working
					tmp.append((img, datestamp))
				data[key] = tmp

		except:
			print('Error reading file: {}'.format(filename))
			raise

		return data


class BagWriter(Base):
	"""
	"""

	def __init__(self):
		self.clear()

	def __del__(self):
		pass

	def stringify(self, keys):
		if type(keys) is list:
			print('list', keys)
			for key in keys:
				self.data['b64keys'].append(key)
		elif type(keys) is str:
			print('str', keys)
			self.data['b64keys'].append(keys)
		else:
			raise Exception('Bag::stringify, invalid input: {}'.format(keys))

	def push(self, key, data):
		if key in self.data:
			# have to convert images (binary) to strings
			if key in self.data['b64keys']:
				data = self.encodeB64(data)

			timestamp = time.time()
			self.data[key].append((data, timestamp))
		else:
			raise Exception('Bag::push, Invalid key: {}'.format(key))

	def clear(self):
		self.data = {}
		self.data['b64keys'] = []

	def open(self, topics):
		self.clear()
		for key in topics:
			self.data[key] = []

	def write(self, filename):
		"""
		Once you close a bag, it is written to disk and the data is cleared
		"""
		if self.data == {}:
			return

		if self.use_compression:
			with gzip.open(filename, 'wb') as f:
				# json.dump(self.data, f)
				s=json.dumps(self.data).encode('utf8')
				f.write(s)
		else:
			with open(filename, 'wb') as f:
				# json.dump(self.data, f)
				s=json.dumps(self.data).encode('utf8')
				f.write(s)
	
	# def reset(self):
	# 	files = os.listdir('./')
	# 	for f in files:
	# 		if f == self.filename:
	# 			os.remove(self.filename)
	# 	self.written = False

	# def size(self):
	# 	size = os.path.getsize(self.filename)//(2**10)
	# 	# print('{}: {} kb'.format(self.filename, size))
	# 	return size
