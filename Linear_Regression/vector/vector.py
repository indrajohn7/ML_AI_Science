#!/usr/bin/python3

import os
import sys
import gradient_descent
import random
from collections import defaultdict


vector_list = gradient_descent.theta

def compute_vector(matrix_list, vector_list):
	
	alist = []
	for row in range(len(matrix_list)):
		temp = 0
		for col in range(len(matrix_list[row])):
			temp += float(matrix_list[row][col] * vector_list[col])
		alist.append(temp)
	return alist

def main():
	with open ("data.txt", 'r') as fp:
		for line in fp:
			line = line.rstrip('\n')
			x_list = [i for i in line.split(' ')]
			x_list = list(map(int, x_list))
	
	matrix_list = []
	for idx in range(len(x_list)):
		alist = [1, x_list[idx]]
		matrix_list.append(alist)
	
	print(matrix_list)
	
	#vector_list = [segment, slope]
	print(vector_list)
	final_list = compute_vector(matrix_list, vector_list)

	print("X_VAL	Y_VAL")
	for idx in range(len(final_list)):
		print("%f	%f" % (matrix_list[idx][1], final_list[idx]))
		

main()
