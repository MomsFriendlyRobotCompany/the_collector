# #!/usr/bin/env python
#
# from __future__ import division, print_function
# from the_collector.bagit import BagWriter, BagReader
# import cv2
# from opencvutils import Camera
# import time
#
#
# def write_bag(filename, compress):
#     """
#     Capture camera images and save to file.
#     """
#     cam = Camera()
#     cam.init(win=(640, 480), cameraNumber=0)
#
#     bag = BagWriter()
#     bag.open(['camera'])
#     bag.stringify('camera')
#     bag.use_compression = compress
#
#     for _ in range(10):
#         ret, img = cam.read()
#
#         if ret:
#             bag.push('camera', img)
#         else:
#             print('ERROR: bad image')
#
#         time.sleep(0.5)
#
#     bag.write(filename)
#
#
# def read_bag(filename, compress):
#     """
#     Given a file, open and display images in file.
#     """
#     bag = BagReader()
#     bag.use_compression = compress
#     data = bag.load(filename)
#
#     for img, stamp in data['camera']:
#         cv2.imshow('camera', img)
#         cv2.waitKey(1000)
#
#
# if __name__ == "__main__":
#     filename = 'test2.json'
#     compress = True
#     write_bag(filename, compress)
#     read_bag(filename, compress)
