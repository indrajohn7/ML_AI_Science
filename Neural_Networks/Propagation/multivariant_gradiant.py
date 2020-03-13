#!/usr/bin/python3

import os
import sys
import random
import math
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
	epsailon = float(0.001)
	list_len = len(alist)
	count = 0
	for idx in range(len(alist)):
		if (abs(alist[idx] - blist[idx]) < epsailon):
			count += 1
	if count >= (float(0.7 * float(list_len))):
		return True;
	
	return False;


def compute_grad_variable(x_list, y_list):
	learning = float(0.0001)
	dict_len = len(y_list)
	theta_list = []
	for i in range(len(x_list[0])):
		theta_list.append(0.2)
	
	print(x_list)
	print(y_list)
	print(dict_len)
	count = 0
	seg_grad = slope_grad = float(0)
	'''
	derivative_list = []
	for i in range(len(theta_list)):
		derivative_list.append(0.01)
	'''
	while (True):
		
		derivative_list = []
		for i in range(len(theta_list)):
			derivative_list.append(0.01)
		for idx in range(len(theta_list)):
			idy = 0
			for alist in x_list:
				derivative_list[idx] += float(derivative_of_cost_function(alist, y_list, dict_len, theta_list, idx, idy))
				idy += 1
		
		grad = float(1 / float(dict_len))
		#print(grad)
		
		theta_meta_list = []
		for i in range(len(theta_list)):
			theta_meta_list.append(0)

		for idx in range(len(theta_list)):
			grad_cal = float(derivative_list[idx] * grad)
			temp = float(theta_list[idx] - float(learning * grad_cal))
			print("Temp Theta[%d]: %f" % (idx, temp))
			theta_meta_list[idx] = temp
		
		if (accepted_diff(theta_meta_list, theta_list)):
			break
		else:
			theta_list = theta_meta_list
		
		print(theta_list)

	return(theta_list)

theta_segment = 0
theta_slope = 0

def get_sigmoid_trend_of_input(input_list, theta_list):
	func = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * input_list[i])
	sigmoid_func = get_sigmoid_val(func)
	return sigmoid_func
	
def main():
	input_dict = defaultdict(list);
	x_list = []
	xlist = []
	y_list = []
	input_data = True
	threshold = float(0.5)
	with open("multi_grad.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			y = alist.pop()
			xlist.append(alist)
			y_list.append(y)
	
	feature_len = len(xlist[0])

	for alist in xlist:
		alist = list(map(int,alist))
		blist = [1]
		for elem in alist:
			blist.append(elem)
		x_list.append(blist)
	
	y_list = list(map(int, y_list))

	theta_list = compute_grad_variable(x_list, y_list)
	
	print("multivariant param")
	print(theta_list)
	
	while(True):
		print("Provide the input values of all features to determine the trend of the params:")
		print("Number of params: %d" % (feature_len))
		raw_input_list = []
		for i in range(feature_len):
			print("provide value of param[%d]: " % (i))
			val = raw_input("Value: ");
			val = float(val)
			raw_input_list.append(val)
		
		print("Threshold: %f" % (threshold))	
		input_list = [1]
		input_list.extend(raw_input_list)
		res = get_sigmoid_trend_of_input(input_list, theta_list)
		if (res < float(threshold)):
			print("The node value of sigmoid curvature for the input: %f and nature is negative." % (res))
		else:
			print("The node value of sigmoid curvature for the input: %f and nature is positive." % (res))

	fp.close()
				

main()
