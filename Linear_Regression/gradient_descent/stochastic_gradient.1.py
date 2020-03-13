#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict


def derivative_of_cost_function(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0

	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[i])
	
	y = y_list[idy]
	#x = x_list[idx]
	x = 1
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
		grad = float(1 / float(dict_len))
		
		theta_meta_list = []
		for i in range(len(theta_list)):
			theta_meta_list.append(0)

		for idx in range(len(y_list)):
			# This is the change in STOCHASTIC APPROACH where we dont need to pass through all the x_list params
			rand_idx = int(random.random() % len(x_list))
			#for alist in x_list:
			derivative_list[rand_idx] += float(derivative_of_cost_function(x_list[rand_idx], y_list, dict_len, theta_list, rand_idx, idx))
			
			for idy in range(len(theta_list)):
				x = x_list[rand_idx][idy]
				grad_cal = float(derivative_list[idy] * grad * x) 
				temp = float(theta_list[idy] - float(learning * grad_cal))
				#print("Temp Theta[%d]: %f" % (idy, temp))
				theta_meta_list[idy] = temp
		
		
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
