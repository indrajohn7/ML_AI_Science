#!/usr/bin/python3

import os
import sys
import random

data_list = []
num = 2
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
        #for i in range(0, l):
        #    if (i % 2):
        #        alist.append(random.randint(start, end))
        #    else#:
        #        alist.append(0)
        for i in range(0, num):
            alist.extend(alist)
        final_list.append(cp)
        final_list.append(ts)
        final_list.extend(alist)
        data_list.append(final_list)
data.close()


with open ('file_boss.txt', 'r') as data:
    count = 0
    for line in data:
        line = line.rstrip('\n')
        alist = line.split(' ')
        l = len(alist)
        #for i in range(0, l):
        #    if (i % 2):
        #        alist.append(random.randint(start, end))
        #    else:
        #        alist.append(0)
        for i in range(0, num):
            alist.extend(alist)
        data_list[count].extend(alist)
        count += 1
data.close()
    
with open ('file1.met.txt.bkp', 'w') as data:
    for alist in data_list:
        alist_str = [str(x) for x in alist]
        str_line = ' '.join(alist_str)
        data.write(str_line)
        data.write("\n")
data.close()

os.system('mv file1.met.txt.bkp file1.met.txt')
