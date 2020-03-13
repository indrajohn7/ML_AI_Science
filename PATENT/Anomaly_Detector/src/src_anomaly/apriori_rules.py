import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori

GAUSSIAN_THRESHOLD = 0.000001

def create_association_rules(gaussian_list, dim_list):
    
    records = []

    for idx in range(len(gaussian_list)):
        if (gaussian_list[idx] <= GAUSSIAN_THRESHOLD):
            records.append(dim_list[idx])
    
    print ("Len of Gaussian List: %d" % len(records))
    
    #This is a test conversion and needs to be changed
    records = records[:1000]
    print ("Len of Records List: %d" % len(records))
    print records

    association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)

    print ("*****************  Association RULES ***********************")
    print (len(association_results))
    print (association_results) 

    for item in association_results:

        # first index of the inner list
        # Contains base item and add item
        #print ("ITEM: %s" % (str(item)))
        pair = item[0]
        items = [x for x in pair]
        print ("**************************    Rule    ************************")
        print items
        #print("Rule: " + items[0] + " -> " + items[1])

        #second index of the inner list
        print("Support: " + str(item[1]))

        #third index of the list located at 0th
        #of the third index of the inner list

        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")
