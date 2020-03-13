#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict
import numpy as np

NUM_FEATURE = 2
USER = 4

def derivative_of_cost_function(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[i])
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
		return True
	
	return False


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
		
		#print ("Meta_List: " + str(theta_meta_list))
		#print ("Theta List: " + str(theta_list))

		if (accepted_diff(theta_meta_list, theta_list)):
			#if (theta_meta_list == theta_list):
			break
		else:
			theta_list = theta_meta_list
		

	return theta_list

def get_param_val(theta_list, x_list):
	
	val = 0.0
	for idx in range(len(theta_list)):
		theta = theta_list[idx]
		x = x_list[idx]
		val += float(theta * x)
	
	return val

def main():
	input_dict = defaultdict(list);
	input_data = True
	user_dict = defaultdict(list)
	out_list = []

	with open("content.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			user = 1
			out_list.append(alist[:-2])

			for elem in alist[:(-1) * NUM_FEATURE]:
				temp_list = [1]
				temp_list.extend(alist[(-1) * NUM_FEATURE:])
				temp_list.append(elem)
				user_dict[user].append(temp_list)
				user += 1
	fp.close()
	
	for user in user_dict:
		count = 1
		user_details = user_dict[user]
		x_list = []
		y_list = []
		q_list = []
		m_list = []
		for alist in user_details:
			# X0 X1 X2 .... Xn => Y
			if (alist[-1] != "x"):
				alist = list(map(float, alist))
				x_list.append(alist[:-1])
				y_list.append(alist[-1])

			else:
				q_list.append(list(map(float, alist[:-1])))
				m_list.append(count)
			
			count += 1
		
		theta_list = compute_grad_variable(x_list, y_list)
		for idx in range(len(q_list)):
			val = get_param_val(theta_list, q_list[idx])
			print ("User %d rates %d movie: %f" % (user, m_list[idx], val))
			out_list[m_list[idx] - 1][user - 1] = str(val)
			
	print np.array(out_list)

main()
