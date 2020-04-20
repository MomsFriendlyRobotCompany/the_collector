#!/usr/bin/env python
from pprint import pprint
from the_collector import BagIt
from the_collector import Json, Pickle

bag = BagIt(Json)
bag.packer.compress(True)
print(f">> {bag.packer.proto}")
fname = "imu-1-2.json-gz"
data = bag.read(fname)
print(type(data))
print(data.keys())
# pprint(data)
