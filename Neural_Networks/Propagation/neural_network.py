#!/usr/bin/python3

import os
import sys
import random
import math
import numpy
from collections import defaultdict

def get_sigmoid_val(val):
	num = 1
	val = float(val * (-1))
	denom = float(1 + math.exp(val))
	sigmoid_val = float(num/denom)
	return (sigmoid_val)


def derivative_of_cost_function(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[i])
	y = y_list[idy]
	x = x_list[idx]
	sigmoid_func = get_sigmoid_val(func)
	deriv_val = float(float(sigmoid_func - y) * x)
		
	return (deriv_val)

def accepted_diff(alist, blist):
	epsailon = float(0.0001)
	list_len = len(alist)
	count = 0
	for idx in range(len(alist)):
		if (abs(alist[idx] - blist[idx]) < epsailon):
			count += 1
	if count >= (float(0.7 * float(list_len))):
		return True;
	
	return False;



def get_sigmoid_trend_of_input(input_list, theta_list):
	func = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * input_list[i])
	sigmoid_func = get_sigmoid_val(func)
	return sigmoid_func
	
feature_list = []
theta_list = []
activation_unit = []
sigmoid_param = []
delta_list = []
partial_deriv_list = []

def assign_dummy_theta_list(layers, feature_len):
	global theta_list
	global delta_list
	for i in range(layers + 1):
		for j in range(feature_len):
			theta_list[i][j] = numpy.random.uniform(-1, 1, size=(feature_len + 1))			
			delta_list[i][j] = numpy.random.uniform(-1, 1, size=(feature_len + 1))			


def get_layer1_activation_unit(feature_len):
	global activation_unit
	global sigmoid_param
	global feature_list
	activation_unit[0].append(1) # Dummy regularization unit in layer 0
	for i in range (feature_len):
		val = 0
		print feature_list[i]
		temp_theta_list = numpy.random.uniform(-1, 1, size=(len(feature_list[i])))			
		for j in range (len(feature_list[i])):
			val += temp_theta_list[j] * feature_list[i][j] 
		sigmoid_param[0].append(val)
		activation_unit[0].append(get_sigmoid_val(val))

def get_all_activation_unit(layers, feature_len):
	global activation_unit
	global sigmoid_param
	global theta_list
	for l in range(1, layers + 1):
		if (l != layers):
			activation_unit[l].append(1)
		for j in range (feature_len): # Due to dummy node +1 feature_len of previous layer gets increased and starts from index 1.
			val = 0
			for i in range (feature_len + 1): #iterates through previous layer's each value
				val += theta_list[l - 1][j][i] * activation_unit[l - 1][i]
			sigmoid_param[l].append(val)
			activation_unit[l].append(get_sigmoid_val(val))

def get_final_output_class(layers, feature_len, act_unit):
	global sigmoid_param
	for l in range(1, layers + 1):
		if (l != layers):
			act_unit[l].append(1)
		for j in range (feature_len): # Due to dummy node +1 feature_len of previous layer gets increased and starts from index 1.
			val = 0
			for i in range (feature_len ): #iterates through previous layer's each value
				val += theta_list[l - 1][j][i] * act_unit[l - 1][i]
			sigmoid_param[l].append(val)
			act_unit[l].append(get_sigmoid_val(val))
	
	return act_unit

def get_partial_deriv_list(layers, feature_len, y_class):
	global theta_list
	global partial_deriv_list
	y_len = len(y_class)
	print y_len
	for l in range(layers , -1, -1):
		print partial_deriv_list
		print l
		for i in range(1, feature_len + 1):
			if (l == layers):
				if (i - 1 < y_len):
					partial_deriv_list[l].append(y_class[i - 1] - activation_unit[l][i - 1])
				else:
					partial_deriv_list[l].append(0)
			else:
				val = 0
				for j in range(1, feature_len + 1):
					if (j < len(theta_list[l]) and j < len(partial_deriv_list[l + 1])):
						val += theta_list[l][j][i] * partial_deriv_list[l + 1][j]
				partial_deriv_list[l].append(val)
		print partial_deriv_list

def get_backward_propagation(layers, feature_len):
	global partial_deriv_list
	global theta_list
	global delta_list
	threshold_layer = 0

	while True:
		if (threshold_layer >= ((layers - 1) * feature_len)):
			break
		threshold_layer = 0
		for l in range(layers):
			for i in range(feature_len):
				temp_theta_list = theta_list[l][i]
				for j in range(feature_len):
					if ((i + 1) < len(activation_unit[l]) and i < partial_deriv_list[l + 1]):
						diff = activation_unit[l][i + 1] * partial_deriv_list[l + 1][i] # activation_unit [l] [i  + 1] because of dummy units and a[0] model
						delta_list[l][i][j] += diff
						theta_list[l][i][j] -= delta_list[l][i][j] 
				if (accepted_diff(temp_theta_list, theta_list[l][i])):
					threshold_layer += 1

def main():
	global feature_list
	global theta_list
	global activation_unit
	global sigmoid_param
	global delta_list
	global partial_deriv_list

	input_dict = defaultdict(list);
	x_list = []
	xlist = []
	y_list = []
	y_class = set()
	input_data = True
	threshold = float(0.5)
	with open("multi_grad.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			y = alist.pop()
			xlist.append(alist)
			y_list.append(y)
			y_class.add(y)
	
	feature_len = len(xlist[0])
	layers = feature_len - 1
	feature_list = [[] for i in range(feature_len)]
	theta_list = [[[] for j in range(feature_len)] for i in range (layers + 1)]
	activation_unit = [[] for i in range (layers + 1)]
	sigmoid_param = [[] for i in range(layers + 1)]
	delta_list = [[[] for j in range(feature_len)] for i in range (layers + 1)]
	partial_deriv_list = [[] for i in range(layers + 1)]
	
	for alist in xlist:
		alist = list(map(int,alist))
		blist = [1]
		blist.extend(alist)
		x_list.append(blist)
		for i in range(feature_len):
			feature_list[i].append(alist[i])
	
	y_class = list(map(float, y_class))
	
	print feature_list
	print theta_list
	print activation_unit
	print sigmoid_param
	
	#***************************************************             FORWARD PROPAGATION START            *********************************************************#
	assign_dummy_theta_list(layers, feature_len)
	print theta_list
	#	Get the layer 1 activation unit
	#	Since layer 1 takes a list of data set and gets the activation_unit value hence compute that first. And thats always 1 time effort.

	get_layer1_activation_unit(feature_len)
	print activation_unit
	
	get_all_activation_unit(layers, feature_len)
	print activation_unit
	#***************************************************             FORWARD PROPAGATION  END            *********************************************************#
	
	#***************************************************             BACKWARD PROPAGATION START            *********************************************************#
	y_class = sorted(y_class)
	get_partial_deriv_list(layers, feature_len, y_class)
	print partial_deriv_list
	
	get_backward_propagation(layers, feature_len)
	print theta_list
	print delta_list
	#***************************************************             BACKWARD PROPAGATION END            *********************************************************#
	
	#***************************************************             USER INPUT START            *********************************************************#
	while (1):
		print "Press 1 to exit:"
		choice = raw_input("choice: ");
		if (choice == 1):
			break
		act_unit = [[] for i in range(layers + 1)]
		print ("There are %d features present in the model" % feature_len)
		for i in range(feature_len):
			print ("param[%d]: " % (i + 1))
			val = raw_input("val: ");
			val = float(val)
			act_unit[0].append(val)
		act_unit = get_final_output_class(layers, feature_len, act_unit)
		print ("****************** RESULT *****************************")
		for l in range(layers + 1):
			print act_unit[l]
	#***************************************************             USER INPUT END            *********************************************************#

	fp.close()
				

main()
