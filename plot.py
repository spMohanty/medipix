#!/usr/bin/env python
import glob
from time import time
import numpy as np
import matplotlib.pyplot as plt
import hashlib
m = hashlib.md5()

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from PIL import Image
import os


DATA_PATH = "datafiles/output_position*"
OUTPUT_PATH = "output_dir"

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

d = {}
max_e = 0

for _file in glob.glob(DATA_PATH):
    print _file
    for _line in open(_file, "r").readlines():
        split = _line[1:-2].split(",")

        _key = _file+"::"+split[0]
        _x = int(split[1])
        _y = int(split[2])
        _e = float(split[3])

        if _e > max_e:
            max_e = _e

        try:
            foo = d[_key]
        except:
            d[_key] = []
        d[_key].append((_x, _y, _e))

#Plot all data points into individual images
for _key in d.keys():
    _image = np.zeros([256, 256], dtype=np.uint8)
    for _entry in d[_key]:
        # _image[_entry[0], _entry[1]] = _entry[2]/max_e * 256
        _image[_entry[0], _entry[1]] = 255
        #TO-DO : In the future you could also experiment with varying energies
    print _image
    _image = Image.fromarray(_image, 'L')
    m.update(_key)
    md5_key = str(m.hexdigest())
    _image.save(OUTPUT_PATH+"/"+md5_key+'.png')
    print _key
