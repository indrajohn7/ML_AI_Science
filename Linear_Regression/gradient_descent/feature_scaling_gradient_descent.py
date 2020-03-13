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
	x = x_list[idx]
	deriv_val = float(float(func - y) * x)
	
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
		
		if count < 200:
			print(derivative_list)
		grad = float(1 / float(dict_len))
		#print(grad)
		
		theta_meta_list = []
		for i in range(len(theta_list)):
			theta_meta_list.append(0)

		for idx in range(len(theta_list)):
			grad_cal = float(derivative_list[idx] * grad)
			temp = float(theta_list[idx] - float(learning * grad_cal))
			if count < 200:
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

def main():
	input_dict = defaultdict(list);
	x_list = []
	xlist = []
	y_list = []
	input_data = True
	with open("multi_grad.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			alist = [i for i in line.split(' ')]
			y = alist.pop()
			xlist.append(alist)
			y_list.append(y)

	feature_scale_dict = defaultdict(list)

	for i in range(len(xlist)):
		xlist[i] = list(map(int,xlist[i]))
		for j in range(len(xlist[i])):
			if j in feature_scale_dict:
				mean = (float(i * (feature_scale_dict[j][0])) + xlist[i][j]) / float(i + 1)
				feature_scale_dict[j][0] = mean
				if (xlist[i][j] < feature_scale_dict[j][1]): #min
					feature_scale_dict[j][1] = float(xlist[i][j])
				elif (xlist[i][j] > feature_scale_dict[j][2]): #max
					feature_scale_dict[j][2] = float(xlist[i][j])
			else:
				blist = []
				mean = float(xlist[i][j])
				blist.append(mean)
				mini = maxi = float(xlist[i][j])
				blist.append(mini)
				blist.append(maxi)
				feature_scale_dict[j] = blist
	
	print(feature_scale_dict)

	for alist in xlist:
		alist = list(map(int,alist))
		blist = [1]
		for i in range(len(alist)):
			alist[i] = float(abs(alist[i] - feature_scale_dict[i][0])) / float(abs(feature_scale_dict[i][2] - feature_scale_dict[i][1]) + 1)
			blist.append(alist[i])
		x_list.append(blist)
	
	print(x_list)	
	
	sys.exit()
	
	y_list = list(map(int, y_list))

	theta_list = compute_grad_variable(x_list, y_list)
	
	print("multivariant param")
	print(theta_list)

	fp.close()
				

main()
