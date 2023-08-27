# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
import json
import pickle
import datetime as dt
import gzip
from pathlib import Path
import csv

class Collector:
    timestamp = False

    """
    Read and write data files using pickle, json, gziped
    json, and csv. Method is determined by filename extension.
    Valid extensions are:
      .pkl: pickle
      .json: json
      .gzip: json compressed with gzip [default]
      .csv: comma separated values
    """
    def read(self, fname):
        """Read filename and return data or None"""
        p = Path(fname)
        suffix = p.suffix
        data = None

        match suffix:
            case ".pkl":
                with open(fname, 'rb') as fd:
                    data = pickle.load(fd)
            case ".json":
                with open(fname, 'r') as fd:
                    data = json.load(fd)
            case ".gzip":
                with gzip.open(fname, 'rt', encoding="ascii") as fd:
                    data = json.load(fd)
            case ".csv":
                data = {"data": []}
                # with open(fname, 'r', newline='', encoding='utf-8') as fd:
                with open(fname, 'r', newline='') as fd:
                    reader = csv.reader(fd, quoting = csv.QUOTE_NONNUMERIC)
                    for row in reader:
                        data["data"].append(row)
            case _:
                print(f"*** {suffix} is invalid ***")
                return None

        if data is not None:
            print(f"Loaded {len(data['data'])} data points from:\n--> {fname}")

        return data

    def write(self, fname, data, info=None):
        """
        Write filename with info and data. Optional, insert
        time stamp into filename.
          data: list of sampled data
          info: optional dictonary providing useful info about data
        """
        # if not isinstance(data,list):
        #     try:
        #         data = data.tolist()
        #     except:
        #         print("*** data needs to be a list ***")
        #         return

        if info is None:
            info = {}

        info["timestamp"] = str(dt.datetime.now().isoformat())
        save = {"info": info, "data": data}

        # print(">>", fname)

        p = self.__set_name(fname)
        suffix = p.suffix
        fname = str(p)
        # print(">>",suffix, fname)
        # return

        match suffix:
            case ".pkl":
                # print(f"Saving {len(data)} data points using pickle")
                fmt = "pickle"
                with open(fname, 'wb') as fd:
                    pickle.dump(save, fd, protocol=pickle.HIGHEST_PROTOCOL)
            case ".json":
                # print(f"Saving {len(data)} data points json")
                fmt = "json"
                with open(fname, 'w') as fd:
                    json.dump(save, fd)
            case ".gzip":
                # print(f"Saving {len(data)} data points json")
                fmt = "json gzip"
                with gzip.open(fname, 'wt', encoding="ascii") as fd:
                    json.dump(save, fd)
            case ".csv":
                # print("Not implemented")
                fmt = "csv"
                with open(fname, 'w', newline='') as fd:
                    writer = csv.writer(fd, quoting = csv.QUOTE_NONNUMERIC)
                    writer.writerows(data)
            case _ :
                fname += ".gzip"
                print(f"Assuming gzip, file name is: {fname}")
                fmt = "json gzip"
                with gzip.open(fname, 'wt', encoding="ascii") as fd:
                    json.dump(save, fd)

        print(f"Saving data points in {fmt} to:\n--> {fname}")
        return fname

    def __set_name(self, fname):
        p = Path(fname)
        # print(">>", p.name, str(p))
        ts = "/"
        if self.timestamp:
            ts += dt.datetime.today().isoformat(sep='_', timespec='seconds') + "_"
            ts = ts.replace(':','-')
        fname = str(p.parent) + ts + str(p.name)
        p = Path(fname)
        return p



def nuke(path=".", patterns=None, recursive=False):
    """
    Deletes all file patterns optionally recursively.
    """
    p = Path(path)
    if patterns is None:
        patterns = ["*.csv","*.gzip","*.pkl","*.json"]
    for ext in patterns:
        if recursive:
            glob = p.rglob(ext)
        else:
            glob = p.glob(ext)
        for f in glob:
            f.unlink()