#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict


def derivative_of_cost_function(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	rand_idx = int(random.random() % len(theta_list))
	
	# This the change in STOCHASTIC APPROACH, where we shall not pass through all the dataset to compute the derivative.

	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[rand_idx])
	
	y = y_list[idy]
	x = x_list[idx]
	deriv_val = float(float(func - y) * x)
	
	return (deriv_val)

def accepted_diff(alist, blist):
	epsailon = float(0.00001)
	list_len = len(alist)
	count = 0
	for idx in range(len(alist)):
		if (abs(alist[idx] - blist[idx]) < epsailon):
			count += 1
	if count >= (float(0.9 * float(list_len))):
		return True;
	
	return False;


def compute_grad_variable(x_list, y_list):
	learning = float(0.0001)
	dict_len = len(y_list)
	theta_list = []
	for i in range(len(x_list[0])):
		theta_list.append(random.random())
	
	print(x_list)
	print(y_list)
	print(dict_len)
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
			theta_meta_list[idx] = temp
		
		print ("Meta_List: " + str(theta_meta_list))
		print ("Theta List: " + str(theta_list))

		if (accepted_diff(theta_meta_list, theta_list)):
			#if (theta_meta_list == theta_list):
			break
		else:
			theta_list = theta_meta_list
		

	return theta_list

theta_segment = 0
theta_slope = 0

def main():
	input_dict = defaultdict(list);
	x_list = []
	xlist = []
	y_list = []
	with open("multi_grad.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			y = alist.pop()
			xlist.append(alist)
			y_list.append(y)
	
	for alist in xlist:
		alist = list(map(int,alist))
		blist = [1]
		blist.extend(alist)
		x_list.append(blist)
	
	y_list = list(map(int, y_list))
	#random.shuffle(y_list)

	theta_list = compute_grad_variable(x_list, y_list)
	
	print("multivariant param")
	print(theta_list)

	fp.close()
				

main()
