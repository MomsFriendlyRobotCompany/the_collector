#!/usr/bin/env python3

from the_collector import Collector
import datetime as dt

# some info about what you are saving
info = {
    "imu": {
        "name": "my cool imu",
        "accel": [4,-4],
        "gyro": 10
    }
}

# Fake data
data = [tuple([x,x,x,dt.datetime.now().timestamp()]) for x in range(100)]

col = Collector()
col.timestamp = True
col.write("test", data, info)