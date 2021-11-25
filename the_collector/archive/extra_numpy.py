##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import numpy as np


def array_pack(img):
    """
    img: numpy array. I primarily use this for OpenCV images
    """
    d = img.tobytes()
    s = img.shape
    t = img.dtype

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
