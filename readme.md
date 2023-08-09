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

- It provides a generic interface to using `pickle`, `csv`, `json` or `gzip.json` as
the protocol for saving data to disk
- It also allows you to convert between them if needed
- Bag files can be read using the original protocol, thus data is never lost
if this library goes away
- Designed to be simple and straight forward

## Usage

See the [notebook](docs/notebooks/the_collector.ipynb) for examples of how to use
it.

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
