#!/usr/bin/python3

import os
import math
from operator import itemgetter, attrgetter

class movies:
	def __init__(self, title, kicks, kisses, category, distance = []):
		self.title = title
		self.kicks = kicks
		self.kisses = kisses
		self.category = category
		self.distance = distance

	def display_movie(self):
		print("Title: %s :: Kicks: %s :: Kisses: %s :: Category:%s" % (self.title, self.kicks, self.kisses, self.category))

def get_euclidian_distance(movies, todo):
	distance = math.sqrt((abs(todo.kicks - movies.kicks)**2)+(abs(todo.kisses - movies.kisses)**2))
	return distance

def predict_category_of_movie(movies_list, todo_list, num):
	for i in range(len(todo_list)):
		for j in range(len(movies_list)):
			todo_list[i].distance.append((get_euclidian_distance(movies_list[j], todo_list[i]), j))  #<< Indra look here
		print("Title: %s :: Kicks: %s :: Kisses: %s :: Category:%s Distance:" % (todo_list[i].title, todo_list[i].kicks, todo_list[i].kisses, todo_list[i].category))
		todo_list[i].distance = sorted(todo_list[i].distance, key = itemgetter(0))
		print(todo_list[i].distance)
		#todo_list[i].distance = sorted(todo_list[i].distance, key=lambda todo_list[i].distance: todo_list[i].distance[0])
		k = 0
		nearest_neighbours = {}
		for p in range(num):
			print(p, k)
			print(movies_list[todo_list[i].distance[p + k][1]].category)
			category = movies_list[todo_list[i].distance[p + k][1]].category
			if (movies_list[todo_list[i].distance[p + k][1]].category != "?"):
				print("true")
				if category in nearest_neighbours:
					nearest_neighbours[category] += 1
				else:
					nearest_neighbours[category] = 1
			else:
				print(p, k)
				p -= 1
				k += 1
		print(nearest_neighbours)
		nearest_neighbours = sorted(nearest_neighbours.items(), key = itemgetter(1), reverse = True)
		todo_list[i].category, counts = nearest_neighbours[0]

	return todo_list

def __main__():
	movies_list = []
	todo_movies_list = []
	with open('data.txt', 'r') as data:
		for line in data:
			line = line.strip('\n')
			title, kicks, kisses, category = line.split(' ')
			movies_list.append(movies(title, int(kicks), int(kisses), category))
	for i in range(len(movies_list)):
		movies_list[i].display_movie()
		if movies_list[i].category == "?":
			todo_movies_list.append(movies_list[i])	
	str1 = input("Provide numbers of nearest Neighbours check: ")
	str1 = int(str1)
	res = predict_category_of_movie(movies_list, todo_movies_list, str1)
	print("Predicted list:")
	for obj in res:
		print("Title: %s :: category:%s" % (obj.title,obj.category))
	return

__main__()
