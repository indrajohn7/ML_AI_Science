#!/usr/bin/python3

import os
import sys


#data_look_up = ['TIMESTAMP':, 'FF_CPCODE', 'CLIENT_ASN', 'CLIENT_COUNTRY', 'CLIENT_CONTINENT', 'GHOST_ASN', 'FF_STATUS_CODE', 'FF_CONTENT_TYPE', 'HTTP_METHD', 'SERVER_REGION', 'CHILD_REGION', 'REQUEST_TYPE', 'OBJECT_SIZE_RANGE', 'EDC_DEVICE_TYPE', 'OS', 'FF_MA_FILE_EXTENSION', 'STREAMID']
#input_file_name = "/ghostcache/home/logger/inbanerj/non_agregated_input.log"


garbage_data = ['-', 'reserved', 'UNKWN', 'others']


if __name__ == '__main__':

	input_file = raw_input("Please enter the input data file\n")
	print(input_file)

	input_file_list = []
	with open(input_file) as f:
		for log_line in f:
			line_list = [line.strip() for line in log_line.split(' ')]
			input_file_list.append(line_list)
	
	for log_line_list in input_file_list:
		for dim_value in log_line_list[:17]:
			if dim_value in garbage_data:
				#print(dim_value)
				dim_index_value = log_line_list.index(dim_value)
				#print(dim_index_value)
				#log_line_index_value = input_file_list.index(log_line_list)
				#print(log_line_index_value)
				#while(dim_value in garbage_data):
				for temp_log_line_list in input_file_list:
					temp_dim_value = temp_log_line_list[dim_index_value]
					if temp_dim_value not in garbage_data:
						log_line_list[dim_index_value] = temp_dim_value
						#print(temp_dim_value)
						break

	with open('input_data_set.txt', 'w') as f:
		for alist in input_file_list:
			alist_str = ' '.join(alist)
			f.write(alist_str+'\n')
	

	'''
	for line_list in input_file_list:
		for value in line_list:
			if value in garbage_data
    	''' 		
	#for line_list in input_file_list:
		#print(line_list)
	
	
