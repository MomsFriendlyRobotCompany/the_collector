#!/usr/bin/env python

from __future__ import print_function
# import sparkline


class CircularBuffer(object):
    def __init__(self, size, mmax=100.0, mmin=0.0):
        """initialization"""
        self.index = 1
        self.size = size
        self._data = [0.0]*size
        self.sum = 0.0
        self.min = 1E900
        self.max = -1E900
        # self.min = mmin
        # self.max = mmax

    def push(self, value):
        """append an element"""
        self.sum += value
        self.max = value if value > self.max else self.max
        self.min = value if value < self.min else self.min

        # if len(self._data) == self.size:
        self._data[self.index] = value
        # else:
        #     self._data.append(value)
        self.index = (self.index + 1) % self.size

    def __getitem__(self, key):
        """get element by index like a regular array"""
        i = self.index + key
        return(self._data[i])

    def __repr__(self):
        """return string representation"""
        return self._data.__repr__() + ' (' + str(len(self._data))+' items)'

    def get_all(self):
        """return a list of all the elements"""
        ret = []
        if self.index > 0:
            ret = self._data[self.index:self.size] + self._data[0:self.index]
        else:
            ret = self._data
        return ret

    def get_last(self):
        return self._data[self.index-1]

    def get_first(self):
        return self._data[self.index]

    # def spark(self):
    #     data = self.get_all()
    #     return sparkline.sparkify(data).encode('utf-8')


if __name__ == "__main__":
    cb = CircularBuffer(60)

    for i in range(200):
        cb.push(i)

    print(cb.get_all())
    print('get cb[7]', cb[7])
    print('get cb[0]', cb[0])
    print('get last', cb.get_last())
    # print('ine', cb.get_last(), sparkline.sparkify(cb.get_all()).encode('utf-8'))
    # print(cb.get_first(), cb.spark(), cb.get_last())
