##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import os

# useful?
# try:
#     import simplejson as json
# except ImportError:
#     import json






try:
    import numpy as np

    def array_pack(img):
        """
        img: numpy array. I primarily use this for OpenCV images
        """
        d = img.tobytes()
        s = img.shape
        t = img.dtype
        # msg = Image(s, d, makets())
        return (s, t, d)

    def array_unpack(shape, data, dtype=np.uint8):
        """
        I primarily use this with OpenCV images, so I think in those terms
        shape: tuple(height, width, colors)
        dtype: numpy data type like np.uint8
        data: byte array that needs to be turned back into an array
        """
        img = np.frombytes(data, dtype=dtype)
        img.reshape(shape)
        return img

except ImportError:
    import warnings
    warnings.warn('WARNING: numpy is not installed, cannot handle images')

    def array_pack(img):
        raise NotImplementedError("array_pack(): numpy not installed")

    def array_unpack(msg):
        raise NotImplementedError("array_unpack(): numpy not installed")


def file_size(filename):
    """
    Returns size of filename in kB
    """
    size = os.path.getsize(filename)//(2**10)
    # print('{}: {} kb'.format(self.filename, size))
    return size


def rm(path, filename):
    """
    Given a path and a file name, it removes the file if found.
    """
    files = os.listdir(path)
    for f in files:
        if f == filename:
            os.remove(filename)
