#!/usr/bin/python3

import os
import sys
import random
from collections import defaultdict


def derivative_of_cost_function(x, y, dict_len, slope, segment):
	func = float(segment + float(slope * x))
	segment_val = float(func - y)
	slope_val = (float(func - y) * x)
	
	print ("Segment Val: %f :: Slope Val: %f" % (segment_val, slope_val))
	return (segment_val, slope_val)


def compute_grad_variable(adict):
	slope = float(0)
	segment = float(0)
	learning = float(0.001)
	
	dict_len = len(adict)
	print(adict)
	print(dict_len)
	seg_grad = slope_grad = float(0)
	while (True):
		for key in adict:
			x = key
			alist = adict[key]
			for idx in range(len(alist)):
				y = alist[idx]
				(seg_val, slope_val) = derivative_of_cost_function(x, y, dict_len, slope, segment)
				seg_grad += seg_val
				slope_grad += slope_val

		grad = float(1 / float(dict_len))
		print(grad)
		seg_grad = float(seg_grad * grad)
		slope_grad = float(slope_grad * grad)
		print ("GRAD Segment: %f :: Slope: %f" % (seg_grad, slope_grad))
		temp_seg = float(segment - float(learning * seg_grad))
		temp_slope = float(slope - float(learning * slope_grad))
		print ("TEMP Segment: %f :: Slope: %f" % (temp_seg, temp_slope))
		print ("Segment: %f :: Slope: %f" % (segment, slope))

		if (segment == temp_seg and slope == temp_slope):
			break
		else:
			segment = temp_seg
			slope = temp_slope
		print ("Segment: %f :: Slope: %f" % (segment, slope))
	
	return(segment, slope)

theta = []

def main():
	input_dict = defaultdict(list);
	x_list = []
	y_list = []
	input_data = True
	with open("grad.txt", 'r') as fp:
		for line in fp:
			if (input_data):
				line = line.rstrip('\n')
				x_list = [i for i in line.split(' ')]
				input_data = False
			else:
				line = line.rstrip('\n')
				y_list = [i for i in line.split(' ')]
				input_data = True

	x_list = list(map(int, x_list))
	y_list = list(map(int, y_list))

	if (len(x_list) != len(y_list)):
		print("Syncing error in input and output data X : Y")
	else:
		for a, b in zip(x_list, y_list):
			input_dict[a].append(b)

	segment, slope = compute_grad_variable(input_dict)
	theta_segment = segment
	theta_slope = slope
	theta.append(theta_segment)
	theta.append(theta_slope)

	print("$1: %f :: $2: %f" % (segment, slope))
	print("$1: %f :: $2: %f" % (theta_segment, theta_slope))
	input_dict.clear()

	fp.close()
				

main()
