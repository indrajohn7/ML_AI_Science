#!/usr/bin/python
import os
import sys
import itertools
from timeit import Timer
import k_mean_dim
from collections import defaultdict

dimension = ['TIMESTAMP', 'FF_CPCODE', 'CLIENT_ASN', 'CLIENT_COUNTRY', 'CLIENT_CONTINENT', 'GHOST_ASN', 'FF_STATUS_CODE', 'FF_CONTENT_TYPE', 'HTTP_METHD', 'SERVER_REGION', 'CHILD_REGION', 'REQUEST_TYPE', 'OBJECT_SIZE_RANGE', 'EDC_DEVICE_TYPE', 'OS', 'FF_MA_FILE_EXTENSION', 'STREAMID']

THRESHOLD_PERCENT = 1

dimension_list = {'CLIENT_COUNTRY' : 4  , 'CLIENT_ASN' : 3, 'OBJECT_SIZE_RANGE' : 13, 'EDC_DEVICE_TYPE' : 14, 'GHOST_ASN' : 6, 'SERVER_REGION' : 10, 'OS' : 15, 'FF_MA_FILE_EXTENSION' : 16}
dimension_set = ['CLIENT_COUNTRY', 'CLIENT_ASN', 'OBJECT_SIZE_RANGE', 'EDC_DEVICE_TYPE', 'GHOST_ASN', 'SERVER_REGION', 'OS', 'FF_MA_FILE_EXTENSION']
dimension_idx = [4, 3, 13, 14, 6, 10, 15, 16]
dimension_new_idx_list = {'CLIENT_COUNTRY' : 1  , 'CLIENT_ASN' : 2, 'OBJECT_SIZE_RANGE' : 3, 'EDC_DEVICE_TYPE' : 4, 'GHOST_ASN' : 5, 'SERVER_REGION' : 6, 'OS' : 7, 'FF_MA_FILE_EXTENSION' : 8}

dim_list = k_mean_dim.recovery_dim_list
final_list = []

for line in dim_list:
	alist = []
	for idx in range(len(dimension_idx)):
		pos = dimension_idx[idx] - 1
		alist.append(line[pos])
	final_list.append(alist)

dimension_powerset = [[] for _ in range(len(dimension_list))]
dimension_idxset = [[] for _ in range(len(dimension_list))]
dimension_powerhits = [[] for _ in range(len(dimension_list))]

total_number_of_list = 0
total_number_of_dim_combinations = 0

'''
for input_list in final_list:
	for counter in range(1, len(input_list)+1):
		for subset in itertools.combinations(input_list, counter):
			dimension_powerset[counter-1].append(list(subset))
			dimension_powerhits[counter-1].append(len(list(subset)))
			total_number_of_list += 1
'''

for counter in range(1, len(dimension_set)+1):
	for subset in itertools.combinations(dimension_set, counter):
		dimension_idxset[counter-1].append(list(subset))
		total_number_of_dim_combinations += 1

powerset = [defaultdict(list) for _ in range(len(dimension_list))]

for input_list in final_list:
	for item in range(len(dimension_set)):
		for idx in range(len(dimension_idxset[item])):
			alist = []
			adict = defaultdict(list)
			dim_set = dimension_idxset[item][idx]
			dim_str = '%'.join(dim_set)
			for j in range(len(dimension_idxset[item][idx])):
				key = dimension_new_idx_list[dimension_idxset[item][idx][j]] - 1
				alist.append(input_list[key])
			if dim_str in powerset[item]:
				powerset[item][dim_str].append(alist)
			else:
				adict[dim_str].append(alist)
				powerset[item][dim_str].append(alist)
			total_number_of_list += 1

print(total_number_of_list)
print(total_number_of_dim_combinations)
print(dimension_idxset)

# It can be a pair as well.
# Below is an example of a pair usage:

recovery_dict = defaultdict(list)
final_recovery_dict = defaultdict(dict)

for item in range(len(dimension_set)):
	for dim in powerset[item]:
		dim_com = str(dim)
		parent_list = powerset[item][dim]
		for alist in parent_list:
			key = '%'.join(alist)
			count_hit = 0
			percent_hit = 0

			if key in recovery_dict:
				occurence_list = recovery_dict[key]
				occurence_list[0] += 1
				occurence_list[1] = float((occurence_list[0] * 100) / float(total_number_of_list))
				percent_hit = occurence_list[1]
				recovery_dict[key] = occurence_list
			else:
				#occurence_lis has a list of occurence counter and percent of appearence
				occurence_list = []
				count_hit += 1
				percent_hit = float((count_hit * 100) / float(total_number_of_list))
				occurence_list.append(count_hit)
				occurence_list.append(percent_hit)
				recovery_dict[key] = occurence_list
		
			if percent_hit >= THRESHOLD_PERCENT:
				final_recovery_dict[dim_com][key] = percent_hit
				
'''
for item in range(len(dimension_set)):
	for idx in range(len(dimension_powerset[item])):
		hits = dimension_powerhits[item][idx]
		dim_set = dimension_idxset[item][idx]
		key_list = dimension_powerset[item][idx]
		dim_com = '%'.join(dim_set)
		key = '%'.join(key_list)
		count_hit = 0
		percent_hit = 0

		if key in recovery_dict:
			occurence_list = recovery_dict[key]
			occurence_list[0] += 1
			occurence_list[1] = float((occurence_list[0] * 100) / float(total_number_of_list))
			percent_hit = occurence_list[1]
			recovery_dict[key] = occurence_list
		else:
			#occurence_lis has a list of occurence counter and percent of appearence
			occurence_list = []
			count_hit += 1
			percent_hit = float((count_hit * 100) / float(total_number_of_list))
			occurence_list.append(count_hit)
			occurence_list.append(percent_hit)
			recovery_dict[key] = occurence_list
		
		if percent_hit >= THRESHOLD_PERCENT:
			final_recovery_dict[dim_com][key] = percent_hit
'''				

print(recovery_dict)
print(len(recovery_dict))
print(final_recovery_dict)
print(len(final_recovery_dict))

for dim_com in final_recovery_dict:
	for key in final_recovery_dict[dim_com]:
		val = float(final_recovery_dict[dim_com][key])
		dim_str = str(dim_com)
		key_str = str(key)
		print("%s :: %s :: %.4f" % (dim_str, key_str, val))

#print(recovery_dict)
#print(len(recovery_dict))
#print(final_recovery_dict)

'''
for line in dimension_powerset:
	print(line)
'''

