#!/usr/bin/python
from __future__ import division
'''
Gaussian Distribution has a similar interpretation as k_mean except the below factors:
	1>	Computation of standard deviation.
	2>	Computation of priority.
	3> 	Computation of probablity distribution.
	4>	There is no soft assignment of any data node to a cluster.
	5>	There is only concept of distribution over a region.
'''
import os
import random
import math
from fractions import Fraction as fr
from operator import truediv

PI = 3.14
THRESHOLD_VAL = 99.0
THRESHOLD_FIELD = 0.9

def probability_distribution_calculation(val, mean, stdev):
	print ("Inside probability_distribution_calculation:")
	prob = (1/(math.sqrt(2*PI*stdev))) * (math.exp((-1) * ((val - mean)**2) / (2 * stdev)))
	#print(prob)
	return prob

def get_data_distribution_list(alist, cluster, means, stdev):	
	print ("Inside get_data_distribution_list:")
	def_list = []
	for i in range(len(alist)):
		def_list.append([])
		for num in range(cluster):
			print ("NUM: %d :: IDX: %d :: mean: %f :: stdev: %f" % (num, i, means[num], stdev[num]))
			value = probability_distribution_calculation(alist[i], means[num], stdev[num])
			print value
			def_list[i].append(value)
	print(def_list)
	return def_list

def bayes_distribution_calculation(data_distribution_list, col, row, cluster):
	#	Since the probablility of each cluster is equidistributive, hence p(cluster[i]) = (1 / cluster)
	#	For a custmized model p(cluster) list would be provided or will be derived from a function
	print ("Inside bayes_distribution_calculation:")
	deno_sum = 0.0
	#cluster = float(cluster)
	print cluster
	common_factor = truediv(1, cluster) #float(float(1) / cluster)
	print common_factor

	for data in data_distribution_list[row]:
		print data
		deno_sum += (data * (common_factor))
	
	print ("Printing Deno_Sum:")
	print deno_sum
	bayes_prob = (data_distribution_list[row][col] * (common_factor)) / (deno_sum)
	print ("Printing Bayes_Prob:")
	print(bayes_prob)
	return bayes_prob

def get_cluster_distribution_list(alist, cluster, means, stdev, data_distribution_list):
	print ("Inside get_cluster_distribution_list:")
	def_list = []
	for num in range(cluster):
		def_list.append([])
		for i in range(len(alist)):
			value = bayes_distribution_calculation(data_distribution_list,num, i, cluster)
			def_list[num].append(value)
	print(def_list)
	return def_list

def put_data_into_clusters(alist, cluster, cluster_distribution_list):
	print ("Inside put_data_into_clusters:")

	def_list = []
	for num in range(cluster):
		def_list.append([])
	for i in range(len(alist)):
		idx = -1
		prob = 0
		for num in range(cluster):
			if (cluster_distribution_list[num][i] > prob):
				idx = num
				prob = cluster_distribution_list[num][i]
		if (idx >= 0):
			def_list[idx].append(alist[i])
		else:
			print("Error: Wrong value of idx:%d " % (idx))
	print(def_list)
	return def_list

def get_mean_list(alist, cluster, cluster_distribution_list):
	print ("Inside get_mean_list:")
	def_list = []
	for num in range(cluster):
		distribution_factor = 0
		deno_factor = 0
		for i in range(len(alist)):
			distribution_factor += cluster_distribution_list[num][i] * alist[i]
			deno_factor += cluster_distribution_list[num][i]
		
		def_list.append(distribution_factor / deno_factor)
	
	print(def_list)
	return def_list

def get_stdev_list(alist, cluster, cluster_distribution_list, mean_list):
	print ("Inside get_stdev_list:")
	def_list = []
	for num in range(cluster):
		distribution_factor = 0
		deno_factor = 0
		for i in range(len(alist)):
			distribution_factor += cluster_distribution_list[num][i] * (abs(alist[i] - mean_list[num])**2)
			deno_factor += cluster_distribution_list[num][i]
		
		def_list.append(distribution_factor / deno_factor)
	
	print(def_list)
	return def_list

def threshold_breached(alist, blist):
	print "Inside threshold_breached"
	size = len(alist)
	count = 0.0

	for i in range(size):
		val1 = alist[i]
		val2 = blist[i]
		print ("VAL1: %s :: VAL2: %s" % (str(val1), str(val2)))

		if ((truediv(abs(val1 - val2), val1) * 100) <= THRESHOLD_VAL):
			count += 1
	
	print ("Breached Count: %f" % count)

	if (float(count / size) >= THRESHOLD_FIELD):
		return True
	
	return False

def create_1Dgaussian_model2(alist, cluster, flag, alist_of_clusters, mean_list = [], stdev_list = []):
	print ("Inside create_1Dgaussian_model2:")
	print alist_of_clusters
	print mean_list
	print stdev_list
	print flag
	print alist

	if(flag == 0):
		size = len(alist)
		if (len(alist_of_clusters) == 0):
			try:
				means = random.sample(range(alist[0], alist[size - 1]), cluster)
				stdev = random.sample(range(alist[0], alist[size - 1]), cluster)
			except ValueError:
				print('Sample size exceeded population size.')
			means.sort()
			stdev.sort()
			print ("printing Means:")
			print(means)
			print ("printing STDEV:")
			print(stdev)
			data_distribution_list = get_data_distribution_list(alist, cluster, means, stdev)

			cluster_distribution_list = get_cluster_distribution_list(alist, cluster, means, stdev, data_distribution_list)

			alist_of_clusters = put_data_into_clusters(alist, cluster, cluster_distribution_list)
			
			mean_list = get_mean_list(alist, cluster, cluster_distribution_list)
			
			stdev_list = get_stdev_list(alist, cluster, cluster_distribution_list, mean_list)
			
			print ("printing CLusters:")
			print(alist_of_clusters)
			create_1Dgaussian_model2(alist, cluster, 0, alist_of_clusters, mean_list, stdev_list)
		else:
			print("Hi\n")
			means = []
			stdev = []
			
			data_distribution_list = get_data_distribution_list(alist, cluster, mean_list, stdev_list)

			cluster_distribution_list = get_cluster_distribution_list(alist, cluster, mean_list, stdev_list, data_distribution_list)

			def_list = put_data_into_clusters(alist, cluster, cluster_distribution_list)
			
			new_mean_list = get_mean_list(alist, cluster, cluster_distribution_list)
			
			new_stdev_list = get_stdev_list(alist, cluster, cluster_distribution_list, new_mean_list)
			
			#if ((mean_list == new_mean_list) and (stdev_list == new_stdev_list)):
			if (threshold_breached(mean_list, new_mean_list) and threshold_breached(stdev_list, new_stdev_list)):
				print("matching!")
				create_1Dgaussian_model2(alist, cluster, 1, alist_of_clusters, mean_list, stdev_list)
			else:
				alist_of_clusters = def_list
				create_1Dgaussian_model2(alist, cluster, 0, alist_of_clusters, new_mean_list, new_stdev_list)

			#do nothing
	else:
		print("Operation Finished\n")
		#do nothing	
	return alist_of_clusters



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
				cluster = input("Enter number of Clusters: ");
				cluster = int(cluster)
				alist_of_clusters = create_1Dgaussian_model2(alist, cluster, 0, [], [], [])
				print(alist_of_clusters)
		except:
			data.close()
			pass
		data.close()
		return

__main__()
