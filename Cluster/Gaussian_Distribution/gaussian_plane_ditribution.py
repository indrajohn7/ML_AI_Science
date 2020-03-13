#!/usr/bin/python

import os
import sys
import numpy as np
import random
import math
from matplotlib import pyplot as plt

def gaussian_transform(u, sig, val):

    pi=math.pi
    
    print ("VAL: %f" % val)

    exp_val = ((val-u)**2)/(2 * (sig**2))
    print ("exp_val: %f" % exp_val)
    
    expo = math.exp((-1) * exp_val)
    print ("expo: %f" % expo)

    fd = ((1/(sig * math.sqrt(2 * pi))) * expo)
    print ("fd: %f" % fd)
    
    return fd

if __name__ == "__main__":
    data_list = []
    with open ('data.txt', 'r') as data:
        for line in data:
            line = line.rstrip()
            alist = line.split(' ')
            data_list.extend(alist)
    
    data.close()
    
    data_list = list(map(int, data_list))
    data_list.sort()
    #arr = np.array(data_list)
    #arr = np.random.uniform(low=5, high=133000, size=(5000,))
    arr = np.random.randint(5, 133000, 500)
    arr = np.sort(arr)
    print ("ARRAY SHAPE: ")
    print arr.shape
    print arr

    mu = arr.mean()
    print mu.shape
    print mu
    
    stdev = arr.std()
    print stdev.shape
    print stdev

    gauss_list = []
    for val in arr:
        gauss_val = gaussian_transform(mu, stdev, val)
        gauss_list.append(gauss_val)
        print ("Gauss Val: %f" % gauss_val)
    
    #gauss_arr = np.array(gauss_list)
    plt.plot(arr.tolist(), gauss_list)
    print gauss_list
