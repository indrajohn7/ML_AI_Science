#!/usr/bin/python3

import os
import sys
import numpy as np
import re
import time

time_list = []
cpcode_list = []
epoch_list = []
field_list = []

with open ('data.txt', 'r') as data:
    for line in data:
        line = line.rstrip('\n')
        alist = line.split(' ')
        cp = alist[0]
        alist.pop(0)
        cpcode_list.append(cp)
        ts = alist[0]
        alist.pop(0)
        time_list.append(ts)
        alist = list(map(float, alist))
        field_list.append(alist)
data.close()

field_mat = np.array(field_list)

print(field_mat.shape)
print(field_mat)

pattern = "%Y/%m/%d:%H:%M:%S"
for ts in time_list:
    pat = re.search('[0-9]+\/[0-9]+\/[0-9]+\:[0-9]+\:[0-9]+\:[0-9]+', ts)    
    if (bool(pat)):
        epoch = int(time.mktime(time.strptime(ts, pattern)))
        epoch_list.append(int(epoch))

#print cpcode_list
#print epoch_list
