#!/usr/bin/python3

import os
import random
from collections import defaultdict
import pickle

DIMENSION_NUMBER = 17
METRIC_NUMBER = 24

metric_dict_idx = {'Throughput' : 16, 'Download_Time' : 5, 'Client_Download_Abort' : 7, 'Origin_Hits' : 9, 'Forward_Error' : 15}
metric_dict_outlier_section = {'Throughput' : 0, 'Download_Time' : 1, 'Client_Download_Abort' : 1, 'Origin_Hits' : 1, 'Forward_Error' : 1}
metric_dict_agregation = {'Throughput' : 0, 'Download_Time' : 0, 'Client_Download_Abort' : 1, 'Origin_Hits' : 1, 'Forward_Error' : 1}

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
				#print (factor)
				for i in range(cluster):
					means.append(first + (diff * factor * counter))
					counter += 1
			
			except ValueError:
				print('Sample size exceeded population size.')
			means.sort()
			print(means)
			
			
			for i in range(cluster):
				def_list.append([])
			#print(def_list)
			
			for data in alist:
				idx = 0
				diff = 999999999999999
				for i in range(len(means)):
					if (abs(means[i] - data) < diff):
						diff = abs(means[i] - data)
						idx = i
				def_list[idx].append(data)
			#print(def_list)
			alist_of_clusters = def_list
			#print(alist_of_clusters)
			form_clusters(alist, cluster, 0, alist_of_clusters)
		else:
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
			#print(def_list)
			
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


def get_metric_index(metric_name):
	try:
		met_index = metric_dict_idx[metric_name]
	except:
		print("metric name  %s not found in the list." % metric_name)
	return met_index


metric_dict_list = defaultdict(list)
outlier_dim_list = []
recovery_dim_list = []

def __main__():
	alist = []
	dim_list = []
	counter = 0
	adict = defaultdict(list)
	met_dim_idx_dict = defaultdict(lambda: defaultdict(list))
	print(metric_dict_idx)
	metric_name = raw_input("Chose Metric name from above: ");
	if ((metric_name in metric_dict_agregation) and (metric_dict_agregation[metric_name])):
		input_file = 'input_agg.log'
	elif (metric_name in metric_dict_agregation):
		input_file = 'input_non_agg.log'
	else:
		print("Chosen metric Does not have an entry.")
		exit()

	try:
		with open(input_file, 'r') as data:
			for data_set in data:
				data_set = data_set.rstrip("\n")
				#print(data_set)

				raw_list = [i for i in data_set.split(' ')]
				#print(raw_list)
				raw_dim_list = raw_list[:DIMENSION_NUMBER]
				raw_met_list = raw_list[DIMENSION_NUMBER:]
				#raw_len = len(raw_list)
				val = 0
				for key in metric_dict_idx:
					col_val = int(metric_dict_idx[key])
					val = int(raw_met_list[col_val - 1])
					metric_dict_list[key].append(raw_met_list[col_val - 1])
					met_dim_idx_dict[key][val].append(counter)
				
				#val = (int)(raw_list[raw_len - 1])
				#alist.append(int(val))
				#raw_list.pop(raw_len - 1)
				#print(raw_list)
				dim_list.append(raw_dim_list)
				#print(dim_list)
				#print(alist)
				counter += 1
	except:
		print("Couldn't complete the Operation.")
		exit()

	cluster = input("Enter number of Clusters: ");
	cluster = int(cluster)
	met_index = get_metric_index(metric_name)
	alist_of_clusters = []
	print(cluster)
	alist = list(set(map(int, metric_dict_list[metric_name])))
	alist.sort()
	print(alist)
	if metric_name in metric_dict_outlier_section:
		outlier = metric_dict_outlier_section[metric_name]
	
	clusters = form_clusters(alist, cluster, 0, alist_of_clusters)
		
	print(clusters)
	#print(met_dim_idx_dict)		
	
	with open('output_dim.txt', 'wb') as fp:
		if outlier:
			outlier = cluster - 1
			recovery = 0
		else:
			outlier = 0
			recovery = cluster - 1
		print("for chosen metric %s, outlier section is : %d and recovery data segment is: %d" % (metric_name,  outlier, recovery))
		#for i in range(len(clusters)):
		
		for j in range(len(clusters[outlier])):
			met_val = clusters[outlier][j]
			dim_idx_list = met_dim_idx_dict[metric_name][met_val] #adict[met_val]
			for dim_idx in dim_idx_list:
				outlier_dim_list.append(dim_list[dim_idx])
				#pickle.dump(dim_list[dim_idx], fp)
				#print (dim_list[dim_idx])
		
		for i in range(len(clusters[recovery])):
			met_val = clusters[recovery][i]
			dim_idx_list = met_dim_idx_dict[metric_name][met_val] #adict[met_val]
			for dim_idx in dim_idx_list:
				recovery_dim_list.append(dim_list[dim_idx])
	#for line in outlier_dim_list:
	#	line = ' '.join(line)
	#	print(line)
	#print(outlier_dim_list)

#While reading back the pickle:
#with open ('outfile', 'rb') as fp:
#    itemlist = pickle.load(fp)

	print("Outlier Computation is finished and been stored in outlier_dim_list data structure of size: %d." % len(outlier_dim_list))
	print("Recovery Computation is finished and been stored in recovery_dim_list data structure of size: %d." % len(recovery_dim_list))
	data.close()
	fp.close()
	return

__main__()
