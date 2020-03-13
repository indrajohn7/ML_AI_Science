#!/usr/bin/python3

import os
from operator import attrgetter
from operator import itemgetter

Users = [
	{ "id" : 0, "name" : "Indra"},
	{ "id" : 1, "name" : "Indra1"},
	{ "id" : 2, "name" : "Indra2"},
	{ "id" : 3, "name" : "Indra3"},
	{ "id" : 4, "name" : "Indra4"},
	{ "id" : 5, "name" : "Indra5"},
	{ "id" : 6, "name" : "Indra6"},
	{ "id" : 7, "name" : "Indra7"},
	{ "id" : 8, "name" : "Indra8"},
	{ "id" : 9, "name" : "Indra9"},
]

friendships = [ 
	(0, 1),
	(0, 2),
	(1, 2),
	(1, 3),
	(2, 3),
	(3, 4),
	(4, 5),
	(5, 6),
	(5, 7),
	(6, 8),
	(7, 8),
	(8, 9),
]


def add_user_list():
	for user in Users:
		user["friends"] = []
	
	for i, j in friendships:
		Users[i]["friends"].append(Users[j])
		Users[j]["friends"].append(Users[i])

def number_of_friends(user):
	return len(user["friends"])

def total_connections():
	total = 0
	for user in Users:
		total += number_of_friends(user)
	return total

def average_connections():
	num_user = len(Users)
	return (total_connections() / num_user)

def pick_number_of_friends(elem):
	return elem[1]

def sorted_order_list():
	num_freinds_by_id = []
	for user in Users:
		num_freinds_by_id.append((user["id"], number_of_friends(user)))
	
	print(num_freinds_by_id)
	
	sorted(num_freinds_by_id, key = itemgetter(1),  #lambda x : x[1], 
			reverse = True)
	
	print(num_freinds_by_id)

add_user_list()
print(total_connections())
print(average_connections())

sorted_order_list()	
