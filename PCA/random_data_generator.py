#!/usr/bin/python3

import os
import sys
import random

data_list = []
num = 4
start = 20
end = 1000



with open ('file1_met.txt', 'r') as data:
    for line in data:
        line = line.rstrip("\n")
        alist = line.split(' ')
        cp = alist[0]
        alist.pop(0)
        ts = alist[0]
        alist.pop(0)
        final_list = []
        l = len(alist)
        alist = []
        for i in range(0, num * l):
            alist.append(random.randint(start, end))
        
        final_list.append(cp)
        final_list.append(ts)
        final_list.extend(alist)
        data_list.append(final_list)
data.close()

with open ('rand.met.txt.bkp', 'w') as data:
    for alist in data_list:
        alist_str = [str(x) for x in alist]
        str_line = ' '.join(alist_str)
        data.write(str_line)
        data.write("\n")
data.close()

os.system('mv rand.met.txt.bkp rand.met.txt')
