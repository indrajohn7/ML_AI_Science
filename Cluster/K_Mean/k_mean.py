#!/usr/bin/python3

import os
import random

def form_clusters(alist, cluster, flag, alist_of_clusters):
	def_list = []
	if(flag == 0):
		size = len(alist)
		if (len(alist_of_clusters) == 0):
			try:
				means = random.sample(range(alist[0], alist[size - 1]), cluster)
			except ValueError:
				print('Sample size exceeded population size.')
			means.sort()
			print(means)
			for i in range(cluster):
				def_list.append([])
			print(def_list)
			for data in alist:
				idx = 0
				diff = 99999999.9
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
				diff = 99999999.9
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
				alist_of_clusters = []
				print(cluster)
				clusters = form_clusters(alist, cluster, 0, alist_of_clusters)
				print(clusters)
		except:
			data.close()
			pass
		data.close()
		return

__main__()
