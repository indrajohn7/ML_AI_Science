#!/usr/bin/python3

import os
import random
from collections import defaultdict
import pickle

def form_clusters(alist, cluster, flag, alist_of_clusters):
	def_list = []
	if(flag == 0):
		size = len(alist)
		first = alist[0]
		diff = alist[size - 1] - alist[0]
		if (len(alist_of_clusters) == 0):
			means = []
			try:
				#means = random.sample(xrange(alist[0], alist[size - 1]), cluster)
				counter = 1
				factor = float(1 / float(cluster))
				factor = int(factor * 10)
				factor = float(factor / float(10.0))
				print (factor)
				for i in range(cluster):
					means.append(first + (diff * factor * counter))
					counter += 1
			
			except ValueError:
				print('Sample size exceeded population size.')
			means.sort()
			print(means)
			
			
			for i in range(cluster):
				def_list.append([])
			print(def_list)
			
			for data in alist:
				idx = 0
				diff = 999999999999999
				for i in range(len(means)):
					if (abs(means[i] - data) < diff):
						diff = abs(means[i] - data)
						idx = i
				def_list[idx].append(data)
			print(def_list)
			alist_of_clusters = def_list
			print(alist_of_clusters)
			form_clusters(alist, cluster, 0, alist_of_clusters)
		else:
			print("Hi\n")
			means = []
			for i in range(cluster):
				#means = reduce(lambda x, y: x + y, alist_of_clusters[i]) / len(alist_of_clusters[i])
				if (len(alist_of_clusters[i]) > 0):
					means.append(int(sum(alist_of_clusters[i])/int(len(alist_of_clusters[i]))))
				else:
					means.append(999999999999999)
			for i in range(cluster):
				def_list.append([])
			
			print(means)	
			for data in alist:
				idx = 0
				diff = 999999999999999
				for i in range(len(means)):
					if (abs(means[i] - data) < diff):
						diff = abs(means[i] - data)
						idx = i
				def_list[idx].append(data)
			new_means = []
			print(def_list)
			
			for i in range(cluster):
				#means = reduce(lambda x, y: x + y, alist_of_clusters[i]) / len(alist_of_clusters[i])
				if (len(def_list[i]) > 0):
					new_means.append(int(sum(def_list[i])/int(len(def_list[i]))))
				else:
					new_means.append(999999999999999)
			print(means)
			print(new_means)
			if (means == new_means):
				form_clusters(alist, cluster, 1, alist_of_clusters)
			else:
				alist_of_clusters = def_list
				form_clusters(alist, cluster, 0, alist_of_clusters)

			#do nothing
	else:
		print("Operation Finished\n")
		#do nothing	
	return alist_of_clusters



def __main__():
	alist = []
	dim_list = []
	counter = 0
	adict = defaultdict(list)
	with open('data_dim.txt', 'r') as data:
		for data_set in data:
			data_set = data_set.rstrip("\n")
			#print(data_set)
			raw_list = [i for i in data_set.split(' ')]
			#print(raw_list)
			raw_len = len(raw_list)
			val = (int)(raw_list[raw_len - 1])
			alist.append(int(val))
			raw_list.pop(raw_len - 1)
			#print(raw_list)
			dim_list.append(raw_list)
			#print(dim_list)
			#print(alist)
			adict[val].append(counter)
			counter += 1
		
	cluster = input("Enter number of Clusters: ");
	cluster = int(cluster)
	alist_of_clusters = []
	print(cluster)
	alist.sort()
	print(alist)
	clusters = form_clusters(alist, cluster, 0, alist_of_clusters)
		
	print(clusters)
	print(adict)		

	with open('output_dim.txt', 'wb') as fp:
		for i in range(len(clusters)):
			for j in range(len(clusters[i])):
				met_val = clusters[i][j]
				dim_idx_list = adict[met_val]
				for dim_idx in dim_idx_list:
					pickle.dump(dim_list[dim_idx], fp)
					#print (dim_list[dim_idx])
					#print(met_val)


#While reading back the pickle:
#with open ('outfile', 'rb') as fp:
#    itemlist = pickle.load(fp)


	data.close()
	fp.close()
	return

__main__()
