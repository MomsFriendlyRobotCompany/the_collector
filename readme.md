[![image](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/the-collector/master/pics/header.jpg)](https://github.com/MomsFriendlyRobotCompany/the-collector)

# The Collector

[![Actions Status](https://github.com/MomsFriendlyRobotCompany/the-collector/workflows/CheckPackage/badge.svg)](https://github.com/MomsFriendlyRobotCompany/the-collector/actions)
![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/the-collector)
[![Latest Version](https://img.shields.io/pypi/v/the-collector.svg)](https://pypi.python.org/pypi/the-collector/)
[![image](https://img.shields.io/pypi/pyversions/the-collector.svg)](https://pypi.python.org/pypi/the-collector)
[![image](https://img.shields.io/pypi/format/the-collector.svg)](https://pypi.python.org/pypi/the-collector)
![PyPI - Downloads](https://img.shields.io/pypi/dm/opencv_camera?color=aqua)

**This is still under heavy development**

The idea behind this a container that can store data and time tag the
data when it is captured. The main structure is a dict which has keys
for each data series stored.

This was written for a class I taught on robotics. It is meant to be simple and
teach the students some things. There are probably better solutions out there,
but I like this.

Additionally, there is nothing magically about what this does:

- It provides a generic interface to using `pickle` or `json` as
the protocol for saving data to disk
- It also allows you to convert between them if needed
- Bag files can be read using the original protocol, thus data is never lost
if this library goes away
- Designed to be simple and straight forward

## Setup

### Install

The suggested way to install this is via the `pip` command as follows:

    pip install the_collector
    pip install the_collector[numpy]

If you install `numpy`, then you get access to working with numpy arrays
using the functions: `array_pack()` and `array_pack()`. These really don't
save you much.

# Usage

## BagIt

Bag stores data in memory until the buffer size limit is reached then it dumps
the data to a file.

```python
#!/usr/bin/env python3
from the_collector import BagIt
from the_collector import Json, Pickle
import json


d = {'a': 1, 'b': 2}

bag = BagIt(Json)      # ascii, cross platform
# bag = BagIt(Pickle)  # binary, python only but handles python objects well

for i in range(10):
    bag.push('test', d) # push value d to key 'test'
    bag.push('bob', d)
    bag.push('tom', ('a', i,))

# timestamp adds a timestamp automatically to the bag file. Thus, you won't
# over write bob.json.bag each time you run this program because the filename
# is bob-2019-04-20-15:35:25.6543.json.bag
fname = bag.write('bob', timestamp=False)

print(">> created:", fname)

data = bag.read(fname) # data is just a dictionary
print(data)
```

Now, since there is nothing super special `the_collector` does with packing
data, you can always read the bag files using the original libraries:

```python
with open(fname, 'rb') as fd:
    data = json.load(fd)

for key, val in data.items():
    print("{}[{}]".format(key, len(val)))
    for v in val:
        print("{}".format(v), end=' ')
        print(' ')
```

## Circular Buffer

This is perhaps a little out of place, but I use circular buffers with handling data
so I stuck it in this library.

```python
from the_collector import CircularBuffer

cb = CircularBuffer(60)  # can only hold 60 items before it copies over data

# Let's push way more than 60 things
for i in range(200):
    cb.push(i)

print(cb.get_all())  # print everything
print('get cb[7]', cb[7])
print('get cb[0]', cb[0])
print('get last', cb.get_last())
```

## Data Tuple

Use a generic `namedtuple` for data storage. It will automatically insert a
timestamp when created. This is useful for tagging data with a timestamp and
not having to remember to do it yourself.

**WARNING:** `json` and `msgpack` have issues with `tuples`, so this is best
used with `pickle` or you have to accept `json` will turn it into a list and
`msgpack` will turn it into a regular `tuple`. Either way, you still keep the
timestamp.

```python
from the_collector import Data

d = Data((1,2,3,))  # timestamp generate when made

print("Data[{}]: {}".format(d.timestamp, d.data))
print("Namedtuple output:", d)
```

# Todo

- [x] add github actions
- [ ] look at enabling `BytesIO` for testing/working so you don't litter filing system
with test bag files
- [x] support PEP517 and replace `setup.py` with `pyprogram.toml`
- [x] move tests from `nose` to `pytest`
- [x] remove `msgpack`, there is no advantage to it over `pickle`(python only) or `json`(cross platform)
- [x] add `json` compression back in

# Change Log

Date        | Version| Notes
------------|--------|----------------------------------
2020-04-19  | 0.8.5  | removed `msgpack`
2019-07-06  | 0.8.2  | add generic data container
2019-04-28  | 0.8.0  | can store data using `json`, `pickle`, or `msgpack`
2018-07-25  | 0.7.0  | added `msgpack` messages and a way to do custom messages
2018-07-14  | 0.6.0  | changed interface to support buffered writing to disk
2018-07-09  | 0.5.0  | moved away from `json` and now using `msgpack`
2017-11-23  | 0.4.0  | fixes, documentation, unit tests
2017-10-04  | 0.0.1  | init

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
