#!/usr/bin/python3

import os
import pickle

alist = [['a', 'b', 'c'], ['p', 'q', 'r'], ['x', 'y', 'z']]
with open('pickle.txt', 'wb') as fp1:
	pickle.dump(alist, fp1)

print (alist)

fp1.close()

blist = []

with open('pickle.txt', 'rb') as fp2:
	blist = pickle.load(fp2)

fp2.close()

print(blist)
