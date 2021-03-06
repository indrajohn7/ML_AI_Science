#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict

PARAMS = 2

def derivative_of_cost_function(x_list, y_list, movie_len, user_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0.0
	
	for i in range(movie_len):
		for j in range(PARAMS):
			func += float(theta_list[idx][idy] * x_list[i][j])
			y = y_list[i][idx]
			if (y != "x"):
				y = float(y)
				x = x_list[i][j]
				deriv_val += (float(float(func - y) * x))

	return (deriv_val)

def derivative_of_feature_param(x_list, y_list, movie_len, user_len, theta_list, idx, idy):
	func = 0
	deriv_val = 0
	
	for i in range(user_len):
		for j in range(PARAMS):
			func += float(theta_list[i][j] * x_list[idx][idy])
			y = y_list[idx][i]
			if (y != "x"):
				y = float(y)
				theta = theta_list[i][j]
				deriv_val += (float(float(func - y) * theta))
	
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


def get_feature_learning_param(x_list, y_list, movie_len, user_len, theta_list):
	
	#print ("Inside get_feature_learning_param")
	learning = float(0.0001)
	derivative_list = []
	for i in range(movie_len):
		alist = []
		for j in range(PARAMS):
			alist.append(0.01)
		
		derivative_list.append(alist)
	
	for idx in range(movie_len):
		for idy in range(PARAMS):
			derivative_list[idx][idy] += float(derivative_of_feature_param(x_list, y_list, movie_len, user_len, theta_list, idx, idy))
		
	grad = float(1 / float(movie_len))
	
	x_meta_list = []
	for i in range(len(x_list)):
		alist = []
		x_meta_list.append(alist)
	
	for idx in range(movie_len):
		for idy in range(PARAMS):
			grad_cal = float(derivative_list[idx][idy] * grad)
			temp = float(x_list[idx][idy] - float(learning * grad_cal))
			x_meta_list[idx].append(temp)
	
	return x_meta_list

def get_feature_learning_quotient(x_list, y_list, movie_len, user_len, theta_list):

	#print ("Inside get_feature_learning_quotient")
	learning = float(0.0001)
	derivative_list = []
	for i in range(user_len):
		alist = []
		for j in range(PARAMS):
			alist.append(0.01)

		derivative_list.append(alist)
		
	for idx in range(user_len):
		for idy in range(PARAMS):
			derivative_list[idx][idy] += float(derivative_of_cost_function(x_list, y_list, movie_len, user_len, theta_list, idx, idy))
	
	grad = float(1 / float(movie_len))
	
	theta_meta_list = []
	for i in range(len(theta_list)):
		alist = []
		theta_meta_list.append(alist)

	for idx in range(len(theta_list)):
		for idy in range(len(theta_list[idx])):
			grad_cal = float(derivative_list[idx][idy] * grad)
			temp = float(theta_list[idx][idy] - float(learning * grad_cal))
			theta_meta_list[idx].append(temp)
	
	return theta_meta_list

def compute_grad_variable(y_list):
	
	#print ("Inside compute_grad_variable")
	learning = float(0.0001)
	movie_len = len(y_list)
	user_len = len(y_list[0])
	theta_list = []

	for i in range(user_len):
		alist = []
		for j in range(PARAMS):
			alist.append(random.random())
		theta_list.append(alist)

	x_list = []

	for i in range(movie_len):
		alist = []
		for j in range(PARAMS):
			alist.append(random.random())
		x_list.append(alist)


	print ("MOVIE_LEN: %d :: USER_LEN: %d" % (movie_len, user_len))
	print (x_list)
	print (y_list)
	print (theta_list)
	
	theta_break = False
	x_break = False
	
	while (True):
		
		if (theta_break != True):
			theta_meta_list = get_feature_learning_quotient(x_list, y_list, movie_len, user_len, theta_list)

			theta_count = 0
			for idx in range(user_len):
				if (accepted_diff(theta_meta_list[idx], theta_list[idx])):
					theta_count += 1
				theta_list = theta_meta_list
			
			if (theta_count == user_len):
				theta_break = True
		
		if (x_break != True):
			x_meta_list = get_feature_learning_param(x_list, y_list, movie_len, user_len, theta_list)
			
			feature_count = 0
			for idx in range(movie_len):
				if (accepted_diff(x_meta_list[idx], x_list[idx])):
					feature_count += 1
				x_list[idx] = x_meta_list[idx]

			if (feature_count == movie_len):
				x_break = True

		#print ("Theta_Meta_List: " + str(theta_meta_list))
		#print ("Theta List: " + str(theta_list))
		#print ("X_List: " + str(x_list))
		#print ("X_META List: " + str(x_meta_list))
		
		if (theta_break and x_break):
			break

	return x_list, theta_list

def get_param_val(theta_list, x_list):
	
	val = 0.0
	
	for idx in range(len(x_list)):
		theta = theta_list[idx]
		x = x_list[idx]
		#print ("theta: %f X: %f" % (theta, x))
		val += float(theta * x)
		
	print ("Val: %f" % val)
	
	return val

def main():
	input_dict = defaultdict(list);
	input_data = True
	user_dict = defaultdict(list)
	
	out_list = []
	with open("feature_learning.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			out_list.append(alist)
	fp.close()
	
	print ("OUT_LIST: %s" % (str(out_list)))

	x_list, theta_list = compute_grad_variable(out_list)

	for movie_idx in range(len(out_list)):
		for user_idx in range(len(out_list[movie_idx])):
			if (out_list[movie_idx][user_idx] == "x"):
				val = get_param_val(theta_list[user_idx], x_list[movie_idx])
				print ("User %d has rated for %d Movie: %f\n" %(user_idx, movie_idx, val))
				out_list[movie_idx][user_idx] = str(val)
	
	print ("****************	FINAL RATING LIST	************************")
	print out_list

main()
