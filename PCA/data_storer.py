#!/usr/bin/python3

import os
import pca as pc
import read_data as rd
import time

cwd = os.getcwd()
epoch_time = int(time.time())

rows = pc.X_PCA.shape[0]
cols = pc.X_PCA.shape[1]

reduced_path = cwd + "/reduced/"
reduced_path2 = cwd + "/reduced2/"
pca_path = "reduced_data.txt"

if not os.path.exists(reduced_path):
    os.makedirs(reduced_path)

if not os.path.exists(reduced_path2):
    os.makedirs(reduced_path2)

proc_path = reduced_path + str(epoch_time) + "/"

if not os.path.exists(proc_path):
    os.makedirs(proc_path)

eigen_path = proc_path + "eigen_trans.txt"
mu_path = proc_path + "mu.txt"

count = 0

for r in range(0, rows):
    ts = rd.epoch_list[count]
    cp = rd.cpcode_list[count]
    #ts = (ts / 1000) * 1000
    path = reduced_path + str(ts) + "/" + str(cp) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    red_path = path + pca_path
    
    path2 = reduced_path2 + str(ts) + "/" + str(cp) + "/"
    if not os.path.exists(path2):
        os.makedirs(path2)
    red_path2 = path2 + pca_path
    
    with open(red_path, "a+") as data:
        for c in range(0, cols):
            val = str(pc.X_PCA[r, c]) + " "
            data.write(val)
        data.write(str(epoch_time))
        data.write('\n')
    data.close()
            
    with open(red_path2, "a+") as data2:
        for c in range(0, cols):
            val = str(int(pc.X_PCA[r, c])) + " "
            data2.write(val)
        data2.write(str(epoch_time))
        data2.write('\n')
    data2.close()
            
    count += 1

rows = pc.eigen_trans.shape[0]
cols = pc.eigen_trans.shape[1]

with open(eigen_path, 'w') as data:
    for r in range(0, rows):
        for c in range(0, cols):
            data.write(str(pc.eigen_trans[r, c]))
            if (c != (cols - 1)):
                data.write(" ")
        data.write("\n")
data.close()


rows = pc.mu.shape[0]

with open(mu_path, 'w') as data:
    for r in range(0, rows):
        #for c in range(0, cols):
        data.write(str(pc.mu[r, ]))
        if (r != (rows - 1)):
            data.write(" ")
    data.write("\n")
data.close()
