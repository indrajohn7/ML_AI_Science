#!/usr/bin/python3

import os
import random
import statistics
from fractions import Fraction as fr

def stat_mod(alist):
	print ("Hi")
	stdv = statistics.stdev(alist)
	mean = statistics.mean(alist)
	var = statistics.variance(alist)
	median = statistics.median(alist)
	#mode = statistics.mode(alist)
	print("Standard Deviation:") 
	print(stdv)
	print("Mean:")
	print(mean)
	print("Variance:")
	print(var)
	#print("Mode					: " % mode)
	print("Median:")
	print(median)
	print("BYE")
	return

def __main__():
	with open('data.txt', 'r') as data:
		try:
			for data_set in data:
				alist = []
				data_set = data_set.rstrip("\n")
				print(data_set)
				alist = [int(i) for i in data_set.split(' ')]
				alist.sort()
				print(alist)
				stat_mod(alist)
		except:
			data.close()
			pass
		data.close()
		return

__main__()
