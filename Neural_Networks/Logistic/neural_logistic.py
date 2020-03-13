#!/usr/bin/python

import os
import sys
import numpy as np
import random
import math
from collections import defaultdict

read_file = "multi_grad.txt"
THRESHOLD_DIFF = 0.8
DEFAULT_COST = -999999.99

def get_vector_mat(x_list, theta_list):
	
	res = 0.0
	for i in range(len(x_list)):
		res += float(x_list[i] * theta_list[i])
	
	return res

def get_sigmoid_val(val):
	
	print ("get_sigmoid_val(%f)" % (val))
	denom = float(1 + math.exp(-val))
	sigmoid_val = float(1 / denom)

	return sigmoid_val

def get_sigmoid2_val(val):
	
	print ("get_sigmoid2_val(%f)" % (val))
	num = float(math.exp(val) - math.exp(val * (-1)))
	denom = float(math.exp(val) + math.exp(val * (-1)))
	sigmoid_val = float(num / denom)

	return sigmoid_val

def get_output_val(theta_list, segment, x_list):
	
	val = 0.0
	for i in range(len(x_list)):
		val += float(theta_list[i] * x_list[i])
	val += segment

	return get_sigmoid_val(val)

def accepted_val_diff(a, b):

	epsailon = float(0.00001)
	if (abs(a - b) < epsailon):
		return True
	
	return False

def accepted_list_diff(alist, blist):
	
	list_len = len(alist)
	count = 0.0
	for i in range(len(alist)):
		if (accepted_val_diff(alist[i], blist[i])):
			count += 1
	
	if (count >= float(THRESHOLD_DIFF * float(list_len))):
		return True
	
	return False
		

def compute_logistic_neural_network(x_list, y_list):
	
	learning = float(0.0001)
	num = len(y_list)
	feature_len = len(x_list[0])
	
	theta_list = []
	derivative_list = []
	theta_meta_list = []

	for i in range(len(x_list[0])):
		theta_list.append(random.random() * 0.01)
		theta_meta_list.append(random.random())
		#derivative_list.append(random.random())
		#theta_list.append(0.2)
		#theta_meta_list.append(0)
		derivative_list.append(0.0)
	
	segment = random.random() * 0.01
	meta_segment = random.random()
	meta_cost_val = cost_val = DEFAULT_COST
	iter = 0

	while (True):
		derivative_list = [(i * 0) for i in derivative_list]
		dzi = dbi = cost_val = 0.0
		for i in range(num):
			zi = float(get_vector_mat(x_list[i], theta_list) + segment)
			y_cap = get_sigmoid_val(zi)
			print ("Y_CAP: %f" % (y_cap))
			#if (iter != 0):
			cost_val += (-1) * (float(float(y_list[i] * math.log(y_cap)) + float((1 - y_list[i]) * math.log(1 - y_cap))) / num)
			print ("COST_VAL: %f" % (cost_val))
			dzi = float((y_cap - y_list[i])) # In course in 2 places 2 forlulae is provided, this formula is not working.
			for j in range(feature_len):
				derivative_list[j] += float(x_list[i][j] * dzi)
			dbi += float(dzi)
		
		dbi /= num
		for i in range(feature_len):
			derivative_list[i] /= num
			theta_list[i] -= float(learning * derivative_list[i])
		segment -= float(learning * dbi)

		if ((accepted_list_diff(theta_list, theta_meta_list) and accepted_val_diff(segment, meta_segment))): #or
			#((iter != 0) and cost_val > meta_cost_val)):
			
			break
		else:
			theta_meta_list = theta_list
			meta_segment = segment
			meta_cost_val = cost_val
		
		print ("DERIVATIVE LIST: %s" % (str(derivative_list)))
		print ("THETA LIST: %s" % (str(theta_list)))
		print ("SEGMENT: %f" % (segment))
		print ("ITER: %d" % (iter))
		iter += 1
	
	return theta_list, segment

def main():
	x_list = []
	y_list = []

	with open (read_file, 'r') as data:
		for line in data:
			line = line.rstrip('\n')
			line = line.split(' ')
			line = list(map(float, line))
			x_list.append(line[:-1])
			y_list.append(line[-1])
	data.close()
	
	feature_len = len(x_list[0])
	feature_vector, segment = compute_logistic_neural_network(x_list, y_list)
	
	while (1):
		
		print("Provide the input values of all features to determine the trend of the params:")
		print("Number of params: %d" % (feature_len))
		
		raw_input_list = []
		for i in range(feature_len):
			print("provide value of param[%d]: " % (i))
			val = raw_input("Value: ");
			val = float(val)
			raw_input_list.append(val)

		value = get_output_val(feature_vector, segment, raw_input_list)
		print ("Value for the Operation: %f" % (value))

main()
