#!/usr/bin/python3

import os
import sys
import time
import numpy as np
import subprocess

cwd = os.getcwd()
reduced_path = cwd + "/reduced/"
eigen_file = "eigen_trans.txt"
mu_file = "mu.txt"
reduced_file = "reduced_data.txt"

while (True):
    
    print ("Provide epoch TIMESTAMP as 1 to TERMINATE.")
    epoch = input('Query EPOCH TIMESTAMP: ')
    if (epoch == '1'):
        break
    cpcode = input('Query CPCODE: ')
    #epoch = '1573127000'
    #cpcode = '103'
    
    path = reduced_path + str(epoch) + "/" + str(cpcode) + "/" + reduced_file
    print(("Reading data cluster from: %s" % (path)))
    with open (path, 'r') as data:
        for line in data:
            line = line.rstrip('\n')
            data_list = line.split(' ')
            proc_time = data_list[-1]
            data_list.pop(-1)
            nComp = len(data_list)
            data_list = list(map(float, data_list))
            data_mat = np.array(data_list)
            data_mat = np.reshape(data_mat, (1, nComp))
            proc_path = reduced_path + str(proc_time) + "/"
            eigen_path = proc_path + eigen_file
            mu_path = proc_path + mu_file
            
            eigen_list = []
            with open (eigen_path, 'r') as fd1:
                for line1 in fd1:
                    line1 = line1.rstrip('\n')
                    alist = line1.split(' ')
                    alist = list(map(float, alist))
                    eigen_list.append(alist)
            fd1.close()
            
            mu_list = []
            with open (mu_path, 'r') as fd2:
                for line2 in fd2:
                    line2 = line2.rstrip('\n')
                    alist = line2.split(' ')
                    alist = list(map(float, alist))
                    mu_list.append(alist)
            fd2.close()
            
            eigen_mat = np.array(eigen_list)
            fields = eigen_mat.shape[1]
            mu_mat = np.array(mu_list)
            mu_mat = np.reshape(mu_mat, fields)

            print(data_mat.shape)
            print(eigen_mat.shape)
            print(mu_mat.shape)

            real_data = np.dot(data_mat, eigen_mat)
            real_data += mu_mat

            print(real_data.shape)
            #print real_data

            list_val = real_data.tolist()

            for alist in list_val:
                if isinstance(alist, list):
                    alist = [int(round(x)) for x in alist]
                    #print alist
                    #entry = " ".join[str(elem) for elem in alist]
                    alist_str = [str(x) for x in alist]
                    entry = " ".join(alist_str)
                    #cmd = 'grep -rn \"' + entry + "\" " + reduced_path
                    #output = subprocess.check_output(cmd, shell = True)
                    print(entry)
                else:
                    print(alist)
