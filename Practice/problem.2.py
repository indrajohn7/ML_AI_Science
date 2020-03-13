#!/usr/bin/python3

import os
import problem_1

from problem_1 import Users
from problem_1 import friendships


def create_list_of_mutual_friends():
	mutual_friends = []
	for user in Users:
		idx = user["id"]
		dicto = dict()
		dicto["name"] = user["name"]
		dicto["friends"] = set()
		#for friend in range(idx, len(friendships), 1):
		for friend in friendships:
			if friend[0] > idx:
				break
			elif (friend[0] == idx) and not friend[1] in dicto["friends"]:
				dicto["friends"].add(Users[friend[1]]["name"])
			elif (friend[1] == idx) and not friend[0] in dicto["friends"]:
				dicto["friends"].add(Users[friend[0]]["name"])

		mutual_friends.append(dicto)
	print(mutual_friends)
	print("\n")

create_list_of_mutual_friends()
		
