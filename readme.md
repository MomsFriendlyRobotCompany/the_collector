[![image](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/the-collector/master/pics/header.jpg)](https://github.com/MomsFriendlyRobotCompany/the-collector)

# The Collector

[![Latest Version](https://img.shields.io/pypi/v/the-collector.svg)](https://pypi.python.org/pypi/the-collector/)
[![License](https://img.shields.io/pypi/l/the-collector.svg)](https://pypi.python.org/pypi/the-collector/)
[![image](https://img.shields.io/pypi/pyversions/the-collector.svg)](https://pypi.python.org/pypi/the-collector)
[![image](https://img.shields.io/pypi/format/the-collector.svg)](https://pypi.python.org/pypi/the-collector)

**This is still under heavy development**

The idea behind this a container that can store data and time tag the
data when it is captured. The main structure is a dict which has keys
for each data series stored.

This was written for a class I taught on robotics. It is meant to be simple and
teach the students some things. There are probably better solutions out there,
but I like this. :smirk:

## Setup

### Install

The suggested way to install this is via the `pip` command as follows:

    pip install the_collector
    pip install the_collector[numpy]

If you install `numpy`, then you get access to working with numpy arrays
using the functions: `array_pack()` and `array_pack()`. These really don't
save you much.

### Development

To submit git pulls, clone the repository and set it up as follows:

    git clone https://github.com/MomsFriendlyRobotCompany/the-collector
    cd the-collector
    pip install -e .

# Usage

Bag stores data in memory until the buffer size limit is reached then it dumps
the data to a file.

```python
from __future__ import print_function
from the_collector import BagReader, BagWriter


d = {'a': 1, 'b': 2}
# bag = BagWriter('bob.bag', buffer_size=1000)  # you can change buffer size
bag = BagWriter('bob.bag') # .bag is automagically appended if not present

# grab some data
for _ in range(100):
    bag.push('temperature', d)    # the key name can be anything
    bag.push('something else', d) # when you use BagReader, these become dict keys

# flushes any remaining data to the file and closes the file
bag.close()

# now read it back
bag = BagReader()
data = bag.read('bob.bag')
```

If you want to record a time stamp for each data collect (using python's
  `time.time()`), just do a `bag.push_stamp()`. However, when you read back
  the data, it will now be (data, time_stamp).

## Custom Pack/Unpack

You can pass functions to `pack` or `unpack` custom data structures to
`BagReader(pack=...)` and `BagWriter(unpack=...)` as expained in the `msgpack`
docs [here](https://github.com/msgpack/msgpack-python#packingunpacking-of-custom-data-type)

```python
def ext_unpack(msg):
    # do some cool stuff here
    # see msgpack docs for examples

# calls the function ext_unpack when something custom is encountered
bag = BagReader(unpack=ext_unpack)
```

```python
def ext_pack(msg):
    # do some cool stuff here
    # see msgpack docs for examples

# calls the function ext_unpack when something custom is encountered
bag = BagWriter('bob.bag', pack=ext_pack)
```

## Todo

- Maybe allow `BagReader` and `BagWriter` to accept a file-like object (io.BytesIO)
  but I am not sure of the value for this. It would be nice for testing, so I
  don't have to always use `os.remove()` to clean up bag files. What is a use
  case?

# History

- Originally started with storing the file as a json file
- Added compression to reduce the size, this proved to be superior to python's
  pickle library
- Looked at Google's protobufs, they seemed complex and the message types didn't
  really have what I wanted
- `msgpack` seems to be fast and compact, tried using compression (gzip library)
  on msgpack data, but it actually made it worse. Decided to go with this and
  it saves me a compression step

# Change Log

| Date | Version | Notes |
------------|--------|----------------------------------
2018-07-14  | 0.6.0  |  changed interface to support buffered writing to disk
2018-07-09  | 0.5.0  |  moved away from `json` and now using `msgpack`
2017-11-23  | 0.4.0  |  fixes, documentation, unit tests
2017-10-04  | 0.0.1  |  init

# The MIT License (MIT)

Copyright (c) 2017 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
