import os
import gaussian_plane_ditribution as gauss
import apriori_rules as apriori

INPUT_FILE = "/Users/inbanerj/CODE/Data_Science/PATENT/Anomaly_Detector/test-logs/input.2.log"
#metric_index_list = [80, 81, 82, 83, 118, 119, 133, 134]
metric_index_list = [80]
DIM_NUM = 41
GAUSSIAN_THRESHOLD = 0.00001
DIMENSION_DICT = {"Country" : 8, "CITY" : 6, "OS" : 10, "BROWSER" : 9, "ASN" : 17, "FILE_SIZE" : 20, "MAP_RULE" : 23, "DMA" : 28}

if __name__ == "__main__":
	
	dim_list = []
	met_list = []
	with open (INPUT_FILE, 'r') as data:
		for line in data:
			line = line.rstrip("\n")
			alist = line.split(' ')
			
			#dim_list.append(alist[:41])
			temp_list = []
			for key in DIMENSION_DICT:
				idx = DIMENSION_DICT[key]
				hash_key = str(key) + " : " + alist[idx]
				temp_list.append(hash_key)
			dim_list.append(temp_list)
			met_list.append(alist[41:])

	for idx in metric_index_list:
		print ("Metric to be used: %d" % idx)
		idx = idx - DIM_NUM
		metric_list = [met_list[i][idx] for i in range(len(met_list))]
		(gaussian_list, dim_list) = gauss.get_gaussian_plane_distribution(metric_list, dim_list)
		print ("*********************	GAUSSIAN DISTRIBUTION	*****************************")
		print gaussian_list

		apriori.create_association_rules(gaussian_list, dim_list)
