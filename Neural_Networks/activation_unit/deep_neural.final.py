#!/usr/bin/python

import os
import sys
import random
import math
import numpy as np

data_file = "multi_grad.txt"
DECIMAL = 5
THRESHOLD = 0.9

def sigmoid(x):
  return float(1 / (1 + math.exp(-x)))

def tanh (x):
	num = float(math.exp(x) - math.exp(-x))
	denom = float(math.exp(x) + math.exp(-x))
	return float(num / denom)

def differential(y, a):
	
	return (float((-1) * (y / a)) + float((1 - y) / (1 - a)))

def get_derivative(z):
	
	sigmoid_v = np.vectorize(sigmoid)
	tanh_v = np.vectorize(tanh)
	tanh_val = True
	sigmoid_val = False

	if(sigmoid_val):
		sig_z = sigmoid_v(z)
		return (sig_z * (1 - sig_z))
	elif (tanh_val):
		tan_z = tanh_v(z)
		return ((1 - tan_z) * (1 - tan_z))
	
	return np.zeros(z.shape[0], z.shape[1])

def compute_activation_neural_network(x_list, y_list):
	
	learning = float(0.0001)
	num = len(y_list)
	feature_len = len(x_list[0])
	nodes = feature_len
	layers = feature_len
	sigmoid_v = np.vectorize(sigmoid)
	tanh_v = np.vectorize(tanh)
	
	theta_array_list = []
	seg_array_list = []
	activation_array_list = []
	meta_theta_array_list = []
	meta_seg_array_list = []

	differential_v = np.vectorize(differential)

	for l in range(layers):
		theta_array = np.random.rand(nodes, feature_len) * 0.01
		print theta_array.shape
		#seg_array = np.random.rand(nodes, num)
		#seg_array would be broadcasted to (nodes, num)
		seg_array = np.random.rand(nodes, 1)
		theta_array_list.append(theta_array)
		seg_array_list.append(seg_array)
		activation_layer = np.zeros((nodes, num))
		#dummy_array = np.random.rand((nodes - feature_len), num) * 0.01
		#activation_layer = np.append(activation_layer, dummy_array, axis = 0)
		activation_array_list.append(activation_layer)
		meta_theta_array = np.random.rand(nodes, feature_len)
		#meta_seg_array = np.random.rand(nodes, num)
		#Broadcast
		meta_seg_array = np.random.rand(nodes, 1)
		meta_theta_array_list.append(meta_theta_array)
		meta_seg_array_list.append(meta_seg_array)
	
	x_array = np.array(x_list)
	x_array = x_array.T
	print x_array.shape
	y_array = np.array(y_list)
	y_array.reshape(1, num)
	
	final_theta_array = np.random.rand(1, nodes) * 0.01
	final_seg_arr = np.random.rand(1, num)

	meta_final_theta_array = np.random.rand(1, nodes)
	#meta_final_seg_arr = np.random.rand(1, num)
	#BROADCAST
	meta_final_seg_arr = np.random.rand(1, 1)
	
	iteration = 0
	while (True):
		#	**************************	FORWARD PROPAGATION	********************************	#
		Z_list = []

		for layer in range(layers):
			if (layer == 0):
				activation_layer = x_array
				#dummy_array = np.random.rand((nodes - feature_len), num) * 0.01
				#activation_layer = np.append(activation_layer, dummy_array, axis = 0)
			else:
				activation_layer = activation_array_list[layer - 1]
			
			seg_array = seg_array_list[layer]
			theta_array = theta_array_list[layer]
			print theta_array.shape
			print theta_array
			print activation_layer.shape
			print activation_layer
			print seg_array.shape
			print seg_array

			Z1 = np.dot(theta_array , activation_layer) + seg_array
			print Z1.shape
			Z_list.append(Z1)
			#A1 = sigmoid_v(Z1)
			A1 = tanh_v(Z1)
			print A1.shape
			activation_array_list[layer] = A1
		
		Z2 = np.dot(final_theta_array, A1) + final_seg_arr
		print Z2.shape
		A2 = sigmoid_v(Z2)
		print A2.shape
		print A2

		#	**************************	BACKWARD PROPAGATION	********************************	#
		
		da2 = differential_v(y_array, A2)
		dz2 = A2 - y_array
		print dz2.shape
		dw2 = float(1 / num) * (np.dot(dz2, A1.T))
		print dw2.shape
		db2 = float(1 / num) * (np.sum(dz2, axis = 1, keepdims = True))
		count_hidden_layer = count_final_layer = 0

		da = da1 = np.array([])	
		for layer in range(layers - 1, 0, -1):
		
			Z1 = Z_list[layer]
			theta_array = theta_array_list[layer]
			seg_array = seg_array_list[layer]
			meta_theta_array = meta_theta_array_list[layer]
			meta_seg_array = meta_seg_array_list[layer]
			#	dz1 = da1 * g`(z1)  --> Formulae for dz1
			#	This code needs to be corrected
			
			if (layer == layers - 1):
				da = da2
			else:
				da = da1
			dz1 = (da * (get_derivative(Z1)))
			dw1 = float(1 / num) * (np.dot(dz1, activation_array_list[layer - 1].T))
			db1 = float(1 / num) * (np.sum(dz1, axis = 1, keepdims = True))
			da1 = np.dot(theta_array.T, dz1) 

			theta_array = theta_array - (learning * dw1)
			seg_array = seg_array - (learning * db1)
		
		
			if ((np.array_equal(np.around(theta_array, decimals = DECIMAL), np.around(meta_theta_array, decimals = DECIMAL))) and 
				(np.array_equal(np.around(seg_array, decimals = DECIMAL), np.around(meta_seg_array, decimals = DECIMAL)))):
				
				count_hidden_layer += 1
			
			meta_theta_array_list[layer] = theta_array
			meta_seg_array_list[layer] = seg_array
		
		final_theta_array = final_theta_array - (learning * dw2)
		final_seg_arr = final_seg_arr - (learning * db2)
		
		if (np.array_equal(np.around(final_theta_array, decimals = DECIMAL), np.around(meta_final_theta_array, decimals = DECIMAL)) and
			(np.array_equal(np.around(final_seg_arr, decimals = DECIMAL), np.around(meta_final_seg_arr, decimals = DECIMAL)))):
			
			count_final_layer += 1 
		
		meta_final_theta_array = final_theta_array
		meta_final_seg_arr = final_seg_arr

		print ("ITERATION: %d :: COUNT_HIDDEN: %d COUNT_FINAL: %d" % (iteration, count_hidden_layer, count_final_layer))
		print ("FEATURE_VECTOR:\n%s\nFINAL_ACTIVATION:%s" % (str(theta_array_list), str(final_theta_array)))
		print ("SEGMENT_VECTOR:\n%s\nFINAL_SEGMENT:%s" % (str(seg_array_list), str(final_seg_arr)))
		iteration += 1

		if (count_hidden_layer >= float(THRESHOLD * layers) and count_final_layer > 0):
			break
	
	return theta_array_list, seg_array_list, final_theta_array, final_seg_arr


def main():
	
	x_list = []
	y_list = []

	with open(data_file, 'r') as data:
		for line in data:
			line = line.rstrip('\n')
			line = line.split(' ')
			line = list(map(float, line))
			x_list.append(line[:-1])
			y_list.append(line[-1])
	data.close()
	
	feature_len = len(x_list[0])
	
	feature_len = len(x_list[0])
	feature_vector, segment, final_activation, final_segment = compute_activation_neural_network(x_list, y_list)
	print ("FEATURE_VECTOR:\n%s\nFINAL_ACTIVATION:%s" % (str(feature_vector), str(final_activation)))
	print ("SEGMENT_VECTOR:\n%s\nFINAL_SEGMENT:%s" % (str(segment), str(final_segment)))
'''	
	while (True):
		
		print("Provide the input values of all features to determine the trend of the params:")
		print("Number of params: %d" % (feature_len))
		
		raw_input_list = []
		for i in range(feature_len):
			print("provide value of param[%d]: " % (i))
			val = raw_input("Value: ");
			val = float(val)
			raw_input_list.append(val)
		
		raw_input_array = np.array(raw_input_list)
		value = get_output_val(feature_vector, segment, final_activation, final_segment, raw_input_array)
		print ("Value for the Operation: %f" % (value))
'''

main()
