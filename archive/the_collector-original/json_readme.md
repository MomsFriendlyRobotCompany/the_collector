# Old Json Version

The old version always returned a `dict` and always appended a timestamp. I will
eventually remove this code.

## Usage

In the code example below, sensor data is saved to a file. Specifically,
it is saving:

-   imu: accel, gyro, magnetometer
-   camera: raspberry pi images.

Every time data is pushed into the Bag file, each data point is given a
time stamp. Thus, for the camera, the Bag (which is a dictionary) would
have an array of:

```python
bag['camera'] = [[frame0, stamp], [frame1, stamp], ... ]
bag['imu'] = [[imu0, stamp], [imu1, stamp], ... ]
```

where `stamp` is a time stamp, `frame` is an image from from a camera,
and imu is an array of \[accel, gyro, magnetometer\] data. Now to save
data to disk:

```python
from the_collector.bagit import BagJsonWriter
import time

# this file name gives a time/date when it was created
# you don't have to do this, 'data.json' would work fine too
filename = 'robot-{}.json'.format(time.ctime().replace(' ', '-'))

# create the writer
bag = BagJsonWriter()
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
```

To read data from a bag file:

``` python
from the_collector.bagit import BagJsonReader

reader = BagJsonReader()
data = reader.load('my_file.json')  # read in the file and conver to dict

# now print everything out
for key, value in data.items():
    print('-- {} -----------------'.format(key))
    for sample in value:
        point, timestamp = sample
        print(timestamp, point)
    print('')
```

### Compression

You can turn on or off compress to reduce file size. If you use the
compression, then it really **isn\'t a json file anymore**. Thus, other
programs won\'t be able to read it.

``` python
bag = BagJsonWriter()           # or BagReader()
bag.use_compression = True  # or False (default)
```
