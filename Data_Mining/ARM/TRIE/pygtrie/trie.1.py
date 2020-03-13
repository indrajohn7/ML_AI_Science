import pygtrie as trie


def add_items(tr, key, val):
	tr[key] = val
	return tr

def search_items(tr, key):
	
	print ("	**************	HasNode chech	******************		")
	print (str(tr.has_node(key)))
	
	print ("	**************	HasKey chech	******************		")
	print (str(tr.has_key(key)))

	print ("	**************	HasSubTrie chech	******************		")
	print (str(tr.has_subtrie(key)))

def del_items(tr, key):
	
	print ("Delete Operation %s key from the Trie: " % (key))
	if (tr.has_key(key) or tr.has_subtrie(key)):
		del tr[key:]
	elif (tr.has_node(key)):
		print ("key %s is a slice in the Trie, hence can't be deleted" % key)
	else:
		print ("Key %s is not present in the Trie." % key)

def print_items(tr):
	print tr.items()

def prefix_search(tr, key):
	
	if (tr.has_node(key)):
		print(tr.items(prefix = key))
	else:
		print ("Node %s does not present in the Trie." % key)


def iter_items(tr):
	
	print ("	*******************		Printing Keys	*************	")
	print(tr.iterkeys())

	print ("	*******************		Printing Values	*************	")
	print(tr.itervalues())

def prefix(tr, key):
	
	if (not tr.has_node(key)):
		print ("Node %s does not present in the Trie." % key)
	
	print ("	******************** Prefix *************************	")
	print (tr.items(prefix = key))

	print ("	******************** Longest Prefix *************************	")
	print(tr.longest_prefix(key))

	print ("	******************** Shortest Prefix *************************	")
	print(tr.shortest_prefix(key))

	print ("	******************** All Prefix *************************	")
	print(list(tr.prefixes(key)))


if __name__ == '__main__':
	tr = trie.StringTrie()
	try:
		while(True):
			print ("1. Enter 1 for Add()\n\
					2. Enter 2 for Update()\n\
					3. Enter 3 for Search()\n\
					4. Enetr 4 for Delete()\n\
					5. Enter 5 for print()\n\
					6. Enter 6 for iterate on trie()\n\
					7. Enter 7 for Prefix Search()\n\
					8. Enter 99 for Terminate the Process\n")
			ch = raw_input("Enter your Choice: ")
			print ch
			if (ch == "99"):
				break
			if (ch == "1"):
				ch_key = raw_input("Enter Key to be Added: ")
				print ch_key
				ch_val = raw_input("Enter val to be Added: ")
				tr = add_items(tr, ch_key, ch_val)
	
			if (ch == "3"):
				ch_search = raw_input("Enter element to be Searched: ")
				print ch_search
				search_items(tr, ch_search)
	
			if (ch == "4"):
				ch_del = raw_input("Enter element to be Deleted: ")
				print ch_del
				tr = del_items(tr, ch_del)
	
			if (ch == "5"):
				print_items(tr)
	
			if (ch == "6"):
				iter_items(tr)
			
			if (ch == "7"):
				ch_key = raw_input("Enter element to be Searched: ")
				print ch_key
				prefix(tr, ch_key)
	
	except Exception as e:
		
		print ("Exception caught as %s" % str(e))
		exit(1)

