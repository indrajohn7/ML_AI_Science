#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict

PARAMS = 2

def derivative_of_cost_function(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[i])
	y = y_list[idy]
	x = x_list[idx]
	deriv_val = float(float(func - y) * x)
	
	return (deriv_val)

def derivative_of_feature_param(x_list, y_list, dict_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	for i in range(len(theta_list)):
		func += float(theta_list[i] * x_list[i])
	y = y_list[idy]
	theta = theta_list[idx]
	deriv_val = float(float(func - y) * theta)
	
	return (deriv_val)

def accepted_diff(alist, blist):
	epsailon = float(0.000001)
	list_len = len(alist)
	count = 0
	for idx in range(len(alist)):
		if (abs(alist[idx] - blist[idx]) < epsailon):
			count += 1
	if count >= (float(0.9 * float(list_len))):
		return True
	
	return False


def get_feature_learning_param(x_list, y_list, dict_len, theta_list):
	
	learning = float(0.0001)
	derivative_list = []
	for i in range(len(theta_list)):
		derivative_list.append(0.01)
	
	for idx in range(len(theta_list)):
		idy = 0
		for alist in x_list:
			derivative_list[idx] += float(derivative_of_feature_param(alist, y_list, dict_len, theta_list, idx, idy))
			idy += 1
	
	grad = float(1 / float(dict_len))
	#print(grad)
	
	x_meta_list = []
	for i in range(len(x_list)):
		alist = []
		x_meta_list.append(alist)
	
	for idx in range(len(x_list)):
		for idy in range(len(x_list[0])):
			grad_cal = float(derivative_list[idy] * grad)
			temp = float(x_list[idx][idy] - float(learning * grad_cal))
			x_meta_list[idx].append(temp)
	
	return x_meta_list


def compute_grad_variable(y_list):
	learning = float(0.0001)
	dict_len = len(y_list)
	theta_list = []

	x_list = []
	for idx in range(len(y_list)):
		alist = []
		for idy in range(PARAMS):
			alist.append(random.random())
		x_list.append(alist)

	for i in range(len(x_list[0])):
		theta_list.append(random.random())
	
	print (x_list)
	print (y_list)
	print (dict_len)
	print (theta_list)
	
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
		

		theta_break = False
		if (accepted_diff(theta_meta_list, theta_list)):
			theta_break = True
		else:
			theta_list = theta_meta_list
		
		x_meta_list = get_feature_learning_param(x_list, y_list, dict_len, theta_list)
		
		feature_count = 0
		x_break = False
		for idx in range(dict_len):
			if (accepted_diff(x_meta_list[idx], x_list[idx])):
				feature_count += 1
			x_list[idx] = x_meta_list[idx]

		if (feature_count == dict_len):
			x_break = True

		#print ("Meta_List: " + str(theta_meta_list))
		#print ("Theta List: " + str(theta_list))
		#print ("X_List: " + str(x_list))
		#print ("X_META List: " + str(x_meta_list))
		
		if (theta_break and x_break):
			break

	return x_list, theta_list

def get_param_val(theta_list, x_list):
	
	val_list = []
	for idx in range(len(x_list)):
		val = 0.0
		for idy in range(len(x_list[idx])):
			theta = theta_list[idy]
			x = x_list[idx][idy]
			#print ("theta: %f X: %f" % (theta, x))
			val += float(theta * x)
		
		print ("Val: %f" % val)
		val_list.append(val)
	
	return val_list

def main():
	input_dict = defaultdict(list);
	input_data = True
	user_dict = defaultdict(list)

	with open("feature_learning.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			count = 1
			for elem in alist:
				temp_list = []
				temp_list.append(elem)
				user_dict[count].append(temp_list)
				count += 1
	fp.close()
	
	
	for user in user_dict:
		count = 1
		user_details = user_dict[user]
		y_list = []
		q_list = []
		m_list = []
		
		for alist in user_details:
			# X0 X1 X2 .... Xn => Y
			if (alist[-1] != "x"):
				alist = list(map(float, alist))
				y_list.append(alist[-1])

			else:
				q_list.append(list(map(float, alist[:-1])))
				m_list.append(count)
				#y_list.append(0)
			
			count += 1
		
		x_list, theta_list = compute_grad_variable(y_list)
		print ("X_LIST: %s" % str(x_list))
		print ("THETA_LIST: %s" % str(theta_list))
		print ("Y_LIST: %s" % str(y_list))
		print ("Q_LIST: %s" % str(q_list))
		
		for idx in range(len(q_list)):
			val = get_param_val(theta_list, x_list)
			print ("User %d rates %d movie: %s" % (user, m_list[idx], str(val)))
				
main()
